# Sistema de Integración y Validación Multimodal de Datos COVID-19 en México

## Descripción General

Este proyecto implementa un sistema de integración de datos heterogéneos para el análisis epidemiológico de COVID-19 en México, combinando tres fuentes de datos complementarias: registros clínicos individuales (datos relacionales), series temporales agregadas por entidad federativa (datos de grafo), y cobertura mediática (datos de texto). El sistema incluye un marco de evaluación de calidad de datos, procesos de limpieza automatizados y estrategias de federación de datos para análisis integrados.

## Marco Conceptual

### Fuentes de Datos Integradas

#### 1. Datos Relacionales
**Fuente:** Secretaría de Salud de México - Dirección General de Epidemiología  
**Período:** 2020-2023  
**Contenido:** Registros individuales de casos con información clínica, demográfica y temporal

**Características principales:**
- Variables clínicas y epidemiológicas
- Casos confirmados, sospechosos y negativos
- Información de comorbilidades
- Desenlaces clínicos (hospitalización, UCI, intubación, defunción)
- Cobertura: 32 entidades federativas

**Actualizaciones importantes del esquema:**
- Eliminación de `RESULTADO_LAB`, reemplazada por `RESULTADO_PCR` y `RESULTADO_PCR_COINFECCION`
- Adición de `CLASIFICACION_FINAL_COVID` para casos positivos confirmados
- Adición de `CLASIFICACION_FINAL_FLU` para identificación de influenza

#### 2. Datos de Series Temporales (Grafo)
**Fuente:** CONACYT - COVID-19 Tablero México  
**Período:** 2020-2023  
**Contenido:** Series temporales diarias por entidad federativa

**Métricas disponibles:**
- Casos confirmados diarios
- Defunciones diarias
- Casos negativos diarios
- Casos sospechosos diarios

**Estructura:** Base de datos de grafos (Apache AGE) con nodos de entidad y fecha conectados por relaciones `TIENE_CASOS` con valores métricos.

#### 3. Datos de Texto (Noticias)
**Fuente:** UNAM Global - Cobertura Coronavirus  
**Período:** 2020-2023  
**Contenido:** Artículos de cobertura mediática sobre COVID-19

**Metadatos extraídos:**
- Título, autor, fecha de publicación
- Categorías temáticas
- Contenido completo en español e inglés

## Arquitectura del Sistema

### Infraestructura Tecnológica

**Base de Datos:**
- PostgreSQL 16+ con extensión Apache AGE para gestión de grafos
- Esquemas organizados por tipo de datos (`relational`, `graph`, `text`, `federation`)
- Contenedorización mediante Docker

**Stack de Análisis:**
- Python 3.10+
- SQLAlchemy (ORM para carga masiva)
- psycopg2 (operaciones DDL y consultas especializadas)
- Pandas/NumPy (procesamiento de datos)
- OpenPyXL (lectura de catálogos en Excel)
- BeautifulSoup4 (extracción de noticias)
- Plotly (visualizaciones interactivas)


## Marco de Evaluación de Calidad de Datos

El sistema implementa un protocolo de validación exhaustivo basado en seis dimensiones de calidad según las normas ISO 8000 y DAMA-DMBOK:

### 1. Validación de Datos Relacionales

#### 1.1 Exactitud y Conformidad
- Validación de conformidad con catálogos oficiales
- Verificación de tipos de datos
- Detección de valores fuera de rango

#### 1.2 Completitud
- Medición de valores nulos por columna clave
- Identificación de registros con alta proporción de campos faltantes
- Evaluación de completitud en campos esenciales

#### 1.3 Validez de Dominio
- Conformidad con catálogos oficiales
- Integridad referencial con catálogo de entidades
- Validación de códigos especiales (NO APLICA, SE IGNORA, NO ESPECIFICADO)

#### 1.4 Consistencia Temporal
- Detección de inconsistencias cronológicas
- Validación lógica de secuencias de eventos
- Verificación de rangos temporales válidos

#### 1.5 Unicidad y Duplicados
- Identificación de duplicados por identificador único
- Detección de duplicados funcionales Multi-Column Weighted Similarity Score Levenshtein
- Análisis de redundancia en el dataset

#### 1.6 Integridad Referencial
- Verificación de relaciones entre tablas
- Coherencia entre variables derivadas
- Validación de jerarquías geográficas

### 2. Validación de Datos de Grafo (Series Temporales)

#### 2.1 Estructura del Grafo
- Validación de nodos y aristas
- Verificación de propiedades obligatorias
- Consistencia en el esquema del grafo

#### 2.2 Correspondencia Semántica
- Verificación de entidades presentes en catálogo relacional
- Análisis de diferencias entre fuentes
- Normalización de identificadores

#### 2.3 Integridad de Valores
- Validación de rangos numéricos
- Detección de valores atípicos
- Coherencia en las métricas

#### 2.4 Consistencia Temporal
- Análisis de continuidad de fechas
- Detección de gaps temporales
- Evaluación de densidad temporal

#### 2.5 Duplicidad de Relaciones
- Detección de aristas repetidas
- Validación de unicidad en relaciones

### 3. Validación de Datos de Texto

#### 3.1 Parseo Estructural
- Validación de extracción de artículos
- Análisis de longitud de contenido
- Detección de errores de delimitación

#### 3.2 Completitud de Metadatos
- Evaluación de campos obligatorios
- Análisis de categorización
- Verificación de metadatos extraídos

#### 3.3 Validez Temporal
- Validación de rangos de fechas
- Detección de formatos incorrectos
- Coherencia con período de estudio

#### 3.4 Normalización Lingüística
- Validación de codificación de caracteres
- Unificación de categorías
- Estandarización de texto

## Pipeline de Limpieza de Datos

