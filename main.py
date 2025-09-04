import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#Title
st.title("BAAP KA PAISA AND RELATED OVERTHINKING")

#No. of variables
num_assets = st.number_input("How many assets would you like to work with?", min_value=1, max_value=20, step=1)

assets = []
for i in range(int(num_assets)):
    st.subheader(f"Asset{i+1}")
    name = st.text_input(f"Name of the Asset {i+1}", key=f"name_{i}")
    current_value = st.number_input(f"Current value of {name}", min_value=0.00, step=100.0, key=f"value_{i}")
    rate_of_return = st.number_input(f"Expected Rate of Return (%) on {name}", min_value=0.0, step=0.1, key=f"rate_{i}")
    assets.append({"name": name, "current": current_value, "rate": rate_of_return})

#Years for projection
years = st.slider("Number of years to project", min_value=1, max_value=40, value=10)

if st.button("Show Projection"):
    if all(asset["name"] and asset["current"] > 0 for asset in assets):
        #DataFrames(using Pandas)
        projections = {}
        t = np.arange(0, years+1)

        for asset in assets:
            fv = asset["current"] * (1 + asset["rate"]/100) ** t
            projections[asset["name"]] = fv

        df = pd.DataFrame(projections, index=t)
        df.index.name = "Year"

        #Line Chart
        st.subheader("Growth over time")
        st.line_chart(df)

        #Final Year Values for Pie Chart
        final_values = df.iloc[-1]
        fig, ax = plt.subplots()
        ax.pie(final_values, labels=final_values.index, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.subheader(f"Portfolio Composition after {years} Years")
        st.pyplot(fig)

        #Table
        st.subheader("Values in Future")
        st.dataframe(df)

        #Download Excel
        excel_file = pd.ExcelWriter("Portfolio Projection.xlsx", engine="xlsxwriter")
        df.to_excel(excel_file, sheet_name="Projection")
        excel_file.close()
        with open("Portfolio Projection.xlsx", "rb") as f:
            st.download_button("⬇️ Download as Excel", data=f, file_name="Portfolio Projection.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    else:
        st.warning("Please fill in Asset Names and Current Values")