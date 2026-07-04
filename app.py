import streamlit as st
from fpdf import FPDF
from datetime import date

# PDF Class
class InvoicePDF(FPDF):
    def header(self):
        # Top Blue Strip
        self.set_fill_color(0, 153, 224)
        self.rect(0, 0, 210, 25, 'F')
        
        # Company Name
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 18)
        self.cell(0, 15, 'Badar Diagnostics & Medical Equipments', 0, 1, 'R')
        self.ln(15)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-35)
        # Bottom Blue Strip
        self.set_fill_color(0, 153, 224)
        self.rect(0, 260, 210, 37, 'F')
        
        # Footer Text
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', '', 8)
        self.multi_cell(0, 5, 'Lahore Office: D Block Nawab Town, Lahore  |  Okara Office: Adjacent Ibn-e-Sina Lab, Opposite DHQ, Okara\nPindi Office: Commercial Market, Rawalpindi.  |  Bahawalpur Office: Model Town C, Bahawalpur\n0300-7303020, 0334-7303020   E-mail: munir.badar1@gmail.com', 0, 'C')

# Streamlit App
st.title("📄 Document Generator")

doc_type = st.selectbox("Document Type", ["Quotation", "Invoice"])
client_name = st.text_input("Client Name")
ref_no = st.text_input("Reference No", "QTR/BD/")

if 'products' not in st.session_state: st.session_state.products = []

col1, col2, col3, col4 = st.columns(4)
with col1: p_name = st.text_input("Product")
with col2: p_desc = st.text_input("Description")
with col3: p_qty = st.number_input("Qty", 1)
with col4: p_price = st.number_input("Price Unit", 0.0)

if st.button("Add Product"):
    st.session_state.products.append({"name": p_name, "desc": p_desc, "qty": p_qty, "price": p_price})

if st.session_state.products:
    st.table(st.session_state.products)

terms = st.text_area("Terms & Conditions")

if st.button("Generate Final PDF"):
    pdf = InvoicePDF()
    pdf.add_page()
    
    # Header Details
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(100, 10, f"No. {ref_no}", 0, 0)
    pdf.cell(0, 10, f"Date: {date.today()}", 0, 1, 'R')
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, client_name, 0, 1)
    pdf.cell(0, 10, doc_type, 0, 1, 'C')
    
    # Table Header
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(10, 10, "SR#", 1)
    pdf.cell(40, 10, "Product", 1)
    pdf.cell(60, 10, "Description", 1)
    pdf.cell(20, 10, "Qty", 1)
    pdf.cell(30, 10, "Price", 1)
    pdf.cell(30, 10, "Total", 1, 1)
    
    # Table Body
    grand_total = 0
    for i, p in enumerate(st.session_state.products, 1):
        total = p['qty'] * p['price']
        grand_total += total
        pdf.set_font("Arial", '', 10)
        pdf.cell(10, 10, str(i), 1)
        pdf.cell(40, 10, p['name'], 1)
        pdf.cell(60, 10, p['desc'], 1)
        pdf.cell(20, 10, str(p['qty']), 1, 0, 'C')
        pdf.cell(30, 10, str(p['price']), 1, 0, 'C')
        pdf.cell(30, 10, str(total), 1, 1, 'C')
    
    # Terms
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 10, "Terms & Conditions:", 0, 1)
    pdf.set_font("Arial", '', 10)
    pdf.multi_cell(0, 5, terms)
    
    # Account Details Footer section inside body
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 5, "Regards,", 0, 1)
    pdf.cell(0, 5, "Badar Diagnostics & Medical Equipment", 0, 1)
    pdf.cell(0, 5, "Faysal Bank: 0155007000005585", 0, 1)
    
    pdf.output("document.pdf")
    with open("document.pdf", "rb") as f:
        st.download_button("Download PDF", f, file_name="document.pdf")
