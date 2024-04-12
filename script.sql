DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS joueurs;
DROP TABLE IF EXISTS map;
DROP TABLE IF EXISTS agent;
# DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS compo;

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

# CREATE TABLE IF NOT EXISTS utilisateur(
#     idUtilisateur INT NOT NULL AUTO_INCREMENT,
#     nomUtilisateur VARCHAR(50),
#     email VARCHAR(50),
#     mdp VARCHAR(255),
#     idJoueur INT,
#     PRIMARY KEY(idUtilisateur),
#     FOREIGN KEY (idJoueur) REFERENCES joueurs(idJoueur)
# );


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

CREATE TABLE IF NOT EXISTS compo(
    idJoueur INT,
    idMap INT,
    idAgent INT,
    PRIMARY KEY (idJoueur,idMap,idAgent),
    FOREIGN KEY (idJoueur) REFERENCES joueurs(idJoueur),
    FOREIGN KEY (idMap) REFERENCES map(idMap),
    FOREIGN KEY (idAgent) REFERENCES agent(idAgent)
);

INSERT INTO compo (idJoueur, idMap, idAgent) VALUES
(1, 1, 1),
(2, 2, 2),
(3, 3, 3),
(4, 4, 4),
(5, 5, 5),
(1, 6, 6),
(2, 7, 7),
(3, 1, 8),
(4, 2, 9),
(5, 3, 10),
(1, 4, 11),
(2, 5, 12),
(3, 6, 13),
(4, 7, 14),
(5, 1, 15);


INSERT INTO agent (nomAgent) VALUES
('Astra'),
('Breach'),
('Brimstone'),
('Chamber'),
('Clove'),
('Cypher'),
('Deadlock'),
('Fade'),
('Gekko'),
('Harbor'),
('Iso'),
('Jett'),
('KAY/O'),
('Killjoy'),
('Neon'),
('Omen'),
('Phoenix'),
('Raze'),
('Reyna'),
('Skye'),
('Sage'),
('Sova'),
('Viper'),
('Yoru');




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

