-- phpMyAdmin SQL Dump
-- version 4.2.12deb2+deb8u3
-- http://www.phpmyadmin.net
--
-- Machine: localhost
-- Gegenereerd op: 29 nov 2018 om 21:47
-- Serverversie: 5.5.62-0+deb8u1
-- PHP-versie: 5.6.38-0+deb8u1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Databank: `dapaprs`
--
-- DROP DATABASE `dapaprs`;
CREATE DATABASE IF NOT EXISTS `dapaprs` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `dapaprs`;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `masktable`
--

DROP TABLE IF EXISTS `masktable`;
CREATE TABLE IF NOT EXISTS `masktable` (
`MASK_ID` int(11) NOT NULL,
  `OWNER_CALL` varchar(10) NOT NULL,
  `MASK_CALL` varchar(10) NOT NULL,
  `MASK_CHANGEDATE` date NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

--
-- Indexen voor geëxporteerde tabellen
--

--
-- Indexen voor tabel `masktable`
--
ALTER TABLE `masktable`
 ADD PRIMARY KEY (`MASK_ID`), ADD UNIQUE KEY `MASK_ID` (`MASK_ID`);

--
-- AUTO_INCREMENT voor geëxporteerde tabellen
--

--
-- AUTO_INCREMENT voor een tabel `masktable`
--
ALTER TABLE `masktable`
MODIFY `MASK_ID` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=9;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
