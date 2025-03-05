# import
import streamlit as st 
import pandas as pd
import os 
from io import BytesIO

# set up app
st.set_page_config(page_title="💿Data swiper", layout="wide")
st.title("💿Data swiper")
st.write("Transform your file between CSV and excel with built in data cleaning and visualization!")
uploded_File = st.file_uploader("Uplode your file(CSV And Excle):",type=["csv","xlsx"],accept_multiple_files=True)
if uploded_File:
    for file in uploded_File:
        file_ext=os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df=pd.read_csv(file)
        elif file_ext==".xlsx":
            df=pd.read_excel(file)
        else:
            st.error(f"unsupport file type: {file_ext}")
            continue

        # Display info about the file
        st.write(f"**File Name:**{file.name}")
        st.write(f"**File Size:**{file.size/1024}")

        # show five row of Data fram
        st.write("🔍 Preview the head of data fram! ")
        st.dataframe(df.head())

        # Option for data cleaning 
        st.subheader("⚒️ Data cleaning option")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1,col2=st.columns(2)

            with col1:
                if st.button(f"Remove Duplicate from file {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicate Remove!")
            
            with col2:
                if st.button(f"Fill missing value for {file.name}"):
                    numarical_cols=df.select_dtypes(include={'number'}).columns
                    df[numarical_cols]=df[numarical_cols].fillna(df[numarical_cols].mean())
                    st.write("Missing value have been Filled!")
        
        # Keep specific columns to keep or Convert   
        st.subheader("🎯 Select Columns to convert")
        columns=st.multiselect(f"Chose columns for {file.name}",df.columns,default=df.columns)
        df=df[columns]

        # Create some visualizations
        st.subheader("💾 Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

        # Convert the file -> CSV to Excel
        st.subheader("🔁 Coversion Options ")
        coversion_type=st.radio(f"Convert {file.name} to:",["CSV","Excel"],key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer=BytesIO()
            if coversion_type== "Excel":
                df.to_excel(buffer,index=False)
                file_name=file.name.replace(file_ext,".xlsx")
                mime_type="application/vnd.opnexmlformats-officedocument.spreadsheetml.sheet"
            elif coversion_type=="CSV":
                df.to_csv(buffer,index=False)
                file_name=file.name.replace(file_ext,".csv")
                mime_type="text/csv"
            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"⬇️ Download {file.name} as {coversion_type}",
                data=buffer.getvalue(),
                file_name=file_name,
                mime=mime_type,

            )
st.success("🎉 All file processed!")