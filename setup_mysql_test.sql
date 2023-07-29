-- Prepares a MySQL Test server for the project.

-- Revoke existing privileges if any
REVOKE ALL PRIVILEGES ON hbnb_test_db.* FROM 'hbnb_test'@'localhost';
REVOKE SELECT ON performance_schema.* FROM 'hbnb_test'@'localhost';

-- Create the database if not exists
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Create the user if not exists
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant privileges to the user
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';

-- Flush privileges to apply the changes
FLUSH PRIVILEGES;
