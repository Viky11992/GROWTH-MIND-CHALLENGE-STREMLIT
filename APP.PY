# imports 
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# setup our app:
st.set_page_config(page_title="Data Sweeper", layout="wide")
st.title("Data Sweeper")
st.write("Transform your files between CSV and EXCEL formats with built-in data cleaning and visualization")

uploaded_files = st.file_uploader("Upload your file (CSV or EXCEL):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue
        
        # Display info about file
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")
        
        # Show preview of the DataFrame
        st.write("Preview of the DataFrame:")
        st.dataframe(df.head())
        
        # Data cleaning options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data For {file.name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button(f"Remove Duplicates From {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates removed successfully!")
            
            with col2:
                if st.button(f"Fill Missing Values For {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing values filled successfully!")
        
        # Column selection
        st.subheader("Select Columns to Keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]
        
        # Data visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])
        
        # File conversion
        st.subheader("Conversion Options")
        conversion_type = st.radio(
            f"Convert {file.name} to:", 
            ["CSV", "EXCEL"], 
            key=f"conv_{file.name}"
        )
        
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                new_filename = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "EXCEL":
                df.to_excel(buffer, index=False)
                new_filename = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)
            
            st.download_button(
                label=f"Download {new_filename}",
                data=buffer,
                file_name=new_filename,
                mime=mime_type
            )

st.success("All files processed!")