### Etapa 1: Limpieza de Datos Relacionales

**Reglas de transformación aplicadas:**

1. **Limpieza de fechas:**
   - Validación de secuencias temporales lógicas
   - Eliminación de fechas fuera de rango válido

2. **Validación de entidades:**
   - Verificación de códigos de entidad válidos
   - Eliminación de códigos especiales no aplicables

3. **Normalización de variables categóricas:**
   - Conversión de códigos especiales a valores nulos
   - Validación de rangos de edad
   - Aplicación de reglas de negocio específicas

4. **Eliminación de duplicados:**
   - Detección basada en combinaciones de campos clave
   - Resolución de registros redundantes

**Métricas de calidad agregadas:**
- `quality_score`: puntuación basada en completitud de campos esenciales
- `completeness_pct`: porcentaje de campos poblados
- `has_death_data`: indicador de información de defunción
- `has_severe_symptoms`: indicador de casos graves

### Etapa 2: Limpieza de Datos de Texto

**Reglas aplicadas:**
- Eliminación de contenido insuficiente
- Validación de rango temporal
- Eliminación de duplicados
- Normalización de metadatos

### Etapa 3: Federación de Datos

**Vista: `federation.unified_covid_data`**
- Integración de casos individuales con catálogos
- Columnas organizadas por categorías:
  - Identificadores
  - Variables categóricas
  - Indicadores médicos
  - Indicadores demográficos
  - Comorbilidades
  - Métricas de calidad

**Vista: `federation.comprehensive_correlation`**
- Agregación por fecha y entidad
- Métricas calculadas:
  - Conteos de casos por tipo
  - Indicadores demográficos agregados
  - Resumen de comorbilidades
  - Métricas de calidad promedio
  - Integración con datos de noticias

## Análisis de Cobertura Representativa

### Dimensiones Evaluadas

#### Cobertura Temporal
- Período completo de análisis
- Días con datos disponibles
- Continuidad de series temporales

#### Cobertura Geográfica
- Representación de entidades federativas
- Distribución espacial de casos

#### Cobertura Mediática
- Disponibilidad de noticias por período
- Correlación temporal con eventos epidemiológicos

#### Distribución Demográfica
- Representación por sexo
- Distribución por grupos etarios
- Comparación con demografía poblacional

## Instalación y Configuración

### Requisitos Previos
- Docker y Docker Compose
- Python 3.10+
- Git

### Descarga de Datos

**IMPORTANTE:** Los archivos de datos no están incluidos en el repositorio. Deben descargarse de las fuentes oficiales:

#### Datos Relacionales (CSV)
**Fuente:** [Datos Abiertos - Secretaría de Salud](https://www.gob.mx/salud/documentos/datos-abiertos-152127)

Archivos requeridos:
- COVID19MEXICO2020.csv
- COVID19MEXICO2021.csv
- COVID19MEXICO2022.csv
- COVID19MEXICO2023.csv

Ubicación: `data/relational/`

#### Datos de Series Temporales (CSV)
**Fuente:** [COVID-19 Tablero México - CONACYT](https://datos.covid-19.conacyt.mx/)

Archivos requeridos:
- Casos_Diarios_Estado_Nacional_Confirmados_20230625.csv
- Casos_Diarios_Estado_Nacional_Defunciones_20230625.csv
- Casos_Diarios_Estado_Nacional_Negativos_20230625.csv
- Casos_Diarios_Estado_Nacional_Sospechosos_20230625.csv

Ubicación: `data/graph/`

#### Datos de Texto (Extracción Automática)
**Fuente:** [UNAM Global - Cobertura Coronavirus](https://unamglobal.unam.mx/cobertura-coronavirus/)

Ejecutar script de extracción:
```bash
python init-scripts/download_covid_news.py
```

Ubicación: `data/text/`

### Procedimiento de Instalación

1. **Clonar repositorio:**
```bash
git clone <repository-url>
cd project
```

2. **Configurar variables de entorno:**
```bash
cat > .env << EOF
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=covid_analysis
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
EOF
```

3. **Iniciar base de datos PostgreSQL con Apache AGE:**
```bash
docker-compose up -d
docker-compose logs -f postgres
```

4. **Instalar dependencias de Python:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

5. **Ejecutar pipeline de integración y validación:**
```bash
jupyter notebook notebooks/main_post.ipynb
```

## Uso del Sistema

### Verificación del Estado del Sistema

```bash
# Verificar estado de contenedores
docker-compose ps

# Conectar a PostgreSQL
docker-compose exec postgres psql -U postgres -d covid_analysis

# Verificar conteo de registros por esquema
SELECT 
    schemaname, 
    tablename, 
    n_tup_ins as records
FROM pg_stat_user_tables 
WHERE schemaname IN ('relational', 'graph', 'text', 'federation')
ORDER BY schemaname, tablename;
```

## Estructura del Notebook Principal

El notebook `main_post.ipynb` implementa el siguiente flujo:

1. **Carga e Inspección de Datos**
   - Conexión a PostgreSQL y configuración de extensiones
   - Carga de archivos CSV anuales
   - Inspección de catálogos y descriptores

2. **Transformación y Carga**
   - Creación de tablas relacionales
   - Construcción del grafo con Apache AGE
   - Carga de noticias desde archivos de texto

3. **Validación de Calidad de Datos**
   - Validación de datos relacionales
   - Validación de datos de grafo
   - Validación de datos de texto

4. **Análisis de Cobertura**
   - Cobertura temporal, geográfica y demográfica
   - Generación de dashboards interactivos

5. **Limpieza de Datos**
   - Aplicación de reglas de limpieza
   - Creación de tablas limpias
   - Agregación de métricas de calidad

6. **Federación de Datos**
   - Creación de vistas integradas
   - Reporte final de calidad
