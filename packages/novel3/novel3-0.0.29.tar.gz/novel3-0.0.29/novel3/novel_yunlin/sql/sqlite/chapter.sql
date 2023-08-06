DROP TABLE IF EXISTS chapter;
CREATE TABLE `chapter` (
  `chapter_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `book_name` varchar(50) NOT NULL,
  `chapter_name` varchar(50) NOT NULL UNIQUE,
  `content` MEDIUMTEXT NOT NULL
) ;
update
  book
SET
  latest = 0;