import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
from datetime import datetime
from datetime import time


st.set_page_config(layout="wide")

DATA_URL = [
    "https://github.com/Maplub/odsample/raw/master/20190101.csv" , "https://github.com/Maplub/odsample/raw/master/20190102.csv" ,"https://github.com/Maplub/odsample/raw/master/20190103.csv"
    ,"https://github.com/Maplub/odsample/raw/master/20190104.csv" , "https://github.com/Maplub/odsample/raw/master/20190105.csv"
]


@st.cache(persist=True)
#load Data
def load_data(DATA_URL):
    data = pd.read_csv(DATA_URL)
    #lowercase = lambda x: str(x).lower()
    #data.rename(lowercase, axis="columns", inplace=True)
    data['timestart'] = pd.to_datetime(data['timestart'])
    data['timestop'] = pd.to_datetime(data['timestop'])
    data = data.fillna(0)
    return data

data1 = load_data(DATA_URL[0]) ; data2 = load_data(DATA_URL[1])
data3 = load_data(DATA_URL[2]) ; data4 = load_data(DATA_URL[3])
data5 = load_data(DATA_URL[4]) ; data_all = data1.append([data2,data3,data4,data5],ignore_index=True)
data_all = data_all.fillna(0)

#Setting Map
def map(Data,lat, lon, zoom):
    st.write(pdk.Deck(
				layers=[
            pdk.Layer(
                "HexagonLayer",
                data=Data,
                get_position=["lonstartl", "latstartl"],
								auto_highlight=True,
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
								coverage=1
            )
        ],map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50 },
						))

row1_1, row1_2 = st.columns((2,3))

#Select Data
with row1_1:
    st.title("Pickup and Destination Data")
    date_selected = st.select_slider(
     'Select Date (M/D/YYYY)',
     options=['1/1/2019', '2/1/2019', '3/1/2019', '4/1/2019', '5/1/2019','All'])
    hour_sta,hour_sto = st.select_slider(
     'Select Time',options=['00:00','03:00','06:00','09:00','12:00','15:00','18:00','21:00','24:00'],value=('00:00','06:00'))
    if hour_sto == '24:00' :
       hour_sto = '23:59'

with row1_2:
    st.header('Mapping of Pickup and Destination extracted from iTIC data')
    st.write('Lab 5 Geospatial Data Science By ')
    st.write('6130816521 Paponpat Limpanithiphat ')
    st.write('Select Data')
    pick = row1_2.button("Pickup") ; des = row1_2.button("Destination")

hour_sta1 = hour_sta ; hour_sto1 = hour_sto
hour_sta = time.fromisoformat(hour_sta) ; hour_sto = time.fromisoformat(hour_sto)

op = ['1/1/2019', '2/1/2019', '3/1/2019', '4/1/2019', '5/1/2019','All']


#Mapping

