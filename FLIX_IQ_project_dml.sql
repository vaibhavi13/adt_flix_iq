---------- Populate User entries start -----------------

---- Flix IQ Queries -----

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

-- create table ratings
drop table if exists ratings; 

CREATE TABLE ratings (
  rating_id SERIAL PRIMARY KEY,
  rating_name VARCHAR(255) UNIQUE
);

INSERT INTO ratings (rating_name)
select distinct rating from netflix;

select * from ratings;

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