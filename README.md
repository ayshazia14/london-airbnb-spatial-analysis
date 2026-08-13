# London Airbnb Distribution & Transit Density Analytics Engine

A geospatial data pipeline and interactive analytics web application examining the relationship between public transit accessibility and short-term rental distribution across all 32 London boroughs. 

This system integrates census boundaries, large-scale accommodation data, and live transit data streams to model how platform-economy housing intersects with critical urban infrastructure.

---

## Core Objectives

- **Spatial Correlation:** Examine the relationship between transit accessibility and short-term rental supply across London boroughs.
- **Data Pipeline Engineering:** Construct an end-to-end workflow to ingest, reproject, and clean disparate tabular and geospatial datasets.
- **Interactive Delivery:** Build an interactive mapping dashboard integrating TfL transit data, dynamic marker clustering, and layered geospatial visualisations.

---

## Data Infrastructure & Lineage

| Component / Dataset | Source | Technical Format / Protocol |
|---|---|---|
| **Airbnb Market Listings** | [Inside Airbnb](http://insideairbnb.com) | `listings.csv` — Full geospatial point data with attributes |
| **Borough Census Boundaries** | [London Datastore](https://data.london.gov.uk) | ESRI Shapefile — Local Coordinate System (`EPSG:27700`) |
| **TfL Station Locations** | [TfL Unified API](https://api.tfl.gov.uk) | Live JSON Stream — `/StopPoint/Type/NaptanMetroStation` |

---

## System Architecture & Workflow

1. **Geospatial Ingestion & ETL:** Load vector boundary shapefiles and reproject geometries to Web Mercator (`EPSG:3857`) for accurate web-mapping alignment.
2. **Tabular Feature Engineering:** Ingest and isolate massive accommodation records, filtering for specific supply types (`Entire home/apt`).
3. **Geometric Spatial Joins:** Execute vectorized spatial joins via `GeoPandas` to aggregate and index point-in-polygon listing counts per administrative borough.
4. **Asynchronous API Integration:** Query the Transport for London (TfL) Unified API programmatically, parsing JSON payloads into real-time coordinate geometries.
5. **Contextual Hydrographic Layering:** Programmatically extract the River Thames geometry via `OSMnx` from OpenStreetMap for advanced cartographic context.
6. **Interactive Visualization Layer:** Render a multi-layered dashboard featuring:
   - Dynamic choropleth overlays mapping borough-wide density gradients.
   - Asynchronous `MarkerCluster` objects managing localized point distribution.
   - Live TfL transit nodes overlaid on high-contrast basemap tiles.

---

## Key Analytical Insights

- **Infrastructure Clustering:** Short-term accommodation listings are concentrated in inner London boroughs, particularly Westminster, Tower Hamlets, Southwark, and Camden, which also contain major public transport hubs.
- **Predictive Power:** Areas with greater public transit accessibility show higher concentrations of short-term rental listings, indicating a strong spatial association between transport infrastructure and Airbnb supply.
- **Urban Impact:** The observed concentration of short-term rentals around well-connected areas provides insight into how platform-based accommodation interacts with London's existing transport and housing infrastructure.

---

## Toolchain & Tech Stack

* **Core Language:** Python
* **Data Engineering:** `pandas`, `NumPy`
* **Geospatial Processing:** `GeoPandas`, `Shapely`, `OSMnx`
* **API Ingestion:** `requests` (TfL Unified API Gateway)
* **Visualization Engine:** `Folium` (Leaflet.js wrapper), `matplotlib`, `seaborn`, `contextily`
* **Application Framework:** `Streamlit`

---

## Deployment & Local Execution

This application is deployed on **Streamlit Community Cloud**.

**[View the Live Dashboard](https://london-airbnb-spatial-analysis.streamlit.app/)**

### Run Locally

1. **Clone the repository:**

```bash
git clone https://github.com/ayshazia14/london-airbnb-spatial-analysis.git
cd london-airbnb-spatial-analysis
