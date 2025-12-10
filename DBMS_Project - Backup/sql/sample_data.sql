-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: college_db
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

USE college_db;

--
-- Dumping data for table `advisor`
--

LOCK TABLES `advisor` WRITE;
/*!40000 ALTER TABLE `advisor` DISABLE KEYS */;
INSERT INTO `advisor` VALUES (1,'alan@faculty.edu',NULL,NULL,1),(2,'grace@faculty.edu',NULL,NULL,2),(3,'donna@faculty.edu',NULL,NULL,3),(4,'helen@faculty.edu',NULL,NULL,4),(5,'irene@faculty.edu',NULL,NULL,5);
/*!40000 ALTER TABLE `advisor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,'CS101','Intro to Programming',3,1),(2,'MATH164','Calculus I',4,2),(3,'BUS201','Principles of Management',3,3),(4,'ENG205','Thermodynamics',3,4),(5,'BIO110','Cell Biology',4,5),(6,'CS204','Data Structures',4,1);
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES (1,'CS','Computer Science'),(2,'MATH','Mathematics'),(3,'BUS','Business Administration'),(4,'ENG','Engineering'),(5,'BIO','Biology');
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `instructor`
--

LOCK TABLES `instructor` WRITE;
/*!40000 ALTER TABLE `instructor` DISABLE KEYS */;
INSERT INTO `instructor` VALUES (1,'alan@faculty.edu',1,NULL),(2,'grace@faculty.edu',2,NULL),(3,'donna@faculty.edu',1,NULL),(4,'helen@faculty.edu',4,NULL),(5,'irene@faculty.edu',5,NULL);
/*!40000 ALTER TABLE `instructor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `person`
--

LOCK TABLES `person` WRITE;
/*!40000 ALTER TABLE `person` DISABLE KEYS */;
INSERT INTO `person` VALUES ('alan@faculty.edu','Alan','Turing','1980-06-23'),('alice@student.edu','Alice','Fernandez','2002-04-15'),('bashar@student.edu','Bashar','Ghebari',NULL),('bob@student.edu','Bob','Johnson','2001-11-08'),('carol@student.edu','Carol','Singh','2003-02-22'),('david@student.edu','David','Nguyen','2002-07-05'),('donna@faculty.edu','Donna','Adams','1982-03-14'),('emma@student.edu','Emma','Lopez','2002-09-30'),('faadil@student.edu','Faadil','Ahmed',NULL),('grace@faculty.edu','Grace','Hopper','1978-12-09'),('helen@faculty.edu','Helen','Shaw','1979-08-19'),('irene@faculty.edu','Irene','Clark','1985-05-27'),('jack@student.edu','Jack','Johnson',NULL),('monish@student.edu','Monish','MG',NULL),('steven@student.edu','Steven','Aaprahamian',NULL),('vansh@student.edu','Vansh','Mago',NULL);
/*!40000 ALTER TABLE `person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (2,'Advisor'),(1,'Student');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `section`
--

LOCK TABLES `section` WRITE;
/*!40000 ALTER TABLE `section` DISABLE KEYS */;
INSERT INTO `section` VALUES (1,1,1,1,'001',35),(2,2,1,2,'001',30),(3,1,2,1,'002',40),(4,3,1,3,'001',25),(5,6,1,1,'001',30);
/*!40000 ALTER TABLE `section` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (1,'alice@student.edu',1,'Engineering',2.30,'2029-05-10',2025),(2,'bob@student.edu',2,'Mathematics',3.40,'2028-05-10',2024),(3,'carol@student.edu',3,'Business',3.20,'2029-05-10',2025),(4,'david@student.edu',4,'Mechanical Engg',3.70,'2029-05-10',2025),(5,'emma@student.edu',5,'Biology',3.90,'2028-05-10',2025),(7,'faadil@student.edu',1,'Business Management',1.50,'2028-11-26',2025),(8,'steven@student.edu',1,'Mechanical Engineering',3.60,'2028-11-26',2025),(10,'monish@student.edu',1,'Mechanical Engineering',3.90,'2028-11-26',2025);
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `student_takes_section`
--

LOCK TABLES `student_takes_section` WRITE;
/*!40000 ALTER TABLE `student_takes_section` DISABLE KEYS */;
INSERT INTO `student_takes_section` VALUES (1,1,NULL,NULL),(1,2,NULL,NULL),(2,2,'2025-08-30','A-'),(3,3,'2025-08-30',NULL),(4,4,'2025-08-30','B'),(5,5,'2025-08-30','A');
/*!40000 ALTER TABLE `student_takes_section` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `term`
--

LOCK TABLES `term` WRITE;
/*!40000 ALTER TABLE `term` DISABLE KEYS */;
INSERT INTO `term` VALUES (1,'Fall 2025','2025-08-25','2025-12-15'),(2,'Spring 2025','2025-01-13','2025-05-02'),(3,'Summer 2025','2025-06-02','2025-07-25'),(4,'Fall 2024','2024-08-26','2024-12-13'),(5,'Spring 2024','2024-01-15','2024-05-05');
/*!40000 ALTER TABLE `term` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'alice','pass123','alice@student.edu',1,1),(2,'bob','pass123','bob@student.edu',1,1),(3,'carol','pass123','carol@student.edu',1,1),(4,'david','pass123','david@student.edu',1,1),(5,'emma','pass123','emma@student.edu',1,1),(6,'alan','pass123','alan@faculty.edu',2,1),(7,'grace','pass123','grace@faculty.edu',2,1),(8,'donna','pass123','donna@faculty.edu',2,1),(9,'helen','pass123','helen@faculty.edu',2,1),(10,'irene','pass123','irene@faculty.edu',2,1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-06 19:02:02