if pick == True :
	show = date_selected+' (M/D/YYYY)' +' from '+ hour_sta1 + ' to '+ hour_sto1 + ' (Pickup)'
	st.write( show )
	midpoint = (np.average(data_all["latstartl"]), np.average(data_all["lonstartl"]))
	data_all = data_all[(data_all['timestart'].dt.hour >= hour_sta.hour) & ( data_all['timestart'].dt.hour <= hour_sto.hour)]
	data1 = data1[(data1['timestart'].dt.hour >= hour_sta.hour) & ( data1['timestart'].dt.hour <= hour_sto.hour)]
	data2 = data2[(data2['timestart'].dt.hour >= hour_sta.hour) & ( data2['timestart'].dt.hour <= hour_sto.hour)]
	data3 = data3[(data3['timestart'].dt.hour >= hour_sta.hour) & ( data3['timestart'].dt.hour <= hour_sto.hour)]
	data4 = data4[(data4['timestart'].dt.hour >= hour_sta.hour) & ( data4['timestart'].dt.hour <= hour_sto.hour)]
	data5 = data5[(data5['timestart'].dt.hour >= hour_sta.hour) & ( data5['timestart'].dt.hour <= hour_sto.hour)]
	if date_selected == op[5] :
	   data = data_all
	   map(data_all,midpoint[0],midpoint[1],11)
	   row2_1, row2_2, row2_3, row2_4 ,row2_5 = st.columns((1,1,1,1,1))
	   with row2_1:
			   st.write('1/1/2019')	   
			   map(data1,13.75,100.55,11)
	   with row2_2:
			   st.write('2/1/2019')   
			   map(data2,13.75,100.55,11)
	   with row2_3:
			   st.write('3/1/2019')
			   map(data3,13.75,100.55,11)
	   with row2_4:
			   st.write('4/1/2019')
			   map(data4,13.75,100.55,11)
	   with row2_5:
			   st.write('5/1/2019')
			   map(data5,13.75,100.55,11)	
	if date_selected == op[0] :
	   data = data1
	   map(data1,midpoint[0],midpoint[1],11)
	   row2_1, row2_2, row2_3, row2_4 = st.columns((1,1,1,1))
	   with row2_1:
			   st.write('2/1/2019')
			   map(data2,13.75,100.55,11)
	   with row2_2:
			   st.write('3/1/2019')
			   map(data3,13.75,100.55,11)
	   with row2_3:
			   st.write('4/1/2019')
			   map(data4,13.75,100.55,11)
	   with row2_4:
			   st.write('5/1/2019')
			   map(data5,13.75,100.55,11)
	if date_selected == op[1] :
	   data = data2
	   map(data2,midpoint[0],midpoint[1],11)
	   row2_1, row2_2, row2_3, row2_4 = st.columns((1,1,1,1))
	   with row2_1:
			   st.write('1/1/2019')
			   map(data1,13.75,100.55,11)
	   with row2_2:
			   st.write('3/1/2019')
			   map(data3,13.75,100.55,11)
	   with row2_3:
			   st.write('4/1/2019')
			   map(data4,13.75,100.55,11)
	   with row2_4:
			   st.write('5/1/2019')
			   map(data5,13.75,100.55,11)
	if date_selected == op[2] :
	   data = data3
	   map(data3,midpoint[0],midpoint[1],11)
	   row2_1, row2_2, row2_3, row2_4 = st.columns((1,1,1,1))
	   with row2_1:
			   st.write('1/1/2019')
			   map(data1,13.75,100.55,11)
	   with row2_2:
			   st.write('2/1/2019')
			   map(data2,13.75,100.55,11)
	   with row2_3:
			   st.write('4/1/2019')
			   map(data4,13.75,100.55,11)
	   with row2_4:
			   st.write('5/1/2019')
			   map(data5,13.75,100.55,11)	
	if date_selected == op[3] :
	   data = data4
	   map(data4,midpoint[0],midpoint[1],11)
	   row2_1, row2_2, row2_3, row2_4 = st.columns((1,1,1,1))
	   with row2_1:
			   st.write('1/1/2019')
			   map(data1,13.75,100.55,11)
	   with row2_2:
			   st.write('2/1/2019')
			   map(data2,13.75,100.55,11)
	   with row2_3:
			   st.write('3/1/2019')
			   map(data3,13.75,100.55,11)
	   with row2_4:
			   st.write('5/1/2019')
			   map(data5,13.75,100.55,11)		 
	if date_selected == op[4] :
	   data = data5
	   map(data5,midpoint[0],midpoint[1],11)
	   row2_1, row2_2, row2_3, row2_4 = st.columns((1,1,1,1))
	   with row2_1:
			   st.write('1/1/2019')
			   map(data1,13.75,100.55,11)
	   with row2_2:
			   st.write('2/1/2019')
			   map(data2,13.75,100.55,11)
	   with row2_3:
			   st.write('3/1/2019')
			   map(data3,13.75,100.55,11)
	   with row2_4:
			   st.write('4/1/2019')		   
			   map(data4,13.75,100.55,11)
