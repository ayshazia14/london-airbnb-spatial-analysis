# Airbnb Distribution and Transport Infrastructure in London
### MSc Data Science & AI — University of Liverpool

A geospatial analysis of London's short-term rental market, examining how Airbnb listing density relates to TfL transport infrastructure across all 32 London Boroughs. The project progresses from static choropleth maps to a live, API-driven interactive map.

---

## Overview

This project investigates the spatial logic of Airbnb's presence in Greater London, arguing that listing density is not random but closely mirrors the city's transit network. By combining borough-level census boundaries, Inside Airbnb listings data, and live TfL API station data, the analysis builds a multi-layered geospatial picture of how platform-economy housing intersects with urban infrastructure.

---

## Research Question

> To what extent does London's Airbnb market cluster around Tube and metro stations, and what does this reveal about how transit accessibility drives short-term rental density?

---

## Data Sources

| Dataset | Source | Description |
|---|---|---|
| Airbnb listings | [Inside Airbnb](http://insideairbnb.com) | `listings.csv` — full London listings with coordinates and room type |
| Borough boundaries | [London Datastore](https://data.london.gov.uk) | `London_Borough_Excluding_MHW.shp` — ESRI Shapefile (EPSG:27700) |
| TfL station locations | [TfL Unified API](https://api.tfl.gov.uk) | Live JSON — all NaptanMetroStation stop points |

> **Note:** Update the file paths in the notebook to match your local directory before running.

---

## Workflow

1. Load London borough boundaries (Shapefile) and reproject to EPSG:3857
2. Load Airbnb listings CSV and filter to `Entire home/apt` room type
3. Spatial join: aggregate listing counts per borough using GeoPandas
4. Produce a **static choropleth map** of listing density by borough
5. Fetch live TfL station data via the TfL Unified API (`/StopPoint/Type/NaptanMetroStation`)
6. Parse API response into a GeoDataFrame of station point geometries
7. Overlay Thames River geometry (via OSMnx) for cartographic context
8. Build an **interactive Folium map** with:
   - Choropleth layer for Airbnb density by borough
   - MarkerCluster layer for individual listings
   - TfL station markers
   - Spatial join linking listings and stations to boroughs

---

## Key Findings

- Airbnb listings cluster heavily around Tube stations, particularly in inner London boroughs (Westminster, Tower Hamlets, Southwark, Camden)
- Transit accessibility is the primary spatial predictor of short-term rental density
- The relationship between infrastructure and listing density reflects the platformisation of urban housing markets, consistent with Cocola-Gant (2018) and Gurran & Phibbs (2017)

---

## Technologies Used

- Python
- pandas, NumPy
- GeoPandas
- matplotlib, seaborn
- contextily (basemap tiles)
- OSMnx (OpenStreetMap features)
- Folium (interactive mapping)
- requests (TfL API)
- Shapely

---

## How to Run

1. Download the Inside Airbnb `listings.csv` for London from [insideairbnb.com](http://insideairbnb.com/get-the-data/)
2. Download the London Borough Shapefile from [London Datastore](https://data.london.gov.uk/dataset/statistical-gis-boundary-files-london)
3. Update the file paths in the notebook:
   ```python
   path = 'path/to/London_Borough_Excluding_MHW.shp'
   df_airbnb = pd.read_csv('path/to/listings.csv')
   ```
4. Install dependencies and run:
   ```bash
   pip install pandas numpy geopandas matplotlib seaborn contextily osmnx folium shapely requests
   jupyter notebook Assignment_1.ipynb
   ```

> An active internet connection is required for the TfL API call and basemap tiles.

---

## References

- Adamiak, C. (2018). Mapping Airbnb supply in European cities. *Annals of Tourism Research*, 71, 67–70.
- Cocola-Gant, A. (2018). Tourism gentrification. *Handbook of Gentrification Studies*. Edward Elgar.
- Gurran, N. & Phibbs, P. (2017). When tourists move in: How should urban planners respond to Airbnb? *Journal of the American Planning Association*, 83(1), 80–92.
- Guttentag, D. (2015). Airbnb: disruptive innovation and the rise of the informal tourism accommodation sector. *Current Issues in Tourism*, 18(12), 1192–1217.
