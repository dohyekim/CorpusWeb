drop table User;
create table User(
	id int unsigned not null auto_increment primary key,
    passwd varchar(256),
    email varchar(256),
    username varchar(256)
);


select * from User;
/*truncate table Post; */
select * from Post;
/*drop table Post;*/

CREATE TABLE `Post` (
	`id` int unsigned auto_increment primary key,
  `postid` int(10) unsigned NOT NULL,
  `title` varchar(256),
  `date_posted` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `content` text NOT NULL,
  `user_id` int(10) unsigned NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

insert into Post(postid,title, content, user_id) values(1,'글1', '이것은 글입니다', 1);
insert into Post(postid,title, content, user_id) values(2,'글2', '이것은 글2입니다', 1);
insert into Post(postid,title, content, user_id) values(3,'글3', '이것은 글2입니다', 1);