# Proyecto Dagster + MySQL

Este repositorio orquesta un pipeline de Dagster que carga una matriz de relaciones desde un archivo Excel hacia una base de datos MySQL, y persiste metadata (runs, eventos y schedules) también en MySQL.

## 📋 Requisitos previos

* **Docker** (>=20.10)
* **Docker Compose** (>=1.29)
* (Opcional) **Cliente MySQL** para validación manual

## 🗂️ Estructura del proyecto

```text
.
├── docker-compose.yml
├── Dockerfile_mysql
├── Dockerfile_dagster
├── Dockerfile_user_code
├── init.sql                  # Creación de DB, tabla y usuario fileciteturn3file0
├── dagster.yaml             # Configuración de storage en MySQL
├── workspace.yaml           # Definición de workspace de Dagster
├── requirements.txt         # Dependencias de Python fileciteturn3file1
└── src/                     # Código del pipeline (transform & load)
    └── pipeline.py
```

## ⚙️ Configuración de entorno

1. Clona el repositorio:

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
   ```
2. Define la variable de conexión a MySQL:

   ```bash
   export MYSQL_URL=mysql+pymysql://PalaceAdmin:Str0ngSecurePAssw0rd@mysql-palace:3306/relationships_db
   ```

## 🚀 Levantar los servicios

### Con Docker Compose

Solo un paso para crear y correr todos los contenedores:

```bash
docker-compose up -d --build
```

### Método manual

1. **MySQL**

   ```bash
   docker build -f Dockerfile_mysql -t mysql-custom .
   docker run -d \
     --name mysql-palace \
     -p 3306:3306 \
     -v mysql_data:/var/lib/mysql \
     mysql-custom
   ```
2. **Dagster + Dagit**

   ```bash
   docker build -f Dockerfile_dagster -t dagster-mysql .
   docker run -d \
     --name dagster \
     --link mysql-palace:mysql-palace \
     -p 3000:3000 \
     -e MYSQL_URL=$MYSQL_URL \
     -v dagster_home:/opt/dagster_home \
     dagster-mysql
   ```
3. **Código del pipeline** (si aplica)

   ```bash
   docker build -f Dockerfile_user_code -t pipeline-code .
   docker run -d \
     --name pipeline-code \
     --link mysql-palace:mysql-palace \
     pipeline-code
   ```

## 🎛️ Uso

1. Abre la interfaz web de Dagster (Dagit): [http://localhost:3000](http://localhost:3000)
2. Ejecuta manualmente el job `relationships_job` o verifica el schedule diario.
3. Observa en pantalla el estado de la corrida y los logs.

## ✅ Validación de inserción de datos

### Desde dentro del contenedor MySQL

```bash
# Conéctate y muestra algunas filas
docker exec -it mysql-palace mysql \
  -UPalaceAdmin -pStr0ngSecurePAssw0rd \
  -e "SELECT * FROM relationships_db.person_relationship LIMIT 10;"
```

### Usando un cliente externo

```bash
mysql -h127.0.0.1 -P3306 -UPalaceAdmin -p
# contraseña: Str0ngSecurePAssw0rd

USE relationships_db;
SELECT COUNT(*) FROM person_relationship;
```

---

Con estos pasos podrás construir, desplegar y probar tu pipeline Dagster con MySQL como backend de datos y de metadata. ¡Éxito!
