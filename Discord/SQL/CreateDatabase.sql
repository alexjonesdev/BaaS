CREATE DATABASE `discord` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
CREATE TABLE `mhw_armor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `category` varchar(45) NOT NULL,
  `rarity` int(11) DEFAULT '0',
  `defense` int(11) DEFAULT '0',
  `fire` int(11) DEFAULT '0',
  `water` int(11) DEFAULT '0',
  `thunder` int(11) DEFAULT '0',
  `ice` int(11) DEFAULT '0',
  `dragon` int(11) DEFAULT '0',
  `slot1` int(11) DEFAULT '0',
  `slot2` int(11) DEFAULT '0',
  `slot3` int(11) DEFAULT '0',
  `slot4` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1527 DEFAULT CHARSET=utf8mb4 COMMENT='a table for holding armor and their stats';

CREATE TABLE `mhw_armor_set` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `rarity` int(11) DEFAULT '0',
  `bonus` varchar(45) DEFAULT NULL,
  `bonus_description` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=utf8mb4 COMMENT='a table for holding armor sets and their bonus';

CREATE TABLE `mhw_armor_set_piece` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `armor_set_id` int(11) NOT NULL,
  `armor_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_piece_set_idx` (`armor_set_id`),
  KEY `fk_piece_armor_idx` (`armor_id`),
  CONSTRAINT `fk_piece_armor` FOREIGN KEY (`armor_id`) REFERENCES `mhw_armor` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_piece_set` FOREIGN KEY (`armor_set_id`) REFERENCES `mhw_armor_set` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='a table for connecting all the pieces of an armor set together';

CREATE TABLE `mhw_monster` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `fire` int(11) DEFAULT '0',
  `water` int(11) DEFAULT '0',
  `thunder` int(11) DEFAULT '0',
  `ice` int(11) DEFAULT '0',
  `dragon` int(11) DEFAULT '0',
  `poison` int(11) DEFAULT '0',
  `sleep` int(11) DEFAULT '0',
  `paralysis` int(11) DEFAULT '0',
  `blast` int(11) DEFAULT '0',
  `stun` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='a table for holding monsters and their stats';

CREATE TABLE `mhw_skill` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `levels` int(11) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=115 DEFAULT CHARSET=utf8mb4 COMMENT='a table for holding skills and their descriptions';

CREATE TABLE `mhw_tools` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `category` varchar(45) DEFAULT NULL,
  `effect` varchar(500) DEFAULT NULL,
  `duration` int(11) DEFAULT '0',
  `recharge` int(11) DEFAULT NULL,
  `acquire` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='a table for holding the specialized tools';

CREATE TABLE `mhw_weapon` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) CHARACTER SET utf8 NOT NULL,
  `category` varchar(45) CHARACTER SET utf8 NOT NULL,
  `attack` int(11) DEFAULT NULL,
  `element` varchar(45) CHARACTER SET utf8 DEFAULT NULL,
  `element_amount` int(11) DEFAULT NULL,
  `element_locked` tinyint(1) DEFAULT NULL,
  `mod` int(11) DEFAULT NULL,
  `affinity` int(11) DEFAULT '0',
  `slot1` int(11) DEFAULT '0',
  `slot2` int(11) DEFAULT '0',
  `slot3` int(11) DEFAULT '0',
  `slot4` int(11) DEFAULT '0',
  `augmentation` int(11) DEFAULT '0',
  `rarity` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1206 DEFAULT CHARSET=utf8mb4 COMMENT='a table for holding weapons and their stats';

CREATE TABLE `test` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `value` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='a test table';
