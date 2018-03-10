# Host: 127.0.0.1  (Version 5.7.13-log)
# Date: 2016-08-28 21:03:26
# Generator: MySQL-Front 5.3  (Build 6.25)

/*!40101 SET NAMES utf8 */;

#
# Structure for table "trkprice"
#
CREATE DATABASE `botbid`;

USE `botbid`;

DROP TABLE IF EXISTS `trkprice`;
CREATE TABLE `trkprice` (
  `p_key` int(11) unsigned zerofill NOT NULL AUTO_INCREMENT,
  `aid` varchar(10) NOT NULL DEFAULT '',
  `product_id` varchar(10) NOT NULL DEFAULT '',
  `product_name` varchar(150) NOT NULL DEFAULT '',
  `opt_txt` varchar(30) NOT NULL DEFAULT '',
  `winner` varchar(30) NOT NULL DEFAULT '',
  `price` int(6) unsigned NOT NULL DEFAULT '0',
  `enddate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `sts` char(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`p_key`),
  KEY `product_id` (`product_id`),
  KEY `winner` (`winner`),
  KEY `sts` (`sts`)
) ENGINE=MyISAM AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;

#
# Data for table "trkprice"
#

/*!40000 ALTER TABLE `trkprice` DISABLE KEYS */;
INSERT INTO `trkprice` VALUES (00000000001,'18930159','56-011','กระทะทอดขนาด 11 นิ้ว','ไซส์ เดียว','kaijae.ake',64,'2016-08-28 21:03:02','1');
/*!40000 ALTER TABLE `trkprice` ENABLE KEYS */;
