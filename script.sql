#! /usr/bin/python
# -*- coding:utf-8 -*-

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
DROP TABLE IF EXISTS matchs;
DROP TABLE IF EXISTS pracc;
DROP TABLE IF EXISTS root;
DROP TABLE IF EXISTS Plan;
DROP TABLE IF EXISTS indexPatch;
DROP TABLE IF EXISTS indexDiscord;
DROP TABLE IF EXISTS log;
drop table  if exists dossierPlan;

DROP TABLE IF EXISTS images;
CREATE TABLE if not exists images(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    image LONGBLOB NOT NULL
);


CREATE TABLE IF NOT EXISTS root(
  idRoot INT not null auto_increment,
  nomRoot VARCHAR(50) ,
  mdp VARCHAR(255) ,
  PRIMARY KEY (idRoot)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;



CREATE TABLE IF NOT EXISTS role(
   idRole INT NOT NULL AUTO_INCREMENT,
   libelle VARCHAR(50) ,
   PRIMARY KEY(idRole)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS joueurs(
    idJoueur INT NOT NULL AUTO_INCREMENT,
    pseudo VARCHAR(50) ,
    titulaire BOOLEAN,
    idRole INT NOT NULL,
    PRIMARY KEY(idJoueur),
    FOREIGN KEY(idRole) REFERENCES Role(idRole)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS utilisateur(
   idUtilisateur INT not null auto_increment,
   nomUtilisateur VARCHAR(50) ,
    imgProfile LONGBLOB,
   login VARCHAR(50) ,
   email VARCHAR(50) ,
   mdp VARCHAR(255) ,
   fonction VARCHAR(50) ,
   connected BOOLEAN,
   idAdmin INT,
   idJoueur INT,
   PRIMARY KEY(idUtilisateur),
   UNIQUE(idAdmin),
   UNIQUE(idJoueur),
   FOREIGN KEY(idAdmin) REFERENCES admin(idAdmin),
   FOREIGN KEY(idJoueur) REFERENCES Joueurs(idJoueur)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS admin(
   idAdmin INT not null auto_increment,
   nomAdmin VARCHAR(50) ,
   PRIMARY KEY(idAdmin)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS map(
  idMap INT NOT NULL AUTO_INCREMENT,
  libelle VARCHAR(50) ,
    imgMap VARCHAR(255),
  PRIMARY KEY (idMap)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS agent(
  idAgent INT AUTO_INCREMENT,
  nomAgent VARCHAR(50) ,
    imgAgent VARCHAR(255),
    roleAgent VARCHAR(50),
  PRIMARY KEY (idAgent)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS compo(
    idJoueur INT,
    idMap INT,
    idAgent INT,
    PRIMARY KEY (idJoueur,idMap,idAgent),
    FOREIGN KEY (idJoueur) REFERENCES joueurs(idJoueur),
    FOREIGN KEY (idMap) REFERENCES map(idMap),
    FOREIGN KEY (idAgent) REFERENCES agent(idAgent)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS jour(
   idJour INT,
   nomJour VARCHAR(50) ,
   PRIMARY KEY(idJour)
) DEFAULT CHARACTER SET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE IF NOT EXISTS heure(
   idHeure INT,
   heure BOOLEAN,
   PRIMARY KEY(idHeure)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS horaire(
   idJoueur INT,
   idJour INT,
   idHeure INT,
   PRIMARY KEY(idJoueur, idJour, idHeure),
   FOREIGN KEY(idJoueur) REFERENCES Joueurs(idJoueur),
   FOREIGN KEY(idJour) REFERENCES Jour(idJour),
   FOREIGN KEY(idHeure) REFERENCES Heure(idHeure)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS matchs(
    idMatch INT NOT NULL AUTO_INCREMENT,
    nomMatch VARCHAR(50) ,
    commentaire VARCHAR(255) ,
    date_match DATE,
    date_ajout DATETIME,
    lien VARCHAR(255),
    idJoueur INT,
    idAdmin INT,
    PRIMARY KEY (idMatch),
    FOREIGN KEY (idJoueur) references joueurs(idJoueur),
    FOREIGN KEY (idAdmin) references admin(idAdmin)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS pracc(
    idPracc INT NOT NULL AUTO_INCREMENT,
    nomPracc VARCHAR(50) ,
    commentaire VARCHAR(255) ,
    date_pracc DATE,
    date_ajout DATETIME,
    idJoueur INT,
    idAdmin INT,
    PRIMARY KEY (idPracc),
    FOREIGN KEY (idJoueur) references joueurs(idJoueur),
    FOREIGN KEY (idAdmin) references admin(idAdmin)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;


CREATE TABLE IF NOT EXISTS Plan (
    idPlan INT NOT NULL AUTO_INCREMENT,
    nomPlan VARCHAR(50),
    description VARCHAR(255),
    Image LONGBLOB,
    idDossier int,
    PRIMARY KEY (idPlan),
    foreign key (idDossier) references dossierPlan(idDossier)
)CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;


create table if not exists dossierPlan (
    idDossier int not null auto_increment,
    nomDossier VARCHAR(50),
    description VARCHAR(255),
    idMap int,
    primary key (idDossier),
    foreign key (idMap) references map(idMap)
)CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS indexDiscord(
    idindexDiscord int not null auto_increment,
    nomAdmin VARCHAR(50),
    contenu VARCHAR(2550),
    date datetime,
    primary key (idindexDiscord)
)CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS indexPatch(
    idindexPatch int not null auto_increment,
    nomAdmin VARCHAR(50),
    contenu VARCHAR(2550),
    date datetime,
    primary key (idindexPatch)
)CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS log(
    idlog int not null auto_increment,
    idAdmin INT,

    typeaction varchar(255),
    oldaction varchar(255),
    newaction varchar(255),
    date datetime,
    saved boolean,
    primary key (idlog),
    FOREIGN KEY (idAdmin) references admin(idAdmin)
)CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;




INSERT INTO role (libelle)
VALUES
('Duelliste'),
('Initiateur'),
('Flex'),
('Controlleur'),
('Sentinelle'),
('Remplaçant'),
('Coach'),
('Non Défini')
;

INSERT INTO matchs (nomMatch, date_match, date_ajout) VALUES
('Match1', '2024-04-01', NOW()),
('Match2', '2024-04-05', NOW()),
('Match3', '2024-04-10', NOW()),
('Match4', '2024-04-15', NOW()),
('Match5', '2024-04-20', NOW())
;

INSERT INTO pracc (nomPracc, date_pracc, date_ajout) VALUES
('Pracc1', '2024-04-02', NOW()),
('Pracc2', '2024-04-06', NOW()),
('Pracc3', '2024-04-11', NOW()),
('Pracc4', '2024-04-16', NOW()),
('Pracc5', '2024-04-21', NOW())
;

INSERT INTO `compo` (`idJoueur`, `idMap`, `idAgent`) VALUES
('1', '1', '25'),
('1', '2', '6'),
('1', '3', '20'),
('1', '4', '6'),
('1', '5', '20'),
('1', '6', '6'),
('1', '7', '6'),
('1', '8', '25'),
('1', '9', '25'),
('1', '10', '25'),
('2', '1', '8'),
('2', '2', '4'),
('2', '3', '3'),
('2', '4', '2'),
('2', '5', '8'),
('2', '6', '4'),
('2', '7', '2'),
('2', '8', '3'),
('2', '9', '2'),
('2', '10', '11'),
('3', '1', '12'),
('3', '2', '9'),
('3', '3', '4'),
('3', '4', '9'),
('3', '5', '11'),
('3', '6', '2'),
('3', '7', '3'),
('3', '8', '9'),
('3', '9', '12'),
('3', '10', '4'),
('4', '1', '24'),
('4', '2', '24'),
('4', '3', '17'),
('4', '4', '13'),
('4', '5', '14'),
('4', '6', '24'),
('4', '7', '24'),
('4', '8', '16'),
('4', '9', '14'),
('4', '10', '24'),
('5', '1', '11'),
('5', '2', '10'),
('5', '3', '12'),
('5', '4', '14'),
('5', '5', '10'),
('5', '6', '12'),
('5', '7', '10'),
('5', '8', '10'),
('5', '9', '11'),
('5', '10', '12');


INSERT INTO agent (nomAgent) VALUES('None');

INSERT INTO utilisateur ( nomUtilisateur, login, email, mdp, fonction,connected ,idAdmin, idJoueur) VALUES
( 'SpicyFire', 'SpicyFire', 'khnagui.adam@gmail.com', 'pbkdf2:sha256:600000$m3xBga3XDY6uJ1xN$643e2e8a715664cc946998a911ef5f448d26e042ff8a6915166b1faa2406e2e6', 'PLAYER',FALSE, 2, 1),
( 'sPer', 'sPer', 'email@email.com', 'pbkdf2:sha256:600000$O9qKKhEFNyQ7hRuH$42c407dea492321a6fe1111c4ca3a8ddd32f5ac692ab9a6f1ea5560eacc74c33', 'PLAYER',FALSE, null, 2),
( 'DracotiuM', 'DracotiuM', 'email@email.com', 'pbkdf2:sha256:600000$OOZasfGUuvZLLJwb$129b88a20f33102a30558f75adda1d2879003017d467a80a4a727d769b823e14', 'PLAYER',FALSE, 3, 3),
( 'Diamond', 'Diamond', 'email@email.com', 'pbkdf2:sha256:600000$l87LCYNGvs52HS8M$4c02c55dec139ea7b32d98eec763f610846fd135e3f3b7c7c2d17201784f2993', 'PLAYER',FALSE, null, 4),
( 'Zerios', 'Zerios', 'email@email.com', 'pbkdf2:sha256:600000$TGhqz3j9ggePkEcv$0b6c8570399d567daef07578bce853315c129610c77a975b851caacf07dfe59f', 'PLAYER',FALSE, null, 5);

INSERT INTO joueurs (pseudo, titulaire, idRole) VALUES
('SpicyFire', TRUE, 1),
('sPer', TRUE, 2),
('DracotiuM', TRUE, 3),
('Diamond', TRUE, 4),
('Zerios', TRUE, 2);



INSERT INTO admin (nomAdmin) VALUES
('API'),
('SpicyFire'),
('DracotiuM');

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

INSERT INTO root (nomRoot,mdp) values ('root1','pbkdf2:sha256:600000$m3xBga3XDY6uJ1xN$643e2e8a715664cc946998a911ef5f448d26e042ff8a6915166b1faa2406e2e6');
