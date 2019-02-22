/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50553
Source Host           : localhost:3306
Source Database       : mh

Target Server Type    : MYSQL
Target Server Version : 50553
File Encoding         : 65001

Date: 2019-02-22 16:30:09
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for m_data
-- ----------------------------
DROP TABLE IF EXISTS `m_data`;
CREATE TABLE `m_data` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(40) DEFAULT NULL,
  `logo` varchar(200) DEFAULT NULL,
  `author` varchar(20) DEFAULT NULL,
  `url` varchar(200) DEFAULT NULL,
  `desc` varchar(200) DEFAULT NULL,
  `last_title` varchar(40) DEFAULT NULL,
  `last_url` varchar(200) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `status` varchar(20) DEFAULT NULL,
  `type` varchar(20) DEFAULT NULL,
  `count` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title` (`title`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='漫画';

-- ----------------------------
-- Records of m_data
-- ----------------------------

-- ----------------------------
-- Table structure for m_data_list
-- ----------------------------
DROP TABLE IF EXISTS `m_data_list`;
CREATE TABLE `m_data_list` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `pid` int(11) DEFAULT NULL,
  `title` varchar(40) DEFAULT NULL,
  `url` varchar(200) DEFAULT NULL,
  `size` int(11) DEFAULT NULL,
  `chapter` varchar(20) DEFAULT NULL,
  `cid` int(11) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `dir` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='漫画';

-- ----------------------------
-- Records of m_data_list
-- ----------------------------
