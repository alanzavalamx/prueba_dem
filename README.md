# Actividad 1: ETL Excel Adyacencia

Este repositorio orquesta un pipeline de Dagster que carga una matriz de relaciones desde un archivo Excel hacia una base de datos MySQL, utilizando Dagster como orquestador.
Todo basado en una Arquitectura escalable utilizando Docker para todos los componentes.

## 📋 Requisitos previos

* **Docker** (>=20.10) (https://docs.docker.com/desktop/setup/install/windows-install/)
* **Docker Compose** (>=1.29)
* Git https://git-scm.com/downloads (o puedes descargar directmente el repositorio)
* (Opcional) **Cliente MySQL** para validación manual

## 🗂️ Estructura del proyecto

```text
.
├── docker-compose.yml
├── Dockerfile_mysql
├── Dockerfile_dagster
├── Dockerfile_user_code
├── init.sql                  # Creación de DB, tabla y usuario 
├── dagster.yaml             # Configuración de storage en Postgres
├── workspace.yaml           # Definición de workspace de Dagster
├── requirements.txt         # Dependencias de Python
└── ops/                     # Código del pipeline
    └── app.py
    └── definitions.py
    └── Matriz_de_adyacencia_data_team.xlsx

```

Nota: Para cualquier prueba podras sustituir el archivo de Excel dentro de la carpeta ops/

Docker la tiene enlazada la carpeta con un volumen, asi mismo cambios en el codigo de app.py o definitions.py se podran realizar y reflejarse inmediatamente.

## ⚙️ Configuración de entorno

1. Clona el repositorio:

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
   ```

## 🚀 Levantar los servicios con Docker Compose

```bash
docker-compose up -d --build
```


## 🎛️ Uso

1. Abre la interfaz web de Dagster (Dagit): [http://localhost:3000](http://localhost:3000)
2. Ejecuta manualmente el job `daily_app_job` o verifica el schedule diario. 
4. Observa en pantalla el estado de la corrida y los logs.

<img width="1393" height="92" alt="image" src="https://github.com/user-attachments/assets/d9f66d33-9934-4ed3-a0a4-5ca499d72df7" />
<img width="1574" height="806" alt="image" src="https://github.com/user-attachments/assets/a106a41e-ccc8-493e-94ec-6210a86187c4" />

## Base de Datos y Tabla.

Dentro de init.sql esta el codigo para crear la base de datos y tabla que sera alimentada con los datos del Excel.
Nota: Docker la creara automaticamente al cargarse el Dockerfile de MySQL

```Docker
FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=RootP@ssw0rd
ENV MYSQL_DATABASE=relationships_db
ENV MYSQL_USER=PalaceAdmin
ENV MYSQL_PASSWORD=Str0ngSecurePAssw0rd

COPY ./init.sql /docker-entrypoint-initdb.d/

EXPOSE 3306

VOLUME ["/var/lib/mysql"]
```

```SQL
CREATE DATABASE IF NOT EXISTS relationships_db;
USE relationships_db;

-- Crea la tabla de relaciones
CREATE TABLE IF NOT EXISTS person_relationship (
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    person_a VARCHAR(255) NOT NULL,
    person_b VARCHAR(255) NOT NULL,
    relationship TINYINT(1) NOT NULL,
    PRIMARY KEY (person_a, person_b, date_created)
);


CREATE USER IF NOT EXISTS 'PalaceAdmin'@'%' 
  IDENTIFIED BY 'Str0ngSecurePAssw0rd';
GRANT ALL PRIVILEGES 
  ON relationships_db.* 
  TO 'PalaceAdmin'@'%';

FLUSH PRIVILEGES;
```

## Aplicacion ETL

Dentro de *ops/app.py* encontraras un codigo basico que leera, acomodara y cargara los datos a MySQL
Para la tabla de adycencia solo se toma en cuenta las relaciones (1) para reducir el espacio de los datos, el resto se toma como obvio sin relacion (0).


```python
import pandas as pd
from sqlalchemy import create_engine

def main():
    engine = create_engine(
        "mysql+pymysql://PalaceAdmin:Str0ngSecurePAssw0rd@mysql-db:3306/relationships_db"
    )

    df = (
        pd.read_excel("Matriz_de_adyacencia_data_team.xlsx")
        .iloc[1:, 2:]
        .reset_index()
        .rename(columns={"index": "person_a"})
    )

    df = df.melt(id_vars=["person_a"], var_name="person_b", value_name="relationship")
    df = df[df["relationship"] > 0].reset_index(drop=True)
    df["date_created"] = pd.Timestamp.now()

    df.to_sql(
        name="person_relationship",
        con=engine,
        if_exists="append",
        index=False,
    )

    print(f"Table 'person_relationship' updated with {len(df)} records.")

if __name__ == "__main__":
    main()
```

## ✅ Validación de inserción de datos

### Desde Command Prompt o Powershell

```bash
# Conéctate y muestra algunas filas
1. docker exec -it mysql-db bash
2. mysql -h 127.0.0.1 -P 3306 -u PalaceAdmin -p relationships_db
3. Str0ngSecurePAssw0rd
4. SELECT * FROM relationships_db.person_relationship;
```

<img width="437" height="180" alt="image" src="https://github.com/user-attachments/assets/83c84509-b952-42a5-93bf-7e887cacc55c" />


### Usando un cliente externo

Puedes descargar MySQL Workbench 
https://dev.mysql.com/downloads/file/?id=539682

<img width="508" height="469" alt="image" src="https://github.com/user-attachments/assets/510875b7-50b1-4931-b5ce-1a520cb0e423" />

---

Con estos pasos podrás construir, desplegar y probar tu pipeline Dagster con MySQL como backend de datos y de metadata. ¡Éxito!
