DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS joueurs;
DROP TABLE IF EXISTS map;
DROP TABLE IF EXISTS agent;

CREATE TABLE IF NOT EXISTS role(
   idRole INT NOT NULL AUTO_INCREMENT,
   libelle VARCHAR(50),
   PRIMARY KEY(idRole)
);

CREATE TABLE IF NOT EXISTS joueurs(
    idJoueur INT NOT NULL AUTO_INCREMENT,
    pseudo VARCHAR(50),
    login VARCHAR(50),
    email VARCHAR(50),
    mdp VARCHAR(255),
    fonction VARCHAR(50),
    idRole INT NOT NULL,
    PRIMARY KEY(idJoueur),
    FOREIGN KEY(idRole) REFERENCES Role(idRole)
);

CREATE TABLE IF NOT EXISTS map(
  idMap INT NOT NULL AUTO_INCREMENT,
  libelle VARCHAR(50),
    PRIMARY KEY (idMap)
);

CREATE TABLE IF NOT EXISTS agent(
  idAgent INT NOT NULL AUTO_INCREMENT,
    nomAgent VARCHAR(50),
    PRIMARY KEY (idAgent)
);

INSERT INTO agent (nomAgent) VALUES
('Brimstone'),
('Viper'),
('Omen'),
('Killjoy'),
('Cypher'),
('Sova'),
('Sage'),
('Phoenix'),
('Jett'),
('Reyna'),
('Breach'),
('Skye'),
('Yoru'),
('Astra'),
('KAY/O'),
('Iso'),
('Raze'),
('Deadlock'),
('Fade'),
('Chamber'),
('Clove'),
('Gekko'),
('Harbor'),
('Néon')
;



INSERT INTO map(idMap, libelle) VALUES
(NULL,'Ascent'),
(NULL,'Bind'),
(NULL,'Breeze'),
(NULL,'Icebox'),
(NULL,'Lotus'),
(NULL,'Split'),
(NULL,'Sunset'),
(NULL,'Fracture'),
(NULL,'Haven');

