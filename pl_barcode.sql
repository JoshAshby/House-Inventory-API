-- phpMyAdmin SQL Dump
-- version 3.2.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 17, 2011 at 04:28 AM
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
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=22 ;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `description`, `barcode`, `quantity`, `average`, `flag`) VALUES
(17, 'Apple', 'Round red or green fruit.', '123456789abc', 4, 0, 'L'),
(18, 'Orange', 'Round orange colored citris fruit.', '987654321cba', 6, 0, 'L'),
(3, 'Green Graph Composition', 'Green covered, graph paper filled (.1 in) 100 sheet composition notebook from stables.', '718103025027', 3, 0, 'L'),
(4, 'Orange Graph Notebook', 'Orange notebook from Rhodia. Graph paper, model N11. 7.4cm x 10.5cm.', '3037921120217', 1, 0, 'L'),
(14, 'the social network', 'Movie about facebook.', '043396366268', 1, 0, 'L'),
(20, 'Craisins', 'Craisins, dried cranberries in a big bag.', '1245761134134', 1, 0, 'H'),
(21, 'Kiwi', 'Round fuzy brown fruit.', '34jk5h2345kl2', 6, 0, 'L');

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
('043396366268', 1, '2011-03-16 00:58:00'),
('123456789', 4, '2011-03-15 23:42:26'),
('043396366268', 1, '2011-03-16 00:58:49'),
('043396366268', 1, '2011-03-16 00:58:51'),
('043396366268', 4, '2011-03-16 01:01:41'),
('043396366268', 4, '2011-03-16 01:02:32'),
('043396366268', 4, '2011-03-16 01:03:38'),
('043396366268', 4, '2011-03-16 01:03:45'),
('043396366268', 4, '2011-03-16 01:03:45'),
('043396366268', 5, '2011-03-16 01:03:59'),
('043396366268', 5, '2011-03-16 01:04:33'),
('043396366268', 5, '2011-03-16 01:10:46'),
('043396366268', 6, '2011-03-16 01:13:08'),
('043396366268', 6, '2011-03-16 01:13:18'),
('043396366268', 8, '2011-03-16 01:13:22'),
('043396366268', 9, '2011-03-16 01:15:42'),
('043396366268', 1, '2011-03-16 01:16:11'),
('3037921120217', 1, '2011-03-16 13:33:36'),
('043396366268', 2, '2011-03-16 01:17:54'),
('1234151252344', 2, '2011-03-16 01:18:28'),
('043396366268', 2, '2011-03-16 01:20:17'),
('043396366268', 1, '2011-03-16 01:22:02'),
('043396366268', 1, '2011-03-16 01:22:41'),
('987654321', 1, '2011-03-16 01:23:14'),
('987654321cba', 6, '2011-03-16 14:15:10'),
('1245761134134', 1, '2011-03-16 14:58:03'),
('34jk5h2345kl2', 6, '2011-03-16 15:11:02');
