-- voor DP8/9 is het gebruik van een database vereist
-- gebruik deze startcode om (snel) een database te maken om mee te werken
-- het staat je vrij om de database naar eigen inzicht aan te passen
-- het databaseontwerp staat beschreven in het aangeleverde technisch ontwerp
-- succes!

CREATE DATABASE bestelinterface;

USE bestelinterface;

CREATE TABLE categorie (
    id INTEGER(10) PRIMARY KEY AUTO_INCREMENT,
    naam VARCHAR(255) NOT NULL
);

CREATE TABLE menu (
    id INTEGER(10) PRIMARY KEY AUTO_INCREMENT,
    naam VARCHAR(255) NOT NULL
);

CREATE TABLE product (
    id INTEGER(10) PRIMARY KEY AUTO_INCREMENT,
    categorie_id INTEGER(10),
    naam VARCHAR(255) NOT NULL,
    prijs DECIMAL(6,2) NOT NULL,
    kcal INTEGER(10),
    FOREIGN KEY (categorie_id) REFERENCES categorie(id) ON DELETE SET NULL
);

CREATE TABLE menu_producten (
    menu_id INTEGER(10),
    product_id INTEGER(10),
    aantal INTEGER(10) NOT NULL,
    PRIMARY KEY (menu_id, product_id),
    FOREIGN KEY (menu_id) REFERENCES menu(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
);

CREATE TABLE bestelling (
    id INTEGER(10) PRIMARY KEY AUTO_INCREMENT,
    datum_tijd DATETIME NOT NULL,
    tafelnummer INTEGER(10) NOT NULL
);

CREATE TABLE bestelling_items (
    bestelling_id INTEGER(10),
    product_id INTEGER(10),
    aantal INTEGER(10) NOT NULL,
    opmerking VARCHAR(255),
    PRIMARY KEY (bestelling_id, product_id),
    FOREIGN KEY (bestelling_id) REFERENCES bestelling(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE
);


-- graag dit veranderen naar je eigen (test)gegevens
#CREATE USER IF NOT EXISTS 'bestelinterface_user'@'localhost' IDENTIFIED BY 'bi123';
GRANT ALL PRIVILEGES ON bestelinterface.* TO 'bestelinterface_user'@'localhost';
FLUSH PRIVILEGES;
