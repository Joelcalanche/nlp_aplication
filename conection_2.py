import streamlit as st
import pandas as pd
# import base64
import matplotlib.pyplot as plt
# import seaborn as sns
import numpy as np
import pandas as pd
import sqlite3

# Crea una conexión a la base de datos SQLite
con = sqlite3.connect(r"C:\Users\calanche\Desktop\projectNLP\bbc_db.sqlite")

# Extrae los datos de la consulta directamente a un DataFrame
bbc_df = pd.read_sql_query("SELECT * from bbc_db", con, parse_dates=["timestamps_"])


bbc_df.sort_values(by=["timestamps_"], inplace=True, ascending=False)
st.title('NLP_APPLICATION')
df_tmp = bbc_df.copy()
# print(len(df_tmp))


days = df_tmp.timestamps_.dt.day
print(type(days))
years =df_tmp.timestamps_.dt.year
st.markdown("""
# News filter 

This app performs simple webscraping of  BBC 
please select the text to analyze

* **Python libraries:** base64, pandas, streamlit
* **Data source:** from the pipeline.
""")

st.sidebar.header('User Input Features')
# selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2020))))
selected_day = st.sidebar.selectbox('Days', list(days.unique()))
# selected_day_list = list(selected_day)
selected_year = st.sidebar.selectbox('Years', list(years.unique()))



# # Sidebar - Team selection
# sorted_unique_titles = df_tmp["title"].unique()
# selected_title = st.sidebar.multiselect('titles', list(sorted_unique_titles))
# selected_ = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# # Filtering data
# r = df_tmp[((df_tmp.timestamps_.dt.year.isin(years)) & (df_tmp.timestamps_.dt.day.isin(days)))]
prueba = [selected_year.tolist()]
print(prueba)
# r = df_tmp[((df_tmp.timestamps_.dt.year.isin([2021])) & (df_tmp.timestamps_.dt.day.isin([24])))]
r = df_tmp[((df_tmp.timestamps_.dt.year.isin([selected_year.tolist()])) & (df_tmp.timestamps_.dt.day.isin([selected_day.tolist()])))]
print("este es mi experimento",len(df_tmp))
print(len(r))
unique_titles = r["title"].unique().tolist()
selected_title = st.sidebar.selectbox('titles', unique_titles)
print(selected_title)
print(len(selected_title))


# segundo filtro
r_2 =  r["text_"][(r["title"] == selected_title)]
# print(df_selected_team)
# st.header('Display Player Stats of Selected Team(s)')
# st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
# # print(df_selected_team)
st.write(r_2)
