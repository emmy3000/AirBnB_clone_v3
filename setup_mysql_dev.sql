-- Prepares a MySQL server for the project.

-- Revoke existing privileges if any
REVOKE ALL PRIVILEGES ON hbnb_dev_db.* FROM 'hbnb_dev'@'localhost';
REVOKE SELECT ON performance_schema.* FROM 'hbnb_dev'@'localhost';

-- Create the database if not exists
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create the user if not exists
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- Flush privileges to apply the changes
FLUSH PRIVILEGES;
