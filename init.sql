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

