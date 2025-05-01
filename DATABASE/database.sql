/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.0.67-community-nt : Database - forensic_evidence
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`forensic_evidence` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `forensic_evidence`;

/*Table structure for table `forensic` */

DROP TABLE IF EXISTS `forensic`;

CREATE TABLE `forensic` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(1000) default NULL,
  `email` varchar(1000) default NULL,
  `username` varchar(1000) default NULL,
  `password` varchar(1000) default NULL,
  `status` varchar(1000) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `forensic` */

insert  into `forensic`(`id`,`name`,`email`,`username`,`password`,`status`) values (1,'kishan','gkvtechsolutions@gmail.com','kishan','123','Authorized');

/*Table structure for table `police` */

DROP TABLE IF EXISTS `police`;

CREATE TABLE `police` (
  `id` int(11) NOT NULL auto_increment,
  `station` varchar(1000) default NULL,
  `police` varchar(1000) default NULL,
  `email` varchar(1000) default NULL,
  `p_id` varchar(1000) default NULL,
  `password` varchar(1000) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `police` */

insert  into `police`(`id`,`station`,`police`,`email`,`p_id`,`password`) values (3,'ECIL','Kishan','streamwaytechnologiespvtltd@gmail.com','968154','SGwOKd');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
