import os
import streamlit as st
import hydralit_components as hc
import datetime
import numpy as np # Array handler
import pandas as pd # Data analysis
import seaborn as sns  #Visualization
import matplotlib.pyplot as plt #Visualization
import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots
import plotly.io as pio

#make it look nice from the start
st.set_page_config(layout='wide',initial_sidebar_state='collapsed',)

# specify the primary menu definition
menu_data = [
    {'icon': "fa fa-table", 'label':"Raw Data"},
    {'icon': "fa fa-file", 'label':"Process Data"},
    # {'id':'Copy','icon':"🐙",'label':"Copy"},
    {'icon': "fa-solid fa-radar",'label':"Countplot Category", 'submenu':
    [{'id':'periodeHari','icon': "fa fa-sun", 'label':"Periode Hari"},
    {'id':'kategoriGempa','icon': "fa fa-monument", 'label':"Kategori Gempa"},
    {'id':'musim','icon': "fa fa-wind", 'label':"Musim"}, 
    {'id':'kategoriKedalaman','icon': "fa fa-mountain", 'label':"Kategori Kedalaman"}]},

    {'icon': "fa-solid fa-radar",'label':"Countplot Earthquake Amount", 'submenu':
    [{'id':'periodeHariPerTahun','icon': "fa fa-sun", 'label':"Periode Hari"},
    {'id':'kategoriGempaPerTahun','icon': "fa fa-monument", 'label':"Kategori Gempa"},
    {'id':'musimPerTahun','icon': "fa fa-wind", 'label':"Musim"}, 
    {'id':'kategoriKedalamanPerTahun','icon': "fa fa-mountain", 'label':"Kategori Kedalaman"}, 
    {'id':'kuartalPerTahun','icon': "fa fa-clock", 'label':"Kuartal"}]},

    {'icon': "fa-solid fa-radar",'label':"Mapbox", 'submenu':
    [{'id':'mapDepth','icon': "fa fa-globe", 'label':"Kedalaman"},
    {'id':'mapMag','icon': "fa fa-map", 'label':" Magnitudo"}]},
    
    {'icon': "fa fa-clone", 'label':"Treemap"},#no tooltip message
    # {'id':' Crazy return value 💀','icon': "💀", 'label':"Calendar"},
    # {'icon': "fas fa-tachometer-alt", 'label':"Dashboard",'ttip':"I'm the Dashboard tooltip!"}, #can add a tooltip message
    # {'icon': "far fa-copy", 'label':"Right End"},
    # {'icon': "fa-solid fa-radar",'label':"Dropdown2", 'submenu':[{'label':"Sub-item 1", 'icon': "fa fa-meh"},{'label':"Sub-item 2"},{'icon':'🙉','label':"Sub-item 3",}]},
]

over_theme = {'txc_inactive': 'purple','menu_background':'white','txc_active':'#FFBEA3','option_active':'white'}
menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name='Home',
    login_name='Users',
    hide_streamlit_markers=False, #will show the st hamburger as well as the navbar now!
    sticky_nav=True, #at the top or not
    sticky_mode='pinned', #jumpy or not-jumpy, but sticky or pinned
)


dir_path = os.path.dirname(os.path.realpath(__file__))
df = pd.read_csv(dir_path + "\katalog_gempa.csv")
df['tgl'] = pd.to_datetime(df['tgl'], format='%Y-%m-%d')
df['ot'] = pd.to_datetime(df['ot'], format='%H:%M:%S')

if menu_id == 'Home':
    st.header(":bar_chart: Indonesia Earthquake Dashboard")
    st.markdown("----")

# --- Information of total Several Data ---
mean_mag, mean_depth, total_data = st.columns(3)
# average_m = sum(df.mag)/len(df.mag)

mean_mag.metric("Average Magnitude:", df.mag.mean())
mean_depth.metric("Average Depth",  df.depth.mean())
total_data.metric("Total Case",  df.region.count())

st.markdown("----") 

# Display Process Data
if menu_id == 'Raw Data':
    st.write("""## Tabel Data Gempa 2008-2022""") 
    df = pd.DataFrame(df)
    st.dataframe(df)

#make month & year
df['month'] = df['tgl'].dt.month
tempList = []
for i in df['month'].tolist():
    tempVar = 0
    if (i<4):
        tempVar = 1
    elif(i<7):
        tempVar = 2
    elif(i<10):
        tempVar = 3
    else:
        tempVar = 4
    tempList.append(tempVar)
df['quarter'] = tempList
df['year'] = df['tgl'].dt.year

