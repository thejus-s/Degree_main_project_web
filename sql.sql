/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 10.4.32-MariaDB : Database - evoting
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`evoting` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;

USE `evoting`;

/*Data for the table `auth_group` */

/*Data for the table `auth_group_permissions` */

/*Data for the table `auth_permission` */

insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values 
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',2,'add_permission'),
(6,'Can change permission',2,'change_permission'),
(7,'Can delete permission',2,'delete_permission'),
(8,'Can view permission',2,'view_permission'),
(9,'Can add group',3,'add_group'),
(10,'Can change group',3,'change_group'),
(11,'Can delete group',3,'delete_group'),
(12,'Can view group',3,'view_group'),
(13,'Can add user',4,'add_user'),
(14,'Can change user',4,'change_user'),
(15,'Can delete user',4,'delete_user'),
(16,'Can view user',4,'view_user'),
(17,'Can add content type',5,'add_contenttype'),
(18,'Can change content type',5,'change_contenttype'),
(19,'Can delete content type',5,'delete_contenttype'),
(20,'Can view content type',5,'view_contenttype'),
(21,'Can add session',6,'add_session'),
(22,'Can change session',6,'change_session'),
(23,'Can delete session',6,'delete_session'),
(24,'Can view session',6,'view_session'),
(25,'Can add candidates',7,'add_candidates'),
(26,'Can change candidates',7,'change_candidates'),
(27,'Can delete candidates',7,'delete_candidates'),
(28,'Can view candidates',7,'view_candidates'),
(29,'Can add course',8,'add_course'),
(30,'Can change course',8,'change_course'),
(31,'Can delete course',8,'delete_course'),
(32,'Can view course',8,'view_course'),
(33,'Can add department',9,'add_department'),
(34,'Can change department',9,'change_department'),
(35,'Can delete department',9,'delete_department'),
(36,'Can view department',9,'view_department'),
(37,'Can add election',10,'add_election'),
(38,'Can change election',10,'change_election'),
(39,'Can delete election',10,'delete_election'),
(40,'Can view election',10,'view_election'),
(41,'Can add login',11,'add_login'),
(42,'Can change login',11,'change_login'),
(43,'Can delete login',11,'delete_login'),
(44,'Can view login',11,'view_login'),
(45,'Can add post',12,'add_post'),
(46,'Can change post',12,'change_post'),
(47,'Can delete post',12,'delete_post'),
(48,'Can view post',12,'view_post'),
(49,'Can add rules',13,'add_rules'),
(50,'Can change rules',13,'change_rules'),
(51,'Can delete rules',13,'delete_rules'),
(52,'Can view rules',13,'view_rules'),
(53,'Can add user',14,'add_user'),
(54,'Can change user',14,'change_user'),
(55,'Can delete user',14,'delete_user'),
(56,'Can view user',14,'view_user'),
(57,'Can add vote',15,'add_vote'),
(58,'Can change vote',15,'change_vote'),
(59,'Can delete vote',15,'delete_vote'),
(60,'Can view vote',15,'view_vote'),
(61,'Can add review',16,'add_review'),
(62,'Can change review',16,'change_review'),
(63,'Can delete review',16,'delete_review'),
(64,'Can view review',16,'view_review'),
(65,'Can add result',17,'add_result'),
(66,'Can change result',17,'change_result'),
(67,'Can delete result',17,'delete_result'),
(68,'Can view result',17,'view_result'),
(69,'Can add otp',18,'add_otp'),
(70,'Can change otp',18,'change_otp'),
(71,'Can delete otp',18,'delete_otp'),
(72,'Can view otp',18,'view_otp'),
(73,'Can add election_coordinator',19,'add_election_coordinator'),
(74,'Can change election_coordinator',19,'change_election_coordinator'),
(75,'Can delete election_coordinator',19,'delete_election_coordinator'),
(76,'Can view election_coordinator',19,'view_election_coordinator'),
(77,'Can add complaints',20,'add_complaints'),
(78,'Can change complaints',20,'change_complaints'),
(79,'Can delete complaints',20,'delete_complaints'),
(80,'Can view complaints',20,'view_complaints'),
(81,'Can add candidatelogin',21,'add_candidatelogin'),
(82,'Can change candidatelogin',21,'change_candidatelogin'),
(83,'Can delete candidatelogin',21,'delete_candidatelogin'),
(84,'Can view candidatelogin',21,'view_candidatelogin'),
(85,'Can add campaign',22,'add_campaign'),
(86,'Can change campaign',22,'change_campaign'),
(87,'Can delete campaign',22,'delete_campaign'),
(88,'Can view campaign',22,'view_campaign');

/*Data for the table `auth_user` */

/*Data for the table `auth_user_groups` */

/*Data for the table `auth_user_user_permissions` */

/*Data for the table `django_admin_log` */

/*Data for the table `django_content_type` */

