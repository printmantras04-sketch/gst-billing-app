import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Online Billing & GST Assistant", layout="wide")

st.title("📈 Online Billing & GST Assistant")
st.write("Apna bill generate karein aur GST data auto-save karein.")

# Data storage ke liye Excel file ka setup
FILE_NAME = "gst_sales_data.xlsx"
if not os.path.exists(FILE_NAME):
    df_empty = pd.DataFrame(columns=["Invoice No", "Date", "Customer Name", "Customer GSTIN", "Item Description", "Taxable Value", "GST Rate", "CGST", "SGST", "Total Amount"])
    df_empty.to_excel(FILE_NAME, index=False)

# Do columns banayein: Left me Input, Right me Bill Preview
col1, col2 = st.columns([1, 1])

with col1:
    st.header("📋 Entry Form")
    cust_name = st.text_input("Customer Name")
    cust_gstin = st.text_input("Customer GSTIN (Optional)")
    item_desc = st.text_input("Item / Service Description")
    taxable_value = st.number_input("Taxable Value (₹)", min_value=0.0, step=100.0, value=0.0)
    gst_rate = st.selectbox("GST Rate (%)", [0, 5, 12, 18, 28], index=3)
    
    # Auto Calculations
    gst_amount = taxable_value * (gst_rate / 100)
    cgst = gst_amount / 2
    sgst = gst_amount / 2
    total_amount = taxable_value + gst_amount
    
    invoice_no = f"INV-{int(datetime.now().timestamp())}"
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if st.button("Generate & Save Bill", type="primary"):
        if cust_name and taxable_value > 0:
            # Naya data read aur append karna
            df = pd.read_excel(FILE_NAME)
            new_row = {
                "Invoice No": invoice_no, "Date": current_date, "Customer Name": cust_name,
                "Customer GSTIN": cust_gstin, "Item Description": item_desc, 
                "Taxable Value": taxable_value, "GST Rate": gst_rate, 
                "CGST": cgst, "SGST": sgst, "Total Amount": total_amount
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_excel(FILE_NAME, index=False)
            st.success("Bill successfully save ho gaya!")
        else:
            st.error("Please Customer Name aur Taxable Value sahi se bharein.")

with col2:
    st.header("📄 Invoice Preview")
    st.markdown(f"""
    **Invoice No:** {invoice_no}  
    **Date:** {current_date}  
    **Customer:** {cust_name}  
    **GSTIN:** {cust_gstin}  
    ---
    **Item:** {item_desc}  
    **Taxable Value:** ₹{taxable_value:,.2f}  
    **GST Rate:** {gst_rate}%  
    ---
    **CGST (Auto):** ₹{cgst:,.2f}  
    **SGST (Auto):** ₹{sgst:,.2f}  
    ### **Total Amount:** ₹{total_amount:,.2f}
    """)

# GST Report Section (Download for filing)
st.markdown("---")
st.header("📊 GST Filing Report")
df_report = pd.read_excel(FILE_NAME)
st.dataframe(df_report)

# Ek click me GST ready excel download karein
with open(FILE_NAME, "rb") as file:
    st.download_button(
        label="📥 Download GST Report (Excel)",
        data=file,
        file_name="GST_Filing_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
