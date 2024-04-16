SET sql_mode=(SELECT CONCAT(@@sql_mode,',ONLY_FULL_GROUP_BY'));

DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS joueurs;
DROP TABLE IF EXISTS map;
DROP TABLE IF EXISTS agent;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS compo;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS heure;
DROP TABLE IF EXISTS jour;
DROP TABLE IF EXISTS horaire;

CREATE TABLE IF NOT EXISTS role(
   idRole INT NOT NULL AUTO_INCREMENT,
   libelle VARCHAR(50),
   PRIMARY KEY(idRole)
);

CREATE TABLE IF NOT EXISTS joueurs(
    idJoueur INT NOT NULL AUTO_INCREMENT,
    pseudo VARCHAR(50),
    titulaire boolean,
    idRole INT NOT NULL,
    PRIMARY KEY(idJoueur),
    FOREIGN KEY(idRole) REFERENCES Role(idRole)
);

CREATE TABLE IF NOT EXISTS utilisateur(
   idUtilisateur INT not null auto_increment,
   nomUtilisateur VARCHAR(50),
   login VARCHAR(50),
   email VARCHAR(50),
   mdp VARCHAR(255),
    fonction VARCHAR(50),
    connected boolean,
   idAdmin INT ,
   idJoueur INT ,
   PRIMARY KEY(idUtilisateur),
   UNIQUE(idAdmin),
   UNIQUE(idJoueur),
   FOREIGN KEY(idAdmin) REFERENCES admin(idAdmin),
   FOREIGN KEY(idJoueur) REFERENCES Joueurs(idJoueur)
);

CREATE TABLE IF NOT EXISTS admin(
   idAdmin INT not null auto_increment,
   nomAdmin VARCHAR(50),
   PRIMARY KEY(idAdmin)
);

CREATE TABLE IF NOT EXISTS map(
  idMap INT NOT NULL AUTO_INCREMENT,
  libelle VARCHAR(50),
    PRIMARY KEY (idMap)
);

CREATE TABLE IF NOT EXISTS agent(
  idAgent INT AUTO_INCREMENT,
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

CREATE TABLE IF NOT EXISTS jour(
   idJour INT,
   nomJour VARCHAR(50),
   PRIMARY KEY(idJour)
);

CREATE TABLE IF NOT EXISTS heure(
   idHeure INT,
   heure boolean,
   PRIMARY KEY(idHeure)
);

CREATE TABLE IF NOT EXISTS horaire(
   idJoueur INT,
   idJour INT,
   idHeure INT,
   PRIMARY KEY(idJoueur, idJour, idHeure),
   FOREIGN KEY(idJoueur) REFERENCES Joueurs(idJoueur),
   FOREIGN KEY(idJour) REFERENCES Jour(idJour),
   FOREIGN KEY(idHeure) REFERENCES Heure(idHeure)
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
('None'),
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

INSERT INTO utilisateur ( nomUtilisateur, login, email, mdp, fonction,connected ,idAdmin, idJoueur) VALUES
( 'SpicyFire', 'SpicyFire', 'khnagui.adam@gmail.com', 'pbkdf2:sha256:600000$m3xBga3XDY6uJ1xN$643e2e8a715664cc946998a911ef5f448d26e042ff8a6915166b1faa2406e2e6', 'player',FALSE, 1, 1),
( 'sPer', 'sPer', 'email@email.com', 'pbkdf2:sha256:600000$O9qKKhEFNyQ7hRuH$42c407dea492321a6fe1111c4ca3a8ddd32f5ac692ab9a6f1ea5560eacc74c33', 'player',FALSE, null, 2),
( 'DracotiuM', 'DracotiuM', 'email@email.com', 'pbkdf2:sha256:600000$OOZasfGUuvZLLJwb$129b88a20f33102a30558f75adda1d2879003017d467a80a4a727d769b823e14', 'player',FALSE, 2, 3),
( 'Diamond', 'Diamond', 'email@email.com', 'pbkdf2:sha256:600000$l87LCYNGvs52HS8M$4c02c55dec139ea7b32d98eec763f610846fd135e3f3b7c7c2d17201784f2993', 'player',FALSE, null, 4),
( 'Zerios', 'Zerios', 'email@email.com', 'pbkdf2:sha256:600000$TGhqz3j9ggePkEcv$0b6c8570399d567daef07578bce853315c129610c77a975b851caacf07dfe59f', 'player',FALSE, null, 5);

INSERT INTO joueurs (pseudo, titulaire, idRole) VALUES
('SpicyFire', TRUE, 1),
('sPer', TRUE, 2),
('DracotiuM', TRUE, 3),
('Diamond', TRUE, 4),
('Zerios', TRUE, 2);

INSERT INTO role(idRole, libelle) VALUES
(1,'Duelliste'),
(2,'Initiateur'),
(3,'Flex'),
(4,'Controlleur'),
(5,'Sentinelle'),
(6,'Remplaçant'),
(7,'Coach'),
(8,'Non défini');

INSERT INTO admin ( nomAdmin) VALUES
( 'Admin-SpicyFire'),
( 'Admin-DracotiuM');

INSERT INTO jour (idJour, nomJour) VALUES
(1, 'Lundi'),
(2, 'Mardi'),
(3, 'Mercredi'),
(4, 'Jeudi'),
(5, 'Vendredi'),
(6, 'Samedi'),
(7,'Dimanche');

INSERT INTO heure (idHeure, heure) VALUES
(1, FALSE),
(2, FALSE),
(3, FALSE),
(4, FALSE),
(5, FALSE),
(6, FALSE),
(7, FALSE),
(8, FALSE),
(9, FALSE),
(10, FALSE),
(11, FALSE),
(12, FALSE),
(13, FALSE),
(14, FALSE),
(15, FALSE),
(16, FALSE),
(17, FALSE),
(18, FALSE),
(19, FALSE),
(20, FALSE),
(21, FALSE),
(22, FALSE),
(23, FALSE),
(24, FALSE);



# INSERT INTO joueurs (idJoueur, pseudo, login, email, mdp, fonction, idRole) VALUES
# (1, 'SpicyFire', 'SpicyFire', 'khnagui.adam@gmail.com', 'pbkdf2:sha256:600000$m3xBga3XDY6uJ1xN$643e2e8a715664cc946998a911ef5f448d26e042ff8a6915166b1faa2406e2e6', 'player', 0),
# (2, 'sPer', 'sPer', 'email@email.com', 'pbkdf2:sha256:600000$O9qKKhEFNyQ7hRuH$42c407dea492321a6fe1111c4ca3a8ddd32f5ac692ab9a6f1ea5560eacc74c33', 'player', 0),
# (3, 'DracotiuM', 'DracotiuM', 'email@email.com', 'pbkdf2:sha256:600000$OOZasfGUuvZLLJwb$129b88a20f33102a30558f75adda1d2879003017d467a80a4a727d769b823e14', 'player', 0),
# (4, 'Diamond', 'Diamond', 'email@email.com', 'pbkdf2:sha256:600000$l87LCYNGvs52HS8M$4c02c55dec139ea7b32d98eec763f610846fd135e3f3b7c7c2d17201784f2993', 'player', 0),
# (5, 'Zerios', 'Zerios', 'email@email.com', 'pbkdf2:sha256:600000$TGhqz3j9ggePkEcv$0b6c8570399d567daef07578bce853315c129610c77a975b851caacf07dfe59f', 'player', 0);

