---------- Populate Role entries start -------------------

insert into role(id,rolename) values(1,'Patient');
insert into role(id,rolename) values(2,'Doctor');
insert into role(id,rolename) values(3,'Insurance Provider');


---------- Populate Role entries end -------------------


---------- Populate User entries start -----------------

delete from public.user;

insert into public.user(id,password,first_name,last_name,email,role_id)
values(1,'qwerty','Patient1','Pat1','patient1@gmail.com',1);
insert into public.user(id,password,first_name,last_name,email,role_id)
values(2,'qwerty','Patient2','Pat2','patient2@gmail.com',1);
insert into public.user(id,password,first_name,last_name,email,role_id)
values(3,'qwerty','Patient3','Pat3','patient3@gmail.com',1);
insert into public.user(id,password,first_name,last_name,email,role_id)
values(4,'qwerty','Patient4','Pat4','patient4@gmail.com',1);
insert into public.user(id,password,first_name,last_name,email,role_id)
values(5,'qwerty','Patient5','Pat5','patient5@gmail.com',1);
insert into public.user(id,password,first_name,last_name,email,role_id)
values(6,'qwerty','Patient6','Pat6','patient6@gmail.com',1);

insert into public.user(id,password,first_name,last_name,email,role_id)
values(7,'qwerty','Doctor1','Doc1','doctor1@gmail.com',2);
insert into public.user(id,password,first_name,last_name,email,role_id)
values(8,'qwerty','Doctor2','Doc2','doctor2@gmail.com',2);
insert into public.user(id,password,first_name,last_name,email,role_id)
values(9,'qwerty','Doctor3','Doc3','doctor3@gmail.com',2);
insert into public.user(id,password,first_name,last_name,email,role_id)
values(10,'qwerty','Doctor4','Doc4','doctor4@gmail.com',2);
insert into public.user(id,password,first_name,last_name,email,role_id)
values(11,'qwerty','Doctor5','Doc5','doctor5@gmail.com',2);
insert into public.user(id,password,first_name,last_name,email,role_id)
values(12,'qwerty','Doctor6','Doc6','doctor6@gmail.com',2);

------------ Populate User entrie end ---------------------



---------- Populate Doctor entries start -------------------
delete from doctor 
insert into doctor(id,hospital_id,fees,provide_covid_care) values ('7',1,20,TRUE);
insert into doctor(id,hospital_id,fees,provide_covid_care) values ('8',1,40,FALSE);
insert into doctor(id,hospital_id,fees,provide_covid_care) values ('9',2,60,TRUE);
insert into doctor(id,hospital_id,fees,provide_covid_care) values ('10',2,40,TRUE);
insert into doctor(id,hospital_id,fees,provide_covid_care) values ('11',3,50,FALSE);
insert into doctor(id,hospital_id,fees,provide_covid_care) values ('12',4,70,TRUE);

---------- Populate Doctor entries end -------------------

---------- Populate Hospital entries start -------------------

delete from hospital
insert into hospital(id,name,location,no_of_covid_beds) 
values(1,'IU Health Bloomington Hospital','Bloomington',10)
insert into hospital(id,name,location,no_of_covid_beds) 
values(2,'Harrison County Hospital','Corydon',15)
insert into hospital(id,name,location,no_of_covid_beds) 
values(3,'Johnson Memorial Health','Franklin',10)
insert into hospital(id,name,location,no_of_covid_beds) 
values(4,'Monroe Hospital','Bloomington',10)


---------- Populate Hospital entries end -------------------


---------- Populate Doctor disease entries start -------------------

delete from doctor_disease;

insert into doctor_disease(doctor_id,disease_id) values(7,1);
insert into doctor_disease(doctor_id,disease_id) values(7,2);
insert into doctor_disease(doctor_id,disease_id) values(7,3);
insert into doctor_disease(doctor_id,disease_id) values(7,4);
insert into doctor_disease(doctor_id,disease_id) values(7,5);
insert into doctor_disease(doctor_id,disease_id) values(7,6);


