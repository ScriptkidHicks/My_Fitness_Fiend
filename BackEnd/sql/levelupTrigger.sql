USE myFitnessFiends;

/* Level Up and Form Trigger */
DELIMITER //
DROP TRIGGER IF EXISTS level_trigger //
CREATE TRIGGER level_trigger 
BEFORE UPDATE ON monsters
FOR EACH ROW
BEGIN
	/* LEVELS UP THE MONSTER APPROPRIATELY */
	/* Only check the exp if it changed */
	IF NEW.exp <> OLD.exp THEN
		/* Define the experience cap value */
		SET @expCap = (4 * POWER(OLD.level, 3) / 5);
        
        /* While we still are over the exp cap */
        WHILE NEW.exp > @expCap DO
			SET NEW.exp = NEW.exp - @expCap;				/* Decrement the exp */
            SET NEW.level = NEW.level + 1;					/* Increment the level */
            SET @expCap = (4 * POWER(NEW.level, 3) / 5);	/* Reset the exp cap for this level */
        END WHILE;
    END IF;
    
    /* SET THE MONSTER'S FORM APPROPRIATELY */
	# Grab the max level that the species can have (in terms of forms)
	SET @maxLevel = (
		SELECT level_min
        FROM monsterForms
        WHERE monsterForms.monster_species=OLD.species
        ORDER BY level_min DESC
        LIMIT 1
	);
    
    /* If the monster isn't at the max level */
    IF NEW.level < @maxLevel THEN
		/* Set the new form number to the correct form (based on the monster's level) from the monsterForm table */
		SET NEW.form = (
			SELECT form_number
			FROM monsterForms 
			WHERE 
				monsterForms.monster_species=OLD.species AND 
				NEW.level BETWEEN monsterForms.level_min AND monsterForms.level_max
			ORDER BY 
				monsterForms.form_number DESC
		);
	/* Otherwise, we're at the max level, so set it to the max form */
	ELSE 
		SET @maxForm = (
			SELECT form_number 
            FROM monsterForms 
            WHERE monsterForms.monster_species=OLD.species 
            ORDER BY monsterForms.form_number DESC
            LIMIT 1
        );
		SET NEW.form = @maxForm;
    END IF;
END;//
DELIMITER ;

