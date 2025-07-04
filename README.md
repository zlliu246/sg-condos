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
| is the data 100% accurate? | probably not as I can't verify 2000+ condo projects manually. Do lmk if data is screwed up |

# The data
placeholder
