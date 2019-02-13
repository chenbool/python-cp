/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50553
Source Host           : localhost:3306
Source Database       : db

Target Server Type    : MYSQL
Target Server Version : 50553
File Encoding         : 65001

Date: 2019-02-13 14:09:37
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for main
-- ----------------------------
DROP TABLE IF EXISTS `main`;
CREATE TABLE `main` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(40) DEFAULT NULL,
  `name` varchar(40) DEFAULT NULL,
  `name_zh` varchar(40) DEFAULT NULL,
  `symbol` varchar(20) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `current` varchar(20) DEFAULT NULL,
  `diff` varchar(20) DEFAULT NULL,
  `high` varchar(20) DEFAULT NULL,
  `low` varchar(20) DEFAULT NULL,
  `opentime` varchar(30) DEFAULT NULL,
  `opendate` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of main
-- ----------------------------