insert into doctor_disease(doctor_id,disease_id) values(8,1);
insert into doctor_disease(doctor_id,disease_id) values(8,3);
insert into doctor_disease(doctor_id,disease_id) values(8,5);

insert into doctor_disease(doctor_id,disease_id) values(9,2);
insert into doctor_disease(doctor_id,disease_id) values(9,4);
insert into doctor_disease(doctor_id,disease_id) values(9,6);


insert into doctor_disease(doctor_id,disease_id) values(10,1);
insert into doctor_disease(doctor_id,disease_id) values(10,2);
insert into doctor_disease(doctor_id,disease_id) values(10,3);
insert into doctor_disease(doctor_id,disease_id) values(10,4);


insert into doctor_disease(doctor_id,disease_id) values(11,5);
insert into doctor_disease(doctor_id,disease_id) values(11,6);

insert into doctor_disease(doctor_id,disease_id) values(12,1);
insert into doctor_disease(doctor_id,disease_id) values(12,2);
insert into doctor_disease(doctor_id,disease_id) values(12,3);
insert into doctor_disease(doctor_id,disease_id) values(12,4);


---------- Populate Doctor disease entries end -------------------


---------- Disease entries start -----------------------

delete from disease;
insert into disease(id,name) values(1,'Allergies');
insert into disease(id,name) values(2,'Colds and Flu');
insert into disease(id,name) values(3,'Conjunctivitis');
insert into disease(id,name) values(4,'Diarrhea');
insert into disease(id,name) values(5,'Headaches');
insert into disease(id,name) values(6,'Stomach Aches');
								   


---------- Disease entires end -------------------------



---------- Misc queries for testing ----------------

select * from curebox_user 

select * from user 

select * from doctor_specialization

select * from booking


select * from hospital
select * from doctor

select distinct h.location 
from hospital h join doctor d on h.id = d.hospital_id
order by 1

select distinct doc.fees , u.name 
from doctor_disease dd natural join doctor doc natural join curebox_user u , hospital h where  UPPER(u.name) like UPPER('doctor1')
and dd.disease_id = (select disease_id from disease d where d.name = 'Colds and Flu')
and doc.provide_covid_care = true
and doc.hospital_id = h.id and h.location = 'Bloomington'

select * from doctor_disease dd
where dd.disease_id = (select d.id from disease d where d.name = 'Colds and Flu') ;

select distinct doc.fees , u.name 
from doctor_disease dd natural join doctor doc natural join curebox_user u , hospital h where 
1 = 1 and
dd.doctor_id = doc.id and dd.disease_id = (select d.id from disease d where d.name = 'Colds and Flu') ;


select * from doctor 

select distinct doc.fees , u.name
from doctor_disease dd natural join doctor doc natural join curebox_user u , hospital h 
where 1 = 1 and dd.doctor_id = doc.id 
and dd.disease_id = (select disease_id from disease d where d.name = 'Colds and Flu')
and doc.hospital_id = h.id and h.location = 'Bloomington'*/





---- ADT Queries -----

-- Contributed by Vaibhavi Patel

CREATE TABLE netflix_data (
    show_id     varchar(20) PRIMARY KEY,
    show_type   varchar(20),
    title       varchar(500),
    director    varchar(500),
    actor       varchar(1000),
    country      varchar(500),
	date_added   varchar(50),
	release_year varchar(50),
	rating       varchar(50),
	duration     varchar(50),
	listed_in    varchar(500),
	description  varchar(1000)
);

-- import data from csv file manually by right clicking on table name -> import

select * from netflix_data;

-- Normalizing table 

-- Contributed by Shambhavi Shukla

-- Creating main table netflix 

