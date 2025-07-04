<script>

export const DEFAULT_QUERIES = [
    {
        desc: "From condo name, get avg PSFs",
        query: `
WITH normalized AS (
    SELECT
        project_name, 
        price, 
        psf, 
        sale_date, 
        sale_type, 
        floor_level,
        CASE 
            WHEN area < 600 THEN '599 and below'
            WHEN area < 700 THEN '600 to 699'
            WHEN area <  800 THEN '700 to 799'
            WHEN area < 900 THEN '800 to 899'
            WHEN area < 1000 THEN '900 to 999'
            ELSE 'more than 1000'
        END as area,
        num_units,
        top,
        developer
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
    ROUND(AVG(psf)) AS avg_psf,
    COUNT(*) AS num_transactions,
    MIN(num_units) AS num_units,
    MIN(top) AS top,
    MIN(developer) AS developer
FROM
    normalized
GROUP BY
    YEAR(sale_date), floor_level, area
ORDER BY
    YEAR(sale_date) DESC, floor_level, area
LIMIT 100
`
    },
    {
        desc: "From MRTs, get avg PSF of nearby projects",
        query: `
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
LIMIT 100
`
    },
    {
        desc: "From condo name, get nearby facilities",
        query: `
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
LIMIT 100
`
    },
    {
        desc: "From condo name, get transactions",
        query: `
SELECT
    project_name,
    price,
    area,
    psf,
    YEAR(sale_date) AS year,
    MONTH(sale_date) AS month,
    sale_type,
    floor_level,
    tenure,
    postal_district,
    market_segment,
    top,
    developer
FROM
    read_csv_auto('projects.csv') projects
    LEFT JOIN read_csv_auto('sales.csv') sales
    ON projects.id = sales.project_id
WHERE
    project_name = 'the luxurie'
ORDER BY 
    sale_date DESC
LIMIT 100
    `
    }
]

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