-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Erstellungszeit: 28. Sep 2022 um 15:32
-- Server-Version: 8.0.1-dmr
-- PHP-Version: 8.0.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `Strichliste`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `ESS`
--

CREATE TABLE `ESS` (
  `EID` int(11) NOT NULL,
  `EPreis` double NOT NULL,
  `EDAT` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `ESS`
--

INSERT INTO `ESS` (`EID`, `EPreis`, `EDAT`) VALUES
(1, 3.5, '2022-09-22');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `GETR`
--

CREATE TABLE `GETR` (
  `GID` int(11) NOT NULL,
  `GName` text NOT NULL,
  `GPreis` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `GETR`
--

INSERT INTO `GETR` (`GID`, `GName`, `GPreis`) VALUES
(1, 'Wasser', 0.5);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `ID`
--

CREATE TABLE `ID` (
  `ID` int(11) NOT NULL,
  `VF_ID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `ID`
--

INSERT INTO `ID` (`ID`, `VF_ID`) VALUES
(1, 1337);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `NAME`
--

CREATE TABLE `NAME` (
  `ID` int(11) NOT NULL,
  `VNAME` text NOT NULL,
  `NNAME` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `NAME`
--

INSERT INTO `NAME` (`ID`, `VNAME`, `NNAME`) VALUES
(1, 'Test', 'User');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `PERSESS`
--

CREATE TABLE `PERSESS` (
  `ID` int(11) NOT NULL,
  `EID` int(11) NOT NULL,
  `CT` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `PERSESS`
--

INSERT INTO `PERSESS` (`ID`, `EID`, `CT`) VALUES
(1, 1, 35);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `PERSGET`
--

CREATE TABLE `PERSGET` (
  `ID` int(11) NOT NULL,
  `GID` int(11) NOT NULL,
  `CT` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `PERSGET`
--

INSERT INTO `PERSGET` (`ID`, `GID`, `CT`) VALUES
(1, 1, 25);

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `ESS`
--
ALTER TABLE `ESS`
  ADD PRIMARY KEY (`EID`);

--
-- Indizes für die Tabelle `GETR`
--
ALTER TABLE `GETR`
  ADD PRIMARY KEY (`GID`);

--
-- Indizes für die Tabelle `ID`
--
ALTER TABLE `ID`
  ADD PRIMARY KEY (`ID`);

--
-- Indizes für die Tabelle `NAME`
--
ALTER TABLE `NAME`
  ADD PRIMARY KEY (`ID`);

--
-- Indizes für die Tabelle `PERSESS`
--
ALTER TABLE `PERSESS`
  ADD PRIMARY KEY (`ID`,`EID`),
  ADD KEY `ESSCT-EID-MAPPING` (`EID`);

--
-- Indizes für die Tabelle `PERSGET`
--
ALTER TABLE `PERSGET`
  ADD PRIMARY KEY (`ID`,`GID`),
  ADD KEY `GTCT-GID-MAPPING` (`GID`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `ESS`
--
ALTER TABLE `ESS`
  MODIFY `EID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT für Tabelle `GETR`
--
ALTER TABLE `GETR`
  MODIFY `GID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT für Tabelle `ID`
--
ALTER TABLE `ID`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `NAME`
--
ALTER TABLE `NAME`
  ADD CONSTRAINT `NAME_ibfk_1` FOREIGN KEY (`ID`) REFERENCES `ID` (`ID`);

--
-- Constraints der Tabelle `PERSESS`
--
ALTER TABLE `PERSESS`
  ADD CONSTRAINT `ESSCT-EID-MAPPING` FOREIGN KEY (`EID`) REFERENCES `ESS` (`EID`),
  ADD CONSTRAINT `ESSCT-ID-MAPPING` FOREIGN KEY (`ID`) REFERENCES `ID` (`ID`);

--
-- Constraints der Tabelle `PERSGET`
--
ALTER TABLE `PERSGET`
  ADD CONSTRAINT `GTCT-GID-MAPPING` FOREIGN KEY (`GID`) REFERENCES `GETR` (`GID`),
  ADD CONSTRAINT `GTCT-ID-MAPPING` FOREIGN KEY (`ID`) REFERENCES `ID` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
