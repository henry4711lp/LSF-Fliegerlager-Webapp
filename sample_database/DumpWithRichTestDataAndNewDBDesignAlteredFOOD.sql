-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Erstellungszeit: 06. Mai 2024 um 18:01
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
(1, 3.5, '2022-09-22'),
(2, 3.5, '2022-09-23'),
(3, 3.5, '2022-09-24'),
(4, 3.5, '2022-09-25'),
(5, 3.5, '2022-09-26'),
(6, 3.5, '2022-09-27');

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
(1, 'Wasser', 0.5),
(2, 'Bier', 1.2),
(3, 'Softdrink', 1),
(4, 'Eistee', 0.8);

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
(1, 1337),
(48, 0),
(50, 0),
(51, 0),
(52, 0);


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
(48, 'Jan', 'Sellerbeck'),
(51, 'Robin', 'B'),
(52, 'Test', 'User');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `PERSESS`
--

CREATE TABLE `PERSESS` (
  `ID` int(11) NOT NULL,
  `EID` int(11) NOT NULL,
  `CT_VEG` int(11) NOT NULL,
  `CT_NORM` int(11) NOT NULL,
  `CT_VEG_KID` int(11) NOT NULL,
  `CT_NORM_KID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `PERSESS`
--

INSERT INTO `PERSESS` (`ID`, `EID`, `CT_VEG`, `CT_NORM`, `CT_VEG_KID`, `CT_NORM_KID`) VALUES
(1, 1, 35, 0, 0, 0),
(48, 1, 2, 0, 0, 0),
(48, 2, 3, 0, 0, 0),
(48, 3, 2, 0, 0, 0),
(48, 4, 2, 0, 0, 0),
(48, 5, 2, 0, 0, 0),
(48, 6, 2, 0, 0, 0);

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
(1, 1, 25),
(48, 1, 25),
(48, 2, 20),
(48, 3, 5),
(48, 4, 13);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `STAY`
--

CREATE TABLE `STAY` (
  `ID` int(11) NOT NULL,
  `STAYDATE_START` date DEFAULT NULL,
  `STAYDATE_END` date DEFAULT NULL,
  `CTR` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `STAY`
--

INSERT INTO `STAY` (`ID`, `STAYDATE_START`, `STAYDATE_END`, `CTR`) VALUES
(48, '2022-07-01', '2022-07-28', 27);

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
-- Indizes für die Tabelle `STAY`
--
ALTER TABLE `STAY`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `ESS`
--
ALTER TABLE `ESS`
  MODIFY `EID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT für Tabelle `GETR`
--
ALTER TABLE `GETR`
  MODIFY `GID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT für Tabelle `ID`
--
ALTER TABLE `ID`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=57;

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

--
-- Constraints der Tabelle `STAY`
--
ALTER TABLE `STAY`
  ADD CONSTRAINT `STAY_ibfk_1` FOREIGN KEY (`ID`) REFERENCES `ID` (`ID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
