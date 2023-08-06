from . import markov, shapley, heuristicos

class Modelo():
    """
    Datos para formatear y calcular modelos.
    
    :param data: data con la cual crear los modelos.
    :type data: dataframe or list
    :param formateada: si la data tiene una columna de recorridos y otra con la conversion.
    :type formateada: bool
    """
    def __init__(self, data, formateada=True):
        self.data = data
        self.formateada = formateada

        return None

    def markov(self, orden=1, ventana=30, touchpoints=8, conversion=True):
        """
        Si la data no esta formateada, lo hace en base a los parametros. 
        Luego, crea un modelo de Markov.
        
        :param orden: El orden del modelo de Markov, entre 1 y 4.
        :type orden: int
        :param ventana: La cantidad de dias que se toman antes de cada conversion.
        :type ventana: int
        :param touchpoints: La cantidad de canales maxima que se toma por cada conversion.
        :type touchpoints: int
        :param conversion: Si se corta el camino con cada nueva conversion.
        :type conversion: bool
        """
        # formatear la data
        if self.formateada == False:
            parametros = {
                'orden' : orden,
                'ventana' : ventana,
                'touchpoints' : touchpoints,
                'conversion' : conversion
            }
            self.markov = markov.formatear(self.data, parametros)
        else:
            self.markov = self.data

        # calcular el modelo de markov
        resultado = markov.calcular(self.markov)

        return resultado

    def shapley(self, ventana=30, touchpoints=8):
        """
        Si no esta formateada, busca si ya hay data formateada y sino lo hace en base a los parametros. 
        Luego, crea un modelo de Shapley.

        :param ventana: La cantidad de dias que se toman antes de cada conversion.
        :type ventana: int
        :param touchpoints: La cantidad de canales maxima que se toma por cada conversion.
        :type touchpoints: int
        """
        # formatear la data
        if self.formateada == False:
            parametros = {
                'ventana' : ventana,
                'touchpoints' : touchpoints,
            }
            self.shapley = shapley.formatear(self.data, parametros)        
        else:
            self.shapley = self.data

        # calcular el modelo de shapley
        resultado = shapley.calcular(self.shapley)

        return resultado

    def first(self, ventana=30, touchpoints=8):
        """
        Si no esta formateada, busca si ya hay data formateada y sino lo hace en base a los parametros. 
        Luego, crea un modelo First Click.
        
        :param ventana: La cantidad de dias que se toman antes de cada conversion.
        :type ventana: int
        :param touchpoints: La cantidad de canales maxima que se toma por cada conversion.
        :type touchpoints: int
        :return resultado: Un dicci

        """
        # si ya se formateo para shapley
        if not hasattr(self, "shapley"):
            # formatear la data
            if self.formateada == False:
                parametros = {
                    'ventana' : ventana,
                    'touchpoints' : touchpoints,
                }
                self.shapley = shapley.formatear(self.data, parametros)        
            else:
            # usar la data original
                self.shapley = self.data

        # calcular el modelo first click
        resultado = heuristicos.calcular_first_click(self.shapley)

        return resultado

    def last(self, ventana=30, touchpoints=8):
        """
        Si no esta formateada, busca si ya hay data formateada y sino lo hace en base a los parametros. 
        Luego, crea un modelo Last Click.
        
        :param ventana: La cantidad de dias que se toman antes de cada conversion.
        :type ventana: int
        :param touchpoints: La cantidad de canales maxima que se toma por cada conversion.
        :type touchpoints: int
        :return resultado: Un dicci

        """
        # si ya se formateo para shapley
        if not hasattr(self, "shapley"):
            # formatear la data
            if self.formateada == False:
                parametros = {
                    'ventana' : ventana,
                    'touchpoints' : touchpoints,
                }
                self.shapley = shapley.formatear(self.data, parametros)        
            else:
            # usar la data original
                self.shapley = self.data

        # calcular el modelo last click
        resultado = heuristicos.calcular_last_click(self.shapley)

        return resultado

    def linear(self, ventana=30, touchpoints=8):
        """
        Si no esta formateada, busca si ya hay data formateada y sino lo hace en base a los parametros. 
        Luego, crea un modelo Linear.
        
        :param ventana: La cantidad de dias que se toman antes de cada conversion.
        :type ventana: int
        :param touchpoints: La cantidad de canales maxima que se toma por cada conversion.
        :type touchpoints: int
        :return resultado: Un dicci

        """
        # si ya se formateo para shapley
        if hasattr(self, "shapley"):
            resultado = heuristicos.calcular_linear(self.shapley)
        else:
            # formatear la data
            if self.formateada == False:
                parametros = {
                    'ventana' : ventana,
                    'touchpoints' : touchpoints,
                }
                self.shapley = shapley.formatear(self.data, parametros)        
            else:
            # usar la data original
                self.shapley = self.data

        # calcular el modelo linear
        resultado = heuristicos.calcular_linear(self.shapley)

        return resultado

    def comparacion(self):
        pass


