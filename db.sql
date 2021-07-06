DROP SCHEMA IF EXISTS `_temp_ecompy`;

CREATE SCHEMA `_temp_ecompy` CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_as_ci;

USE `_temp_ecompy`;


CREATE TABLE `products` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(250) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `n_stock` SMALLINT UNSIGNED,
  `n_sales` SMALLINT UNSIGNED,
  `rating` decimal(1,1),
  `shop_title` varchar(100) NOT NULL,
  `shop_href` varchar(200) NOT NULL,
  
  PRIMARY KEY (`id`)
 
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
