DROP TABLE IF EXISTS role;
DROP TABLE IF EXISTS joueurs;

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





