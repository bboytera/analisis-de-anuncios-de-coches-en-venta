# Análisis de anuncios de coches en venta
# Introducción

En **Crankshaft List** cientos de anuncios gratuitos de vehículos se publican en su sitio web cada día. Necesitaremos estudiar los datos recopilados durante los últimos años y determinar qué factores influyen en el precio de un vehículo.

# Descripción de los datos
El dataset contiene los siguientes campos:
- `'price'`      -precio del vehículo
- `'model_year'` -año del vehículo
- `'model'`      -modelo del vehículo
- `'condition'`  -concición en la que se encuentra
- `'cylinders'`  -cilindraje
- `'fuel'`       - gasolina, diesel, etc.
- `'odometer'`   - el millaje del vehículo cuando el anuncio fue publicado
- `'transmission'` -el tipo de transmisión del vehículo
- `'paint_color'`  -el color del vehículo
- `'is_4wd'`     - si el vehículo tiene tracción a las 4 ruedas (tipo Booleano)
- `'date_posted'`- la fecha en la que el anuncio fue publicado
- `'days_listed'`- desde la publicación hasta que se elimina

  Se encuentran en el archivo `datasets/vehicles_us.csv`

  # Habilidades técnicas
  - `Pandas`
  - `Matplotlib`
  - `Seaborn`
  # Conclusión General
  **Preprocesamos los datos:**

- Remplazamos lo valores ausentes usando(la mediana,la moda, usamos el valor más comun en paint_color, Buscamos tambien patrones en los datos agrupandolos o en valores booleanos rellenamos con el opuesto al valor 

- Corregimos los tipos de datos

- Agregamos valores adicionales al dataframe como el promedio del millaje, los años del vehiculo desde su pubicacion etc...

**Visualizamos los datos:**

- Realizamos histogramas estudiando y comparando con valores atipicos y sin valores atipicos de algunos parametros: precio, los años del vehículo cuando el anuncio se colocó, millaje, número de cilindros y la condicion

- observamos el periodo de colocación de los anuncios siendo por arriba de 50 dias listados es un tiempo anormalmente alto la mayoria de vehiculos vendidos duran no menos a 50 dias y como de 0 a 20 dias se eliminan rápidamente los anuncios.

- observamos tambien en grafica de dispersion el promedio de precio por tipo de vehiculo siendo el bus con mayor precio promedio

- Tambien obtuvimos los dos tipos más populares: bus y truck

- Y realizamos graficas de dispersion para observar que factores impactaban  más sobre el precio si el precio tenia que ver con el tipo de transmision, color, la edad del vehiculo, millaje o condición,

**LOS FACTORES QUE MAS IMPACTAN EN EL BUS SON:**
- automatico
- blanco 
- 7 a 8 años
- un millaje de casi 200000 de millaje
- condicion buena


**LOS FACTORES QUE MAS IMPACTAN  EN TRUCK SON:**
- automatico
- color negro
- 6 a 7 años 
- 150 mil millas 
- condicion buena


