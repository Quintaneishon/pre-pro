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

## Estructura del Notebook Principal

El notebook `main_post.ipynb` implementa el siguiente flujo:

### 1. Configuración e Instalación
- Instalación de dependencias necesarias
- Configuración de conexiones a PostgreSQL
- Configuración de extensiones Apache AGE

### 2. Carga e Inspección de Datos
- Conexión a PostgreSQL y configuración de extensiones
- Carga de archivos CSV anuales
- Inspección de catálogos y descriptores
- Análisis de la información de la base de datos relacional

### 3. Validación de Integridad de Datos
- Comparación de entidades en catálogo vs entidades con casos COVID
- Validación del rango de fechas
- Verificación de consistencia temporal

### 4. Transformación y Carga de Datos
- Creación de esquemas de base de datos relacional
- Inserción de información relacional
- Análisis de información de grafos
- Transformación y carga de datos de series temporales
- Validación de nombres de entidades
- Creación de esquemas de grafos con Apache AGE

### 5. Perfilado de Datos por Fuente

#### 5.1 Fuente Relacional
- Evaluación de integridad estructural
- Análisis de completitud por columna clave
- Validación de dominio y conformidad con catálogos
- Verificación de consistencia temporal
- Detección de duplicados y unicidad
- Validación de integridad referencial

#### 5.2 Fuente de Grafo
- Validación de estructura del grafo
- Verificación de correspondencia semántica
- Análisis de integridad de valores
- Evaluación de consistencia temporal
- Detección de duplicidad de relaciones

#### 5.3 Fuente Textual
- Validación de parseo estructural
- Análisis de completitud de metadatos
- Verificación de validez temporal
- Normalización lingüística

#### 5.4 Vista Federada
- Evaluación de integridad estructural
- Validación de consistencia inter-fuente
- Análisis de completitud federada
- Verificación de duplicidad y unicidad global
- Evaluación de coherencia general

### 6. Análisis de Cobertura Representativa

#### 6.1 Dimensiones Evaluadas
- **Cobertura Temporal:** Período completo de análisis, días con datos disponibles, continuidad de series temporales
- **Cobertura Geográfica:** Representación de entidades federativas, distribución espacial de casos
- **Cobertura Mediática:** Disponibilidad de noticias por período, correlación temporal con eventos epidemiológicos
- **Distribución Demográfica:** Representación por sexo, distribución por grupos etarios

#### 6.2 Métricas de Validación
- Validación geográfica (entidad_id ∈ catálogo)
- Validación temporal (fecha coincide entre relacional y grafo)
- Validación semántica (confirmados coherente entre fuentes)
- Validación textual (correlación noticias vs contagios)

### 7. Limpieza de Datos

#### 7.1 Limpieza de Datos Relacionales
- Creación de tabla de respaldo
- Aplicación de reglas de limpieza específicas:
  - Limpieza de fechas con validación de secuencias temporales lógicas
  - Validación de entidades con códigos válidos
  - Normalización de variables categóricas
  - Conversión de códigos especiales a valores nulos
  - Validación de rangos de edad y consistencia clínica
- Eliminación de duplicados con criterios estrictos
- Agregación de flags de calidad
- Creación de índices optimizados

#### 7.2 Limpieza de Datos de Texto
- Eliminación de contenido insuficiente
- Validación de rango temporal
- Eliminación de duplicados
- Normalización de metadatos

#### 7.3 Recreación de Vistas Federadas
- Actualización de vistas con datos limpios
- Generación de métricas de calidad agregadas

### 8. Visualizaciones y Dashboards

#### 8.1 Dashboard de Calidad y Cobertura
- Resumen general de cobertura por criterio
- Cumplimiento de metas establecidas
- Distribución demográfica
- Calidad de datos por fuente

#### 8.2 Métricas de Calidad de Datos
- Dimensiones de calidad (Completitud, Validez, Consistencia)
- Métricas por fuente de datos
- Indicadores de integridad

#### 8.3 Cobertura Geográfica
- Mapa de cobertura por estado
- Distribución espacial de casos
- Análisis de representatividad territorial

#### 8.4 Evolución Temporal
- Timeline de cobertura temporal
- Análisis de continuidad de datos
- Identificación de gaps temporales

#### 8.5 Comparación de Fuentes
- Métricas comparativas entre fuentes
- Análisis de completitud y consistencia
- Evaluación de cobertura por fuente

### 9. Análisis de Preguntas de Negocio

#### 9.1 Preguntas Descriptivas
- Evolución del número de casos confirmados por año y estado
- Proporción de casos confirmados que resultaron en hospitalización
- Distribución de comorbilidades entre casos positivos
- Tasa de letalidad por entidad y grupo de edad
- Análisis de pacientes intubados por año
- Concentración de casos por sector de salud
- Distribución de casos en población indígena
- Casos positivos en mujeres embarazadas
- Municipios con mayor número de casos por entidad
- Proporción de resultados positivos en pruebas de laboratorio vs antígeno

#### 9.2 Preguntas Predictivas
- Probabilidad de requerir UCI según comorbilidades
- Factores que aumentan el riesgo de defunción
- Estados con mayor probabilidad de repunte
- Probabilidad de hospitalización según edad y sexo
- Características clínicas que predicen necesidad de intubación
- Probabilidad de hospitalización en pacientes migrantes
- Factores predictivos de mortalidad en mujeres embarazadas
- Probabilidad de positividad de pruebas según entidad y fecha
- Municipios con mayor riesgo de saturación hospitalaria
- Relación entre sentimientos en redes sociales y repunte de casos

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

## Resultados y Métricas

El sistema genera métricas de calidad y cobertura que incluyen:

- **Completitud de datos:** Porcentaje de campos poblados por fuente
- **Validez de dominio:** Conformidad con catálogos oficiales
- **Consistencia temporal:** Coherencia en secuencias de fechas
- **Integridad referencial:** Validación de relaciones entre tablas
- **Cobertura representativa:** Evaluación de representatividad geográfica, temporal y demográfica
- **Calidad federada:** Métricas integradas de las tres fuentes de datos

El notebook proporciona visualizaciones interactivas y dashboards que permiten evaluar la calidad de los datos y su adecuación para análisis epidemiológicos y de salud pública.