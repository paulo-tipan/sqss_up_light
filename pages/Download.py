import streamlit as st
import pandas as pd

import psycopg2
from sqlalchemy import create_engine

from datetime import datetime, timedelta

#url = 'postgresql+psycopg2://username:password@host:port/database'
url = 'postgresql+psycopg2://dashboard_select:AVNS_hf_HkycGlpPX1osvfYX@db-postgresql-sgp1-32435-do-user-12241536-0.b.db.ondigitalocean.com:25060/client_template'
engine = create_engine(url)

yesterday = datetime.today() - timedelta(days=1)

def query_data(start_date_query,end_date_query):
    sql_code = f'''
                SELECT 
                    insert_date,
                    co2x,
                    o2xx,
                    temp,
                    humi,
                    sensor_name
                FROM 
                    sensors.sqss_data
                WHERE insert_date BETWEEN '{start_date_query}' AND '{end_date_query}'
                AND sensor_name = 'client_sqss_O'
                ORDER BY insert_date DESC;
                '''
    df = pd.read_sql(sql_code,con=engine)
    return df

def main():

    st.title('AniTech SQSS Data Download')
    col1, col2 = st.columns(2)

    with col1:
        st.header("Start Date")
        start_date = st.date_input("Start Date", yesterday)

    with col2:
        st.header("End Date")
        end_date =  st.date_input("End Date", datetime.today())
        end_date_q = end_date + timedelta(days=1)
    

    if st.button('Check Data'):
        print(start_date,end_date)
        
        query_df = query_data(start_date,end_date_q)

        st.dataframe(query_df)

        @st.cache
        def convert_df(data_f):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return data_f.to_csv(index=False).encode('utf-8')

        csv = convert_df(query_df)

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f'sqss_data_{start_date}.csv',
            mime='text/csv',
        )


if __name__ == "__main__":
    main()