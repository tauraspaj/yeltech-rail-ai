CREATE DATABASE yeltech_ai_db;
USE yeltech_ai_db;
SET default_storage_engine=InnoDB;
SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE models (
    _model_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    model_file_name VARCHAR(255) NOT NULL,
    param_provider VARCHAR(255) NOT NULL
);

CREATE TABLE prediction_parameters (
    _parameter_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    parameter_name VARCHAR(255) NOT NULL,
    unit VARCHAR(255),
    param_provider VARCHAR(255) NOT NULL
);

CREATE TABLE model_parameters (
    _model_parameter_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    model_id INT UNSIGNED NOT NULL,
    prediction_parameter_id INT UNSIGNED NOT NULL,
    FOREIGN KEY (model_id) REFERENCES models(_model_id),
    FOREIGN KEY (prediction_parameter_id) REFERENCES prediction_parameters(_parameter_id)
);

CREATE TABLE devices (
    _device_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    device_name VARCHAR(255) NOT NULL,
    prediction_status BOOLEAN DEFAULT 0 NOT NULL,
    latitude DECIMAL(10, 6),
    longitude DECIMAL(10, 6),
    depo_location VARCHAR(255) NOT NULL,
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

CREATE TABLE parameter_history (
    _parameter_history_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY NOT NULL,
    parameter_value VARCHAR(255) DEFAULT NULL,
    parameter_id INT UNSIGNED,
    prediction_id INT UNSIGNED,
    FOREIGN KEY (parameter_id) REFERENCES prediction_parameters(_parameter_id),
    FOREIGN KEY (prediction_id) REFERENCES predictions(_prediction_id)
);

INSERT INTO prediction_parameters(parameter_name, unit, param_provider)
VALUES
    ('month', null, 'Manual'),
    ('day_of_year', null, 'Manual'),
    ('hour_of_day', null, 'Manual'),
    ('azimuth', null, 'Manual'),
    ('altitude', null, 'Manual'),
    ('temperature_2m', 'C', 'Open-Meteo'),
    ('relativehumidity_2m', '%', 'Open-Meteo'),
    ('dewpoint_2m', 'C', 'Open-Meteo'),
    ('apparent_temperature', 'C', 'Open-Meteo'),
    ('precipitation', 'mm', 'Open-Meteo'),
    ('cloudcover', '%', 'Open-Meteo'),
    ('cloudcover_low', '%', 'Open-Meteo'),
    ('cloudcover_mid', '%', 'Open-Meteo'),
    ('cloudcover_high', '%', 'Open-Meteo'),
    ('shortwave_radiation', 'w/m2', 'Open-Meteo'),
    ('et0_fao_evapotranspiration', 'mm', 'Open-Meteo'),
    ('windspeed_10m', 'km/h', 'Open-Meteo'),
    ('direct_radiation', 'w/m2', 'Open-Meteo'),
    ('diffuse_radiation', 'w/m2', 'Open-Meteo'),
    ('direct_normal_irradiance', 'w/m2', 'Open-Meteo'),
    ('depo_location', null, 'Manual');

INSERT INTO models(model_file_name, param_provider) VALUES ('baseline_global_lgbm_mean_model.pkl', 'Open-Meteo');
INSERT INTO models(model_file_name, param_provider) VALUES ('baseline_global_lgbm_95q_model.pkl', 'Open-Meteo');
INSERT INTO models(model_file_name, param_provider) VALUES ('baseline_global_lgbm_5q_model.pkl', 'Open-Meteo');
INSERT INTO models(model_file_name, param_provider) VALUES ('baseline_global_lgbm_50q_model.pkl', 'Open-Meteo');

INSERT INTO model_parameters(model_id, prediction_parameter_id) VALUES
	(1, 1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9), (1,10), (1,11), (1,12), (1, 13), (1,14), (1,15), (1,16), (1,17), (1,18), (1,19), (1,20), (1,21);
INSERT INTO model_parameters(model_id, prediction_parameter_id) VALUES
	(2, 1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (2,9), (2,10), (2,11), (2,12), (2, 13), (2,14), (2,15), (2,16), (2,17), (2,18), (2,19), (2,20);
INSERT INTO model_parameters(model_id, prediction_parameter_id) VALUES
	(3, 1), (3,2), (3,3), (3,4), (3,5), (3,6), (3,7), (3,8), (3,9), (3,10), (3,11), (3,12), (3, 13), (3,14), (3,15), (3,16), (3,17), (3,18), (3,19), (3,20);
INSERT INTO model_parameters(model_id, prediction_parameter_id) VALUES
	(4, 1), (4,2), (4,3), (4,4), (4,5), (4,6), (4,7), (4,8), (4,9), (4,10), (4,11), (4,12), (4, 13), (4,14), (4,15), (4,16), (4,17), (4,18), (4,19), (4,20);

INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2941', 1, 52.055988, -2.717550, 1, 'Hereford');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2941', 1, 52.055988, -2.717550, 2, 'Hereford');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2941', 1, 52.055988, -2.717550, 3, 'Hereford');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2941', 1, 52.055988, -2.717550, 4, 'Hereford');

INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 3225', 1, 51.702048, -0.708333, 1, 'Saltley');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 3225', 1, 51.702048, -0.708333, 2, 'Saltley');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 3225', 1, 51.702048, -0.708333, 3, 'Saltley');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 3225', 1, 51.702048, -0.708333, 4, 'Saltley');

INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2757', 1, 51.519930, -0.194570, 1, 'Plumstead');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2757', 1, 51.519930, -0.194570, 2, 'Plumstead');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2757', 1, 51.519930, -0.194570, 3, 'Plumstead');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2757', 1, 51.519930, -0.194570, 4, 'Plumstead');

INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 3187', 1, 51.406272, 0.386779, 1, 'High Speed Singlewell');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 3187', 1, 51.406272, 0.386779, 2, 'High Speed Singlewell');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 3187', 1, 51.406272, 0.386779, 3, 'High Speed Singlewell');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 3187', 1, 51.406272, 0.386779, 4, 'High Speed Singlewell');

INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2915', 1, 51.538691, 0.083143, 1, 'Barking');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2915', 1, 51.538691, 0.083143, 2, 'Barking');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2915', 1, 51.538691, 0.083143, 3, 'Barking');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2915', 1, 51.538691, 0.083143, 4, 'Barking');

INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2823', 1, 51.139800, 0.879120, 1, 'Ashford');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2823', 1, 51.139800, 0.879120, 2, 'Ashford');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2823', 1, 51.139800, 0.879120, 3, 'Ashford');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2823', 1, 51.139800, 0.879120, 4, 'Ashford');
