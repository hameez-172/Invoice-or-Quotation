import streamlit as st
from fpdf import FPDF
from datetime import date

# PDF Class with Colors and Logo
class InvoicePDF(FPDF):
    def header(self):
        # Background Header Color
        self.set_fill_color(0, 51, 102) # Navy Blue
        self.rect(0, 0, 210, 35, 'F')
        
        # Logo
        try:
            self.image('logo.png', 10, 8, 20)
        except:
            pass
            
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 20)
        self.cell(0, 15, 'BADAR DIAGNOSTICS', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, 'Medical Equipments & Diagnostic Solutions', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-40)
        self.set_draw_color(0, 51, 102)
        self.line(10, 255, 200, 255)
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 5, 'Lahore | Okara | Rawalpindi | Bahawalpur', 0, 1, 'C')
        self.cell(0, 5, 'Faysal Bank: 0155007000005585 | Contact: 0300-7303020', 0, 1, 'C')
        self.set_font('Arial', 'B', 9)
        self.cell(0, 10, 'Stamp: __________________________', 0, 1, 'R')

# Streamlit App
st.set_page_config(page_title="Badar Diagnostics Generator")
st.title("📄 Invoice & Quotation Generator")

doc_type = st.selectbox("Document Type", ["Quotation", "Invoice"])
client_name = st.text_input("Client Name")

if 'products' not in st.session_state: st.session_state.products = []

col1, col2, col3, col4 = st.columns(4)
with col1: p_name = st.text_input("Product")
with col2: p_desc = st.text_input("Desc")
with col3: p_qty = st.number_input("Qty", 1)
with col4: p_price = st.number_input("Price", 0.0)

if st.button("Add Product"):
    st.session_state.products.append({"name": p_name, "desc": p_desc, "qty": p_qty, "price": p_price})

if st.session_state.products:
    st.table(st.session_state.products)

terms = st.text_area("Terms & Conditions")

if st.button("Generate Final PDF"):
    pdf = InvoicePDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, doc_type, 0, 1, 'L')
    pdf.cell(0, 10, f"Date: {date.today()} | Client: {client_name}", 0, 1, 'L')
    
    # Colorful Table Header
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(40, 10, "Product", 1, 0, 'C', 1)
    pdf.cell(70, 10, "Description", 1, 0, 'C', 1)
    pdf.cell(20, 10, "Qty", 1, 0, 'C', 1)
    pdf.cell(30, 10, "Price", 1, 0, 'C', 1)
    pdf.cell(30, 10, "Total", 1, 1, 'C', 1)
    
    pdf.set_text_color(0, 0, 0)
    grand_total = 0
    for p in st.session_state.products:
        total = p['qty'] * p['price']
        grand_total += total
        pdf.cell(40, 10, p['name'], 1)
        pdf.cell(70, 10, p['desc'], 1)
        pdf.cell(20, 10, str(p['qty']), 1, 0, 'C')
        pdf.cell(30, 10, str(p['price']), 1, 0, 'C')
        pdf.cell(30, 10, str(total), 1, 1, 'C')
    
    pdf.cell(160, 10, "Grand Total", 1, 0, 'R')
    pdf.cell(30, 10, str(grand_total), 1, 1, 'C')
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Terms & Conditions:", 0, 1)
    pdf.set_font("Arial", '', 10)
    pdf.multi_cell(0, 5, terms)
    
    pdf.output("final.pdf")
    with open("final.pdf", "rb") as f:
        st.download_button("Download Final PDF", f, file_name="final.pdf")
