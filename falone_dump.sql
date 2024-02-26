-- MySQL dump 10.13  Distrib 8.3.0, for macos14.2 (x86_64)
--
-- Host: localhost    Database: falone
-- ------------------------------------------------------
-- Server version	8.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accounts_profile`
--

DROP TABLE IF EXISTS `accounts_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts_profile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `mobile_number` varchar(100) DEFAULT NULL,
  `token` varchar(150) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `date` datetime(6) DEFAULT NULL,
  `date_update` datetime(6) DEFAULT NULL,
  `type` varchar(7) NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `accounts_profile_user_id_49a85d32_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_profile`
--

LOCK TABLES `accounts_profile` WRITE;
/*!40000 ALTER TABLE `accounts_profile` DISABLE KEYS */;
INSERT INTO `accounts_profile` VALUES (1,NULL,'Andrea','Cocco','3472195905',NULL,1,'andrea@madstudio.it',NULL,NULL,'STAFF',1),(3,NULL,'Profilo','Due','3472195905',NULL,1,'andrea2@madstudio.it',NULL,NULL,'STAFF',2);
/*!40000 ALTER TABLE `accounts_profile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apartments_apartments`
--

DROP TABLE IF EXISTS `apartments_apartments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apartments_apartments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `floor` varchar(100) DEFAULT NULL,
  `note` varchar(100) DEFAULT NULL,
  `owner` varchar(100) DEFAULT NULL,
  `owner_phone` varchar(100) DEFAULT NULL,
  `owner_email` varchar(254) DEFAULT NULL,
  `owner_cf` varchar(100) DEFAULT NULL,
  `link` varchar(100) DEFAULT NULL,
  `date` datetime(6) NOT NULL,
  `date_update` datetime(6) NOT NULL,
  `worksite_id` bigint NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `apartments_apartment_worksite_id_0127b195_fk_worksites` (`worksite_id`),
  CONSTRAINT `apartments_apartment_worksite_id_0127b195_fk_worksites` FOREIGN KEY (`worksite_id`) REFERENCES `worksites_worksites` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apartments_apartments`
--

LOCK TABLES `apartments_apartments` WRITE;
/*!40000 ALTER TABLE `apartments_apartments` DISABLE KEYS */;
/*!40000 ALTER TABLE `apartments_apartments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apartments_apartmentsub`
--

DROP TABLE IF EXISTS `apartments_apartmentsub`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apartments_apartmentsub` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sub` varchar(100) DEFAULT NULL,
  `apartment_id` bigint NOT NULL,
  `foglio_particella_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `apartments_apartment_apartment_id_95c8e55f_fk_apartment` (`apartment_id`),
  KEY `apartments_apartment_foglio_particella_id_42c817e5_fk_worksites` (`foglio_particella_id`),
  CONSTRAINT `apartments_apartment_apartment_id_95c8e55f_fk_apartment` FOREIGN KEY (`apartment_id`) REFERENCES `apartments_apartments` (`id`),
  CONSTRAINT `apartments_apartment_foglio_particella_id_42c817e5_fk_worksites` FOREIGN KEY (`foglio_particella_id`) REFERENCES `worksites_foglioparticella` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apartments_apartmentsub`
--

LOCK TABLES `apartments_apartmentsub` WRITE;
/*!40000 ALTER TABLE `apartments_apartmentsub` DISABLE KEYS */;
/*!40000 ALTER TABLE `apartments_apartmentsub` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apartments_checklist`
--

DROP TABLE IF EXISTS `apartments_checklist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apartments_checklist` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apartments_checklist`
--

LOCK TABLES `apartments_checklist` WRITE;
/*!40000 ALTER TABLE `apartments_checklist` DISABLE KEYS */;
/*!40000 ALTER TABLE `apartments_checklist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apartments_checklistworksites`
--

DROP TABLE IF EXISTS `apartments_checklistworksites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apartments_checklistworksites` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` datetime(6) NOT NULL,
  `order` int NOT NULL,
  `is_done` tinyint(1) NOT NULL,
  `apartment_id` bigint NOT NULL,
  `checklist_id` bigint NOT NULL,
  `worksites_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `apartments_checklist_apartment_id_7b4ec7aa_fk_apartment` (`apartment_id`),
  KEY `apartments_checklist_checklist_id_91e23f9c_fk_apartment` (`checklist_id`),
  KEY `apartments_checklist_worksites_id_5c67a6ab_fk_worksites` (`worksites_id`),
  CONSTRAINT `apartments_checklist_apartment_id_7b4ec7aa_fk_apartment` FOREIGN KEY (`apartment_id`) REFERENCES `apartments_apartments` (`id`),
  CONSTRAINT `apartments_checklist_checklist_id_91e23f9c_fk_apartment` FOREIGN KEY (`checklist_id`) REFERENCES `apartments_checklist` (`id`),
  CONSTRAINT `apartments_checklist_worksites_id_5c67a6ab_fk_worksites` FOREIGN KEY (`worksites_id`) REFERENCES `worksites_worksites` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apartments_checklistworksites`
--

LOCK TABLES `apartments_checklistworksites` WRITE;
/*!40000 ALTER TABLE `apartments_checklistworksites` DISABLE KEYS */;
/*!40000 ALTER TABLE `apartments_checklistworksites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apartments_clientapartments`
--

DROP TABLE IF EXISTS `apartments_clientapartments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `apartments_clientapartments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `is_active` tinyint(1) NOT NULL,
  `apartment_id` bigint NOT NULL,
  `profile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `apartments_clientapa_apartment_id_0aef2e08_fk_apartment` (`apartment_id`),
  KEY `apartments_clientapa_profile_id_844df2ad_fk_accounts_` (`profile_id`),
  CONSTRAINT `apartments_clientapa_apartment_id_0aef2e08_fk_apartment` FOREIGN KEY (`apartment_id`) REFERENCES `apartments_apartments` (`id`),
  CONSTRAINT `apartments_clientapa_profile_id_844df2ad_fk_accounts_` FOREIGN KEY (`profile_id`) REFERENCES `accounts_profile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apartments_clientapartments`
--

LOCK TABLES `apartments_clientapartments` WRITE;
/*!40000 ALTER TABLE `apartments_clientapartments` DISABLE KEYS */;
/*!40000 ALTER TABLE `apartments_clientapartments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=137 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add blacklisted token',7,'add_blacklistedtoken'),(26,'Can change blacklisted token',7,'change_blacklistedtoken'),(27,'Can delete blacklisted token',7,'delete_blacklistedtoken'),(28,'Can view blacklisted token',7,'view_blacklistedtoken'),(29,'Can add outstanding token',8,'add_outstandingtoken'),(30,'Can change outstanding token',8,'change_outstandingtoken'),(31,'Can delete outstanding token',8,'delete_outstandingtoken'),(32,'Can view outstanding token',8,'view_outstandingtoken'),(33,'Can add profile',9,'add_profile'),(34,'Can change profile',9,'change_profile'),(35,'Can delete profile',9,'delete_profile'),(36,'Can view profile',9,'view_profile'),(37,'Can add apartments',10,'add_apartments'),(38,'Can change apartments',10,'change_apartments'),(39,'Can delete apartments',10,'delete_apartments'),(40,'Can view apartments',10,'view_apartments'),(41,'Can add client apartments',11,'add_clientapartments'),(42,'Can change client apartments',11,'change_clientapartments'),(43,'Can delete client apartments',11,'delete_clientapartments'),(44,'Can view client apartments',11,'view_clientapartments'),(45,'Can add categories',12,'add_categories'),(46,'Can change categories',12,'change_categories'),(47,'Can delete categories',12,'delete_categories'),(48,'Can view categories',12,'view_categories'),(49,'Can add check list',13,'add_checklist'),(50,'Can change check list',13,'change_checklist'),(51,'Can delete check list',13,'delete_checklist'),(52,'Can view check list',13,'view_checklist'),(53,'Can add contractor',14,'add_contractor'),(54,'Can change contractor',14,'change_contractor'),(55,'Can delete contractor',14,'delete_contractor'),(56,'Can view contractor',14,'view_contractor'),(57,'Can add financier',15,'add_financier'),(58,'Can change financier',15,'change_financier'),(59,'Can delete financier',15,'delete_financier'),(60,'Can view financier',15,'view_financier'),(61,'Can add worksites',16,'add_worksites'),(62,'Can change worksites',16,'change_worksites'),(63,'Can delete worksites',16,'delete_worksites'),(64,'Can view worksites',16,'view_worksites'),(65,'Can add worksites profile',17,'add_worksitesprofile'),(66,'Can change worksites profile',17,'change_worksitesprofile'),(67,'Can delete worksites profile',17,'delete_worksitesprofile'),(68,'Can view worksites profile',17,'view_worksitesprofile'),(69,'Can add worksites categories',18,'add_worksitescategories'),(70,'Can change worksites categories',18,'change_worksitescategories'),(71,'Can delete worksites categories',18,'delete_worksitescategories'),(72,'Can view worksites categories',18,'view_worksitescategories'),(73,'Can add collab worksites',19,'add_collabworksites'),(74,'Can change collab worksites',19,'change_collabworksites'),(75,'Can delete collab worksites',19,'delete_collabworksites'),(76,'Can view collab worksites',19,'view_collabworksites'),(77,'Can add check list worksites',20,'add_checklistworksites'),(78,'Can change check list worksites',20,'change_checklistworksites'),(79,'Can delete check list worksites',20,'delete_checklistworksites'),(80,'Can view check list worksites',20,'view_checklistworksites'),(81,'Can add board attachments',21,'add_boardattachments'),(82,'Can change board attachments',21,'change_boardattachments'),(83,'Can delete board attachments',21,'delete_boardattachments'),(84,'Can view board attachments',21,'view_boardattachments'),(85,'Can add board read',22,'add_boardread'),(86,'Can change board read',22,'change_boardread'),(87,'Can delete board read',22,'delete_boardread'),(88,'Can view board read',22,'view_boardread'),(89,'Can add boards',23,'add_boards'),(90,'Can change boards',23,'change_boards'),(91,'Can delete boards',23,'delete_boards'),(92,'Can view boards',23,'view_boards'),(93,'Can add check list',24,'add_checklist'),(94,'Can change check list',24,'change_checklist'),(95,'Can delete check list',24,'delete_checklist'),(96,'Can view check list',24,'view_checklist'),(97,'Can add check list worksites',25,'add_checklistworksites'),(98,'Can change check list worksites',25,'change_checklistworksites'),(99,'Can delete check list worksites',25,'delete_checklistworksites'),(100,'Can view check list worksites',25,'view_checklistworksites'),(101,'Can add survey',26,'add_survey'),(102,'Can change survey',26,'change_survey'),(103,'Can delete survey',26,'delete_survey'),(104,'Can view survey',26,'view_survey'),(105,'Can add survey question',27,'add_surveyquestion'),(106,'Can change survey question',27,'change_surveyquestion'),(107,'Can delete survey question',27,'delete_surveyquestion'),(108,'Can view survey question',27,'view_surveyquestion'),(109,'Can add survey question choices',28,'add_surveyquestionchoices'),(110,'Can change survey question choices',28,'change_surveyquestionchoices'),(111,'Can delete survey question choices',28,'delete_surveyquestionchoices'),(112,'Can view survey question choices',28,'view_surveyquestionchoices'),(113,'Can add boards recipient',29,'add_boardsrecipient'),(114,'Can change boards recipient',29,'change_boardsrecipient'),(115,'Can delete boards recipient',29,'delete_boardsrecipient'),(116,'Can view boards recipient',29,'view_boardsrecipient'),(117,'Can add apartment sub',30,'add_apartmentsub'),(118,'Can change apartment sub',30,'change_apartmentsub'),(119,'Can delete apartment sub',30,'delete_apartmentsub'),(120,'Can view apartment sub',30,'view_apartmentsub'),(121,'Can add foglio particella',31,'add_foglioparticella'),(122,'Can change foglio particella',31,'change_foglioparticella'),(123,'Can delete foglio particella',31,'delete_foglioparticella'),(124,'Can view foglio particella',31,'view_foglioparticella'),(125,'Can add worksites foglio particella',32,'add_worksitesfoglioparticella'),(126,'Can change worksites foglio particella',32,'change_worksitesfoglioparticella'),(127,'Can delete worksites foglio particella',32,'delete_worksitesfoglioparticella'),(128,'Can view worksites foglio particella',32,'view_worksitesfoglioparticella'),(129,'Can add status',33,'add_status'),(130,'Can change status',33,'change_status'),(131,'Can delete status',33,'delete_status'),(132,'Can view status',33,'view_status'),(133,'Can add worksites status',34,'add_worksitesstatus'),(134,'Can change worksites status',34,'change_worksitesstatus'),(135,'Can delete worksites status',34,'delete_worksitesstatus'),(136,'Can view worksites status',34,'view_worksitesstatus');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$320000$RYPLtFjNc3xq1s7NbCMobH$t4cp1GIpmBWwefWduObxZnEkksdm4bARwcLPyzInjps=',NULL,1,'andrea','','','',1,1,'2024-02-06 20:40:23.178042'),(2,'pbkdf2_sha256$320000$FTjIoLcmtX2hB37nPTwi8m$NjIBcsyGp3lPu+FtlrS61Xaqc/3G7Vzn4NCL7OtXCyQ=',NULL,1,'gestione','','','',1,1,'2024-02-08 14:59:21.515223');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `board_boardattachments`
--

DROP TABLE IF EXISTS `board_boardattachments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `board_boardattachments` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `attachment_link` varchar(200) DEFAULT NULL,
  `type` varchar(8) NOT NULL,
  `date` datetime(6) NOT NULL,
  `board_id` bigint NOT NULL,
  `survey_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `board_boardattachments_board_id_b7620aec_fk_board_boards_id` (`board_id`),
  KEY `board_boardattachments_survey_id_3f5b9efe_fk_board_survey_id` (`survey_id`),
  CONSTRAINT `board_boardattachments_board_id_b7620aec_fk_board_boards_id` FOREIGN KEY (`board_id`) REFERENCES `board_boards` (`id`),
  CONSTRAINT `board_boardattachments_survey_id_3f5b9efe_fk_board_survey_id` FOREIGN KEY (`survey_id`) REFERENCES `board_survey` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `board_boardattachments`
--

LOCK TABLES `board_boardattachments` WRITE;
/*!40000 ALTER TABLE `board_boardattachments` DISABLE KEYS */;
/*!40000 ALTER TABLE `board_boardattachments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `board_boardread`
--

DROP TABLE IF EXISTS `board_boardread`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `board_boardread` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` datetime(6) NOT NULL,
  `board_id` bigint NOT NULL,
  `profile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `board_boardread_board_id_95afb6c8_fk_board_boards_id` (`board_id`),
  KEY `board_boardread_profile_id_74c64e08_fk_accounts_profile_id` (`profile_id`),
  CONSTRAINT `board_boardread_board_id_95afb6c8_fk_board_boards_id` FOREIGN KEY (`board_id`) REFERENCES `board_boards` (`id`),
  CONSTRAINT `board_boardread_profile_id_74c64e08_fk_accounts_profile_id` FOREIGN KEY (`profile_id`) REFERENCES `accounts_profile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `board_boardread`
--

LOCK TABLES `board_boardread` WRITE;
/*!40000 ALTER TABLE `board_boardread` DISABLE KEYS */;
/*!40000 ALTER TABLE `board_boardread` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `board_boards`
--

DROP TABLE IF EXISTS `board_boards`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `board_boards` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) DEFAULT NULL,
  `title` varchar(250) NOT NULL,
  `body` longtext NOT NULL,
  `author` varchar(150) NOT NULL,
  `date` datetime(6) NOT NULL,
  `date_update` datetime(6) NOT NULL,
  `type` varchar(7) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `board_boards`
--

LOCK TABLES `board_boards` WRITE;
/*!40000 ALTER TABLE `board_boards` DISABLE KEYS */;
/*!40000 ALTER TABLE `board_boards` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `board_boardsrecipient`
--

DROP TABLE IF EXISTS `board_boardsrecipient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `board_boardsrecipient` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `recipient_type` varchar(50) NOT NULL,
  `date` datetime(6) NOT NULL,
  `apartment_id` bigint DEFAULT NULL,
  `board_id` bigint NOT NULL,
  `profile_id` bigint DEFAULT NULL,
  `worksites_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `board_boardsrecipient_board_id_6400fbe2_fk_board_boards_id` (`board_id`),
  KEY `board_boardsrecipien_apartment_id_2f78cf4e_fk_apartment` (`apartment_id`),
  KEY `board_boardsrecipient_profile_id_4f91ef83_fk_accounts_profile_id` (`profile_id`),
  KEY `board_boardsrecipien_worksites_id_4f0af579_fk_worksites` (`worksites_id`),
  CONSTRAINT `board_boardsrecipien_apartment_id_2f78cf4e_fk_apartment` FOREIGN KEY (`apartment_id`) REFERENCES `apartments_apartments` (`id`),
  CONSTRAINT `board_boardsrecipien_worksites_id_4f0af579_fk_worksites` FOREIGN KEY (`worksites_id`) REFERENCES `worksites_worksites` (`id`),
  CONSTRAINT `board_boardsrecipient_board_id_6400fbe2_fk_board_boards_id` FOREIGN KEY (`board_id`) REFERENCES `board_boards` (`id`),
  CONSTRAINT `board_boardsrecipient_profile_id_4f91ef83_fk_accounts_profile_id` FOREIGN KEY (`profile_id`) REFERENCES `accounts_profile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `board_boardsrecipient`
--

LOCK TABLES `board_boardsrecipient` WRITE;
/*!40000 ALTER TABLE `board_boardsrecipient` DISABLE KEYS */;
/*!40000 ALTER TABLE `board_boardsrecipient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `board_survey`
--

DROP TABLE IF EXISTS `board_survey`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `board_survey` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(250) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `board_survey`
--

LOCK TABLES `board_survey` WRITE;
/*!40000 ALTER TABLE `board_survey` DISABLE KEYS */;
/*!40000 ALTER TABLE `board_survey` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `board_surveyquestion`
--

DROP TABLE IF EXISTS `board_surveyquestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `board_surveyquestion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(250) NOT NULL,
  `survey_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `board_surveyquestion_survey_id_b05b5ed4_fk_board_survey_id` (`survey_id`),
  CONSTRAINT `board_surveyquestion_survey_id_b05b5ed4_fk_board_survey_id` FOREIGN KEY (`survey_id`) REFERENCES `board_survey` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `board_surveyquestion`
--

LOCK TABLES `board_surveyquestion` WRITE;
/*!40000 ALTER TABLE `board_surveyquestion` DISABLE KEYS */;
/*!40000 ALTER TABLE `board_surveyquestion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `board_surveyquestionchoices`
--

DROP TABLE IF EXISTS `board_surveyquestionchoices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `board_surveyquestionchoices` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(250) NOT NULL,
  `question_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `board_surveyquestion_question_id_07158a61_fk_board_sur` (`question_id`),
  CONSTRAINT `board_surveyquestion_question_id_07158a61_fk_board_sur` FOREIGN KEY (`question_id`) REFERENCES `board_surveyquestion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `board_surveyquestionchoices`
--

LOCK TABLES `board_surveyquestionchoices` WRITE;
/*!40000 ALTER TABLE `board_surveyquestionchoices` DISABLE KEYS */;
/*!40000 ALTER TABLE `board_surveyquestionchoices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (9,'accounts','profile'),(1,'admin','logentry'),(10,'apartments','apartments'),(30,'apartments','apartmentsub'),(24,'apartments','checklist'),(25,'apartments','checklistworksites'),(11,'apartments','clientapartments'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(21,'board','boardattachments'),(22,'board','boardread'),(23,'board','boards'),(29,'board','boardsrecipient'),(26,'board','survey'),(27,'board','surveyquestion'),(28,'board','surveyquestionchoices'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(7,'token_blacklist','blacklistedtoken'),(8,'token_blacklist','outstandingtoken'),(12,'worksites','categories'),(13,'worksites','checklist'),(20,'worksites','checklistworksites'),(19,'worksites','collabworksites'),(14,'worksites','contractor'),(15,'worksites','financier'),(31,'worksites','foglioparticella'),(33,'worksites','status'),(16,'worksites','worksites'),(18,'worksites','worksitescategories'),(32,'worksites','worksitesfoglioparticella'),(17,'worksites','worksitesprofile'),(34,'worksites','worksitesstatus');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-02-06 20:38:45.974878'),(2,'contenttypes','0002_remove_content_type_name','2024-02-06 20:38:46.089869'),(3,'auth','0001_initial','2024-02-06 20:38:46.562249'),(4,'auth','0002_alter_permission_name_max_length','2024-02-06 20:38:46.617325'),(5,'auth','0003_alter_user_email_max_length','2024-02-06 20:38:46.643206'),(6,'auth','0004_alter_user_username_opts','2024-02-06 20:38:46.654414'),(7,'auth','0005_alter_user_last_login_null','2024-02-06 20:38:46.710185'),(8,'auth','0006_require_contenttypes_0002','2024-02-06 20:38:46.712565'),(9,'auth','0007_alter_validators_add_error_messages','2024-02-06 20:38:46.724609'),(10,'auth','0008_alter_user_username_max_length','2024-02-06 20:38:46.764090'),(11,'auth','0009_alter_user_last_name_max_length','2024-02-06 20:38:46.802609'),(12,'auth','0010_alter_group_name_max_length','2024-02-06 20:38:46.825802'),(13,'auth','0011_update_proxy_permissions','2024-02-06 20:38:46.838178'),(14,'auth','0012_alter_user_first_name_max_length','2024-02-06 20:38:46.887272'),(15,'accounts','0001_initial','2024-02-06 20:38:46.964334'),(16,'admin','0001_initial','2024-02-06 20:38:47.077589'),(17,'admin','0002_logentry_remove_auto_add','2024-02-06 20:38:47.092147'),(18,'admin','0003_logentry_add_action_flag_choices','2024-02-06 20:38:47.108384'),(19,'worksites','0001_initial','2024-02-06 20:38:47.549012'),(20,'apartments','0001_initial','2024-02-06 20:38:47.561809'),(21,'apartments','0002_initial','2024-02-06 20:38:47.611828'),(22,'apartments','0003_clientapartments','2024-02-06 20:38:47.695112'),(23,'board','0001_initial','2024-02-06 20:38:47.779706'),(24,'board','0002_initial','2024-02-06 20:38:47.961228'),(25,'sessions','0001_initial','2024-02-06 20:38:47.991406'),(26,'token_blacklist','0001_initial','2024-02-06 20:38:48.111189'),(27,'token_blacklist','0002_outstandingtoken_jti_hex','2024-02-06 20:38:48.147774'),(28,'token_blacklist','0003_auto_20171017_2007','2024-02-06 20:38:48.180542'),(29,'token_blacklist','0004_auto_20171017_2013','2024-02-06 20:38:48.241984'),(30,'token_blacklist','0005_remove_outstandingtoken_jti','2024-02-06 20:38:48.290296'),(31,'token_blacklist','0006_auto_20171017_2113','2024-02-06 20:38:48.326231'),(32,'token_blacklist','0007_auto_20171017_2214','2024-02-06 20:38:48.486726'),(33,'token_blacklist','0008_migrate_to_bigautofield','2024-02-06 20:38:48.710486'),(34,'token_blacklist','0010_fix_migrate_to_bigautofield','2024-02-06 20:38:48.745899'),(35,'token_blacklist','0011_linearizes_history','2024-02-06 20:38:48.749916'),(36,'token_blacklist','0012_alter_outstandingtoken_user','2024-02-06 20:38:48.777278'),(37,'worksites','0002_alter_worksites_address_alter_worksites_image_and_more','2024-02-06 20:38:49.021760'),(38,'worksites','0003_alter_worksites_contractor_alter_worksites_date_and_more','2024-02-06 20:38:49.432206'),(39,'worksites','0004_alter_collabworksites_worksite','2024-02-06 20:38:49.460582'),(40,'worksites','0005_remove_worksites_type','2024-02-06 20:38:49.510474'),(41,'worksites','0006_alter_worksitescategories_worksite','2024-02-06 20:38:49.540982'),(42,'worksites','0007_remove_checklistworksites_checklist_and_more','2024-02-13 18:44:39.328865'),(43,'apartments','0004_checklist_checklistworksites','2024-02-13 18:44:39.484070'),(44,'worksites','0008_alter_collabworksites_date_start','2024-02-13 18:44:39.499816'),(45,'board','0003_survey_alter_boardattachments_attachment_link_and_more','2024-02-13 18:44:39.585307'),(46,'board','0004_surveyquestion_remove_boards_apartment_and_more','2024-02-13 18:44:39.977792'),(47,'board','0005_alter_boardsrecipient_apartment_and_more','2024-02-13 18:44:40.256756'),(48,'board','0006_alter_boardsrecipient_board','2024-02-13 18:44:40.281790'),(49,'board','0007_alter_boards_image','2024-02-13 18:44:40.308806'),(50,'worksites','0009_foglioparticella_worksitesfoglioparticella','2024-02-26 17:56:05.539077'),(51,'worksites','0010_alter_worksitesfoglioparticella_worksite','2024-02-26 17:56:05.566489'),(52,'worksites','0011_alter_collabworksites_profile','2024-02-26 17:56:05.593173'),(53,'worksites','0012_alter_foglioparticella_foglio_and_more','2024-02-26 17:56:05.688242'),(54,'worksites','0013_alter_worksites_codice_cig_and_more','2024-02-26 17:56:05.887882'),(55,'apartments','0005_rename_foglio_apartments_floor_and_more','2024-02-26 17:56:06.081200'),(56,'apartments','0006_alter_apartmentsub_apartment','2024-02-26 17:56:06.109208'),(57,'apartments','0007_alter_apartments_floor','2024-02-26 17:56:06.159611'),(58,'apartments','0008_alter_apartmentsub_sub','2024-02-26 17:56:06.202047'),(59,'apartments','0009_alter_apartmentsub_foglio_particella','2024-02-26 17:56:06.279264'),(60,'apartments','0010_apartments_is_active','2024-02-26 17:56:06.330220'),(61,'worksites','0014_worksites_is_active','2024-02-26 17:56:06.454251'),(62,'worksites','0015_worksites_approved','2024-02-26 17:57:06.454000'),(63,'worksites','0016_status_worksitesstatus','2024-02-26 17:57:16.454000'),(64,'worksites','0016_status_worksitesstatus2','2024-02-26 18:02:18.994158');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token_blacklist_blacklistedtoken`
--

DROP TABLE IF EXISTS `token_blacklist_blacklistedtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_blacklistedtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `blacklisted_at` datetime(6) NOT NULL,
  `token_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_id` (`token_id`),
  CONSTRAINT `token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk` FOREIGN KEY (`token_id`) REFERENCES `token_blacklist_outstandingtoken` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_blacklistedtoken`
--

LOCK TABLES `token_blacklist_blacklistedtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token_blacklist_outstandingtoken`
--

DROP TABLE IF EXISTS `token_blacklist_outstandingtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_outstandingtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` int DEFAULT NULL,
  `jti` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq` (`jti`),
  KEY `token_blacklist_outs_user_id_83bc629a_fk_auth_user` (`user_id`),
  CONSTRAINT `token_blacklist_outs_user_id_83bc629a_fk_auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_outstandingtoken`
--

LOCK TABLES `token_blacklist_outstandingtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` DISABLE KEYS */;
INSERT INTO `token_blacklist_outstandingtoken` VALUES (1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTAyNDU1OCwiaWF0IjoxNzA3MjQ4NTU4LCJqdGkiOiJkY2Q5YWE2MDRjNzc0ZjEwOWJiMDFhOGYwMGU5NGYyOCIsInVzZXJfaWQiOjF9.oP-K06IJXAA44FZbQfmOPwgsf_A9QU2aAPeeu6L217g','2024-02-06 20:42:38.173420','2024-05-06 21:42:38.000000',1,'dcd9aa604c774f109bb01a8f00e94f28'),(2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTAyNDY1NywiaWF0IjoxNzA3MjQ4NjU3LCJqdGkiOiJkMzllOGEwYjdlMjQ0MjljOGY1YTBhMGQ5OTRhMTM3YiIsInVzZXJfaWQiOjF9.5nup8axDXspYzFfdPX_4Zo2A9Gk_Evz8EnjRazWBgc0','2024-02-06 20:44:17.765395','2024-05-06 21:44:17.000000',1,'d39e8a0b7e24429c8f5a0a0d994a137b'),(3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTAyOTExNywiaWF0IjoxNzA3MjUzMTE3LCJqdGkiOiI5MTJhNWQ3ZDBjY2E0MWYzYTQ1ZmQ1NWVmOWU1YzYzNyIsInVzZXJfaWQiOjF9.rUjH370yGqWXlWNwObeXe1T1Oh8ItjNiG93QH8CamVc','2024-02-06 21:58:37.794564','2024-05-06 22:58:37.000000',1,'912a5d7d0cca41f3a45fd55ef9e5c637'),(4,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTA4MjAwNiwiaWF0IjoxNzA3MzA2MDA2LCJqdGkiOiIyOThkZjFjMmI2ZmY0Njk2ODMxZmRkZjRkMzhmNjQxNSIsInVzZXJfaWQiOjF9.JiXYFKxaTw9fnqU_EqFZbRtu4HAgVbQxjFxQGzJ6uwY','2024-02-07 12:40:06.386576','2024-05-07 13:40:06.000000',1,'298df1c2b6ff4696831fddf4d38f6415'),(5,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTA4MjI1MiwiaWF0IjoxNzA3MzA2MjUyLCJqdGkiOiJkOTE1MzQ1MjFmZmQ0MmQ3Yjk4ODgwZjQ2NWM3OGUxNSIsInVzZXJfaWQiOjF9.FrpJorea7JVuCMYeul2R-K1Rq0h_HRcj67hI9Tg37Y0','2024-02-07 12:44:12.825766','2024-05-07 13:44:12.000000',1,'d91534521ffd42d7b98880f465c78e15'),(6,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTA4MjMwNCwiaWF0IjoxNzA3MzA2MzA0LCJqdGkiOiJmMjJlMzczMjUzMTk0OTIwODU0ZGUxMjU3YjRkNzgwMiIsInVzZXJfaWQiOjF9.k_tCCzZapntmthIkX89wTuMlcfLNc3WpO0t0E7z9wgE','2024-02-07 12:45:04.753088','2024-05-07 13:45:04.000000',1,'f22e373253194920854de1257b4d7802'),(7,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTA4MjkxNywiaWF0IjoxNzA3MzA2OTE3LCJqdGkiOiI1MmVhNDAxYzBiNmI0MTcyOTQ1N2E4ZTQwMjlmMGJkNiIsInVzZXJfaWQiOjF9.9f_lD09bcQRHymActLRz4PZ-q5CSWy_F2_79Da9CRvo','2024-02-07 12:55:17.347976','2024-05-07 13:55:17.000000',1,'52ea401c0b6b41729457a8e4029f0bd6'),(8,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTA4Mjk0NCwiaWF0IjoxNzA3MzA2OTQ0LCJqdGkiOiI2NGUzMDhhMzljMjE0YTg1YjdmMmIyNmUyNzA3NTMyOSIsInVzZXJfaWQiOjF9.3_TzftBxttVQuGHW5Koi2MlxlvgkaPiBnQOuRTKxobs','2024-02-07 12:55:44.423790','2024-05-07 13:55:44.000000',1,'64e308a39c214a85b7f2b26e27075329'),(9,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTA4MzI2NSwiaWF0IjoxNzA3MzA3MjY1LCJqdGkiOiIzMWI0OTA4ZjI4YmY0Y2QzYWU2YWMxNDEwODFhYjk4ZiIsInVzZXJfaWQiOjF9.qfFVJl_ZiSldPxqBdzweUM9cMIB6s4Q_mJuUgKLMQ94','2024-02-07 13:01:05.160854','2024-05-07 14:01:05.000000',1,'31b4908f28bf4cd3ae6ac141081ab98f'),(10,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTA4NDA1MiwiaWF0IjoxNzA3MzA4MDUyLCJqdGkiOiI2MDQ3MjhkNWY3YzQ0NGFmOGRkNmI3N2I1NjE0NTVlOSIsInVzZXJfaWQiOjF9.eybgQww7hpW65vADVcg33xPQ6fGxXg1rNR7XZT61N5k','2024-02-07 13:14:12.533680','2024-05-07 14:14:12.000000',1,'604728d5f7c444af8dd6b77b561455e9'),(11,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTA4NDA3NSwiaWF0IjoxNzA3MzA4MDc1LCJqdGkiOiI2NGIyNWJiN2VkODk0ZjNiYjJjNWIwMzFlZmNhYjc1NCIsInVzZXJfaWQiOjF9.gczueWqa_b7B4ymPJuzMOygxD8FZdzVfHhPfZcITW4A','2024-02-07 13:14:35.501432','2024-05-07 14:14:35.000000',1,'64b25bb7ed894f3bb2c5b031efcab754'),(12,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTA4NTk5MSwiaWF0IjoxNzA3MzA5OTkxLCJqdGkiOiIxYjc3OWUxMDg1NTU0ZjBiOGQ3MWM2M2Q0YmU4M2NlMyIsInVzZXJfaWQiOjF9.pbVWdtRqMlPfPjGCSDDTSNqWKDkwJnSzz-VCoGtOeTI','2024-02-07 13:46:31.336859','2024-05-07 14:46:31.000000',1,'1b779e1085554f0b8d71c63d4be83ce3'),(13,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTA5NjU2MSwiaWF0IjoxNzA3MzIwNTYxLCJqdGkiOiJmNzMzNzE1MjU2YzA0Nzk4YmE0ZjQ1YmM1MzRjNTgwNSIsInVzZXJfaWQiOjF9.yg93eF7RyT2hgyUSFv0jsfwiiendst1Y2zKQ44tJIHM','2024-02-07 16:42:41.457349','2024-05-07 17:42:41.000000',1,'f733715256c04798ba4f45bc534c5805'),(14,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTA5NzQ0MCwiaWF0IjoxNzA3MzIxNDQwLCJqdGkiOiIxM2ZmOWQ2YmU3OTU0NTY2YTg1ZmM4ZGIxMTgzZWI0MiIsInVzZXJfaWQiOjF9.B_YfI-_inHpEUOoQasVF_twXK4UcYyzav--Hih-J3Mc','2024-02-07 16:57:20.770700','2024-05-07 17:57:20.000000',1,'13ff9d6be7954566a85fc8db1183eb42'),(15,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTA5NzU1NiwiaWF0IjoxNzA3MzIxNTU2LCJqdGkiOiJmMjA2ZGJhMGE3YjM0NGM3OTM0NzI1ZTk3Yzk4YmM0MiIsInVzZXJfaWQiOjF9.U635Djfj34HrB0OXrLwOvxjmHIXAjaY61RHxfzPMwpA','2024-02-07 16:59:16.121137','2024-05-07 17:59:16.000000',1,'f206dba0a7b344c7934725e97c98bc42'),(16,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTA5ODA3MiwiaWF0IjoxNzA3MzIyMDcyLCJqdGkiOiI2ODExMDA3M2Q2YTI0MjAzOWVhYzhlOWJiMWE3ZGEzNyIsInVzZXJfaWQiOjF9.Y9uJwy1b_vpmHiAzGxkFnaeZOj6AFuGVuYI6hAuq7OA','2024-02-07 17:07:52.786543','2024-05-07 18:07:52.000000',1,'68110073d6a242039eac8e9bb1a7da37'),(17,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTA5ODA5NywiaWF0IjoxNzA3MzIyMDk3LCJqdGkiOiI3ODI3YzFkYmNlM2U0MmE3YjI4ODc0NzYwNzZlNmFmMCIsInVzZXJfaWQiOjF9.dc7trUiskGlLXozJYlLEVrRywv6CkK5570vyVOKhnPU','2024-02-07 17:08:17.474990','2024-05-07 18:08:17.000000',1,'7827c1dbce3e42a7b2887476076e6af0'),(18,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTA5ODI2OCwiaWF0IjoxNzA3MzIyMjY4LCJqdGkiOiIwMjMzZGI5ODdhYmM0ODc2YTFkZjI3MmNkNDcwZGIzMiIsInVzZXJfaWQiOjF9.5Ec4dTe05wGdSuExK2B0P2q0bC7uESLyhheniZdj2Ic','2024-02-07 17:11:08.600324','2024-05-07 18:11:08.000000',1,'0233db987abc4876a1df272cd470db32'),(19,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTA5ODU2MywiaWF0IjoxNzA3MzIyNTYzLCJqdGkiOiIyMzQzMjI5NjVkNWU0MGVjODgxMmJiNzU5ZTUwYjM4NyIsInVzZXJfaWQiOjF9.8GJT-mJtOSAtIUB15C80VcUBpvK6PSLE7n3loRFrHBE','2024-02-07 17:16:03.143987','2024-05-07 18:16:03.000000',1,'234322965d5e40ec8812bb759e50b387'),(20,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTA5OTgyMywiaWF0IjoxNzA3MzIzODIzLCJqdGkiOiI3ODI1MjQwZDc4NTM0MDE0ODJmMjU2YTdiNjkzZmU3YyIsInVzZXJfaWQiOjF9.-Et5usbZUDuPuoXqUucJqu5If80B_rsq8V2gMBHLPso','2024-02-07 17:37:03.932196','2024-05-07 18:37:03.000000',1,'7825240d7853401482f256a7b693fe7c'),(21,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTA5OTg2NCwiaWF0IjoxNzA3MzIzODY0LCJqdGkiOiIwMWI0MjdjOGQwMDI0NjU2ODJkM2M0NjU3OWRhNzA2YSIsInVzZXJfaWQiOjF9.Y1J7GTWDzR8TdyUfyFk6vh24MMSmdBeIwVKJvlJTTCQ','2024-02-07 17:37:44.365724','2024-05-07 18:37:44.000000',1,'01b427c8d002465682d3c46579da706a'),(22,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTEwMDE2MSwiaWF0IjoxNzA3MzI0MTYxLCJqdGkiOiIyYWRkYmE1OTgyMzE0NjAyOWI0ZjIyZTRkY2EwMzk5MyIsInVzZXJfaWQiOjF9.hEqiZp3L468EIEglKvnJ3-Co3DpjeAl6nQ4TEDtfO_g','2024-02-07 17:42:41.556918','2024-05-07 18:42:41.000000',1,'2addba59823146029b4f22e4dca03993'),(23,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTEwMDIzNSwiaWF0IjoxNzA3MzI0MjM1LCJqdGkiOiJiYjgzN2VkZDYyZmU0YTU5YjEwY2M3Nzk5YzQ2ZDQ2MyIsInVzZXJfaWQiOjF9.q1KqP3wu10vcjAYPCzTBEBAXOuhH8fma3EdjjQX_CYU','2024-02-07 17:43:55.398800','2024-05-07 18:43:55.000000',1,'bb837edd62fe4a59b10cc7799c46d463'),(24,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTEwMDk2NSwiaWF0IjoxNzA3MzI0OTY1LCJqdGkiOiJjNzg1Zjc5NDQ3ZTc0YTcyYjM4YzMyNmI1ZGNiZmE3YyIsInVzZXJfaWQiOjF9.R9mh_NJ2U3PxQ0UEYNDxKxUnfXgVKhJxNWk24HpOKe8','2024-02-07 17:56:05.309047','2024-05-07 18:56:05.000000',1,'c785f79447e74a72b38c326b5dcbfa7c'),(25,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTEwMTExMCwiaWF0IjoxNzA3MzI1MTEwLCJqdGkiOiJhYzQ4NzkwYTRhZWM0MWQ4YjNjNjJkNTk3NWU5NjRlYyIsInVzZXJfaWQiOjF9.0tO0cauFvU4gPomX0WBjIBN8NHQHmkUtPAe4ehzdG2Q','2024-02-07 17:58:30.071439','2024-05-07 18:58:30.000000',1,'ac48790a4aec41d8b3c62d5975e964ec'),(26,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTEwMTY5NCwiaWF0IjoxNzA3MzI1Njk0LCJqdGkiOiJlYWE5MjRhNDI3NTQ0MzZlOWI1YmZiZjk4NTE2NDUzMyIsInVzZXJfaWQiOjF9.71JujtTulrqdGy4Mv8m2y_9sxoVa4kh-A5rBcyM7xfg','2024-02-07 18:08:14.466633','2024-05-07 19:08:14.000000',1,'eaa924a42754436e9b5bfbf985164533'),(27,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTE4MzkxOSwiaWF0IjoxNzA3NDA3OTE5LCJqdGkiOiJjNzk0MGQwMTFhODg0OTA0OTZhZWEyMzkzZjIxOGE3MCIsInVzZXJfaWQiOjF9.DUMbobqPKlHqzIgQjDkUWYeJHKxZoKm9TUgCjqTb6Lo','2024-02-08 16:58:39.000483','2024-05-08 17:58:39.000000',1,'c7940d011a88490496aea2393f218a70'),(28,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTE4NDE3NywiaWF0IjoxNzA3NDA4MTc3LCJqdGkiOiI5ZjRlODA3ZGY1NWY0ZjE4OTc2ODJmNThlYzBjOTQ3YiIsInVzZXJfaWQiOjJ9.3h5Hn5CoTWyqErQ6rNEzJXWRj35A8pOzmDtfelR1edc','2024-02-08 17:02:57.396438','2024-05-08 18:02:57.000000',2,'9f4e807df55f4f1897682f58ec0c947b'),(29,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTE4NDMzNSwiaWF0IjoxNzA3NDA4MzM1LCJqdGkiOiIzNDY5NmM4MmU4NDA0YjZiYTBhMjU4Y2IyYjIzMjgxNyIsInVzZXJfaWQiOjJ9.xDeIfjVQUNmq_2pdPPkrsKEn1AzTtIJt87jH-ydxHYM','2024-02-08 17:05:35.480812','2024-05-08 18:05:35.000000',2,'34696c82e8404b6ba0a258cb2b232817'),(30,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTE4NTE1NiwiaWF0IjoxNzA3NDA5MTU2LCJqdGkiOiI3ODdlZGRmMzNkMDE0ZmU3OTA2MzFjNmQ2ZGMzNTVmYiIsInVzZXJfaWQiOjJ9.kTOVQFxVudf4_NMYnVe-eE-Lg9QiMptie0GW4fRRqHc','2024-02-08 17:19:16.202676','2024-05-08 18:19:16.000000',2,'787eddf33d014fe790631c6d6dc355fb'),(31,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTE4NTMwNSwiaWF0IjoxNzA3NDA5MzA1LCJqdGkiOiI5MTA4ZDQzN2E3Yzk0ZTdhYjlhMWE3NjU1YmVlYTVlYyIsInVzZXJfaWQiOjJ9.KYAGWG8y1BmJqlWczoknaMtlk0bW71xUeTkN_RIcPt4','2024-02-08 17:21:45.790248','2024-05-08 18:21:45.000000',2,'9108d437a7c94e7ab9a1a7655beea5ec'),(32,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTE4NTQ0OSwiaWF0IjoxNzA3NDA5NDQ5LCJqdGkiOiI5Njc5MDNjZjBmMDE0ODRhYTc1MWI1NTEyZTYyODRiMCIsInVzZXJfaWQiOjJ9.TqnUSikJJpsmw5jXI-cd2xwdkWTNH5fBxCWpz2BJj2A','2024-02-08 17:24:09.848685','2024-05-08 18:24:09.000000',2,'967903cf0f01484aa751b5512e6284b0'),(33,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTE4NTQ2NywiaWF0IjoxNzA3NDA5NDY3LCJqdGkiOiJiZjQ1OThlMGZmNjc0MjljYjkyYmFhZGMwMzBmYjAxMyIsInVzZXJfaWQiOjJ9.CrAxDtkm20XqxW-QBHylV0nusPPsq0lAf3WOtfdDn1g','2024-02-08 17:24:27.291589','2024-05-08 18:24:27.000000',2,'bf4598e0ff67429cb92baadc030fb013'),(34,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTE4NTU2MiwiaWF0IjoxNzA3NDA5NTYyLCJqdGkiOiI4ZmYyZWNlZjE0OGU0OTkzOWNjYzBhNDA4MzllYmYxNiIsInVzZXJfaWQiOjJ9.4pJkOZpQdfdZUA9FUaVQFxJav5S4Wb9jvUbusypLoh4','2024-02-08 17:26:02.947374','2024-05-08 18:26:02.000000',2,'8ff2ecef148e49939ccc0a40839ebf16'),(35,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxNTE4NjIxNiwiaWF0IjoxNzA3NDEwMjE2LCJqdGkiOiJiZTcxZWJjMTZkZTE0ZWZkYTkwYzdkZTE2N2UxNzUyMyIsInVzZXJfaWQiOjJ9.abRcIc8DKY9uOYK30xp9_q4HtunSZMg9NpnzQCuixEA','2024-02-08 17:36:56.902506','2024-05-08 18:36:56.000000',2,'be71ebc16de14efda90c7de167e17523');
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `worksites_categories`
--

DROP TABLE IF EXISTS `worksites_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `worksites_categories` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `worksites_categories`
--

LOCK TABLES `worksites_categories` WRITE;
/*!40000 ALTER TABLE `worksites_categories` DISABLE KEYS */;
/*!40000 ALTER TABLE `worksites_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `worksites_collabworksites`
--

DROP TABLE IF EXISTS `worksites_collabworksites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `worksites_collabworksites` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role` varchar(150) NOT NULL,
  `order` int NOT NULL,
  `profile_id` bigint NOT NULL,
  `worksite_id` bigint NOT NULL,
  `date_end` datetime(6) DEFAULT NULL,
  `date_start` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `worksites_collabwork_profile_id_9669ad6a_fk_accounts_` (`profile_id`),
  KEY `worksites_collabwork_worksite_id_b01aaecb_fk_worksites` (`worksite_id`),
  CONSTRAINT `worksites_collabwork_profile_id_9669ad6a_fk_accounts_` FOREIGN KEY (`profile_id`) REFERENCES `accounts_profile` (`id`),
  CONSTRAINT `worksites_collabwork_worksite_id_b01aaecb_fk_worksites` FOREIGN KEY (`worksite_id`) REFERENCES `worksites_worksites` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `worksites_collabworksites`
--

LOCK TABLES `worksites_collabworksites` WRITE;
/*!40000 ALTER TABLE `worksites_collabworksites` DISABLE KEYS */;
INSERT INTO `worksites_collabworksites` VALUES (1,'DTC',1,1,1,NULL,NULL),(2,'ASDV',1,1,1,NULL,NULL),(4,'ASD',1,1,1,NULL,NULL),(6,'ASD',1,3,1,NULL,NULL);
/*!40000 ALTER TABLE `worksites_collabworksites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `worksites_contractor`
--

DROP TABLE IF EXISTS `worksites_contractor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `worksites_contractor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `worksites_contractor`
--

LOCK TABLES `worksites_contractor` WRITE;
/*!40000 ALTER TABLE `worksites_contractor` DISABLE KEYS */;
/*!40000 ALTER TABLE `worksites_contractor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `worksites_financier`
--

DROP TABLE IF EXISTS `worksites_financier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `worksites_financier` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `worksites_financier`
--

LOCK TABLES `worksites_financier` WRITE;
/*!40000 ALTER TABLE `worksites_financier` DISABLE KEYS */;
/*!40000 ALTER TABLE `worksites_financier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `worksites_foglioparticella`
--

DROP TABLE IF EXISTS `worksites_foglioparticella`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `worksites_foglioparticella` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `foglio` varchar(50) DEFAULT NULL,
  `particella` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `worksites_foglioparticella`
--

LOCK TABLES `worksites_foglioparticella` WRITE;
/*!40000 ALTER TABLE `worksites_foglioparticella` DISABLE KEYS */;
/*!40000 ALTER TABLE `worksites_foglioparticella` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `worksites_status`
--

DROP TABLE IF EXISTS `worksites_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `worksites_status` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `description` varchar(150) NOT NULL,
  `order` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `worksites_status`
--

LOCK TABLES `worksites_status` WRITE;
/*!40000 ALTER TABLE `worksites_status` DISABLE KEYS */;
/*!40000 ALTER TABLE `worksites_status` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `worksites_worksites`
--

DROP TABLE IF EXISTS `worksites_worksites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `worksites_worksites` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `image` varchar(100) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `address` varchar(100) DEFAULT NULL,
  `lat` decimal(10,6) DEFAULT NULL,
  `lon` decimal(10,6) DEFAULT NULL,
  `is_visible` tinyint(1) DEFAULT NULL,
  `net_worth` double DEFAULT NULL,
  `link` varchar(100) DEFAULT NULL,
  `date` datetime(6) DEFAULT NULL,
  `date_update` datetime(6) DEFAULT NULL,
  `contractor_id` bigint DEFAULT NULL,
  `financier_id` bigint DEFAULT NULL,
  `codice_CIG` varchar(100) DEFAULT NULL,
  `codice_CUP` varchar(100) DEFAULT NULL,
  `codice_commessa` varchar(100) DEFAULT NULL,
  `date_end` datetime(6) DEFAULT NULL,
  `date_start` datetime(6) DEFAULT NULL,
  `percentage_worth` double DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `worksites_worksites_contractor_id_2cb4e057_fk_worksites` (`contractor_id`),
  KEY `worksites_worksites_financier_id_1600a38d_fk_worksites` (`financier_id`),
  CONSTRAINT `worksites_worksites_contractor_id_2cb4e057_fk_worksites` FOREIGN KEY (`contractor_id`) REFERENCES `worksites_contractor` (`id`),
  CONSTRAINT `worksites_worksites_financier_id_1600a38d_fk_worksites` FOREIGN KEY (`financier_id`) REFERENCES `worksites_financier` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `worksites_worksites`
--

LOCK TABLES `worksites_worksites` WRITE;
/*!40000 ALTER TABLE `worksites_worksites` DISABLE KEYS */;
INSERT INTO `worksites_worksites` VALUES (1,NULL,'Cantiere Melatino','via melatina 1',NULL,NULL,1,5000,NULL,'2024-02-02 09:17:00.727309',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'APERTO',1);
/*!40000 ALTER TABLE `worksites_worksites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `worksites_worksitescategories`
--

DROP TABLE IF EXISTS `worksites_worksitescategories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `worksites_worksitescategories` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `category_id` bigint NOT NULL,
  `worksite_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `worksites_worksitesc_category_id_e58e5ef5_fk_worksites` (`category_id`),
  KEY `worksites_worksitesc_worksite_id_af173152_fk_worksites` (`worksite_id`),
  CONSTRAINT `worksites_worksitesc_category_id_e58e5ef5_fk_worksites` FOREIGN KEY (`category_id`) REFERENCES `worksites_categories` (`id`),
  CONSTRAINT `worksites_worksitesc_worksite_id_af173152_fk_worksites` FOREIGN KEY (`worksite_id`) REFERENCES `worksites_worksites` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `worksites_worksitescategories`
--

LOCK TABLES `worksites_worksitescategories` WRITE;
/*!40000 ALTER TABLE `worksites_worksitescategories` DISABLE KEYS */;
/*!40000 ALTER TABLE `worksites_worksitescategories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `worksites_worksitesfoglioparticella`
--

DROP TABLE IF EXISTS `worksites_worksitesfoglioparticella`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `worksites_worksitesfoglioparticella` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `foglio_particella_id` bigint NOT NULL,
  `worksite_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `worksites_worksitesf_foglio_particella_id_0f5c3d72_fk_worksites` (`foglio_particella_id`),
  KEY `worksites_worksitesf_worksite_id_dcee49cb_fk_worksites` (`worksite_id`),
  CONSTRAINT `worksites_worksitesf_foglio_particella_id_0f5c3d72_fk_worksites` FOREIGN KEY (`foglio_particella_id`) REFERENCES `worksites_foglioparticella` (`id`),
  CONSTRAINT `worksites_worksitesf_worksite_id_dcee49cb_fk_worksites` FOREIGN KEY (`worksite_id`) REFERENCES `worksites_worksites` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `worksites_worksitesfoglioparticella`
--

LOCK TABLES `worksites_worksitesfoglioparticella` WRITE;
/*!40000 ALTER TABLE `worksites_worksitesfoglioparticella` DISABLE KEYS */;
/*!40000 ALTER TABLE `worksites_worksitesfoglioparticella` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `worksites_worksitesprofile`
--

DROP TABLE IF EXISTS `worksites_worksitesprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `worksites_worksitesprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `profile_id` bigint NOT NULL,
  `worksite_id` bigint NOT NULL,
  `approved` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `worksites_worksitesp_profile_id_b0fd0c3e_fk_accounts_` (`profile_id`),
  KEY `worksites_worksitesp_worksite_id_9534216c_fk_worksites` (`worksite_id`),
  CONSTRAINT `worksites_worksitesp_profile_id_b0fd0c3e_fk_accounts_` FOREIGN KEY (`profile_id`) REFERENCES `accounts_profile` (`id`),
  CONSTRAINT `worksites_worksitesp_worksite_id_9534216c_fk_worksites` FOREIGN KEY (`worksite_id`) REFERENCES `worksites_worksites` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `worksites_worksitesprofile`
--

LOCK TABLES `worksites_worksitesprofile` WRITE;
/*!40000 ALTER TABLE `worksites_worksitesprofile` DISABLE KEYS */;
/*!40000 ALTER TABLE `worksites_worksitesprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `worksites_worksitesstatus`
--

DROP TABLE IF EXISTS `worksites_worksitesstatus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `worksites_worksitesstatus` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` datetime(6) DEFAULT NULL,
  `date_update` datetime(6) DEFAULT NULL,
  `status_id` bigint NOT NULL,
  `worksite_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `worksites_worksitess_status_id_9b5c2548_fk_worksites` (`status_id`),
  KEY `worksites_worksitess_worksite_id_213c1213_fk_worksites` (`worksite_id`),
  CONSTRAINT `worksites_worksitess_status_id_9b5c2548_fk_worksites` FOREIGN KEY (`status_id`) REFERENCES `worksites_status` (`id`),
  CONSTRAINT `worksites_worksitess_worksite_id_213c1213_fk_worksites` FOREIGN KEY (`worksite_id`) REFERENCES `worksites_worksites` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `worksites_worksitesstatus`
--

LOCK TABLES `worksites_worksitesstatus` WRITE;
/*!40000 ALTER TABLE `worksites_worksitesstatus` DISABLE KEYS */;
/*!40000 ALTER TABLE `worksites_worksitesstatus` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-02-26 19:22:19
