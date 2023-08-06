DROP TABLE IF EXISTS book;
CREATE TABLE `book` (
  `book_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `book_name` varchar(50) unique NOT NULL,
  `author` varchar(50) NOT NULL,
  `type` varchar(20) NOT NULL ,
  `word_number` int(11) NOT NULL DEFAULT '0',
  `popularity` int(11) NOT NULL DEFAULT '0' ,
  `update_time` DATE NOT NULL,
  `introduction` varchar(1000) NOT NULL,
  `status` varchar(10)  NOT NULL,
  `chapter_number` int(11) NOT NULL DEFAULT '0' ,
  `latest` BIT NOT NULL
);