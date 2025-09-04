import pandas as pd 
import pickle
import streamlit as st 
import numpy as np 

pipe = pickle.load(open('pipe.pkl' , 'rb'))
df = pickle.load(open('lapidata.pkl' , 'rb'))

st.title("Laptop Price Predicotor")

#brand
company = st.selectbox('Brand',df['Company'].unique())

# type of Laapi
type = st.selectbox('Type', df['TypeName'].unique())

# Ram
ram = st.selectbox('Ram(in GB)', [2,4,6,8,12,16,24,32,64])

# weight
weight = st.number_input('Weight')

#touchscreen
if company != 'Apple':
    touchscreen = st.selectbox('Touch Screen' , ['No','Yes'])
else:
    touchscreen = st.selectbox('Touch Screen' , ['No'])

# IPS
ips = st.selectbox('IPS' , ['No','Yes'])

# screen size
screen_size = st.number_input('Screen Size')

# res
resolution = st.selectbox('Screen Resolution' , ['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])

# Cpu
cpu = st.selectbox('CPU',df['cpu_brand'].unique())

# HDD
hardDrive = st.selectbox('Hard Drive(in GB)',[0,128,256,512,1024,2048])

# SSD
ssd = st.selectbox('SSD(in GB)',[0,128,256,512,1024,2048])

# Gpu
gpu = st.selectbox('GPU',df['GpuBrand'].unique())

# os 
if company != 'Apple':
    os_for_win = df['os'].unique().tolist()[1:]
    os = st.selectbox('OS',os_for_win)
else:
    os = st.selectbox('OS',['Mac'])


if st.button('Predict Price'):
    #Company	TypeName	Ram	Weight	Touchscreen	IPS_Panel	ppi	cpu_brand	ssd	hdd	GpuBrand	os
    ppi = None

    if touchscreen == 'Yes':
        touchscreen = 1 
    else:
        touchscreen = 0 
    
    if ips == 'Yes':
        ips = 1 
    else:
        ips = 0 

    x_res = int(resolution.split('x')[0])
    y_res = int(resolution.split('x')[0])
    ppi = ((x_res)**2 + (y_res)**2)**0.5/screen_size
    query = np.array([company,type,ram,weight,touchscreen,ips,ppi,cpu,ssd,hardDrive,gpu,os]) 
    query = query.reshape(1,-1)
    ans = pipe.predict(query)[0]
    st.title(round(np.exp(ans)))