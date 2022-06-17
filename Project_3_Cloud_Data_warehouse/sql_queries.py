import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')
ARN = config.get("IAM_ROLE", "ARN")
LOG_DATA = config.get("S3", "LOG_DATA")
LOG_JSONPATH = config.get("S3", "LOG_JSONPATH")
SONG_DATA = config.get("S3", "SONG_DATA")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay "
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE  IF NOT EXISTS staging_events(
        artist VARCHAR,
        auth VARCHAR,
        firstName VARCHAR,
        gender CHAR(1),
        itemInSession INT,
        lastName VARCHAR,
        length FLOAT,
        level VARCHAR,
        location TEXT,
        method VARCHAR,
        page VARCHAR,
        registration VARCHAR,
        sessionId INT,
        song VARCHAR,
        status INT,
        ts BIGINT,
        userAgent TEXT,
        userId INT
)

""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
        artist_id VARCHAR,
        artist_latitude FLOAT,
        artist_location TEXT,
        artist_longitude FLOAT,
        artist_name VARCHAR,
        duration FLOAT,
        num_songs INT,
        song_id VARCHAR,
        title VARCHAR,
        year INT

)
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
songplay_id IDENTITY(0,1) PRIMARY KEY,
start_time TIMESTAMP NOT NULL,
user_id INT NOT NULL,
level VARCHAR NOT NULL,
song_id VARCHAR,
artist_id VARCHAR,
session_id INT NOT NULL,
location VARCHAR NOT NULL,
user_agent VARCHAR NOT NULL

)
""")

user_table_create = ("""
CREATE TABLE IF NOT EXITS users (
user_id INT PRIMARY KEY,
first_name VARCHAR,
last_name VARCHAR,
gender VARCHAR,
level VARCHAR
)
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
song_id VARCHAR PRIMARY KEY,
title VARCHAR NOT NULL,
artist_id VARCHAR,
year INT,
duration NUMERIC NOT NULL
)
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists(
artist_id VARCHAR PRIMARY KEY,
name VARCHAR NOT NULL,
location VARCHAR,
latitude DOUBLE PRECISION,
longitude DOUBLE PRECISION

)
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
start_time TIMESTAMP PRIMARY KEY,
hour INT,
day INT,
week INT,
month INT, 
year INT, 
weekday VARCHAR
)
""")

# STAGING TABLES

staging_events_copy = ("""
copy staging_events from 's3://udacity-dend/log_data'
    credentials 'aws_iam_role={}'
    gzip delimiter ';' compupdate off region 'us-west-2';
""").format(LOG_DATA, ARN, LOG_JSONPATH)

staging_songs_copy = ("""
copy staging_songs from 's3://udacity-dend/song_data'
    credentials 'aws_iam_role={}'
    gzip delimiter ';' compupdate off region 'us-west-2';
""").format(SONG_DATA, ARN)

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT DISTINCT 
    se.ts,
    se.userId,
    se.level,
    ss.song_id,
    ss.artist_id,
    se.sessionId,
    se.location,
    se.userAgent
FROM staging_events se
INNER JOIN staging_songs ss
    ON se.song = ss.title
WHERE se.page = 'NextSong';
""")

user_table_insert = ("""
INSERT INTO users(user_id, first_name, last_name, gender, level )
SELECT DISTINCT
    se.userId,
    se.firstName,
    se.lastName,
    se.gender,
    se.level
FROM staging_events se
WHERE se.userId IS NOT NULL;
""")

song_table_insert = ("""
INSERT INTO songs (song_id, title, artist_id, year, duration)
SELECT DISTINCT
    ss.song_id,
    ss.title,
    ss.artist_id,
    ss.year,
    ss.duration
FROM staging_songs ss;
""")

artist_table_insert = ("""
INSERT INTO
artists (artist_id, name, location, latitude, longitude)
SELECT DISTINCT
    ss.artist_id,
    ss.artist_name,
    ss.artist_latitude,
    ss.artist_longitude,
    CASE WHEN 
        ss.artist_location IS NOT NULL 
        AND ss.artist_location != '' 
    THEN ss.artist_location else 'N/A' END 
FROM staging_songs ss
WHERE ss.artist_id IS NOT NULL;
""")

time_table_insert = ("""
INSERT INTO
time (start_time, hour, day, week, month, year, weekday)
SELECT DISTINCT
    se.ts,
    CAST(DATE_PART('hour',  se.ts) as INT),
    CAST(DATE_PART('day',   se.ts) as INT),
    CAST(DATE_PART('week',  se.ts) as INT),
    CAST(DATE_PART('month', se.ts) as INT),
    CAST(DATE_PART('year',  se.ts) as INT),
    CAST(DATE_PART('dow',   se.ts) as INT)
FROM staging_events se
WHERE se.page = 'NextSong';
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]