drop table netflix;
CREATE TABLE netflix (
    show_id     varchar(50) PRIMARY KEY,
    show_type   varchar(20),
    title       varchar(500),
    date_added   date ,
	release_year integer,
	rating       varchar(50),
	duration     varchar(50),
	description  varchar(1000));


INSERT INTO netflix (show_id, show_type, title, date_added, release_year, rating, duration, description)
SELECT show_id, show_type, title, TO_DATE(date_added, 'Month DD, YYYY'), cast(release_year as integer), rating, duration, description
FROM netflix_data;

select * from netflix;

-- Contributed by Vaibhavi Patel

drop table if exists actor ; 
-- Creating actor table
CREATE TABLE actor(show_id varchar(50) NOT NULL,
	              actor_name varchar(1000),    
				  primary key(show_id,actor_name),   
                  foreign key(show_id) references netflix(show_id));

INSERT INTO actor (show_id, actor_name)
SELECT show_id, TRIM(unnest(string_to_array(actor, ','))) AS actor_name
FROM netflix_data
GROUP BY show_id, actor_name;

select * from actor ;

-- Contributed by Shambhavi Shukla

-- Creating director table 

drop table if exists director;
CREATE TABLE director(show_id varchar(50) NOT NULL,
	              director_name varchar(100),
				  primary key(show_id,director_name),
                  foreign key(show_id) references netflix(show_id));

INSERT INTO director (show_id, director_name)
SELECT show_id, TRIM(unnest(string_to_array(director, ','))) AS director_name
FROM netflix_data
GROUP BY show_id, director_name;

select * from director ;

-- Contributed by Vaibhavi Patel

-- Creating country table 
drop table if exists country; 
CREATE TABLE country(show_id varchar(50) NOT NULL,
	              country_name varchar(100), 
				  primary key(show_id,country_name),
                  foreign key(show_id) references netflix(show_id));

INSERT INTO country (show_id, country_name)
SELECT show_id, TRIM(unnest(string_to_array(country, ','))) AS country_name
FROM netflix_data
GROUP BY show_id, country_name;

select * from country ;

-- Contributed by Shambhavi Shukla

-- Creating genres table 

CREATE TABLE genres (
  genre_id SERIAL PRIMARY KEY,
  genre VARCHAR(255) UNIQUE
);

INSERT INTO genres (genre)
SELECT DISTINCT TRIM(unnest(string_to_array(listed_in, ','))) AS genre FROM netflix_data;

select * from genres;

-- create show_genre_view

create or replace view show_genre_view as (

SELECT show_id, TRIM(unnest(string_to_array(listed_in, ','))) AS genre
FROM netflix_data
GROUP BY show_id, genre
);

select * from show_genre_view ;


-- create show_genre table
drop table if exists show_genre;
CREATE TABLE show_genre(show_id varchar(50) NOT NULL,
	              genre_id integer,    
				  primary key(show_id,genre_id),		
                  foreign key(show_id) references netflix(show_id),
				  foreign key(genre_id) references genres(genre_id));

INSERT INTO show_genre (show_id, genre_id)
SELECT s.show_id, g.genre_id
FROM show_genre_view s, genres g 
where g.genre = s.genre
GROUP BY s.show_id,g.genre_id;

select * from show_genre;

-- Queries to be used in our application ( We plan to develop a search functionality with different attributes to 
-- be used as filter criteria )

-- Find distinct genres to show it in Genre filter drop down on our web page

-- Contributed by Vaibhavi Patel

select distinct genre
from show_genre_view;

-- Find movies from specific country which will pass as a parameter from our web app

select title 
from netflix n join country c
on n.show_id = c.show_id 
where c.country_name = 'United States'
and n.show_type = 'Movie';

-- Contibuted by Shambhavi Shkula

-- Find distinct directors from netflix_data
select distinct director_name
from director;
-- Find count of Tv shows produced in India 

select count(*)
from netflix n join country c 
on n.show_id = c.show_id 
where c.country_name = 'India' 
and n.show_type = 'TV Show';