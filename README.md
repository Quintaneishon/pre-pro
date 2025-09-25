# Análisis Multimodal de Datos COVID-19 en México

Este proyecto integra múltiples fuentes de datos para realizar análisis comprehensivos sobre la pandemia de COVID-19 en México, combinando datos relacionales, series temporales y análisis de noticias.

## Descripción del Proyecto

El proyecto implementa un pipeline de análisis multimodal que integra:
- **Datos relacionales**: Casos individuales de COVID-19 con información clínica detallada (2020-2023)
- **Datos de series temporales**: Métricas diarias por entidad federativa
- **Datos de texto**: Análisis de sentimientos de noticias

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
- **Noticias UNAM Global**: Artículos de noticias extraídos automáticamente (2020-2023)
- **Período**: 2020-2023 (era COVID-19)
- **Idiomas**: Principalmente español e inglés
- **Características**: Sentimientos, ubicación geográfica, entidades nombradas

## Tecnologías Utilizadas

### Base de Datos
- **PostgreSQL 16+** con Apache AGE (Graph Database Extension)
- **Docker** para contenedorización
- **SQLAlchemy** para ORM y carga masiva de datos desde pandas DataFrames
- **psycopg2** para conexión directa, operaciones DDL, y funciones específicas de PostgreSQL (extensiones, grafos AGE)

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

#### Descarga de Datos

**IMPORTANTE**: Los archivos de datos son demasiado grandes para GitHub (>1GB). Debes descargarlos por separado desde las fuentes oficiales:

### 1. 📊 Datos Relacionales (COVID-19) - Secretaría de Salud México

**Fuente Oficial**: [Datos Abiertos - Dirección General de Epidemiología](https://www.gob.mx/salud/documentos/datos-abiertos-152127)

**Enlaces de Descarga Directa:**
   - [COVID19MEXICO2020.csv](https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/historicos/2020/COVID19MEXICO2020.zip) (~620MB) - 3.8M registros
   - [COVID19MEXICO2021.csv](https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/historicos/2021/COVID19MEXICO2021.zip) (~1.4GB) - 8.8M registros  
   - [COVID19MEXICO2022.csv](https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/historicos/2022/COVID19MEXICO2022.zip) (~1.0GB) - 6.5M registros
   - [COVID19MEXICO2023.csv](https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/historicos/2023/COVID19MEXICO2023.zip) (~190MB) - 1.2M registros

**Ubicación en el proyecto**: `data/relational/`

### 2. 📈 Datos de Series Temporales - CONACYT

**Fuente Oficial**: [COVID-19 Tablero México - CONACYT](https://datos.covid-19.conacyt.mx/)

**Portal de Descarga**: [Sección de Descargas CSV](https://datos.covid-19.conacyt.mx/#DownZCSV)

**Ubicación en el proyecto**: `data/graph/`

### 3. 📰 Datos de Texto - UNAM Global

**Fuente Oficial**: [UNAM Global - Cobertura Coronavirus](https://unamglobal.unam.mx/cobertura-coronavirus/)

**Extracción Automática de Noticias**:

```bash
# Ejecutar script de descarga automática (2020-2023)
python init-scripts/download_covid_news.py
```

**Ubicación en el proyecto**: `data/text/`

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

## 🔧 Scripts de Inicialización

### Descarga Automática de Noticias (`init-scripts/download_covid_news.py`)

Este script automatiza la extracción completa de noticias de COVID-19 desde UNAM Global:

```bash
# Ejecutar desde la raíz del proyecto
python init-scripts/download_covid_news.py
```

**Características Técnicas:**
- ✅ Extrae noticias de UNAM Global (enero 2020 - diciembre 2023)
- ✅ Procesamiento automático de 48 meses de datos
- ✅ Parsing inteligente de contenido HTML con BeautifulSoup4
- ✅ Manejo robusto de errores y reintentos automáticos
- ✅ User-Agent real para evitar bloqueos
- ✅ Genera logs detallados del proceso con timestamps
- ✅ Extracción de metadatos (título, autor, fecha, categorías)
- ✅ Limpieza y estructuración de texto para análisis con LLMs

**Archivos Generados:**
- `data/text/1_2020.txt` hasta `data/text/12_2023.txt` (48 archivos)
- Formato estructurado compatible con procesamiento de LLMs
- Metadatos incluidos: autor, fecha publicación, categorías temáticas
- Separadores claros entre artículos para análisis individual

**Ejemplo de Estructura de Archivo Generado:**
```
=== ARTÍCULO 1 ===
Título: [Título del artículo]
Autor: [Nombre del autor]
Fecha: [DD de Mes de YYYY]
Categorías: [Cat1, Cat2, Cat3]
--- CONTENIDO ---
[Contenido completo del artículo...]

=== ARTÍCULO 2 ===
[...]
```

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

## Esquema de Base de Datos

### Esquemas Organizados
- **`relational`**: Datos de casos individuales COVID-19
- **`graph`**: Datos de series temporales (Apache AGE)
- **`text`**: Datos de noticias y análisis de texto
- **`federation`**: Vistas unificadas para análisis

### Logs y Monitoreo

```bash
# Ver logs de la base de datos
docker-compose logs -f postgres

# Monitorear uso de recursos
docker stats

# Verificar espacio en disco
docker system df
```
