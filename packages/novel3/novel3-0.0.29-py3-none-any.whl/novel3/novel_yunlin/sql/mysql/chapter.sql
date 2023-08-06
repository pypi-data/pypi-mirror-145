DROP TABLE IF EXISTS chapter;
CREATE TABLE `chapter` (
  `chapter_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '章节号',
  `book_name` varchar(50) NOT NULL COMMENT '书名',
  `chapter_name` varchar(50) NOT NULL UNIQUE COMMENT '章节名',
  `content` MEDIUMTEXT NOT NULL COMMENT '内容',
  PRIMARY KEY (`chapter_id`)
) ENGINE = MyISAM DEFAULT CHARSET = utf8mb4;
update
  book
SET
  latest = 0;