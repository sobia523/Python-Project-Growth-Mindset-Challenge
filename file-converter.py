import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Converter", layout='wide')
st.title("File Converter & Cleaner")
st.write("Upload csv or excel files, clean data, and convert formats.")

files = st.file_uploader("Upload CSV or Excel Files.", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        
        # Read the file (CSV or Excel) with the appropriate engine for Excel
        if ext == "csv":
            df = pd.read_csv(file)
        elif ext == "xlsx":
            df = pd.read_excel(file, engine='openpyxl')
        else:
            continue

        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        # Remove duplicates if checkbox is checked
        if st.checkbox(f"Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("Duplicates Removed Successfully!")
            st.dataframe(df.head())

        # Fill missing values if checkbox is checked
        if st.checkbox(f"Fill Missing values - {file.name}"):
            # Fill missing values with the mean of the respective column for numerical columns
            df[df.select_dtypes(include='number').columns] = df.select_dtypes(include='number').fillna(df.mean())
            st.success("Missing values filled successfully!")
            st.dataframe(df.head())

        # Select columns to keep
        selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        # Show chart if checkbox is checked and there are numerical columns
        if st.checkbox(f"Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # Convert to a different format (CSV or Excel)
        format_choice = st.radio(f"Convert {file.name} to:", ["csv", "Excel"], key=file.name)

        # Button to download the converted file
        if st.button(f"Download {file.name} as {format_choice}"):

            # Prepare the file for download
            output = BytesIO()
            if format_choice == "csv":
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.replace(ext, "csv")

            else:
                df.to_excel(output, index=False, engine="openpyxl")
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")

            output.seek(0)
            st.download_button("Download File", file_name=new_name, data=output, mime=mime)

            st.success("Processing Complete!")
