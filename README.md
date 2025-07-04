# Sg-condos

Link: https://condo-db-sg.netlify.app

# Summary

A simple project that:
- collects historical condo data in Singapore
- cleans and augments it (eg. latitude/longitude/num_nuits/top/developer/facilties)
- splits it into 3 related SQL tables
- exposes it to the public to query using SQL using Vue

# How to use
- go to `https://condo-db-sg.netlify.app`
- use SQL to query historical condo data
- done

# General FAQ

| Question | Answer |
| --- | --- |
| why did you create this project? | my GF and I were looking for condos, and existing historical condo data sources were annoying to use |
| why are you exposing this to the public? | I'll be sad if my hard works simply goes into the project graveyard |
| do you earn money from this? | no |
| how does the site work? | Vue 3 + duckdb magic. Note that there's no backend, and the data is served through static CSV files |
| how often is data updated? | probably every month or so |

# The data schema

3 tables:
1) sales - each row == one transaction of 1 unit in a condo projecr
2) projects - each row == one condo project 
3) projects_facilities_assoc == relation between (condo, facility)

Sales:

| Column | Description |
| --- | --- |
| id | autoincrement unique identifier |
| price | price in SGD that unit was sold at |
| area | area in square feet of unit | 
| psf | price per square foot |
| sale_date | sale date | 
| sale_type | new sale, resale or subsale |
| floor_level | floor level |
| project_id | id of condo project. foreign key to projects(id) |

Projects:

| Column | Description |
| --- | --- |
| id | autoincrement unique identiier |
| project_name | name of condo project |
| street_name | name of street | 
| area_type | strata or land |
| property_type | Apartment or Condominium |
| tenure | freehold, 99 ie how long before ah gong takes back your property |
| tenure_start | year that tenure starts |
| postal_district | 1 to 28 |
| market_segment | CCR, RCR, or OCR |
| latitude | latitude |
| longitude | longitude |
| num_units | total number of units in project | 
| top | year project is finished |
| developer | name of developer |

Project_facilities_assoc:

| Column | Description |
| --- | --- |
| project_id | id of project. foreign key to projects(id) |
| facility_name | name of facility |
| facility_type | mrt, school or mall |
| dist_meters | distance to facility in meters |

# FAQ on data

How is the data collected:
- transaction data from URA's official site
- (latitude, longitude) data from onemap free api
- condo project info (eg. num_nuits, top, developer) from 99.co

Tech used for data: Python | Selenium | OneMap API | Airflow | Pandas | SQL

Tech used for site: Vue | DuckDB | Netlify

# Even More FAQ

| Question | Answer |
| --- | --- |
| Is the data 100% accurate? | probably not as I can't verify 2000+ condo projects manually. Do lmk if data is screwed up |
| There's no data before 2020? | URA only has past 5 years worth of data + I don't think data older than 5 years old is that useful |
| Why is there no HDB data? | not my priority |
| Why is there no landed data? | not my priority |
| Why is there no commercial data? | not my priority |
| Frontend code is bad | not my priority |
| CSS is really bad | not my priority |
| My condo is missing? | data is collected on a best-effort basis |