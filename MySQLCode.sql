-- DROP DATABASE ble_mesh_parameters;

CREATE DATABASE ble_mesh_parameters;

USE ble_mesh_parameters6;

CREATE TABLE configurations (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    TTL INT(1) NOT NULL,
    TransmissionPower INT(1) NOT NULL,
    TransmissionsNumber INT(1) NOT NULL,
    IntervalTime INT(4) NOT NULL
) ENGINE = INNODB;

CREATE TABLE parameters_performance (
    ID_performance INT AUTO_INCREMENT PRIMARY KEY,
    ID_configurations INT NOT NULL,
    DeviceID INT(1) NOT NULL,
    TTLResidue INT(1) NOT NULL,
    PerformanceDelay DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (ID_configurations) REFERENCES configurations(ID) ON DELETE CASCADE
) ENGINE = INNODB;

CREATE TABLE parameters_pdr (
    ID_PDR INT AUTO_INCREMENT PRIMARY KEY,
    ID_configurations INT NOT NULL,
    PDRSend INT(4) NOT NULL,
    PDRReceived INT(4) NOT NULL,
    FOREIGN KEY (ID_configurations) REFERENCES configurations(ID) ON DELETE CASCADE
) ENGINE = INNODB;
