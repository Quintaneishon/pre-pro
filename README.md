# Análisis Multimodal de Datos COVID-19 en México

Este proyecto integra múltiples fuentes de datos para realizar análisis comprehensivos sobre la pandemia de COVID-19 en México, combinando datos relacionales, series temporales y análisis de sentimientos de redes sociales.

## Descripción del Proyecto

El proyecto implementa un pipeline de análisis multimodal que integra:
- **Datos relacionales**: Casos individuales de COVID-19 con información clínica detallada
- **Datos de series temporales**: Métricas diarias por entidad federativa
- **Datos de texto**: Análisis de sentimientos de publicaciones en Twitter/X


## Fuentes de Datos

### Datos Relacionales
- **COVID19MEXICO.csv**: Base de datos principal con casos individuales (110,103 registros, 42 variables)
- **Catálogos**: Diccionarios de datos para variables categóricas (13 hojas de cálculo)
- **Descriptores**: Documentación detallada de variables y actualizaciones

### Datos de Series Temporales
- **Confirmados**: Casos confirmados diarios por entidad (33 estados, 1,218 días)
- **Defunciones**: Defunciones diarias por entidad
- **Negativos**: Casos negativos diarios por entidad
- **Sospechosos**: Casos sospechosos diarios por entidad

### Datos de Texto
- **Twitter/X**: Publicaciones de redes sociales con análisis de sentimientos
- **Período**: 2020-2023 (era COVID-19)
- **Idiomas**: Principalmente español e inglés
- **Características**: Sentimientos, ubicación geográfica, entidades nombradas

## Instalación de Datos

### Archivos TSV de Twitter (Obligatorio - Subida Manual)

Los archivos de datos de Twitter/X son demasiado grandes para incluir en el repositorio. Para usar el proyecto completo, debes descargar y colocar manualmente los siguientes archivos en la carpeta `data/text/`:

- `mexico_1-003.tsv`
- `mexico_2-001.tsv` 
- `mexico_3-004.tsv`

**Instrucciones:**
1. Descargar los archivos TSV desde la fuente original
2. Colocar los archivos en la carpeta `data/text/`
3. Asegurarse de que los nombres de archivo coincidan exactamente
4. El archivo `data_descriptor.txt` ya está incluido y describe la estructura de los datos

**Nota:** Sin estos archivos, el análisis de sentimientos y correlación con redes sociales no estará disponible, pero el resto del pipeline funcionará normalmente con los datos relacionales y de series temporales.


## Tecnologías Utilizadas

- **Python 3.10+**
- **Pandas**: Manipulación de datos
- **DuckDB**: Base de datos analítica en memoria
- **OpenPyXL**: Lectura de archivos Excel
- **Jupyter Notebooks**: Análisis interactivo

## Instalación

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd project
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar el notebook principal:
```bash
jupyter notebook notebooks/main.ipynb
```

## Características Principales

### Integración Multimodal
- **Relacional-Gráfico**: Correlación entre casos individuales y métricas agregadas
- **Gráfico-Texto**: Análisis de correlación entre sentimientos y números de casos
- **Vista Unificada**: Esquema canónico para consultas integradas

### Análisis Disponibles
- Análisis temporal de la pandemia por entidad federativa
- Correlación entre sentimientos de redes sociales y métricas de salud
- Análisis geográfico de la propagación del virus
- Detección de entidades nombradas y análisis de ubicación
- Modelado de temas en discusiones sobre COVID-19

### Métricas Calculadas
- Tasas de incidencia por 100,000 habitantes
- Tasas de letalidad
- Tasas de positividad de pruebas
- Análisis de sentimientos agregados por día/ubicación

## Esquema de Datos

### Dimensión Territorio
- `entidad_id`: Identificador de entidad federativa
- `entidad_nombre`: Nombre de la entidad
- `municipio_id`: Identificador de municipio (opcional)
- `municipio_nombre`: Nombre del municipio (opcional)

### Dimensión Tiempo
- `fecha`: Fecha del evento (día)
- `semana`: Semana epidemiológica (opcional)
- `mes`: Mes del año (opcional)

### Hechos Clínicos
- Variables del archivo COVID19MEXICO.csv limpias y enlazadas con catálogos
- Clasificación final de COVID-19 e influenza
- Resultados de PCR y antígenos

### Hechos de Series Temporales
- `(entidad_id, fecha, metrica, valor)`
- `metrica ∈ {confirmados, defunciones, negativos, sospechosos}`

### Hechos de Texto
- `(doc_id, embedding, metadatos)`
- Análisis de sentimientos y ubicación geográfica
