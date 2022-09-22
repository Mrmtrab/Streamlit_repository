######################
# Import libraries
######################

import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px

path_row_data = ""

######################
# Page Title
######################

mass_logo = Image.open('Logo-MASS-Analytics.png')
uor_logo = Image.open('Universal_Orlando_Resort_logo.svg.png')

images = ['P2100483.JPG', 'P2100486.JPG', 'P2100488.JPG']
st.image([uor_logo], use_column_width=True)


st.write("""
# EDA attendance data
2022-09-21

***
""")



######################
# Side bar
######################
st.sidebar.header('Upload data')
uploaded_file = st.sidebar.file_uploader("Upload your input xlsx file", type=["xlsx"])
if uploaded_file is not None:
    input_df = pd.read_excel(uploaded_file)
else :
    input_df = pd.read_excel(path_row_data+"test.xlsx")
    st.sidebar.write("test.xlsx is loaded")

df_display = input_df
st.sidebar.header('Filters')
years = sorted(list(df_display.WeekEndDate.dt.year.unique()))
start_year, end_year = st.sidebar.select_slider(
    'Year',
    options=years,
    value = (min(years),max(years))
)
df_display = df_display[(df_display.WeekEndDate<=str(end_year+1))&(df_display.WeekEndDate>=str(start_year))]

poos = df_display.Point_of_Origin.unique()
selected_poos = st.sidebar.multiselect('POOs', poos, poos)
df_display = df_display[df_display.Point_of_Origin.isin(selected_poos)]

types = df_display.Product_Type.unique()
selected_types = st.sidebar.multiselect('Product_Type', types, types)
df_display = df_display[df_display.Product_Type.isin(selected_types)]

channels = df_display.Channel.unique()
selected_channels = st.sidebar.multiselect('Channels', channels, channels)
df_display = df_display[df_display.Channel.isin(selected_channels)]


######################
# Main column
######################


st.header('Show data')
if input_df.shape[0] > 0:
    st.dataframe(df_display.head(10))
    st.write('Data Dimension: ' + str(df_display.shape[0]) + ' rows and ' + str(df_display.shape[1]) + ' columns.')

    columns = ["Point_of_Origin","Product_Type","Channel"]
    for column in columns :
        col1, col2 = st.columns([3, 2])
        view1 = df_display[[column, "Attendance"]].groupby(column).sum().reset_index()
        fig = go.Figure(data=[go.Pie(labels=view1[column], values=view1.Attendance, hole=.3)])
        fig.update_layout(
            title_text="Attendance by "+column)
        col1.plotly_chart(fig, use_container_width=True)
        col2.write(view1.round().sort_values("Attendance", ascending = False), use_column_width=True)

    view = df_display[["Product_Type","Point_of_Origin","Attendance"]].groupby(["Product_Type","Point_of_Origin"], as_index = False).sum()

    fig = go.Figure()
    for poo in view.Point_of_Origin.unique():
        view1 = view[view.Point_of_Origin == poo]
        fig.add_trace(go.Bar(x=view1.Product_Type, y=view1.Attendance, name = poo))
    fig.update_layout(barmode='stack',
                      xaxis={'categoryorder':'total descending'},
                      title_text="Attendance by product type by POO")
    st.plotly_chart(fig)

    df_display["month"] = df_display.WeekEndDate.dt.to_period("M")
    view = df_display[["month","Attendance"]].groupby("month", as_index=False).sum()
    fig = go.Figure()
    fig.add_trace(go.Scatter(name='Total Attendance',x = view.month.astype(str),y = view.Attendance,mode = 'lines+markers'))
    fig.layout.xaxis.tickvals = pd.date_range('2018-01', '2022-10', freq='QS')
    fig.layout.xaxis.tickformat = "%m-%Y"
    fig.update_xaxes(tickangle=-90)
    fig.update_layout(title_text="Total attendance over time")
    st.plotly_chart(fig)

    view = df_display[["month","Point_of_Origin","Attendance"]].groupby(["month","Point_of_Origin"], as_index=False).sum()
    fig = go.Figure()
    for poo in view.Point_of_Origin.unique():
        view1 = view[view.Point_of_Origin == poo]
        fig.add_trace(go.Scatter(name=poo,x = view1.month.astype(str),y = view1.Attendance,mode = 'lines+markers'))
    fig.layout.xaxis.tickvals = pd.date_range('2018-01', '2022-10', freq='QS')
    fig.layout.xaxis.tickformat = "%m-%Y"
    fig.update_xaxes(tickangle=-90)
    fig.update_layout(title_text="Total attendance by POO over time")
    st.plotly_chart(fig)

    view = df_display[["month","Product_Type","Attendance"]].groupby(["month","Product_Type"], as_index=False).sum()
    fig = go.Figure()
    for tp in view.Product_Type.unique():
        view1 = view[view.Product_Type == tp]
        fig.add_trace(go.Bar(name=tp, x = view1.month.astype(str),y = view1.Attendance))
    fig.layout.xaxis.tickvals = pd.date_range('2018-01', '2022-10', freq='QS')
    fig.layout.xaxis.tickformat = "%m-%Y"
    fig.update_xaxes(tickangle=-90)
    fig.update_layout(barmode='stack',
                      xaxis={'categoryorder':'total descending'},
                      title_text="Total attendance by Product Type over time"
                      )
    st.plotly_chart(fig)







