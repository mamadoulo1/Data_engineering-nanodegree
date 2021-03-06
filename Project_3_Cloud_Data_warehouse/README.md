<h1>Project: Cloud Data Warehouse</h1>

<h3>Introduction</h3>
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.
As their data engineer,  i'm tasked with building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights into what songs their users are listening to. I'll test my database and ETL pipeline by running queries given to me by the analytics team from Sparkify and compare my results with the expected results.

<h3>Project Description</h3>
In this project, i'll apply what i've learned on data warehouses and AWS to build an ETL pipeline for a database hosted on Redshift. To complete the project, i will need to load data from S3 to staging tables on Redshift and execute SQL statements that create the analytics tables from these staging tables.

<h3>Song Dataset</h3>
The first dataset is a subset of real data from the Million Song Dataset. Each file is in JSON format and contains metadata about a song and the artist of that song. The files are partitioned by the first three letters of each song's track ID. For example, here are file paths to two files in this dataset.

<h3>Log Dataset</h3>
The second dataset consists of log files in JSON format generated by this event simulator based on the songs in the dataset above. These simulate activity logs from a music streaming app based on specified configurations.
The log files in the dataset are partitioned by year and month. 


<h3>Schema for Song Play Analysis</h3>
Using the song and log datasets, we need to create a star schema optimized for queries on song play analysis. This includes the following tables.
<h5>Fact Table</h5>
<ul>
  <li>songplays - records in log data associated with song plays i.e. records with page NextSong <br>
    (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    </li>
</ul>
 
<h5>Dimension Tables</h5>

<ul>
  <li>users - users in the app<br>
    (user_id, first_name, last_name, gender, level)
    </li>
  <li>songs - songs in music database <br>
    (song_id, title, artist_id, year, duration)
    </li>
  <li>artists - artists in music database <br>
    (artist_id, name, location, latitude, longitude)
    </li>
  <li>time - timestamps of records in songplays broken down into specific units <br>
    (start_time, hour, day, week, month, year, weekday)
    </li>
</ul> 



<h3>Project files</h3>
<ol>
 
  <li>create_tables.py is where i'll create the fact and dimension tables for the star schema in Redshift.</li>
  <li>etl.py is where i'll load data from S3 into staging tables on Redshift and then process that data into my analytics tables on Redshift.</li>
  <li>sql_queries.py  is where i'll define SQL statements, which will be imported into the two other files above.</li>
    <li>README.md provides an introduction on the project.</li>
</ol> 


<h3>Project Steps</h3>
<h4>Create Table Schemas</h4>
Below are steps that we follow to realize the project:
<ol>
  <li>Design schemas for your fact and dimension tables </li> 
  <li>Write a SQL CREATE statement for each of these tables in sql_queries.py</li>
  <li>Complete the logic in create_tables.py to connect to the database and create these tables</li>
  <li>Write SQL DROP statements to drop tables in the beginning of create_tables.py if the tables already exist. </li>
  <li>Launch a redshift cluster and create an IAM role that has read access to S3.</li>
    <li>Add redshift database and IAM role info to dwh.cfg.</li>
    <li>Test by running create_tables.py and checking the table schemas in your redshift database.</li>
</ol> 

<h4>Build ETL Pipeline</h4>
<li>Implement the logic in etl.py to load data from S3 to staging tables on Redshift.</li>
<li>Implement the logic in etl.py to load data from staging tables to analytics tables on Redshift.</li>
<li>Test by running etl.py after running create_tables.py and running the analytic queries on your Redshift database to compare the results with the expected results.</li>
<li>Delete your redshift cluster when finished.</li>
