# Limpieza y análisis de anuncios de vehículos

Proyecto formativo con Python, pandas y Matplotlib.

## Reproducción

Python 3.12. Instalar requirements.txt en un entorno virtual. Desde esta carpeta:

```powershell
python analysis.py --data https://practicum-content.s3.us-west-1.amazonaws.com/datasets/vehicles_us.csv
```

También puede pasarse una ruta CSV local a --data. El archivo datasets_vehicles_us.csv del repositorio es una referencia URL, no el dataset completo. Se requiere acceso al dataset público del proveedor; no se redistribuyen los datos.

El notebook llama al mismo módulo y presenta tablas y gráficos regenerados. Para usar datos locales en él, definir VEHICLES_DATA.

## Correcciones

Imputación escalar de cilindros por modelo con respaldo; indicadores de ausentes; color desconocido explícito; sensibilidad de medianas a la imputación; protección frente a división por edad cero; IQR independiente por variable; popularidad calculada por número de anuncios con mínimo de 50.

results/ contiene tablas de frecuencia, resumen, sensibilidad y figuras. No se afirma que los tipos de mayor precio sean los más populares ni que las asociaciones sean causas del precio. Los anuncios retirados no prueban una venta.

## Pruebas de regresión

```powershell
python -m unittest discover -p "test_*.py" -v
```

Consultar VALIDACION.md para distinguir pruebas con datos reales, sintéticos y límites de integración.
