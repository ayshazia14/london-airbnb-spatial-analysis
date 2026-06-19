# 📍 London Airbnb Distribution & Transit Density Analytics Engine

A production-ready geospatial data pipeline and interactive analytics web application examining how public transit accessibility drives short-term rental clustering across all 32 London Boroughs. 

This system integrates census boundaries, large-scale accommodation data, and live transit data streams to model how platform-economy housing intersects with critical urban infrastructure.

---

## 🚀 Core Objectives

- **Spatial Correlation:** Model the relationship between high-density transit hubs and short-term rental supply in Greater London.
- **Data Pipeline Engineering:** Construct an end-to-end workflow to ingest, reproject, and clean disparate tabular and geospatial datasets.
- **Interactive Delivery:** Deploy a live, scalable mapping dashboard utilizing asynchronous API streams and dynamic marker clustering for end-user analysis.

---

## 📊 Data Infrastructure & Lineage

| Component / Dataset | Source | Technical Format / Protocol |
|---|---|---|
| **Airbnb Market Listings** | [Inside Airbnb](http://insideairbnb.com) | `listings.csv` — Full geospatial point data with attributes |
| **Borough Census Boundaries** | [London Datastore](https://data.london.gov.uk) | ESRI Shapefile — Local Coordinate System (`EPSG:27700`) |
| **TfL Station Locations** | [TfL Unified API](https://api.tfl.gov.uk) | Live JSON Stream — `/StopPoint/Type/NaptanMetroStation` |

---

## ⚙️ System Architecture & Workflow

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

## 💡 Key Analytical Insights

- **Infrastructure Clustering:** Short-term accommodations cluster exponentially around Tier-1 transit nodes, heavily concentrated in inner London economic corridors (Westminster, Tower Hamlets, Southwark, Camden).
- **Predictive Power:** Transit accessibility serves as the primary spatial and economic predictor of rental inventory volume.
- **Urban Impact:** The direct correlation between public infrastructure and platform supply reflects a profound structural platformisation of urban housing markets, matching frameworks established by Cocola-Gant (2018).

---

## 🛠️ Toolchain & Tech Stack

* **Core Language:** Python
* **Data Engineering:** `pandas`, `NumPy`
* **Geospatial Processing:** `GeoPandas`, `Shapely`, `OSMnx`
* **API Ingestion:** `requests` (TfL Unified API Gateway)
* **Visualization Engine:** `Folium` (Leaflet.js wrapper), `matplotlib`, `seaborn`, `contextily`
* **Application Framework:** `Streamlit`

---

## 💻 Deployment & Local Execution

This application is deployed and available via **Streamlit Community Cloud** [Insert your live app URL link here!].

To spin up the environment and run the pipelines locally:

1. Clone the repository:
```bash
   git clone [https://github.com/ayshazia14/london-airbnb-spatial-analysis.git](https://github.com/ayshazia14/london-airbnb-spatial-analysis.git)
   cd london-airbnb-spatial-analysis
