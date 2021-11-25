USE myFitnessFiends;

DROP TABLE IF EXISTS monsterForms;
CREATE TABLE monsterForms (
	monster_species varchar(64) NOT NULL,
    form_number int NOT NULL,
    level_min int NOT NULL,
    level_max int
) ENGINE=InnoDB;

INSERT INTO monsterForms (monster_species, form_number, level_min, level_max)
VALUES
	("aqua", 1, 0, 5),
    ("aqua", 2, 6, 10),
    ("aqua", 3, 11, NULL),
    ("blob", 1, 0, 5),
    ("blob", 2, 6, 10),
    ("blob", 3, 11, 15),
    ("blob", 4, 16, NULL);
    