else :
	show = date_selected+' (M/D/YYYY)' +' from '+ hour_sta1 + ' to '+ hour_sto1 + ' (Destination)'
	st.write( show )
	data_all = data_all[(data_all['timestop'].dt.hour >= hour_sto.hour) & ( data_all['timestop'].dt.hour <= hour_sto.hour)]
	data1 = data1[(data1['timestop'].dt.hour >= hour_sta.hour) & ( data1['timestop'].dt.hour <= hour_sto.hour)]
	data2 = data2[(data2['timestop'].dt.hour >= hour_sta.hour) & ( data2['timestop'].dt.hour <= hour_sto.hour)]
	data3 = data3[(data3['timestop'].dt.hour >= hour_sta.hour) & ( data3['timestop'].dt.hour <= hour_sto.hour)]
	data4 = data4[(data4['timestop'].dt.hour >= hour_sta.hour) & ( data4['timestop'].dt.hour <= hour_sto.hour)]
	data5 = data5[(data5['timestop'].dt.hour >= hour_sta.hour) & ( data5['timestop'].dt.hour <= hour_sto.hour)]			   	   	  	  	  
	midpoint = (np.average(data_all["latstop"]), np.average(data_all["lonstop"]))
	if date_selected == op[5] :
	   data = data_all
	   map(data_all,midpoint[0],midpoint[1],11)
	   row2_1, row2_2, row2_3, row2_4 ,row2_5 = st.columns((1,1,1,1,1))
	   with row2_1:
			   st.write('1/1/2019')	   
			   map(data1,13.75,100.55,11)
	   with row2_2:
			   st.write('2/1/2019')   
			   map(data2,13.75,100.55,11)
	   with row2_3:
			   st.write('3/1/2019')
			   map(data3,13.75,100.55,11)
	   with row2_4:
			   st.write('4/1/2019')
			   map(data4,13.75,100.55,11)
	   with row2_5:
			   st.write('5/1/2019')
			   map(data5,13.75,100.55,11)	
	if date_selected == op[0] :
	   data = data1
	   map(data1,midpoint[0],midpoint[1],11)
	   row2_1, row2_2, row2_3, row2_4 = st.columns((1,1,1,1))
	   with row2_1:
			   st.write('2/1/2019')
			   map(data2,13.75,100.55,11)
	   with row2_2:
			   st.write('3/1/2019')
			   map(data3,13.75,100.55,11)
	   with row2_3:
			   st.write('4/1/2019')
			   map(data4,13.75,100.55,11)
	   with row2_4:
			   st.write('5/1/2019')
			   map(data5,13.75,100.55,11)
	if date_selected == op[1] :
	   data = data2
	   map(data2,midpoint[0],midpoint[1],11)
	   row2_1, row2_2, row2_3, row2_4 = st.columns((1,1,1,1))
	   with row2_1:
			   st.write('1/1/2019')
			   map(data1,13.75,100.55,11)
	   with row2_2:
			   st.write('3/1/2019')
			   map(data3,13.75,100.55,11)
	   with row2_3:
			   st.write('4/1/2019')
			   map(data4,13.75,100.55,11)
	   with row2_4:
			   st.write('5/1/2019')
			   map(data5,13.75,100.55,11)
	if date_selected == op[2] :
	   data = data3
	   map(data3,midpoint[0],midpoint[1],11)
	   row2_1, row2_2, row2_3, row2_4 = st.columns((1,1,1,1))
	   with row2_1:
			   st.write('1/1/2019')
			   map(data1,13.75,100.55,11)
	   with row2_2:
			   st.write('2/1/2019')
			   map(data2,13.75,100.55,11)
	   with row2_3:
			   st.write('4/1/2019')
			   map(data4,13.75,100.55,11)
	   with row2_4:
			   st.write('5/1/2019')
			   map(data5,13.75,100.55,11)	
	if date_selected == op[3] :
	   data = data4
	   map(data4,midpoint[0],midpoint[1],11)
	   row2_1, row2_2, row2_3, row2_4 = st.columns((1,1,1,1))
	   with row2_1:
			   st.write('1/1/2019')
			   map(data1,13.75,100.55,11)
	   with row2_2:
			   st.write('2/1/2019')
			   map(data2,13.75,100.55,11)
	   with row2_3:
			   st.write('3/1/2019')
			   map(data3,13.75,100.55,11)
	   with row2_4:
			   st.write('5/1/2019')
			   map(data5,13.75,100.55,11)		 
	if date_selected == op[4] :
	   data = data5
	   map(data5,midpoint[0],midpoint[1],11)
	   row2_1, row2_2, row2_3, row2_4 = st.columns((1,1,1,1))
	   with row2_1:
			   st.write('1/1/2019')
			   map(data1,13.75,100.55,11)
	   with row2_2:
			   st.write('2/1/2019')
			   map(data2,13.75,100.55,11)
	   with row2_3:
			   st.write('3/1/2019')
			   map(data3,13.75,100.55,11)
	   with row2_4:
			   st.write('4/1/2019')		   
			   map(data4,13.75,100.55,11)

fil = pd.DataFrame()
## filter data
if pick == True :
	len_hour = hour_sto.hour-hour_sta.hour
	for i in range(len_hour) :
		a = data['timestart'].dt.hour
		fil1 = data['timestart'][a == hour_sta.hour+i ]
		fil2 = fil1.dt.minute+(60*i)
		fil2 = pd.DataFrame(fil2)
		fil = fil.append(fil2,ignore_index=True)
		len2 = len(data['timestart'].dt.minute)
		len_min = len_hour*60
		hist = np.histogram(fil['timestart'], bins=len_min, range=(0,len_min))[0]
		chart_data = pd.DataFrame({"minute": range(len_min), "pickups": hist})
else :
	len_hour = hour_sto.hour-hour_sta.hour
	for i in range(len_hour) :
		a = data['timestop'].dt.hour
		fil1 = data['timestop'][a == hour_sta.hour+i ]
		fil2 = fil1.dt.minute+(60*i)
		fil2 = pd.DataFrame(fil2)
		fil = fil.append(fil2,ignore_index=True)
		len2 = len(data['timestop'].dt.minute)
		len_min = len_hour*60
		hist = np.histogram(fil['timestop'], bins=len_min, range=(0,len_min))[0]
		chart_data = pd.DataFrame({"minute": range(len_min), "pickups": hist})

st.write("   ")
st.write("   Breakdown of rides per minute between %i:00 and %i:00  " % (hour_sta.hour,hour_sto.hour ))
# Set Chart
st.altair_chart(alt.Chart(chart_data)
    .mark_area(
        interpolate='step-after',
    ).encode(
        x=alt.X("minute:Q", scale=alt.Scale(nice=False)),
        y=alt.Y("pickups:Q"),
        tooltip=['minute', 'pickups']
    ).configure_mark(
        opacity=0.5,
        color='red'
    ), use_container_width=True)