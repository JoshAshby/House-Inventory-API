-- phpMyAdmin SQL Dump
-- version 3.4.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 09, 2011 at 06:37 PM
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
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `description` text NOT NULL,
  `barcode` text NOT NULL,
  `quantity` int(11) NOT NULL,
  `average` int(11) NOT NULL DEFAULT '1',
  `flag` char(1) NOT NULL DEFAULT 'L',
  KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `description`, `barcode`, `quantity`, `average`, `flag`) VALUES
(3, 'Green Graph Composition', 'Green covered, graph paper filled (.1 in) 100 sheet composition notebook from stables.', '718103025027', 1, 1, 'M'),
(4, 'Orange Graph Notebook', 'Orange notebook from Rhodia. Graph paper, model N11. 7.4cm x 10.5cm.', '3037921120217', 1, 1, 'L'),
(14, 'the social network', 'Movie about facebook.', '043396366268', 1, 1, 'M'),
(23, 'Beagle', 'A Dog', 'dog987', 3, 1, 'L');

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
('718103025027', '[-1.75, -1.75, -1.75, -1.75, -1.75]', '[-1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75, -1.75]'),
('dog987', '[]', '[]'),
('3037921120217', '', ''),
('043396366268', '', '');

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
('043396366268', 2, '2011-03-19 07:15:09'),
('718103025027', 5, '2011-03-18 23:27:49'),
('718103025027', 1, '2011-03-13 22:57:48'),
('718103025027', 6, '2011-02-17 23:57:21'),
('718103025027', 3, '2011-03-07 07:47:48'),
('3037921120217', 1, '2011-03-01 07:47:46'),
('043396366268', 1, '2011-03-06 07:47:43'),
('dog986', 3, '2011-05-01 18:37:57'),
('dog986', 3, '2011-05-01 18:39:38'),
('dog986', 3, '2011-05-02 21:31:22');
