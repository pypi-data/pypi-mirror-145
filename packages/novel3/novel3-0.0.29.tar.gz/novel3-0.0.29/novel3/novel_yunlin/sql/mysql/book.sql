DROP TABLE IF EXISTS book;
CREATE TABLE `book` (
  `book_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '书号',
  `book_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '书名',
  `author` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '作者',
  `type` varchar(20) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '类型',
  `word_number` int(11) NOT NULL DEFAULT '0' COMMENT '字数',
  `popularity` int(11) NOT NULL DEFAULT '0' COMMENT '人气',
  `update_time` DATE NOT NULL COMMENT '更新时间',
  `introduction` varchar(1000) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '简介',
  `status` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '状态',
  `chapter_number` int(11) NOT NULL DEFAULT '0' COMMENT '章节数',
  `latest` BIT NOT NULL COMMENT '是否是最新',
  PRIMARY KEY (`book_id`),
  UNIQUE KEY `book_name` (`book_name`)
) ENGINE = MyISAM DEFAULT CHARSET = utf8 COLLATE = utf8_unicode_ci;