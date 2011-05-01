-- phpMyAdmin SQL Dump
-- version 3.2.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 19, 2011 at 09:01 AM
-- Server version: 5.1.41
-- PHP Version: 5.3.1

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `pl_barcode`
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
  `average` int(11) NOT NULL,
  `flag` text NOT NULL,
  KEY `id` (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=24 ;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `description`, `barcode`, `quantity`, `average`, `flag`) VALUES
(3, 'Green Graph Composition', 'Green covered, graph paper filled (.1 in) 100 sheet composition notebook from stables.', '718103025027', 3, 1, 'M'),
(4, 'Orange Graph Notebook', 'Orange notebook from Rhodia. Graph paper, model N11. 7.4cm x 10.5cm.', '3037921120217', 1, 1, 'L'),
(14, 'the social network', 'Movie about facebook.', '043396366268', 1, 1, 'M'),
(23, 'Beagle', 'A Dog', 'dog987', 3, 1, 'L');

-- --------------------------------------------------------

--
-- Table structure for table `stats`
--

CREATE TABLE IF NOT EXISTS `stats` (
  `barcode` text NOT NULL,
  `quantity` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `stats`
--

INSERT INTO `stats` (`barcode`, `quantity`, `date`) VALUES
('718103025027', 3, '2011-03-17 17:27:49'),
('dog987', 3, '2011-03-17 23:01:42'),
('dog987', 2, '2011-03-18 00:39:26'),
('718103025027', 3, '2011-03-19 01:16:33'),
('718103025027', 1, '2011-03-19 01:16:23'),
('dog987', 3, '2011-03-19 01:16:08'),
('718103025027', 3, '2011-03-19 01:16:01'),
('3037921120217', 1, '2011-03-19 01:15:54'),
('3037921120217', 5, '2011-03-19 01:15:47'),
('043396366268', 1, '2011-03-19 01:15:17'),
('043396366268', 2, '2011-03-19 01:15:09'),
('718103025027', 5, '2011-03-17 17:27:49'),
('718103025027', 3, '2011-03-13 16:57:49'),
('718103025027', 6, '2011-02-17 16:57:21'),
('718103025027', 3, '2011-03-07 00:47:48'),
('3037921120217', 1, '2011-03-01 00:47:46'),
('043396366268', 1, '2011-03-06 00:47:43');