# DayPeriod
df['hours'] = df['ot'].dt.hour
df['minutes'] = df['ot'].dt.minute
tempList = []
for i in df['hours'].tolist():
    tempVar = ''
    if (i<3):
        tempVar = 'Dini hari'
    elif(i<5):
        tempVar = 'Subuh'
    elif(i<12):
        tempVar = 'Pagi'
    elif(i<15):
        tempVar = 'Siang'
    elif(i<18):
        tempVar = 'Sore'
    else:
        tempVar = 'Malam'
    tempList.append(tempVar)
df['dayPeriod'] = tempList

#Earthquake Category
tempList = []
for i in df['mag'].tolist():
    tempVar = ''
    if (i<3):
        tempVar = 'Micro'
    elif (i<4):
        tempVar = 'Minor'
    elif (i<5):
        tempVar = 'Ringan'
    elif (i<6):
        tempVar = 'Sedang'
    elif (i<7):
        tempVar = 'Kuat'
    elif (i<8):
        tempVar = 'Mayor'
    else:
        tempVar = 'Great'
    tempList.append(tempVar)
df['earthquakeCategory'] = tempList

#Season
tempList = []
for i in df['month'].tolist():
    tempVar = ''
    if ((i>3)&(i<11)):
        tempVar = 'Kemarau'
    else:
        tempVar = 'Hujan'
    tempList.append(tempVar)
df['season'] = tempList

#Depth
tempList = []
for i in df['depth'].tolist():
    tempVar = ''
    if (i<60):
        tempVar = 'Dangkal'
    elif (i<300):
        tempVar = 'Menengah'
    else:
        tempVar = 'Dalam'
    tempList.append(tempVar)
df['depthCategory'] = tempList

#New earthquake table
dfe = df[['year','quarter','month','lat','lon','depth','mag','hours', 'minutes', 'dayPeriod', 'earthquakeCategory','season','depthCategory', 'remark', 'region']].copy()
dfe = dfe.loc[(df['year']>=2008)&(df['year']<=2022)]
dfe = dfe.reset_index(drop=True)
# Display Process Data
if menu_id == 'Process Data':
    st.write("""## Tabel Data Final Gempa 2008-2022""") 
    dfe = pd.DataFrame(dfe)
    st.dataframe(dfe)

# Display Countplot Category

elif menu_id == 'periodeHari':
    st.write("""## Trend Distribusi Karakteristik berdasarkan Periode Hari""") 
    fig = plt.figure(figsize = (9,2.8)) 
    ax = sns.countplot(data = dfe, x = dfe['dayPeriod'], palette = 'magma')
    ax.set(xlabel='Periode Hari', ylabel='Jumlah Data')
    st.pyplot(fig)

elif menu_id == 'kategoriGempa':
    st.write("""## Trend Distribusi Karakteristik berdasarkan Kategori Gempa""") 
    fig = plt.figure(figsize = (9,2.8)) 
    ax = sns.countplot(data = dfe, x = dfe['earthquakeCategory'], palette = 'magma')
    ax.set(xlabel='Kategori Gempa', ylabel='Jumlah Data')
    st.pyplot(fig)

elif menu_id == 'musim':
    st.write("""## Trend Distribusi Karakteristik berdasarkan Musim""") 
    fig = plt.figure(figsize = (9,2.8)) 
    ax = sns.countplot(data = dfe, x = dfe['season'], palette = 'magma')
    ax.set(xlabel='Musim', ylabel='Jumlah Data')
    st.pyplot(fig)

elif menu_id == 'kategoriKedalaman':
    st.write("""## Trend Distribusi Karakteristik berdasarkan Kategori Kedalaman Gempa""") 
    fig = plt.figure(figsize = (9,2.8)) 
    ax = sns.countplot(data = dfe, x = dfe['depthCategory'], palette = 'magma')
    ax.set(xlabel='Kategori Kedalaman', ylabel='Jumlah Data')
    st.pyplot(fig)

# Display Countplot Earthquake Amount
elif menu_id == 'periodeHariPerTahun':
    st.write("""## Jumlah Gempa per Tahun berdasarkan Periode Hari""") 
    fig = plt.figure(figsize = (24,8)) 
    ax = sns.countplot(data = dfe, x = 'year', hue = dfe['dayPeriod'], palette = 'magma')
    ax.set(xlabel='Tahun', ylabel='Jumlah Data')
    st.pyplot(fig)

elif menu_id == 'kategoriGempaPerTahun':
    st.write("""## Jumlah Gempa per Tahun berdasarkan Kategori Gempa""") 
    fig = plt.figure(figsize = (24,8)) 
    ax = sns.countplot(data = dfe, x = 'year', hue = dfe['earthquakeCategory'], palette = 'magma')
    ax.set(xlabel='Tahun', ylabel='Jumlah Data')
    st.pyplot(fig)

