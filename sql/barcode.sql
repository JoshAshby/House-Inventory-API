-- phpMyAdmin SQL Dump
-- version 3.4.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 12, 2011 at 12:15 AM
-- Server version: 5.5.13
-- PHP Version: 5.3.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `barcode`
--

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE IF NOT EXISTS `products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  `description` text NOT NULL,
  `barcode` text NOT NULL,
  `quantity` int(11) NOT NULL,
  `picture` text NOT NULL,
  `thumb` text NOT NULL,
  `flag` char(1) NOT NULL DEFAULT 'L',
  KEY `id` (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=53 ;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `description`, `barcode`, `quantity`, `picture`, `thumb`, `flag`) VALUES
(3, 'Green Graph Composition', 'Green covered, graph paper filled (.1 in) 100 sheet composition notebook from stables.', '718103025027', 1, '718103025027.png', '718103025027_thumb.png', 'M'),
(4, 'Orange Graph Notebook', 'Orange notebook from Rhodia. Graph paper, model N11. 7.4cm x 10.5cm.', '3037921120217', 1, '3037921120217.png', '3037921120217_thumb.png', 'L'),
(14, 'the social network', 'Movie about facebook.', '043396366268', 1, '043396366268.png', '043396366268_thumb.png', 'M'),
(23, 'Beagle', 'A Dog', 'dog987', 3, 'dog987.png', 'dog987_thumb.png', 'L'),
(52, 'god''s dog', 'a dog of god', 'dog', 10, 'dog.png', 'dog_thumb.png', 'L');

-- --------------------------------------------------------

--
-- Table structure for table `stats`
--

CREATE TABLE IF NOT EXISTS `stats` (
  `barcode` text NOT NULL,
  `last_5` text NOT NULL,
  `all` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `stats`
--

INSERT INTO `stats` (`barcode`, `last_5`, `all`) VALUES
('718103025027', '[-1.5, -1.5, -1.5, -1.5, -1.5]', '[-1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5, -1.5]'),
('dog987', '[]', '[]'),
('3037921120217', '[]', '[]'),
('043396366268', '[-0.07142857142857142, -0.07142857142857142, -0.07142857142857142, -0.07142857142857142, -0.07142857142857142]', '[-0.14634146341463414, -0.07142857142857142, -0.07142857142857142, -0.07142857142857142, -0.07142857142857142, -0.07142857142857142, -0.07142857142857142, -0.07142857142857142, -0.07142857142857142, -0.07142857142857142, -0.07142857142857142, -0.07142857142857142, -0.07142857142857142, -0.07142857142857142, -0.07142857142857142]'),
('dog', '[]', '[]');

-- --------------------------------------------------------

--
-- Table structure for table `usage`
--

CREATE TABLE IF NOT EXISTS `usage` (
  `barcode` text NOT NULL,
  `quantity` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `usage`
--

INSERT INTO `usage` (`barcode`, `quantity`, `date`) VALUES
('718103025027', 7, '2011-03-17 23:27:45'),
('dog987', 3, '2011-03-18 05:01:42'),
('dog987', 2, '2011-03-18 06:39:26'),
('718103025027', 1, '2011-03-22 07:16:32'),
('718103025027', 3, '2011-03-20 07:16:22'),
('dog987', 3, '2011-03-19 07:16:08'),
('718103025027', 4, '2011-03-19 07:16:02'),
('3037921120217', 1, '2011-03-19 07:15:54'),
('3037921120217', 5, '2011-03-19 07:15:47'),
('043396366268', 1, '2011-03-19 07:15:17'),
('043396366268', 2, '2011-02-19 08:15:09'),
('718103025027', 5, '2011-03-18 23:27:49'),
('718103025027', 1, '2011-03-13 22:57:48'),
('718103025027', 6, '2011-02-17 23:57:21'),
('718103025027', 3, '2011-03-07 07:47:48'),
('3037921120217', 1, '2011-03-01 07:47:46'),
('043396366268', 6, '2011-02-06 07:47:43'),
('043396366268', 3, '2011-02-05 07:47:43'),
('dog', 10, '2011-06-12 05:48:25'),
('dog', 10, '2011-06-12 05:38:39'),
('dog', 10, '2011-06-12 05:36:00'),
('dog', 10, '2011-06-12 05:33:47'),
('dog', 10, '2011-06-12 05:29:09'),
('dog', 5, '2011-06-12 05:12:32'),
('dog', 10, '2011-06-12 05:27:20'),
('dog', 10, '2011-06-12 06:12:22'),
('dog', 10, '2011-06-12 05:38:59'),
('dog', 10, '2011-06-12 05:38:15'),
('dog', 10, '2011-06-12 05:35:06'),
('dog', 10, '2011-06-12 05:31:26'),
('dog', 10, '2011-06-12 05:13:26'),
('dog', 10, '2011-06-12 05:26:56'),
('dog', 10, '2011-06-12 05:26:25'),
('dog', 10, '2011-06-12 05:24:14'),
('dog', 10, '2011-06-12 05:15:19');
