import pandas as pd
import streamlit as st

def snake_columns(data):
    """
    returns the columns in snake case
    """
    data.columns = [column.lower().replace(' ', '_') for column in data.columns]
    
def open_data(data): # returns shape, data types & shows a small sample
    """
    open data, returns shape, data types and shows small sample
    """
    st.write(f"Data shape is {data.shape}.")
    st.write()
    st.write(data.dtypes)
    st.write()
    st.write("Data row sample and full columns:")
    return st.write(data.sample(5))
    
# 🎯 Specific functions
def explore_data(data): # sum & returns duplicates, NaN & empty spaces
    """
    sum and returns duplicates, nulls end empty spaces.
    """
    duplicate_rows = data.duplicated().sum()
    nan_values = data.isna().sum()
    empty_spaces = data.eq(' ').sum()
    exploration = pd.DataFrame({"Nulls": nan_values, "Empty spaces": empty_spaces}) # New dataframe with the results
    st.write(f"There are {data.duplicated().sum()} duplicated rows.")
    return st.write(exploration)

def borrar_duplicados(data):
    """
    drop duplicated values
    """
    data = data.drop_duplicates()