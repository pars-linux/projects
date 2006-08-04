
CREATE TABLE `Vezir_Comments` (
  `ID` int(11) NOT NULL auto_increment,
  `Author` varchar(250) NOT NULL,
  `Email` varchar(250) NOT NULL,
  `Comments` tinytext NOT NULL,
  `Date` varchar(10) NOT NULL,
  `EntryID` int(11) NOT NULL,
  PRIMARY KEY  (`ID`),
  FULLTEXT KEY `Author` (`Author`,`Comments`)
) TYPE=MyISAM AUTO_INCREMENT=1 ;

CREATE TABLE `Vezir_Converts` (
  `ID` tinyint(4) NOT NULL auto_increment,
  `Find` tinytext NOT NULL,
  `Replace` tinytext NOT NULL,
  PRIMARY KEY  (`ID`)
) TYPE=MyISAM AUTO_INCREMENT=1 ;

CREATE TABLE `Vezir_Entries` (
  `ID` int(11) NOT NULL auto_increment,
  `Title` varchar(250) NOT NULL,
  `NiceTitle` varchar(250) NOT NULL,
  `Content` text NOT NULL,
  `Date` varchar(10) NOT NULL,
  `Tags` varchar(250) NOT NULL,
  `Author` int(11) NOT NULL,
  `Password` varchar(250) default NULL,
  `Comments` set('on','off') NOT NULL default 'on',
  PRIMARY KEY  (`ID`),
  FULLTEXT KEY `Title` (`Title`,`NiceTitle`,`Content`)
) TYPE=MyISAM AUTO_INCREMENT=1 ;

CREATE TABLE `Vezir_Logs` (
  `ID` bigint(20) NOT NULL auto_increment,
  `Date` varchar(10) NOT NULL,
  `UserName` varchar(250) NOT NULL,
  `IP` varchar(200) NOT NULL,
  `Action` varchar(250) NOT NULL,
  `Query` tinytext NOT NULL,
  PRIMARY KEY  (`ID`)
) TYPE=MyISAM AUTO_INCREMENT=1 ;

CREATE TABLE `Vezir_RSS` (
  `ID` tinyint(4) NOT NULL auto_increment,
  `RssName` varchar(250) NOT NULL,
  `Query` tinytext NOT NULL,
  PRIMARY KEY  (`ID`)
) TYPE=MyISAM AUTO_INCREMENT=1 ;

CREATE TABLE `Vezir_Tags` (
  `TagName` varchar(250) NOT NULL,
  `Count` int(11) NOT NULL default '0',
  PRIMARY KEY  (`TagName`)
) TYPE=MyISAM AUTO_INCREMENT=1 ;

CREATE TABLE `Vezir_Users` (
  `ID` int(11) NOT NULL auto_increment,
  `UserName` varchar(250) NOT NULL,
  `Password` varchar(80) NOT NULL,
  `Status` tinyint(4) NOT NULL,
  `RealName` varchar(250) NOT NULL,
  `Mail` varchar(250) NOT NULL,
  `BirthDate` varchar(10) NOT NULL,
  `PhotoLink` tinytext NOT NULL,
  PRIMARY KEY  (`ID`),
  UNIQUE KEY `UserName` (`UserName`)
) TYPE=MyISAM AUTO_INCREMENT=1 ;

