/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50553
Source Host           : localhost:3306
Source Database       : db

Target Server Type    : MYSQL
Target Server Version : 50553
File Encoding         : 65001

Date: 2019-02-13 17:14:22
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for kan
-- ----------------------------
DROP TABLE IF EXISTS `kan`;
CREATE TABLE `kan` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `logo` varchar(255) DEFAULT NULL,
  `title` varchar(40) DEFAULT NULL,
  `star` varchar(200) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `director` varchar(30) DEFAULT NULL,
  `region` varchar(10) DEFAULT NULL,
  `level` varchar(5) DEFAULT NULL,
  `date` varchar(20) DEFAULT NULL,
  `year` varchar(10) DEFAULT NULL,
  `alias` varchar(40) DEFAULT NULL,
  `desc` text,
  `url` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of kan
-- ----------------------------
INSERT INTO `kan` VALUES ('1', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2');
INSERT INTO `kan` VALUES ('2', 'http://ins.lanku.cc:71/pic/v/2019-1/201911114293495195.jpg', '锈溪惊魂', '赫敏·科菲尔德,John Marshall Jones,肖恩·奥布赖恩,杰伊·保尔森', 'BD中字', 'Jen McGowan', '美国', '0', '2019/1/11 14:29:47', '2019年', '锈色小溪/Rust Creek 2019', '索耶（赫敏·科菲尔德饰）是一位雄心勃勃、成绩优异的大学生。一次求职面试的路上，她开车错误转弯进入了肯塔基州森林深处。 突然之间，她发现自己面临死亡，因为她遭遇了一群无情的不法分子。 如果索耶希望活着逃离，那么她必须抓住一切机会。', 'http://www.kan84.net/bdhd/btxiuxijinghun.html');
