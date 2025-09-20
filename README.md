# Análisis Multimodal de Datos COVID-19 en México

Este proyecto integra múltiples fuentes de datos para realizar análisis comprehensivos sobre la pandemia de COVID-19 en México, combinando datos relacionales, series temporales y análisis de sentimientos de redes sociales.

## Descripción del Proyecto

El proyecto implementa un pipeline de análisis multimodal que integra:
- **Datos relacionales**: Casos individuales de COVID-19 con información clínica detallada (2020-2023)
- **Datos de series temporales**: Métricas diarias por entidad federativa
- **Datos de texto**: Análisis de sentimientos de publicaciones en Twitter/X y noticias

## Fuentes de Datos

### Datos Relacionales
- **COVID19MEXICO2020-2023.csv**: Base de datos principal con casos individuales por año
- **Catálogos**: Diccionarios de datos para variables categóricas (13 hojas de cálculo)
- **Descriptores**: Documentación detallada de variables y actualizaciones

**Actualizaciones importantes:**
- Se eliminó la variable `RESULTADO_LAB`, reemplazada por `RESULTADO_PCR` y `RESULTADO_PCR_COINFECCION`
- Se agregó `CLASIFICACION_FINAL_COVID` para identificar casos positivos de COVID-19
- Se agregó `CLASIFICACION_FINAL_FLU` para identificar casos de influenza

### Datos de Series Temporales
- **Confirmados**: Casos confirmados diarios por entidad (32 estados, 1,218 días)
- **Defunciones**: Defunciones diarias por entidad
- **Negativos**: Casos negativos diarios por entidad
- **Sospechosos**: Casos sospechosos diarios por entidad

### Datos de Texto
- **Twitter/X**: Publicaciones de redes sociales con análisis de sentimientos
- **Noticias UNAM Global**: Artículos de noticias extraídos automáticamente (2020-2023)
- **Período**: 2020-2023 (era COVID-19)
- **Idiomas**: Principalmente español e inglés
- **Características**: Sentimientos, ubicación geográfica, entidades nombradas

## Tecnologías Utilizadas

### Base de Datos
- **PostgreSQL 16+** con Apache AGE (Graph Database Extension)
- **Docker** para contenedorización
- **SQLAlchemy** para ORM
- **psycopg2** para conexión directa

### Análisis de Datos
- **Python 3.10+**
- **Pandas**: Manipulación de datos
- **NumPy**: Cálculos numéricos
- **OpenPyXL**: Lectura de archivos Excel
- **BeautifulSoup4**: Web scraping para noticias
- **Requests**: Cliente HTTP

### Visualización y Análisis
- **Jupyter Notebooks**: Análisis interactivo
- **Matplotlib/Seaborn**: Visualizaciones
- **Apache AGE**: Consultas de grafos con Cypher

## Instalación y Configuración

#### Prerrequisitos
- Docker y Docker Compose instalados
- Git

#### Pasos de Instalación

1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd project
```

2. **Configurar variables de entorno:**
```bash
# Crear archivo .env en la raíz del proyecto
cat > .env << EOF
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=covid_analysis
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
EOF
```

3. **Iniciar la base de datos PostgreSQL con Apache AGE:**
```bash
# Iniciar el contenedor de PostgreSQL
docker-compose up -d

# Verificar que el contenedor esté ejecutándose
docker-compose ps

# Ver logs del contenedor
docker-compose logs postgres
```

4. **Esperar a que la base de datos esté lista:**
```bash
# Verificar conexión (opcional)
docker-compose exec postgres psql -U postgres -d covid_analysis -c "SELECT version();"
```

5. **Instalar dependencias de Python:**
```bash
# Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

6. **Ejecutar el pipeline de datos:**
```bash
# Ejecutar el notebook principal
jupyter notebook notebooks/main_post.ipynb
```

#### Comandos Docker Útiles

```bash
# Iniciar servicios
docker-compose up -d

# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart

# Ver logs en tiempo real
docker-compose logs -f postgres

# Acceder al contenedor PostgreSQL
docker-compose exec postgres psql -U postgres -d covid_analysis

# Eliminar volúmenes (CUIDADO: elimina todos los datos)
docker-compose down -v

# Reconstruir contenedor
docker-compose up -d --build

# Ver estado de contenedores
docker-compose ps

# Ver uso de recursos
docker stats
```

