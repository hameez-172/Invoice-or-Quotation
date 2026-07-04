import streamlit as st
from fpdf import FPDF
from datetime import date

# 1. PDF Class (Header aur Footer yahan fix hain)
class InvoicePDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 18)
        self.cell(0, 10, 'BADAR DIAGNOSTICS & MEDICAL EQUIPMENTS', 0, 1, 'C')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, 'Lahore | Okara | Rawalpindi | Bahawalpur', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-45)
        self.set_font('Arial', 'B', 10)
        self.cell(0, 5, 'Account Details:', 0, 1, 'L')
        self.set_font('Arial', '', 9)
        self.cell(0, 5, 'Badar Diagnostics & Medical Equipments | Faysal Bank: 0155007000005585', 0, 1, 'L')
        self.cell(0, 5, 'Contact: 0300-7303020 | 0334-7303020', 0, 1, 'L')
        self.cell(0, 5, 'Stamp: __________________________', 0, 1, 'R')

# 2. UI Configuration
st.title("Badar Diagnostics Generator")
doc_type = st.selectbox("Document Type", ["Quotation", "Invoice"])
client_name = st.text_input("Client Name (e.g. Mujahid Hospital Faisalabad)")

# Product Table Input
st.subheader("Add Products")
if 'products' not in st.session_state:
    st.session_state.products = []

col1, col2, col3, col4 = st.columns(4)
with col1: prod_name = st.text_input("Product")
with col2: desc = st.text_input("Desc")
with col3: qty = st.number_input("Qty", 1)
with col4: price = st.number_input("Price", 0.0)

if st.button("Add Product to List"):
    st.session_state.products.append({"name": prod_name, "desc": desc, "qty": qty, "price": price})

# Table Display
if st.session_state.products:
    st.table(st.session_state.products)

terms = st.text_area("Terms & Conditions")

# 3. PDF Generation Logic
if st.button("Generate Final PDF"):
    pdf = InvoicePDF()
    pdf.add_page()
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, doc_type, 0, 1, 'L')
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 10, f"Client: {client_name}", 0, 1, 'L')
    pdf.ln(5)

    # Table Header
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(40, 10, "Product", 1, 0, 'C', 1)
    pdf.cell(70, 10, "Description", 1, 0, 'C', 1)
    pdf.cell(20, 10, "Qty", 1, 0, 'C', 1)
    pdf.cell(30, 10, "Price", 1, 0, 'C', 1)
    pdf.cell(30, 10, "Total", 1, 1, 'C', 1)

    # Rows (Table logic)
    grand_total = 0
    pdf.set_font("Arial", '', 10)
    for p in st.session_state.products:
        row_total = p['qty'] * p['price']
        grand_total += row_total
        pdf.cell(40, 10, p['name'], 1)
        pdf.cell(70, 10, p['desc'], 1)
        pdf.cell(20, 10, str(p['qty']), 1, 0, 'C')
        pdf.cell(30, 10, str(p['price']), 1, 0, 'C')
        pdf.cell(30, 10, str(row_total), 1, 1, 'C')

    pdf.cell(160, 10, "Grand Total", 1, 0, 'R')
    pdf.cell(30, 10, str(grand_total), 1, 1, 'C')
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 10, "Terms & Conditions:", 0, 1)
    pdf.set_font("Arial", '', 9)
    pdf.multi_cell(0, 5, terms)
    
    pdf.output("final_doc.pdf")
    with open("final_doc.pdf", "rb") as f:
        st.download_button("Download PDF", f, file_name="document.pdf")
