-- MySQL DB Schema

-- drop database ninuxuu;

CREATE database ninuxuu;
USE ninuxuu;

CREATE TABLE IF NOT EXISTS `resources` (
  `uri` varchar(700) NOT NULL,
  `server` varchar(50) NOT NULL,
  `share` varchar(50) NOT NULL,
  `path` varchar(650),
  `protocol` varchar(10),
  `filetype` varchar(20),
  `filesize` bigint unsigned default 0,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `firstseen` timestamp NOT NULL DEFAULT 0,
  PRIMARY KEY (`uri`)
) ENGINE=InnoDB DEFAULT CHARSET=ascii;

CREATE TABLE IF NOT EXISTS `tags` (
  `uri` varchar(700) NOT NULL,
  `tag` varchar(50) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`uri`,`tag`)
) ENGINE=InnoDB DEFAULT CHARSET=ascii;

-- CREATE OR REPLACE ALGORITHM=TEMPTABLE VIEW `tagstats` AS SELECT SQL_CACHE tag, count(tag) AS tagcount FROM tags WHERE tags.timestamp+0 >= (NOW()+0 - 31536000) GROUP BY tag;
CREATE INDEX tagnameindex ON tags (tag);

CREATE USER 'ninuu'@'localhost' IDENTIFIED BY 'ciaociao';
GRANT ALL PRIVILEGES ON ninuxuu.* TO 'ninuu'@'localhost';

