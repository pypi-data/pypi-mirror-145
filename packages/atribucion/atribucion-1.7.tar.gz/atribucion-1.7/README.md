# MODELOS DE ATRIBUCION
Esta es una librería creada para el trabajo con modelos de atribución sobre datos de marketing digital.
Con esta librería se podrán crear modelos heurísticos (First click, Last click, Linear) o modelos data-driven (Markov, Shapley).
Funciona tanto con datos previamente formateados como con datos sin formatear.

## INSTALACIÓN
```
pip install atribucion
```
## CÓMO SE USA
Primero, es necesario crear un modelo pasando la data a utilizar. Se deberá indicar si la información fue previamente formateada o no.
```
modelo = atribucion.Modelo(data, formateada=True)
```
Luego, se piden los modelos deseados llamando a la función correspondiente.
````
resultado_markov = modelo.markov()
resultado_shapley = modelo.shapley()
resultado_first = modelo.first()
resultado_last = modelo.last()
resultado_linear = modelo.linear()
````
