drop table User;
create table User(
	id int unsigned not null auto_increment primary key,
    passwd varchar(256),
    email varchar(256),
    username varchar(256)
);


select * from Talk;


select * from User;
/*truncate table Post; */
select * from Post;
/*drop table Post;*/

CREATE TABLE `Post` (
  `postid` int(10) unsigned auto_increment NOT NULL primary key,
  `title` varchar(256),
  `date_posted` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `content` text NOT NULL,
  `user_id` int(10) unsigned NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

insert into Post(title, content, user_id) values('글1', '이것은 글입니다', 1);
insert into Post(title, content, user_id) values('글2', '이것은 글2입니다', 1);
insert into Post(postid,title, content, user_id) values(3,'글3', '이것은 글2입니다', 1);

create table Checklist (
	id int unsigned auto_increment primary key,
    user_id int unsigned not null,
    checklist varchar(256)
);

select * from Checklist;