## Scripts de Inicialización

### Descarga Automática de Noticias (`init-scripts/download_covid_news.py`)

Este script automatiza la extracción de noticias de COVID-19 desde UNAM Global:

```bash
# Ejecutar desde la raíz del proyecto
python init-scripts/download_covid_news.py
```

**Características:**
- Extrae noticias de UNAM Global (2020-2023)
- Procesa automáticamente todos los meses del período
- Guarda archivos de texto limpios en `data/text/`
- Maneja errores y reintentos automáticos
- Genera logs detallados del proceso

**Archivos generados:**
- `data/text/1_2020.txt` hasta `data/text/12_2023.txt`
- Formato estructurado para procesamiento con LLMs
- Metadatos incluidos (autor, fecha, categorías)


## Uso del Sistema

### 1. Inicialización Completa

```bash
# 1. Iniciar base de datos
docker-compose up -d

# 2. Descargar noticias (opcional)
python init-scripts/download_covid_news.py

# 3. Ejecutar pipeline de datos
jupyter notebook notebooks/main_post.ipynb
```

### 2. Verificación del Sistema

```bash
# Verificar conexión a base de datos
docker-compose exec postgres psql -U postgres -d covid_analysis -c "
SELECT 
    schemaname, 
    tablename, 
    n_tup_ins as records
FROM pg_stat_user_tables 
WHERE schemaname IN ('relational', 'graph', 'text', 'federation')
ORDER BY schemaname, tablename;
"
```

### 3. Consultas de Ejemplo

```sql
-- Ver datos unificados
SELECT * FROM federation.unified_covid_data LIMIT 10;

-- Análisis de correlación
SELECT * FROM federation.comprehensive_correlation 
WHERE fecha >= '2020-03-01' 
ORDER BY fecha DESC 
LIMIT 10;

-- Análisis de grafos
SELECT * FROM cypher('covid_timeseries', $$
    MATCH (e:entidad)-[r:TIENE_CASOS]->(f:fecha)
    WHERE f.metrica = 'confirmados' AND r.valor > 1000
    RETURN e.nombre, f.fecha, r.valor
    ORDER BY r.valor DESC
    LIMIT 10
$$) AS (entidad agtype, fecha agtype, valor agtype);
```

## Características Principales

### Integración Multimodal Implementada
- **Relacional-Gráfico**: Integración entre casos individuales y métricas agregadas
- **Gráfico-Texto**: Análisis de correlación entre sentimientos y números de casos
- **Vista Unificada**: Esquema canónico para consultas integradas
- **Dataset de Investigación**: Vista limpia y optimizada para análisis

### Análisis Disponibles
- Análisis temporal de la pandemia por entidad federativa (2020-2023)
- Correlación entre sentimientos de redes sociales y métricas de salud
- Análisis geográfico de la propagación del virus
- Análisis de correlación entre sentimientos y casos por métrica
- Integración de datos multi-año con procesamiento optimizado

### Métricas Calculadas
- Tasas de incidencia por 100,000 habitantes
- Tasas de letalidad
- Tasas de positividad de pruebas
- Análisis de sentimientos agregados por día/ubicación
- Correlaciones entre sentimientos y métricas de salud

## Esquema de Base de Datos

### Esquemas Organizados
- **`relational`**: Datos de casos individuales COVID-19
- **`graph`**: Datos de series temporales (Apache AGE)
- **`text`**: Datos de noticias y análisis de texto
- **`federation`**: Vistas unificadas para análisis

### Vistas Principales
- **`federation.unified_covid_data`**: Vista unificada de todas las fuentes
- **`federation.comprehensive_correlation`**: Correlación entre fuentes de datos
- **`federation.graph_analysis`**: Análisis avanzado de series temporales
- **`federation.graph_data_extracted`**: Extracción de datos de grafos

### Logs y Monitoreo

```bash
# Ver logs de la base de datos
docker-compose logs -f postgres

# Monitorear uso de recursos
docker stats

# Verificar espacio en disco
docker system df
```