insert  into `django_content_type`(`id`,`app_label`,`model`) values 
(1,'admin','logentry'),
(3,'auth','group'),
(2,'auth','permission'),
(4,'auth','user'),
(5,'contenttypes','contenttype'),
(22,'evoting','campaign'),
(21,'evoting','candidatelogin'),
(7,'evoting','candidates'),
(20,'evoting','complaints'),
(8,'evoting','course'),
(9,'evoting','department'),
(10,'evoting','election'),
(19,'evoting','election_coordinator'),
(11,'evoting','login'),
(18,'evoting','otp'),
(12,'evoting','post'),
(17,'evoting','result'),
(16,'evoting','review'),
(13,'evoting','rules'),
(14,'evoting','user'),
(15,'evoting','vote'),
(6,'sessions','session');

/*Data for the table `django_migrations` */

insert  into `django_migrations`(`id`,`app`,`name`,`applied`) values 
(1,'contenttypes','0001_initial','2024-04-16 18:48:01.881150'),
(2,'auth','0001_initial','2024-04-16 18:48:02.490785'),
(3,'admin','0001_initial','2024-04-16 18:48:02.631084'),
(4,'admin','0002_logentry_remove_auto_add','2024-04-16 18:48:02.643567'),
(5,'admin','0003_logentry_add_action_flag_choices','2024-04-16 18:48:02.658565'),
(6,'contenttypes','0002_remove_content_type_name','2024-04-16 18:48:02.726377'),
(7,'auth','0002_alter_permission_name_max_length','2024-04-16 18:48:02.789947'),
(8,'auth','0003_alter_user_email_max_length','2024-04-16 18:48:02.808819'),
(9,'auth','0004_alter_user_username_opts','2024-04-16 18:48:02.820976'),
(10,'auth','0005_alter_user_last_login_null','2024-04-16 18:48:02.866977'),
(11,'auth','0006_require_contenttypes_0002','2024-04-16 18:48:02.872975'),
(12,'auth','0007_alter_validators_add_error_messages','2024-04-16 18:48:02.885977'),
(13,'auth','0008_alter_user_username_max_length','2024-04-16 18:48:02.905984'),
(14,'auth','0009_alter_user_last_name_max_length','2024-04-16 18:48:02.924523'),
(15,'auth','0010_alter_group_name_max_length','2024-04-16 18:48:02.945537'),
(16,'auth','0011_update_proxy_permissions','2024-04-16 18:48:02.958521'),
(17,'auth','0012_alter_user_first_name_max_length','2024-04-16 18:48:02.977541'),
(18,'evoting','0001_initial','2024-04-16 18:48:04.470306'),
(19,'evoting','0002_alter_election_date','2024-04-16 18:48:04.481306'),
(20,'sessions','0001_initial','2024-04-16 18:48:04.527609');

/*Data for the table `django_session` */

insert  into `django_session`(`session_key`,`session_data`,`expire_date`) values 
('ln65vpqe33vkt8o5lpd2mfe39ov6sa8d','eyJsaWQiOjMsImxpbiI6IjEiLCJoIjoiQUREIEVMRUNUSU9OIiwiZWlkIjoxfQ:1rwzXD:y14iDBA0Up_-Ften6v6C4FtPpJkTsq0NHhibqm72FUE','2024-05-01 07:16:47.296585');

/*Data for the table `evoting_campaign` */

/*Data for the table `evoting_candidatelogin` */

/*Data for the table `evoting_candidates` */

/*Data for the table `evoting_complaints` */

insert  into `evoting_complaints`(`id`,`comlaint`,`date`,`time`,`replay`,`USER_id`) values 
(1,'hehdhhe','2024-04-17','12:47','pending',1);

/*Data for the table `evoting_course` */

insert  into `evoting_course`(`id`,`coursename`,`DEPARTMENT_id`) values 
(1,'cs',1);

/*Data for the table `evoting_department` */

insert  into `evoting_department`(`id`,`dept`) values 
(1,'bca');

/*Data for the table `evoting_election` */

insert  into `evoting_election`(`id`,`votingdate`,`campaign`,`publishingdate`,`title`,`lastdatesubmission`,`status`,`date`) values 
(3,'2024-04-17','2024-04-17','2024-04-17','general cap','2024-04-17','ongoing','2024-04-17');

/*Data for the table `evoting_election_coordinator` */

insert  into `evoting_election_coordinator`(`id`,`name`,`phno`,`photo`,`email`,`gender`,`LOGIN_id`) values 
(1,'thejus',1234567890,'wallpaperflare.com_wallpaper (2)_VBGjvjI.jpg','thej@gmail.com','male',3);

/*Data for the table `evoting_login` */

insert  into `evoting_login`(`id`,`username`,`password`,`usertype`) values 
(1,'admin','admin','admin'),
(2,'thejus@gmail.com','9355','user'),
(3,'thej@gmail.com','1234','election_coordinator');

/*Data for the table `evoting_otp` */

/*Data for the table `evoting_post` */

/*Data for the table `evoting_result` */

/*Data for the table `evoting_review` */

/*Data for the table `evoting_rules` */

/*Data for the table `evoting_user` */

insert  into `evoting_user`(`id`,`name`,`sem`,`year`,`photo`,`email`,`COURSE_id`,`LOGIN_id`) values 
(1,'Thejus','1SEM',2020,'wallpaperflare.com_wallpaper (2).jpg','thejus@gmail.com',1,2);

/*Data for the table `evoting_vote` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