elif menu_id == 'musimPerTahun':
    st.write("""## Jumlah Gempa per Tahun berdasarkan Musim""") 
    fig = plt.figure(figsize = (24,8)) 
    ax = sns.countplot(data = dfe, x = 'year', hue = dfe['season'], palette = 'magma')
    ax.set(xlabel='Tahun', ylabel='Jumlah Data')
    st.pyplot(fig)

elif menu_id == 'kategoriKedalamanPerTahun':
    st.write("""## Jumlah Gempa per Tahun berdasarkan Kategori Kedalaman Gempa""") 
    fig = plt.figure(figsize = (24,8)) 
    ax = sns.countplot(data = dfe, x = 'year', hue = dfe['depthCategory'], palette = 'magma')
    ax.set(xlabel='Tahun', ylabel='Jumlah Data')
    st.pyplot(fig)

elif menu_id == 'kuartalPerTahun':
    st.write("""## Jumlah Gempa per Tahun berdasarkan Kuartal Momen""") 
    fig = plt.figure(figsize = (24,8)) 
    ax = sns.countplot(data = dfe, x = 'year', hue = dfe['quarter'], palette = 'magma')
    ax.set(xlabel='Tahun', ylabel='Jumlah Data')
    st.pyplot(fig)

# Display Map
elif menu_id == 'mapDepth':
    st.write("""## Mapping Persebaran Gempa berdasarkan Tingkat Kedalaman""") 
    fig = px.scatter_mapbox(dfe, lat="lat", lon="lon", color="depth", 
                        mapbox_style="open-street-map", zoom = 4.3, color_continuous_scale = 'sunsetdark')
    fig.update_layout(autosize=False,width=1700, height=650, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

elif menu_id == 'mapMag':
    st.write("""## Mapping Persebaran Gempa berdasarkan Tingkat Magnitudo dalam Periode 2008-2022""") 
    fig = px.density_mapbox(dfe, lat="lat", lon="lon", z="mag", mapbox_style="open-street-map",
                        animation_frame = 'year', zoom = 4.1, radius = 20, color_continuous_scale = 'sunsetdark', range_color = [5.0,10.0])
    fig.update_layout(autosize=False,width=1700, height=650, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

# Mean
elif menu_id == 'Treemap':
    st.write("""## Urutan Lokasi berdasarkan Total Peristiwa Gempa dalam Periode 2008-2022""") 
    remark_count = dfe.groupby(pd.Grouper(key='remark')).size().reset_index(name='count')
    fig = px.treemap(remark_count, path=['remark'], values='count')
    fig.update_layout(autosize=False,width=1700, height=650)
    # fig.update_layout(title_text='Number of Earthquakes due to Location',
    #                   title_x=0.5, title_font=dict(size=30)
    #                   )
    fig.update_traces(textinfo="label+value")
    st.plotly_chart(fig)

# elif menu_id == 'Users':
    # st.write("""# Visualisasi Data Kepadatan Penduduk Jawa Timur dengan Streamlit""")
    # st.write(""" Nama : M.Khotibul Umam  NIM : 09020620031 """)
    # st.write(""" Nama : Retno  NIM : 09020620032 """)
    # st.write(""" Nama : Fateh  NIM : 09020620033 """)   

    # fig=plt.figure(figsize=(12,8))
    # Time_series=sns.lineplot(x=dfe['year'],y="mag",data=dfe, color="#ffa600")
    # Time_series.set_title("Time Series Of Earthquakes Over Years", color="#58508d")
    # Time_series.set_ylabel("Magnitude", color="#58508d")
    # Time_series.set_xlabel("Date", color="#58508d")
    # st.pyplot(fig)
    
    # mean_mag_date1 = dfe.groupby('year')['mag'].mean().reset_index(drop=False)
    # mean_mag_date1.sort_values(by='year')
    # mean_mag_date1 = pd.DataFrame(mean_mag_date1)
    # st.dataframe(mean_mag_date1)

    # fig = go.Figure(
    #     data = go.Scatter(
    #         x = mean_mag_date1['year'],
    #         y = mean_mag_date1['mag']),
    #     layout = go.Layout(
    #         title = go.layout.Title(text = "Mean magnitude per day", x = 0.5),
    #         xaxis = go.layout.XAxis(title = 'Year', rangeslider = go.layout.xaxis.Rangeslider(visible = True))
    #     )
    # )

    # mean_mag_date1.loc[:,'Mean_Magnitude'] = mean_mag_date1['mag'].mean()
    # fig.add_trace(
    #     go.Scatter(
    #         x = mean_mag_date1['year'],
    #         y = mean_mag_date1['Mean_Magnitude'])
    # )

    # fig.update_layout(showlegend = True)
    # st.plotly_chart(fig)
