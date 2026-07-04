import streamlit as st
from fpdf import FPDF

# Custom PDF class
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Badar Diagnostics & Medical Equipments', 0, 1, 'C')

# Streamlit UI
st.title("Document Generator")

doc_type = st.radio("Select Type", ["Quotation", "Invoice"])
client_name = st.text_input("Client Name")
product = st.text_input("Product")
qty = st.number_input("Quantity", min_value=1)
price = st.number_input("Unit Price")

if st.button("Generate PDF"):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Adding details
    pdf.cell(200, 10, txt=f"Type: {doc_type}", ln=1)
    pdf.cell(200, 10, txt=f"Client: {client_name}", ln=1)
    pdf.cell(200, 10, txt=f"Product: {product} | Qty: {qty} | Total: {qty*price}", ln=1)
    
    # Footer with Contact/Bank Info
    pdf.ln(50)
    pdf.cell(0, 10, "Faysal Bank: 0155007000005585", ln=1)
    pdf.cell(0, 10, "Contact: 0334-0300-103020", ln=1)
    
    # Save/Download
    output_path = "document.pdf"
    pdf.output(output_path)
    
    with open(output_path, "rb") as f:
        st.download_button("Download PDF", f, file_name="document.pdf")