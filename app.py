import streamlit as st
from fpdf import FPDF
from datetime import date
import random

# FPDF2 Class
class InvoicePDF(FPDF):
    def header(self):
        # Top Blue Strip
        self.set_fill_color(0, 153, 224)
        self.rect(0, 0, 210, 25, 'F')
        # Company Name
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 18)
        self.cell(0, 15, 'Badar Diagnostics & Medical Equipments', 0, 1, 'R')
        self.ln(10)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-37)
        # Bottom Blue Strip
        self.set_fill_color(0, 153, 224)
        self.rect(0, 260, 210, 37, 'F')
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', '', 8)
        self.multi_cell(0, 5, 'Lahore Office: D Block Nawab Town, Lahore | Okara Office: Adjacent Ibn-e-Sina Lab, Opposite DHQ, Okara\nPindi Office: Commercial Market, Rawalpindi. | Bahawalpur Office: Model Town C, Bahawalpur\n0300-7303020, 0334-7303020 E-mail: munir.badar1@gmail.com', 0, 'C')

# App UI
st.title("📄 Professional Generator")

if 'products' not in st.session_state: st.session_state.products = []

doc_type = st.selectbox("Document Type", ["Quotation", "Invoice"])
client_name = st.text_input("Client Name")

p_name = st.text_input("Product")
p_desc = st.text_input("Description")
p_qty = st.number_input("Qty", 1)
p_price = st.number_input("Unit Price", 0.0)

if st.button("Add Product"):
    st.session_state.products.append({"name": p_name, "desc": p_desc, "qty": p_qty, "price": p_price})

if st.button("Generate Final PDF"):
    pdf = InvoicePDF()
    pdf.add_page()
    
    # Auto Fields
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(100, 10, f"No. QTR/BD/{random.randint(1000, 9999)}", 0, 0)
    pdf.cell(0, 10, f"Date: {date.today().strftime('%d/%m/%Y')}", 0, 1, 'R')
    
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, client_name, 0, 1)
    pdf.cell(0, 10, doc_type, 0, 1, 'C')
    
    # Table Header
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(10, 10, "SR#", 1, 0, 'C', 1)
    pdf.cell(40, 10, "PRODUCT", 1, 0, 'C', 1)
    pdf.cell(60, 10, "DESCRIPTION", 1, 0, 'C', 1)
    pdf.cell(20, 10, "QTY", 1, 0, 'C', 1)
    pdf.cell(30, 10, "PRICE", 1, 0, 'C', 1)
    pdf.cell(30, 10, "TOTAL", 1, 1, 'C', 1)
    
    # Rows
    for i, p in enumerate(st.session_state.products, 1):
        total = p['qty'] * p['price']
        pdf.cell(10, 10, str(i), 1, 0, 'C')
        pdf.cell(40, 10, p['name'], 1)
        pdf.cell(60, 10, p['desc'], 1)
        pdf.cell(20, 10, str(p['qty']), 1, 0, 'C')
        pdf.cell(30, 10, str(p['price']), 1, 0, 'C')
        pdf.cell(30, 10, str(total), 1, 1, 'C')
        
    pdf.output("final.pdf")
    with open("final.pdf", "rb") as f:
        st.download_button("Download PDF", f, file_name="final.pdf")
