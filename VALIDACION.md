# Validación de las correcciones

Fecha: 17 de noviembre de 2026. Cambios en copias locales; GitHub no se modificó.

## Pruebas

- 6 pruebas de regresión repartidas entre los tres proyectos: todas pasaron.
- 5 comprobaciones transversales adicionales: todas pasaron.
- Coches: script y notebook ejecutados con los 51.525 registros originales. Tipos más frecuentes con mínimo de 50 anuncios: SUV (12.405) y truck (12.353). Gráficas y tablas regeneradas en results/.
- Cancelación: flujo completo de selección por CV, entrenamiento y evaluación ejecutado con un fixture sintético de 160 filas. Esto verifica funcionamiento, no rendimiento con los datos originales; sus métricas NO se incluyen en el portafolio.
- Datos originales de cancelación: descarga del primer CSV rechazada con HTTP 403 por el proveedor. Notebook sin métricas de la versión anterior. Requiere los cuatro CSV originales para validar resultados reales.
- SQL: esquema y diez consultas analizados como MySQL con sqlglot. Comportamiento de consultas probado con un fixture SQLite, incluyendo descuentos de 0%, 10% y 100%, factura vacía y precio de la línea. Esto NO sustituye ejecutar el esquema y cargas en MySQL.
- MySQL no está instalado y el motor Docker no está iniciado en esta sesión; no se afirma validación de integración MySQL.

## Reproducir

Instalar requirements.txt en cada proyecto; Python 3.12. Ejecutar `python -m unittest discover -p "test_*.py" -v` desde cada carpeta.

Coches: `python analysis.py --data data/vehicles_us.csv` (o usar la URL pública indicada en el README).

Cancelación: `python train.py --data RUTA_A_LOS_CUATRO_CSV`.

SQL: usar una base vacía de MySQL 8.0.16+, seguir el orden del README y revisar SHOW WARNINGS tras las cargas. stock se inicia en cero porque los INSERT originales no incluyen existencias.

No se borraron documentos ni cachés del usuario. No se publicaron datos sintéticos como evidencia de rendimiento.
