import pandas as pd
import numpy as np

def formatear(data, parametros):

    for k,v in parametros.items():
        print("Parametros: ",k,v)
    
    print("Proceso de formatear Markov")
    
    return data

def calcular(input):
    """
    El input es un dataframe con los recorridos de cada usuario y si terminan en conversion.
    El output es la cantidad de conversiones atribuidas a cada canal en los recorridos.
    """
    # crear una copia para no alterar la data original
    data = input.copy()

    # calcular conversiones totales
    conversiones_totales = data.iloc[:,1].sum()

    # obtener la matriz de transicion de los canales
    matriz = calcular_matriz_transicion(data)

    # obtener el diciconario del removal effect de cada canal
    proporcion = calcular_removal_effect(matriz)
    
    # aplicar conversiones a proporcion
    atribucion = {k:round(v*conversiones_totales,2) for k,v in proporcion.items()}

    return atribucion

def calcular_matriz_transicion(data):
    '''
    Agregar el estado inicial (start) y los estados absorbentes (conversion), (null).
    Calcula la matriz como la probabilidad de transicion entre dos estados.
    Agrega las columnas necesarias para obtener una matriz cuadrada.
    '''
    # agregar (start) al inicio de cada path
    data[0] = data[0].apply(lambda x:['(start)'] + x)

    # agregar estado absorbente
    data.apply(lambda x: x[0].append('(conversion)') if x[1]==1 else x[0].append('(null)'), axis=1)

    # descartar columna de conversion
    recorridos = data.iloc[:,0].copy()

    # agrupar de dos en dos los canales
    recorridos = recorridos.apply(lambda x: list(zip(x[:],x[1:])))

    # extender los pares de canales en una lista
    recorridos = recorridos.explode().tolist()

    # dar formato de tabla
    df = pd.DataFrame(recorridos,columns=['(start)','(end)'])

    # crear matriz de transicion
    matriz = pd.crosstab(index=df['(start)'], columns=df['(end)'], normalize = 'index', dropna = False)

    # validar si estan todas las columnas
    for columna in ['(conversion)','(null)']:
        if columna not in matriz.columns:
            matriz.insert(0,columna,np.zeros(matriz.shape[0]))

    # agregar start como estado final para lograr matriz cuadrada
    matriz.insert(0,'(start)',np.zeros(matriz.shape[0]))

    return matriz

def calcular_markov(datad):
    '''
    Toma una matriz de transiciones entre los canales (con null, start y conversion).
    Devuelve la tasa de conversion partienda del estado start.
    '''
    # armar matriz de convergencia (columnas finales)
    removal_to_conv = datad[['(null)','(conversion)']]
    
    # armar matriz de canales (filas de canales)
    removal_to_non_conv = datad.drop(['(conversion)','(null)'],axis=1)
    
    # calcular la inversa de (I - canales)
    removal_inv_diff = np.linalg.inv(np.identity(len(removal_to_non_conv.columns)) - np.asarray(removal_to_non_conv))
    
    # calcular producto matricial de la inversa y la de convergencia
    removal_dot_prod = np.dot(removal_inv_diff, np.asarray(removal_to_conv))
        
    # devolver la probabilidad de conversion del inicio en start
    cvr = pd.DataFrame(removal_dot_prod,index=removal_to_conv.index)[[1]].loc['(start)'].values[0]
    
    return cvr

def calcular_removal_effect(datad):
    '''
    Toma una matriz de transiciones entre los canales (con null, start y conversion) y calcula el removal effect
    de cada uno de los canales.
    
    Para eso, itera sobre los canales (sin start, conversion y null) y calcula la tasa de conversion general. 
    Luego, borra la fila del canal, asigna sus probabilidades de transicion a null y recalcula la
    tasa de conversion.
    
    Devuelve la proporcion normalizada en que disminuye la tasa de conversion original.
    
    '''
    # calcular conversion general y guardar
    cr_general = calcular_markov(datad)
    
    # crear un diccionario para almacenar removal effect de cada canal
    removal_effect = {}
    
    # iterar sobre canales validos
    for canal in datad.columns:
        if canal not in ['(start)','(conversion)','(null)']:
            
            # borrar linea y columna del canal
            matriz_canal = datad.drop(canal, axis=1).drop(canal, axis=0)
            
            # reasignar probabilidad a nulo
            for column in matriz_canal.columns:
                if column not in ['(conversion)','(null)']:
                    faltante = float(1) - np.sum(list(matriz_canal.loc[column]))
                    if faltante != 0:
                        matriz_canal.loc[column]['(null)'] = faltante
            
            # calcular la conversion
            cr_canal = calcular_markov(matriz_canal)
           
            # calcular la variacion de la conversion
            removal_effect_canal = 1 - cr_canal / cr_general
            
            # guardar en diccionario
            removal_effect[canal] = removal_effect_canal
    
    # calcular valor total
    suma = np.sum(list(removal_effect.values()))
    
    # normalizar
    removal_effect_normalizado = {key: (value / suma) for key, value in removal_effect.items()}

    # devolver diccionario
    return removal_effect_normalizado
