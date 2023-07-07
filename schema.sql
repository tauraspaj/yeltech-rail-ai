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

INSERT INTO prediction_parameters(_parameter_id, parameter_name, unit, param_provider)
VALUES
    (1, 'depo_location', null, 'Manual'),
    (2, 'device_name', null, 'Manual'),
    (3, 'month', null, 'Manual'),
    (4, 'day_of_year', null, 'Manual'),
    (5, 'hour_of_day', null, 'Manual'),
    (6, 'datetime', null, 'Visual-Crossing'),
    (7, 'temp', 'C', 'Visual-Crossing'),
    (8, 'dew', 'C', 'Visual-Crossing'),
    (9, 'humidity', '%', 'Visual-Crossing'),
    (10, 'precip', 'mm', 'Visual-Crossing'),
    (11, 'visibility', '%', 'Visual-Crossing'),
    (12, 'solarradiation', 'W/m2', 'Visual-Crossing'),
    (13, 'solarenergy', 'Wh', 'Visual-Crossing');

INSERT INTO models(model_file_name, param_provider) VALUES ('baseline_sensor_vc_cleaned_model.pkl', 'Visual-Crossing');
INSERT INTO models(model_file_name, param_provider) VALUES ('baseline_sensor_vc_model.pkl', 'Visual-Crossing');

INSERT INTO model_parameters(model_id, prediction_parameter_id) VALUES
	(1, 1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9), (1,10), (1,11), (1,12), (1, 13);
INSERT INTO model_parameters(model_id, prediction_parameter_id) VALUES
	(2, 1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (2,9), (2,10), (2,11), (2,12), (2, 13);


INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2941', 1, 52.055988, -2.717550, 1, 'Hereford');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2941', 1, 52.055988, -2.717550, 2, 'Hereford');

INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 3225', 1, 51.702048, -0.708333, 1, 'Saltley');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 3225', 1, 51.702048, -0.708333, 2, 'Saltley');

INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2757', 1, 51.519930, -0.194570, 1, 'Plumstead');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2757', 1, 51.519930, -0.194570, 2, 'Plumstead');

INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 3187', 1, 51.406272, 0.386779, 1, 'High Speed Singlewell');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 3187', 1, 51.406272, 0.386779, 2, 'High Speed Singlewell');

INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2915', 1, 51.538691, 0.083143, 1, 'Barking');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2915', 1, 51.538691, 0.083143, 2, 'Barking');

INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2823', 1, 51.139800, 0.879120, 1, 'Ashford');
INSERT INTO devices(device_name, prediction_status, latitude, longitude, model_id, depo_location) VALUES ('RTMU 2823', 1, 51.139800, 0.879120, 2, 'Ashford');
