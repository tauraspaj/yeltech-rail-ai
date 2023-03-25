CREATE DATABASE yeltech_ai_db;
USE yeltech_ai_db;
SET default_storage_engine=InnoDB;

CREATE TABLE models (
    _model_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    model_file_name VARCHAR(255) NOT NULL
);

CREATE TABLE devices (
    _device_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    device_name VARCHAR(255) NOT NULL,
    prediction_status BOOLEAN DEFAULT 0 NOT NULL,
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    model_id INT UNSIGNED DEFAULT NULL,
    FOREIGN KEY (model_id) REFERENCES models(_model_id)
);

CREATE TABLE predictions (
    _prediction_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    time_of_execution TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    prediction FLOAT NOT NULL,
    prediction_timestamp TIMESTAMP,
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    model_id INT UNSIGNED,
    device_id INT UNSIGNED,
    FOREIGN KEY (model_id) REFERENCES models(_model_id),
    FOREIGN KEY (device_id) REFERENCES devices(_device_id)
);

CREATE TABLE prediction_parameters (
    _parameter_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    parameter_name VARCHAR(255) NOT NULL,
    unit VARCHAR(255) NOT NULL,
    param_provider VARCHAR(255) NOT NULL
);

CREATE TABLE parameter_history (
    _parameter_history_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    is_used BOOLEAN DEFAULT 0,
    parameter_value FLOAT DEFAULT NULL,
    parameter_id INT UNSIGNED,
    prediction_id INT UNSIGNED,
    FOREIGN KEY (parameter_id) REFERENCES prediction_parameters(_parameter_id),
    FOREIGN KEY (prediction_id) REFERENCES predictions(_prediction_id)
);

INSERT INTO prediction_parameters(parameter_name, unit, param_provider)
VALUES
    ('month', 'INT', 'Manual'),
    ('day_of_year', 'INT', 'Manual'),
    ('hour_of_day', 'INT', 'Manual'),
    ('temperature_2m', 'C', 'Open-Meteo'),
    ('relativehumidity_2m', '%', 'Open-Meteo'),
    ('dewpoint_2m', 'C', 'Open-Meteo'),
    ('apparent_temperature', 'C', 'Open-Meteo'),
    ('rain', 'mm', 'Open-Meteo'),
    ('showers', 'mm', 'Open-Meteo'),
    ('cloudcover', '%', 'Open-Meteo'),
    ('cloudcover_low', '%', 'Open-Meteo'),
    ('cloudcover_mid', '%', 'Open-Meteo'),
    ('cloudcover_high', '%', 'Open-Meteo'),
    ('shortwave_radiation', 'w/m2', 'Open-Meteo'),
    ('evapotranspiration', 'mm', 'Open-Meteo'),
    ('et0_fao_evapotranspiration', 'mm', 'Open-Meteo'),
    ('windspeed_10m', 'km/h', 'Open-Meteo'),
    ('shortwave_radiation', 'w/m2', 'Open-Meteo'),
    ('direct_radiation', 'w/m2', 'Open-Meteo'),
    ('diffuse_radiation', 'w/m2', 'Open-Meteo'),
    ('direct_normal_irradiance', 'w/m2', 'Open-Meteo'),
    ('terrestrial_radiation', 'w/m2', 'Open-Meteo');
