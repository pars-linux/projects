-- phpMyAdmin SQL Dump
-- version 2.6.4 - Pardus v1.0
-- http://www.phpmyadmin.net
-- 
-- Sunucu: localhost
-- Çıktı Tarihi: Ocak 27, 2006 at 05:14 PM
-- Server sürümü: 4.1.14
-- PHP Sürümü: 5.1.2
-- 
-- Veritabanı: `fasafiso`
-- 

CREATE TABLE `fsfs_autoconverts` (
  `id` int(11) NOT NULL auto_increment,
  `word` varchar(255) collate utf8_turkish_ci NOT NULL default '',
  `text` varchar(255) collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (`id`)
) AUTO_INCREMENT=1 ;

CREATE TABLE `fsfs_category` (
  `id` int(10) NOT NULL auto_increment,
  `parent_id` int(10) NOT NULL default '0',
  `name` varchar(50) collate utf8_turkish_ci NOT NULL default '',
  `description` varchar(255) collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (`id`),
  KEY `parent_id` (`parent_id`)
) AUTO_INCREMENT=1 ;

CREATE TABLE `fsfs_category_act` (
  `id` int(11) NOT NULL auto_increment,
  `cat_id` int(11) NOT NULL default '0',
  `entry_id` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) AUTO_INCREMENT=1 ;

CREATE TABLE `fsfs_comment` (
  `id` int(10) NOT NULL auto_increment,
  `entry_id` int(10) NOT NULL default '0',
  `author` varchar(255) collate utf8_turkish_ci NOT NULL default '',
  `email` varchar(255) collate utf8_turkish_ci NOT NULL default '',
  `website` varchar(255) collate utf8_turkish_ci NOT NULL default '',
  `comment` tinytext collate utf8_turkish_ci NOT NULL,
  `date` tinytext collate utf8_turkish_ci NOT NULL,
  `status` set('0','1') collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (`id`),
  KEY `entry_id` (`entry_id`)
) AUTO_INCREMENT=1 ;

CREATE TABLE `fsfs_entry` (
  `id` int(10) NOT NULL auto_increment,
  `title` tinytext collate utf8_turkish_ci NOT NULL,
  `text` text collate utf8_turkish_ci NOT NULL,
  `date` tinytext collate utf8_turkish_ci NOT NULL,
  `author` int(11) NOT NULL default '0',
  `status` set('0','1') collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (`id`)
) AUTO_INCREMENT=1 ;

CREATE TABLE `fsfs_users` (
  `id` int(10) NOT NULL auto_increment,
  `username` varchar(64) collate utf8_turkish_ci NOT NULL default '',
  `password` varchar(64) collate utf8_turkish_ci NOT NULL default '',
  `name` varchar(255) collate utf8_turkish_ci NOT NULL default '',
  `email` varchar(255) collate utf8_turkish_ci NOT NULL default '',
  `status` set('0','1','2') collate utf8_turkish_ci NOT NULL default '',
  PRIMARY KEY  (`id`)
) AUTO_INCREMENT=1 ;
