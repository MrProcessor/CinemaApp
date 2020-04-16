CREATE DATABASE IF NOT EXISTS cinema_db;
USE cinema_db;

-- 1
CREATE TABLE cinema (
    id INTEGER AUTO_INCREMENT,
    city VARCHAR(30) NOT NULL,
    address VARCHAR(55) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB;

-- 2
CREATE TABLE room (
    id INTEGER AUTO_INCREMENT,
    id_cinema INTEGER,
    place_amount INTEGER UNSIGNED NOT NULL, -- dodać trigger
    room_number INTEGER NOT NULL, -- dodać trigger
    PRIMARY KEY (id),
    FOREIGN KEY
		(id_cinema) REFERENCES cinema(id)
		ON DELETE CASCADE
) ENGINE=InnoDB;

-- 3
CREATE TABLE movie (
    id INTEGER AUTO_INCREMENT,
    title VARCHAR(45) NOT NULL,
    technology ENUM('2D', '3D') NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB;

-- 4
CREATE TABLE customer (
    id INTEGER AUTO_INCREMENT,
    f_name VARCHAR(25) NOT NULL,
    l_name VARCHAR(25) NOT NULL,
    phone INTEGER(9) NOT NULL UNIQUE,
    PRIMARY KEY (id)
) ENGINE=InnoDB;

-- 5
CREATE TABLE place (
    id INTEGER AUTO_INCREMENT,
    id_room INTEGER,
    place_number INTEGER UNSIGNED NOT NULL, -- trigger?
    PRIMARY KEY (id),
    FOREIGN KEY
		(id_room) REFERENCES room (id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- 6
CREATE TABLE projection (
    id INTEGER AUTO_INCREMENT,
    proj_date TIMESTAMP NOT NULL,
    id_movie INTEGER,
    id_room INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY
		(id_movie) REFERENCES movie(id)
        ON DELETE CASCADE,
	FOREIGN KEY
		(id_room) REFERENCES room(id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- 7
CREATE TABLE booking (
    id INTEGER AUTO_INCREMENT,
    id_place INTEGER,
    id_customer INTEGER,
    id_projection INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY
		(id_place) REFERENCES place (id)
        ON DELETE CASCADE,
	FOREIGN KEY
		(id_customer) REFERENCES customer (id)
        ON DELETE CASCADE,
	FOREIGN KEY
		(id_projection) REFERENCES projection (id)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- Trigger that adds seats after insert on room
delimiter $$
create trigger room_add after insert on room
for each row
begin
	SET @set_number = 1;
	i: LOOP
		INSERT INTO place(id_room, place_number) VALUES (NEW.id, @set_number);
        SET @set_number = @set_number + 1;
        IF @set_number > NEW.place_amount THEN LEAVE i; END IF;
	END LOOP i;
end;
$$
delimiter ;

-- Procedure that adds booking (and new customer if not exists)
delimiter $$
CREATE PROCEDURE add_booking(IN cus_f_name VARCHAR(25), IN cus_l_name VARCHAR(25), IN cus_phone INTEGER(9), IN cus_id_place INTEGER, IN cus_id_projection INTEGER)
begin
    IF NOT EXISTS(select id from customer where f_name = cus_f_name AND l_name = cus_l_name AND phone = cus_phone) THEN
		INSERT INTO customer(f_name, l_name, phone) VALUES (cus_f_name, cus_l_name, cus_phone);
    END IF;
    SET @actual_cus_id = (select id from customer where f_name = cus_f_name AND l_name = cus_l_name AND phone = cus_phone);
    INSERT INTO booking(id_place, id_customer, id_projection) VALUES (cus_id_place, @actual_cus_id, cus_id_projection);
end $$
delimiter ;