-- Sunucu: devel.fasafiso.org/proc
-- Çıktı Tarihi: Ocak 27, 2006 at 09:04 PM
-- Server sürümü: 4.1.14
-- PHP Sürümü: 5.1.2

-- Veritabanı: `fasafiso`

CREATE TABLE `fs_category` (
  `id` int(10) NOT NULL auto_increment,
  `parent_id` int(10) NOT NULL default '0',
  `name` varchar(50) collate utf8_turkish_ci NOT NULL default '',
  `description` varchar(255) collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (`id`),
  KEY `parent_id` (`parent_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=2 ;

INSERT INTO `fs_category` VALUES (1, 0, 'fasafiso', 'Fasafiso the blogging system');

CREATE TABLE `fs_category_act` (
  `id` int(11) NOT NULL auto_increment,
  `cat_id` int(11) NOT NULL default '0',
  `entry_id` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=1 ;

CREATE TABLE `fs_comments` (
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

CREATE TABLE `fs_entry` (
  `id` int(10) NOT NULL auto_increment,
  `title` tinytext collate utf8_turkish_ci NOT NULL,
  `entry` text collate utf8_turkish_ci NOT NULL,
  `date` tinytext collate utf8_turkish_ci NOT NULL,
  `author` int(10) NOT NULL default '0',
  `status` set('0','1','2') collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci COMMENT='Fasafiso entries' AUTO_INCREMENT=1 ;

CREATE TABLE `fs_links` (
  `id` int(10) NOT NULL auto_increment,
  `name` varchar(40) collate utf8_turkish_ci NOT NULL default '',
  `url` varchar(255) collate utf8_turkish_ci NOT NULL default '',
  `count` int(10) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci AUTO_INCREMENT=2 ;

INSERT INTO `fs_links` VALUES (1, 'FasaFiso', 'http://www.fasafiso.org', 0);
INSERT INTO `fs_links` VALUES (2, 'LKD Gezegeni', 'http://gezegen.linux.org.tr', 0);
INSERT INTO `fs_links` VALUES (3, 'Uludağ Dünyası', 'http://gezegen.uludag.org.tr', 0);
INSERT INTO `fs_links` VALUES (4, 'Azmesai.net', 'http://www.azmesai.net', 0);

CREATE TABLE `fs_users` (
  `id` int(10) NOT NULL auto_increment,
  `username` varchar(20) collate utf8_turkish_ci NOT NULL default '',
  `name` varchar(40) collate utf8_turkish_ci NOT NULL default '',
  `passwd` tinytext collate utf8_turkish_ci NOT NULL,
  `email` varchar(128) collate utf8_turkish_ci NOT NULL default '',
  `status` set('0','1','2') collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_turkish_ci COMMENT='Fasafiso users' AUTO_INCREMENT=2 ;

INSERT INTO `fs_users` VALUES (1, 'fasafiso', 'fasafiso', 'f75e221dda8d6e34f60170e7e2ace795', 'fasafiso@fasafiso.org', '0');
