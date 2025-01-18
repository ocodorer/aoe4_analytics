# aoe4_analytics
A repository for digestion AoE4 World replay files into datasets for analysis. 

## Features
* Parses manually downloaded game files and processes them using python. 
* Stores data in bronze-silver-gold sqlite databases.
* Defines databases using SQLAlchemy for porting to proper database. 
* Exports data to csv
* Uses a simple Kimball model for data analytics. 
* Optimized for use in PowerBI. 

## The medallion model
* Staging: in this layer the data is stored in raw format. 
* Bronze: in this layer the data is ingested and stored in raw format into a database system.
* Silver: in this layer the data is loaded from bronze and refined. Column names are normalized and some automated flatten/explode of structs/dicts/nested data is done. 
* Gold: the kimbal layer, a fact table with transactions and lots of dimensions. The tables are linked together using surrogate keys (generated integer keys)
* Export: for easier usage, the data is exported as CSV.  

## Kimball
Kimball is a classic way of modelling data. 
* Fact: a transactional table with balance changes and timestamps. The table has lots of columns with keys to dimensions. Tend to have few columns where all columns only contain integers and some decimal values. A transactional value can be that the amount of units with ID 5 was reduced by count 1 at game second 2332.
* Dimension: a support table, where all the values are stored in plain, e.g. unit names and unit stats. 