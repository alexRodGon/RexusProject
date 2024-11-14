-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         10.4.32-MariaDB - mariadb.org binary distribution
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para projecte
CREATE DATABASE IF NOT EXISTS `projecte` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `projecte`;

-- Volcando estructura para tabla projecte.grup
CREATE TABLE IF NOT EXISTS `grup` (
  `idGrup` int(11) NOT NULL AUTO_INCREMENT,
  `nomGrup` varchar(50) NOT NULL DEFAULT '0',
  `descripcioGrup` varchar(128) NOT NULL DEFAULT '0',
  `dataCreacioGrup` date DEFAULT NULL,
  PRIMARY KEY (`idGrup`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla projecte.grup: ~17 rows (aproximadamente)
DELETE FROM `grup`;
INSERT INTO `grup` (`idGrup`, `nomGrup`, `descripcioGrup`, `dataCreacioGrup`) VALUES
	(10, 'wsbwbw', 'webwebwbe', '2024-04-29'),
	(14, '4g3g43g', '3g34g34g', NULL),
	(15, 'ggnn', 'tnntntnen', NULL),
	(16, 'fykfyffy', 'fkyfykykfykfy', '2024-04-29'),
	(18, 'si', 'si', '2024-04-29'),
	(19, 'tnetnet', 'netnentetnetn', '2024-04-29'),
	(21, 'probva', 'tntnproprvbomamev', '2024-04-30'),
	(22, 'noajajja', 'noajjaja', '2024-05-09'),
	(24, 'qbqbq', 'bqbqbq', '2024-05-13'),
	(25, 'qbqbqb', 'qbqbqbq', '2024-05-13'),
	(26, 'bqbqbq', 'bqbqbqb', '2024-05-13'),
	(27, 'CR7', 'siuuuu', '2024-05-15'),
	(28, 'Grtupo1', 'ebebeb', '2024-05-16'),
	(29, 'Equipo de Desarrollo Web', 'El grupo de desarrollo web es un equipo multidisciplinario de profesionales dedicados a la creación y mantenimiento de sitios we', '2024-05-16'),
	(30, 'CodeLib', 'Este equipo multidisciplinario está compuesto por profesionales altamente capacitados en diferentes áreas de la tecnología de la', '2024-05-16'),
	(31, 'EduTech Solutions', 'Este equipo multidisciplinario está compuesto por profesionales con experiencia en el desarrollo de aplicaciones educativas y te', '2024-05-16'),
	(32, 'FinanceTech', 'Este equipo multidisciplinario está compuesto por profesionales con experiencia en desarrollo de aplicaciones móviles y finanzas', '2024-05-16');

-- Volcando estructura para tabla projecte.grupsprojecte
CREATE TABLE IF NOT EXISTS `grupsprojecte` (
  `idProjecte` int(11) NOT NULL,
  `idGrup` int(11) NOT NULL,
  PRIMARY KEY (`idProjecte`,`idGrup`),
  KEY `FK_grupsprojecte_grup` (`idGrup`),
  CONSTRAINT `FK_grupsprojecte_grup` FOREIGN KEY (`idGrup`) REFERENCES `grup` (`idGrup`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_grupsprojecte_projecte` FOREIGN KEY (`idProjecte`) REFERENCES `projecte` (`idProjecte`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla projecte.grupsprojecte: ~19 rows (aproximadamente)
DELETE FROM `grupsprojecte`;
INSERT INTO `grupsprojecte` (`idProjecte`, `idGrup`) VALUES
	(0, 14),
	(0, 16),
	(0, 21),
	(0, 22),
	(1, 21),
	(4, 21),
	(5, 21),
	(6, 21),
	(22, 18),
	(22, 21),
	(24, 27),
	(25, 28),
	(26, 27),
	(26, 28),
	(27, 28),
	(28, 29),
	(29, 30),
	(30, 31),
	(31, 32);

-- Volcando estructura para tabla projecte.membresgrup
CREATE TABLE IF NOT EXISTS `membresgrup` (
  `idGrup` int(11) NOT NULL,
  `idUsuari` int(11) NOT NULL,
  PRIMARY KEY (`idGrup`,`idUsuari`),
  KEY `FK_membresgrup_usuari` (`idUsuari`),
  CONSTRAINT `FK_membresgrup_grup` FOREIGN KEY (`idGrup`) REFERENCES `grup` (`idGrup`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_membresgrup_usuari` FOREIGN KEY (`idUsuari`) REFERENCES `usuari` (`idUsuari`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla projecte.membresgrup: ~15 rows (aproximadamente)
DELETE FROM `membresgrup`;
INSERT INTO `membresgrup` (`idGrup`, `idUsuari`) VALUES
	(18, 3),
	(21, 3),
	(21, 14),
	(22, 3),
	(22, 14),
	(24, 3),
	(25, 3),
	(26, 3),
	(27, 15),
	(28, 15),
	(29, 3),
	(29, 17),
	(30, 17),
	(31, 17),
	(32, 3),
	(32, 17);

-- Volcando estructura para tabla projecte.nota
CREATE TABLE IF NOT EXISTS `nota` (
  `idNota` int(11) NOT NULL AUTO_INCREMENT,
  `titolNota` varchar(250) NOT NULL DEFAULT '',
  `contingutNota` varchar(250) NOT NULL DEFAULT '',
  `dataM` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `idUsuari` int(11) NOT NULL,
  PRIMARY KEY (`idNota`),
  KEY `FK_nota_usuari` (`idUsuari`),
  CONSTRAINT `FK_nota_usuari` FOREIGN KEY (`idUsuari`) REFERENCES `usuari` (`idUsuari`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla projecte.nota: ~18 rows (aproximadamente)
DELETE FROM `nota`;
INSERT INTO `nota` (`idNota`, `titolNota`, `contingutNota`, `dataM`, `idUsuari`) VALUES
	(3, 'nota 3', 'no', '2024-04-15 17:26:33', 3),
	(13, 'nota 1', 'nota 1', '2024-04-15 17:26:33', 3),
	(15, 'Lorem', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam posuere egestas eros, eget eleifend libero dapibus ac. Vestibulum bibendum sit amet diam ut aliquam. Maecenas varius aliquam posuere. Integer consequat diam urna, id fermentum urna egesta', '2024-04-15 17:26:33', 3),
	(16, 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam posuere egestas eros, eget eleifend libero dapibus ac. Vestibulum bibendum sit amet diam ut aliquam. Maecenas varius aliquam posuere. Integer consequat diam urna, id fermentum urna egesta', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam posuere egestas eros, eget eleifend libero dapibus ac. Vestibulum bibendum sit amet diam ut aliquam. Maecenas varius aliquam posuere. Integer consequat diam urna, id fermentum urna egesta', '2024-04-15 17:26:33', 3),
	(17, 'Lorem ipsum dolor sit amet', 'Lorem ipsum dolor sit amet', '2024-04-15 17:26:33', 3),
	(18, 'Lorem ipsum dolor sit amet', 'Lorem ipsum dolor sit amet', '2024-04-15 17:26:33', 3),
	(19, 'Lorem ipsum dolor sit amet', 'Lorem ipsum dolor sit amet', '2024-04-15 17:26:33', 3),
	(20, 'Lorem ipsum dolor sit amet', 'Lorem ipsum dolor sit amet', '2024-04-15 17:26:33', 3),
	(21, 'Lorem ipsum dolor sit amet', 'Lorem ipsum dolor sit amet', '2024-04-15 17:26:33', 3),
	(22, 'Lorem ipsum dolor sit amet', 'Lorem ipsum dolor sit amet', '2024-04-15 17:26:33', 3),
	(24, 'uwu', 'uwu', '2024-04-15 17:26:33', 4),
	(25, 'ramon', 'ramon', '2024-04-15 17:26:33', 14),
	(26, 'vinvionaivnanoevi', 'nievnienbienbienbienb', '2024-04-15 17:31:56', 3),
	(27, 'ebwbewbwbwebbwbdvdv', 'webewbbwbwbwbeb', '2024-04-23 18:07:50', 3),
	(28, 'vavava', 'vavavavav', '2024-04-15 17:38:39', 3),
	(30, 'zaaaaaaaaaa', 'aaaaaaaaaaaa', '2024-05-14 17:55:09', 3),
	(31, 'hula', 'hula', '2024-05-14 22:23:39', 15),
	(32, 'ebvaeb', 'ebaaeb', '2024-05-15 22:17:23', 15),
	(34, 'Diseño de la Interfaz de Usuario', 'Utilizar herramientas como Figma o Sketch para diseñar la interfaz.', '2024-05-16 20:15:17', 17),
	(35, 'Desarrollo del Backend', 'Crear la lógica de negocio y desarrollar la API para manejar las solicitudes del cliente.', '2024-05-16 20:15:37', 17),
	(36, 'Desarrollo de la Aplicación Móvil', 'Utilizar un enfoque de desarrollo ágil para iterar rápidamente sobre las características y obtener retroalimentación del usuario.', '2024-05-16 20:29:27', 17);

-- Volcando estructura para tabla projecte.projecte
CREATE TABLE IF NOT EXISTS `projecte` (
  `idProjecte` int(11) NOT NULL AUTO_INCREMENT,
  `nomProjecte` varchar(250) NOT NULL DEFAULT '',
  `descripcioProjecte` varchar(250) NOT NULL DEFAULT '',
  `dataCreacioProjecte` date DEFAULT NULL,
  `dataEntregaProjecte` date DEFAULT NULL,
  PRIMARY KEY (`idProjecte`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla projecte.projecte: ~27 rows (aproximadamente)
DELETE FROM `projecte`;
INSERT INTO `projecte` (`idProjecte`, `nomProjecte`, `descripcioProjecte`, `dataCreacioProjecte`, `dataEntregaProjecte`) VALUES
	(0, 'Projecte1', 'Descripcio1', NULL, NULL),
	(1, 'Projecte2', 'no', NULL, NULL),
	(2, 'Projecte3', 'Desccripcio3', NULL, NULL),
	(3, 'hh5h', 'hhhh', '2024-05-10', NULL),
	(4, 'bebe', 'zdbzdbz', '2024-05-13', NULL),
	(5, 'aebvaeb', 'ebaebeae', '2024-05-13', NULL),
	(6, 'ebeb', 'ebeb', '2024-05-13', '2024-05-31'),
	(7, 'vaqvav', 'avavavav', '2024-05-13', '2024-06-06'),
	(8, 'veqvq', 'vqvqvq', '2024-05-13', '2024-05-23'),
	(9, 'eveveve', 'vevevev', '2024-05-13', '2024-05-23'),
	(10, 'eavqev', 'qvqevq', '2024-05-13', '2024-06-01'),
	(11, 'projecte2', 'wfwfw', '2024-05-13', '2024-05-18'),
	(12, 'projecte2', 'projecte2', '2024-05-13', '2024-05-29'),
	(13, 'projecte4', 'veev', '2024-05-13', '2024-05-17'),
	(14, 'aaaaaaaaaaaaaaaaa', 'aaaaaaaaaaaaaaaa', '2024-05-13', '2024-05-30'),
	(15, 'aaaaaaaaa', 'aaaaaaaa', '2024-05-13', '2024-05-24'),
	(16, 'aaaaaaaaaaaaa', 'aaaaaaaaaaaaaaaaa', '2024-05-13', '2024-05-11'),
	(17, 'aaaaaaaaaaaa', 'aaaaaaaaaa', '2024-05-13', '2024-05-29'),
	(18, 'aaaaaaa', 'aaaaaaaaaaaaaa', '2024-05-13', '2024-05-05'),
	(19, 'aaaaaaaaaaaa', 'aaaaaaaaaaaaaaa', '2024-05-13', '2024-05-01'),
	(20, 'aaaaaaaa', 'aaaaaaaaaaaaaaa', '2024-05-13', '2024-05-16'),
	(21, 'aaaaaaaaaaa', 'aaaaaaaaaaaaaa', '2024-05-13', '2024-05-16'),
	(22, 'bbbbbbbbbbbbbbb', 'aaaaaaaaaaaaaaa', '2024-05-13', '2024-05-17'),
	(24, 'MESSI', 'D10S', '2024-05-15', '2024-05-26'),
	(25, 'Proyecto1', 'Proyecto1', '2024-05-16', '2024-06-01'),
	(26, 'Proyecto1', 'Proyecto1', '2024-05-16', '2024-05-24'),
	(27, 'aleeeeeeeee', 'ale', '2024-05-16', '2024-05-24'),
	(28, 'Desarrollo de un sitio web de comercio electrónico', 'El proyecto de desarrollo de un sitio web de comercio electrónico tiene como objetivo principal crear una plataforma en línea donde los usuarios puedan comprar y vender productos o servicios de manera conveniente y segura. Este tipo de plataforma dig', '2024-05-16', '2024-05-31'),
	(29, 'Sistema de Gestión de Biblioteca Virtual', 'Este proyecto consiste en desarrollar una aplicación web para gestionar una biblioteca virtual. Permitirá a los usuarios buscar libros, realizar préstamos, devoluciones, y administrar su cuenta.', '2024-05-16', '2024-05-24'),
	(30, 'Plataforma de Aprendizaje en Línea para Escuelas Secundarias', 'Este proyecto consiste en desarrollar una plataforma en línea que permita a las escuelas secundarias ofrecer cursos virtuales a sus estudiantes. La plataforma incluirá funcionalidades como la creación de clases, entrega de tareas, calificación automá', '2024-05-16', '2024-05-31'),
	(31, 'Aplicación de Gestión de Finanzas Personales', 'La aplicación de gestión de finanzas personales es una herramienta diseñada para ayudar a los usuarios a administrar sus ingresos, gastos y ahorros de manera efectiva. ', '2024-05-16', '2024-05-31');

-- Volcando estructura para tabla projecte.tasca
CREATE TABLE IF NOT EXISTS `tasca` (
  `idTasca` int(11) NOT NULL AUTO_INCREMENT,
  `titolTasca` varchar(250) NOT NULL DEFAULT '',
  `descripcioTasca` varchar(250) NOT NULL DEFAULT '',
  `estatTasca` tinyint(4) DEFAULT 0,
  `dataEntregaTasca` datetime DEFAULT NULL,
  `dataCreacioTasca` timestamp NULL DEFAULT NULL,
  `idUsuari` int(11) DEFAULT NULL,
  `idProjecte` int(11) DEFAULT NULL,
  PRIMARY KEY (`idTasca`),
  KEY `FK_tasca_usuari` (`idUsuari`),
  KEY `FK_tasca_projecte` (`idProjecte`),
  CONSTRAINT `FK_tasca_projecte` FOREIGN KEY (`idProjecte`) REFERENCES `projecte` (`idProjecte`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_tasca_usuari` FOREIGN KEY (`idUsuari`) REFERENCES `usuari` (`idUsuari`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla projecte.tasca: ~28 rows (aproximadamente)
DELETE FROM `tasca`;
INSERT INTO `tasca` (`idTasca`, `titolTasca`, `descripcioTasca`, `estatTasca`, `dataEntregaTasca`, `dataCreacioTasca`, `idUsuari`, `idProjecte`) VALUES
	(0, 'aaaaaaaaaaaaaaaa', 'aaaaaaaaaaaaaaaa', 0, NULL, NULL, NULL, NULL),
	(1, 'bbbbbbbbbbbbbbb', 'bbbbbbbbbbbbbbbb', 0, NULL, NULL, NULL, NULL),
	(6, 'aaaaaaaaaaaaaaaa', '    bbbbbbbbbbbbbb', 0, NULL, NULL, 3, NULL),
	(7, 'aaaaaa', 'aaaaaaaaa', 0, NULL, NULL, 3, NULL),
	(8, '1111111111111', '    zzzzzzzzzzzzz', 0, NULL, NULL, 3, NULL),
	(9, 'zzzzz', 'zzzzzzzzzzzzzzzz', 0, NULL, NULL, 3, NULL),
	(10, '4qwerhwh', 'whwehwh', 0, NULL, NULL, 3, NULL),
	(11, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', 'ehhhhhhhhheh', 0, NULL, NULL, 3, NULL),
	(12, 'aegag', 'agaegeg', 0, NULL, NULL, 3, 4),
	(13, 'Nota 1', 'qfqf', 0, NULL, NULL, 3, 4),
	(14, 'jailaits', 'evqaveqv', 1, NULL, NULL, 15, 24),
	(15, 'dxfbionaobn', 'NEBNIOPQWENBPIOQBE', 1, NULL, NULL, 15, 24),
	(16, 'AEVAEVAEVA', 'VAVAVAV', 1, NULL, NULL, 15, 24),
	(17, 'tareas', 'aegvaebvaeb', 1, NULL, NULL, 15, 26),
	(18, 'aaaaaaaaaaaaaaaaaaaaaaaa', 'aaaaaaaaaaaaaaa', 0, NULL, NULL, 15, 27),
	(19, 'vavav', 'avavava', 1, NULL, NULL, 3, 0),
	(20, 'h4h4h4', 'h4h4h', 1, NULL, NULL, 3, 0),
	(21, 'rjajajaja', 'aa', 1, NULL, NULL, 3, 0),
	(22, 'hshsh', 'hshsh', 1, NULL, NULL, 3, 0),
	(23, 'shshsh', 'shshsh', 1, NULL, NULL, 3, 0),
	(24, 'bbbb', 'bbbb', 1, NULL, NULL, 3, 22),
	(25, '3h3h', '3h3h3', 1, NULL, NULL, 3, 0),
	(26, 'Diseño de interfaz de usuario (UI/UX)', 'Esta tarea implica crear el diseño visual y la arquitectura de la interfaz de usuario del sitio web, centrándose en la usabilidad, la accesibilidad y la estética para garantizar una experiencia de usuario positiva.', 0, NULL, NULL, 17, 28),
	(28, 'Desarrollo del backend utilizando un lenguaje como Python, Ruby o Node.js', 'Los desarrolladores backend se encargarán de construir la lógica del servidor y la gestión de datos del sitio web utilizando un lenguaje de programación como Python, Ruby o Node.js. Esto implica la creación de APIs, la manipulación de bases de datos ', 0, NULL, NULL, 17, 28),
	(29, 'Diseño de la Interfaz de Usuario', 'Crear mockups y prototipos de la interfaz de usuario para obtener retroalimentación del cliente.', 1, NULL, NULL, 17, 29),
	(30, 'Desarrollo del Backend', 'Crear la lógica de negocio y desarrollar la API para manejar las solicitudes del cliente.', 1, NULL, NULL, 17, 29),
	(31, 'Implementación del Frontend', 'Desarrollar la interfaz de usuario utilizando HTML, CSS y JavaScript.', 0, NULL, NULL, 17, 29),
	(32, 'Diseño de la Interfaz de Usuario (UI/UX)', 'Crear mockups y prototipos de la interfaz de usuario para obtener retroalimentación del cliente y los usuarios.', 0, NULL, NULL, 17, 30),
	(33, 'Implementación de Funcionalidades Específicas', 'Desarrollar características clave como la creación de clases, entrega de tareas, calificación automática y foros de discusión.', 0, NULL, NULL, 17, 30),
	(34, 'Desarrollo de la Aplicación Móvil', 'Desarrollar la aplicación móvil con todas las funcionalidades requeridas, incluyendo el seguimiento de transacciones, establecimiento de presupuestos y generación de informes financieros.', 0, NULL, NULL, 17, 31);

-- Volcando estructura para tabla projecte.usuari
CREATE TABLE IF NOT EXISTS `usuari` (
  `idUsuari` int(11) NOT NULL AUTO_INCREMENT,
  `usernameUsuari` varchar(250) NOT NULL,
  `emailUsuari` varchar(250) NOT NULL,
  `contraUsuari` varchar(250) NOT NULL,
  `dataRegistreUsuari` date DEFAULT NULL,
  `nomUsuari` varchar(250) NOT NULL,
  `rolUsuari` enum('administrador','gestor','membre','observador') DEFAULT 'observador',
  `dataNaixementUsuari` date DEFAULT NULL,
  `telefonUsuari` int(11) NOT NULL,
  `direccioUsuari` varchar(250) DEFAULT '',
  `premiumUsuari` enum('Y','N') NOT NULL DEFAULT 'N',
  `cognomUsuari` varchar(250) NOT NULL DEFAULT '',
  PRIMARY KEY (`idUsuari`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Volcando datos para la tabla projecte.usuari: ~5 rows (aproximadamente)
DELETE FROM `usuari`;
INSERT INTO `usuari` (`idUsuari`, `usernameUsuari`, `emailUsuari`, `contraUsuari`, `dataRegistreUsuari`, `nomUsuari`, `rolUsuari`, `dataNaixementUsuari`, `telefonUsuari`, `direccioUsuari`, `premiumUsuari`, `cognomUsuari`) VALUES
	(3, 'eric_camon', 'eric_camon@gmail.com', 'scrypt:32768:8:1$StnhTmB6IZfOm4TZ$a0ef2a25c38e9365160da15ee7b7290c3bca201be7dcfc38d6cff2971902a68548cf19dc8a610583a2a0d7ae9c9ebe75b737606cbcb713bcd95570a3e28810a0', '2024-03-09', 'eric', 'administrador', '2024-03-30', 123456789, 'C/ Eric', 'Y', 'camon'),
	(4, 'daniel_amoretti', 'daniel_amoretti@gmail.com', 'scrypt:32768:8:1$14N6qB9LIU27RfLv$f82edaea7ec9d79a2b2f8cda67a9e15d7ed0ae6b68cbfa8761ad8292b661133cb7eb12449a7b279353f2e264be45c9f50c871abfe0c7a0d3456db2817f31eda8', '2024-03-22', 'daniel', 'administrador', '2024-03-30', 123456789, 'C/ Daniel', 'N', 'amoretti'),
	(14, 'ramon_riera', 'ramonriera@gmail.com', 'scrypt:32768:8:1$rtTBemYeSbRMjhnd$8aaef3fb6aba4bc332f0ed9b3a8c6a2e1dfcc58c7661272e6a5b029776d3f2bf9e4e1e2f9ae3b4883bd648a9bbc2a198302e844fc36cbf7657569524938b7d16', '2024-04-15', 'ramon', 'observador', '0000-00-00', 123456781, '', 'Y', 'riera'),
	(15, 'ale', 'ale@gmail.com', 'scrypt:32768:8:1$t7tirCIYmJ5EXGrX$346b9a4d210c5894603aea2a3d826e0ad775b7f7b08680d7171593d12a2fcd866fc768020480919d97a117e5e963cc2c80c7df4fff5d36ce78700ca552bdeb81', '2024-05-09', 'ale', 'observador', '2024-05-07', 123456789, 'Calle Si', 'Y', 'escri'),
	(16, 'avasvavsavav', 'alavavae@gmail.com', 'scrypt:32768:8:1$m8vz0x37k8mmKdIL$4455839813d1637522733f9b88752c543d55b0ce483d5e53cdbab344d42fdd323a67ed9d84dd0f58547cbf0a040b489a37371301fbd3b7472ef4e2019f91b1e9', '2024-05-15', 'aleaaaaa', 'observador', '2024-05-17', 123456789, 'aaaaaaaaaaaa', 'Y', 'awcvasvavav'),
	(17, 'alex', 'alexr@gmail.com', 'scrypt:32768:8:1$nMUCRdlWwhTFE3fG$2da6338ba3440ceb8b945e197de9738e2e3395f7de41fb552f28277fc12b74ecc9169bc267fcae93f99a60d93f868202a809116810ad3e8a1c8db2aa6d18c0ae', '2024-05-16', 'Alex', 'observador', '2005-06-15', 123456789, 'C/ Major', 'Y', 'Rodriguez');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
