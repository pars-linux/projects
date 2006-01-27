-- phpMyAdmin SQL Dump
-- version 2.6.4 - Pardus v1.0
-- http://www.phpmyadmin.net
--
-- Sunucu: localhost
-- Çıktı Tarihi: Ocak 27, 2006 at 09:04 PM
-- Server sürümü: 4.1.14
-- PHP Sürümü: 5.1.2
--
-- Veritabanı: `fasafiso`
--

----------------------------------------------------------

--
--Tablo yapısı : `category`
--

CREATE TABLE `category` (
  `id` int(10) NOT NULL auto_increment,
  `parent_id` int(10) NOT NULL default '0',
  `name` varchar(50) collate utf8_turkish_ci NOT NULL default '',
  `description` varchar(255) collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (`id`),
  KEY `parent_id` (`parent_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=2 ;

--
--Tablo döküm verisi `category`
--

INSERT INTO `category` VALUES (1, 0, 'fasafiso', 'Fasafiso the blogging system');

----------------------------------------------------------

--
--Tablo yapısı : `category_act`
--

CREATE TABLE `category_act` (
  `id` int(11) NOT NULL auto_increment,
  `cat_id` int(11) NOT NULL default '0',
  `entry_id` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=1 ;

--
--Tablo döküm verisi `category_act`
--

----------------------------------------------------------

--
--Tablo yapısı : `comments`
--

CREATE TABLE `comments` (
  `id` int(10) NOT NULL auto_increment,
  `entry_id` int(10) NOT NULL default '0',
  `author` tinytext collate utf8_turkish_ci NOT NULL,
  `email` tinytext collate utf8_turkish_ci NOT NULL,
  `website` tinytext collate utf8_turkish_ci NOT NULL,
  `comment` text collate utf8_turkish_ci NOT NULL,
  `date` tinytext collate utf8_turkish_ci NOT NULL,
  `status` set('0','1') collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci COMMENT='Fasafiso comments' AUTO_INCREMENT=1 ;

--
--Tablo döküm verisi `comments`
--

----------------------------------------------------------

--
--Tablo yapısı : `entry`
--

CREATE TABLE `entry` (
  `id` int(10) NOT NULL auto_increment,
  `title` tinytext collate utf8_turkish_ci NOT NULL,
  `entry` text collate utf8_turkish_ci NOT NULL,
  `date` tinytext collate utf8_turkish_ci NOT NULL,
  `author` int(10) NOT NULL default '0',
  `status` set('0','1','2') collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci COMMENT='Fasafiso entries' AUTO_INCREMENT=1 ;

--
--Tablo döküm verisi `entry`
--

----------------------------------------------------------

--
--Tablo yapısı : `links`
--

CREATE TABLE `links` (
  `id` int(10) NOT NULL auto_increment,
  `name` varchar(40) collate utf8_turkish_ci NOT NULL default '',
  `url` varchar(255) collate utf8_turkish_ci NOT NULL default '',
  `count` int(10) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=2 ;

--
--Tablo döküm verisi `links`
--

INSERT INTO `links` VALUES (1, 'LKD Gezegeni', 'http://gezegen.linux.org.tr', 0);
INSERT INTO `links` VALUES (2, 'Uludağ Dünyası', 'http://gezegen.uludag.org.tr', 0);
INSERT INTO `links` VALUES (3, 'Azmesai.net', 'http://www.azmesai.net', 0);

----------------------------------------------------------

--
--Tablo yapısı : `users`
--

CREATE TABLE `users` (
  `id` int(10) NOT NULL auto_increment,
  `username` varchar(20) collate utf8_turkish_ci NOT NULL default '',
  `name` varchar(40) collate utf8_turkish_ci NOT NULL default '',
  `passwd` tinytext collate utf8_turkish_ci NOT NULL,
  `email` varchar(128) collate utf8_turkish_ci NOT NULL default '',
  `status` set('0','1','2') collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci COMMENT='Fasafiso users' AUTO_INCREMENT=2 ;

--
--Tablo döküm verisi `users`
--

INSERT INTO `users` VALUES (1, 'fasafiso', 'fasafiso', 'f75e221dda8d6e34f60170e7e2ace795', 'fasafiso@fasafiso.org', '0');