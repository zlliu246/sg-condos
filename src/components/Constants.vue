<script>

const SALES_QUERY = `
SELECT
    *
FROM
    read_csv_auto('sales.csv')
LIMIT 5
`

const PROJECTS_QUERY = `
SELECT 
    *
FROM
    read_csv_auto('projects.csv')
LIMIT 5
`

const PROJECT_FACILITIES_ASSOC_QUERY = `
SELECT
    *
FROM
    read_csv_auto('projects_facilities_assoc.csv')
LIMIT 5
`

const AVG_PSF_BY_MRT_QUERY = `
SELECT
    MIN(project_name) AS project_name,
    floor_level,
    YEAR(sale_date) AS year,
    ROUND(AVG(psf)) AS avg_psf,
    MIN(top) AS top,
    MIN(num_units) AS num_units,
    MIN(dist_meters) AS dist_from_mrt
FROM 
    read_csv_auto('sales.csv') sales
    LEFT JOIN read_csv_auto('projects.csv') projects
    ON sales.project_id = projects.id
    LEFT JOIN read_csv_auto('projects_facilities_assoc.csv') faci
    ON projects.id = faci.project_id
WHERE 
    facility_name IN ('serangoon mrt', 'kovan mrt')
    AND YEAR(sale_date) >= 2024
    AND area >= 650
    AND area <= 800
    AND floor_level != '01 to 05'
GROUP BY
    sales.project_id, floor_level, YEAR(sale_date)
ORDER BY
    sales.project_id, floor_level, YEAR(sale_date)
`

const AVG_PSF_SPECIFIC_CONDO_QUERY = `
WITH normalized AS (
    SELECT
        project_name, price, psf, sale_date, sale_type, floor_level,
        CASE 
            WHEN area < 600 THEN '< 600'
            WHEN area < 700 THEN '600 to 699'
            WHEN area <  800 THEN '700 to 799'
            WHEN area < 900 THEN '800 to 899'
            WHEN area < 1000 THEN '900 to 999'
            ELSE '>= 1000'
        END as area
    FROM 
        read_csv_auto('sales.csv') sales
        LEFT JOIN read_csv_auto('projects.csv') projects
        ON sales.project_id = projects.id
    WHERE 
        project_name = 'forest woods'
)
SELECT
    MIN(project_name) AS project_name,
    YEAR(sale_date) AS year,
    floor_level,
    area,
    ROUND(AVG(price)) AS avg_price,
    ROUND(AVG(psf)) AS avg_psf
FROM
    normalized
GROUP BY
    YEAR(sale_date), floor_level, area
ORDER BY
    YEAR(sale_date), floor_level, area
`

const FACILITIES_NEAR_CONDO_QUERY = `
SELECT
    project_name,
    tenure,
    num_units,
    top,
    facility_name,
    facility_type,
    dist_meters
FROM
    read_csv_auto('projects.csv') projects
    LEFT JOIN read_csv_auto('projects_facilities_assoc.csv') faci
    ON projects.id = faci.project_id
WHERE
    project_name = 'the orie'
`


export const QUERY_MAP = {
    SALES: {
        desc: "5 rows from sales.csv",
        query: SALES_QUERY
    },
    PROJECTS: {
        desc: "5 rows from projects.csv",
        query: PROJECTS_QUERY
    },
    PROJECTS_FACILITIES_ASSOC: {
        desc: "5 rows in projects_facilities_assoc.csv",
        query: PROJECT_FACILITIES_ASSOC_QUERY
    },
    AVG_PSF_BY_MRT: {
        desc: "Avg PSFs of projects near certain MRTs",
        query: AVG_PSF_BY_MRT_QUERY
    },
    AVG_PSF_SPECIFIC_CONDO: {
        desc: "Avg PSFs of a specific condo",
        query: AVG_PSF_SPECIFIC_CONDO_QUERY
    },
    FACILITIES_NEAR_CONDO: {
        desc: "Facilities near specifc condo",
        query: FACILITIES_NEAR_CONDO_QUERY
    }
}

export const SCHEMA_METADATA_LIST = [
  {
    name: "sales.csv",
    desc: "each row == 1 sale",
    columns: [
      {name: "id", desc: "autoincrement unique identifier"},
      {name: "price", desc: "price unit was sold at"},
      {name: "area", desc: "area of unit in square feet (sqft)"},
      {name: "psf", desc: "price per sqft"},
      {name: "sale_date", desc: "sale date"},
      {name: "sale_type", desc: "new sale, resale or subsale"},
      {name: "floor_level", desc: "floor level"},
      {name: "project_id", desc: "foreign key to `id` in projects.csv"},
    ]
  },
  {
    name: "projects.csv",
    desc: "each row == 1 condo project",
    columns: [
      {name: "project_name", desc: "name of condo project"},
      {name: "street_name", desc: "name of street"},
      {name: "area_type", desc: "Strata, build-up or build-in"},
      {name: "property_type", desc: "Apartment or Condominium"},
      {name: "tenure", desc: "freehold, 99 etc"},
      {name: "tenure_start", desc: "which year tenure starts"},
      {name: "postal_district", desc: "1 to 28"},
      {name: "market_segment", desc: "CCR, RCR, or OCR"},
      {name: "latitude", desc: "latitude"},
      {name: "longitude", desc: "longitude"},
      {name: "num_units", desc: "number of units in project"},
      {name: "top", desc: "year finished"},
      {name: "developer", desc: "developer name"},
    ]
  },
  {
    name: "projects_facilities_assoc.csv",
    desc: "each row == one (condo, facility) relation",
    columns: [
      {name: "project_id", desc: "foregin key to `id` in projects.csv"},
      {name: "facility_name", desc: "name of facility"},
      {name: "facility_type", desc: "mrt, school or mall"},
      {name: "dist_meters", desc: "distance to facility (meters)"}
    ]
  }
]

</script>