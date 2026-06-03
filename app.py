import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import requests
import osmnx as ox

st.set_page_config(
    page_title="London Airbnb & Transit",
    page_icon="🚇",
    layout="wide"
)

# Styling 
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .title {
            font-family: 'DM Serif Display', serif;
            font-size: 2.6rem;
            line-height: 1.15;
            color: #0d0d0d;
            margin-bottom: 0.2rem;
        }
        .subtitle {
            font-size: 1rem;
            color: #555;
            font-weight: 300;
            margin-bottom: 2rem;
        }
        .stat-box {
            background: #f7f7f5;
            border-left: 3px solid #0019a8;
            padding: 1rem 1.2rem;
            border-radius: 2px;
        }
        .stat-number {
            font-family: 'DM Serif Display', serif;
            font-size: 2rem;
            color: #0019a8;
            line-height: 1;
        }
        .stat-label {
            font-size: 0.78rem;
            color: #777;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 0.3rem;
        }
        .section-label {
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #999;
            margin-bottom: 0.5rem;
        }
        hr {
            border: none;
            border-top: 1px solid #e8e8e8;
            margin: 1.5rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# Header 
st.markdown('<div class="title">Airbnb Distribution &<br>Transit Infrastructure</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Greater London · Entire-home listings vs. TfL Underground network</div>', unsafe_allow_html=True)

# data 
BOROUGH_PATH = 'statistical-gis-boundaries-london/ESRI/London_Borough_Excluding_MHW.shp'

@st.cache_data
def load_airbnb():
    df = pd.read_csv('listings.csv')
    return df[df['room_type'] == 'Entire home/apt'].copy()

@st.cache_data
def load_boroughs():
    gdf = gpd.read_file(BOROUGH_PATH)
    gdf = gdf[gdf['GSS_CODE'].str.startswith('E09')]
    gdf.loc[gdf['NAME'] == 'City of London', 'GSS_CODE'] = 'E09000001'
    return gdf.to_crs(epsg=4326)

@st.cache_data
def fetch_tube_stations():
    url = 'https://api.tfl.gov.uk/StopPoint/Type/NaptanMetroStation'
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    records = [
        {'name': s.get('commonName'), 'lat': s.get('lat'), 'lon': s.get('lon')}
        for s in r.json()
    ]
    return pd.DataFrame(records).dropna(subset=['lat', 'lon'])

@st.cache_data
def load_river():
    river = ox.features_from_place("London, UK", tags={"waterway": "river", "name": "River Thames"})
    return river.to_crs(epsg=4326)

with st.spinner('Loading data…'):
    entire_homes = load_airbnb()
    boroughs = load_boroughs()
    df_stations = fetch_tube_stations()
    river = load_river()

# Compute counts
gdf_points = gpd.GeoDataFrame(
    entire_homes,
    geometry=gpd.points_from_xy(entire_homes.longitude, entire_homes.latitude),
    crs='EPSG:4326'
)
joined = gpd.sjoin(gdf_points, boroughs, predicate='within')
counts = joined.groupby('GSS_CODE').size().reset_index(name='airbnb_count')
boroughs_map = boroughs.merge(counts, on='GSS_CODE', how='left')
boroughs_map['airbnb_count'] = boroughs_map['airbnb_count'].fillna(0).astype(int)

stations_gdf = gpd.GeoDataFrame(
    df_stations,
    geometry=gpd.points_from_xy(df_stations['lon'], df_stations['lat']),
    crs='EPSG:4326'
)
stations_london = gpd.sjoin(stations_gdf, boroughs, predicate='within')

#  Stats row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="stat-box"><div class="stat-number">{len(entire_homes):,}</div><div class="stat-label">Entire-home listings</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="stat-box"><div class="stat-number">{len(stations_london)}</div><div class="stat-label">Tube stations</div></div>', unsafe_allow_html=True)
with col3:
    top_borough = boroughs_map.loc[boroughs_map['airbnb_count'].idxmax(), 'NAME']
    st.markdown(f'<div class="stat-box"><div class="stat-number" style="font-size:1.3rem;padding-top:0.3rem">{top_borough}</div><div class="stat-label">Highest density borough</div></div>', unsafe_allow_html=True)
with col4:
    avg = int(boroughs_map['airbnb_count'].mean())
    st.markdown(f'<div class="stat-box"><div class="stat-number">{avg}</div><div class="stat-label">Avg listings per borough</div></div>', unsafe_allow_html=True)

st.markdown('<hr>', unsafe_allow_html=True)

#  Map
st.markdown('<div class="section-label">Interactive Map — toggle layers using the control (top right)</div>', unsafe_allow_html=True)
m = folium.Map(location=[51.5074, -0.1278], zoom_start=9, tiles='OpenStreetMap')

choropleth = folium.Choropleth(
    geo_data=boroughs_map,
    data=boroughs_map,
    columns=['GSS_CODE', 'airbnb_count'],
    key_on='feature.properties.GSS_CODE',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.3,
    legend_name='Number of Entire-Home Airbnb Listings',
    name='Airbnb Density'
).add_to(m)

choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(
        fields=['NAME', 'airbnb_count'],
        aliases=['Borough:', 'Listings:'],
        style='font-size:13px;'
    )
)

folium.GeoJson(
    river,
    name='River Thames',
    style_function=lambda x: {'color': 'lightblue', 'weight': 4, 'opacity': 0.9}
).add_to(m)

marker_cluster = MarkerCluster(name='TfL Tube Stations').add_to(m)
for idx, row in stations_london.iterrows():
    folium.Marker(
        location=[row.geometry.y, row.geometry.x],
        popup=row['name']
    ).add_to(marker_cluster)

folium.LayerControl(collapsed=False).add_to(m)

st_folium(m, width='100%', height=580, returned_objects=[])

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<hr>', unsafe_allow_html=True)
st.markdown("""
<div style="font-size:0.78rem; color:#aaa; line-height:1.8;">
    <b>Data sources:</b> Inside Airbnb (listings.csv) &nbsp;·&nbsp; 
    Greater London Authority Statistical GIS Boundaries &nbsp;·&nbsp; 
    TfL StopPoint API (NaptanMetroStation) &nbsp;·&nbsp; 
    OpenStreetMap via OSMnx
</div>
""", unsafe_allow_html=True)
