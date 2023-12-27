-- sql script


CREATE DATABASE IF NOT EXISTS bank_db;
       CREATE USER IF NOT EXISTS 'bank_user'@'localhost' IDENTIFIED BY 'bank_pwd';
              GRANT ALL PRIVILEGES ON bank_db.* TO 'bank_user'@'localhost';
                                      GRANT SELECT ON performance_schema.* TO 'bank_user'@'localhost';
FLUSH PRIVILEGES;