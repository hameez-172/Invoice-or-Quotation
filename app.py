import streamlit as st
from fpdf import FPDF
from datetime import date
import random
import os

st.set_page_config(page_title="Professional Invoice Generator", layout="centered")

class InvoicePDF(FPDF):
    def header(self):
        # Top blue strips
        self.set_fill_color(0, 51, 102)
        self.rect(10, 8, 22, 8, "F")
        self.set_fill_color(0, 153, 224)
        self.rect(35, 8, 165, 8, "F")
        
        # Logo
        if os.path.exists("lo.png"):
            self.image("lo.png", x=8, y=17, w=30)

        # Company Name
        self.set_xy(42, 20)
        self.set_font("Arial", "B", 20)
        self.set_text_color(20, 40, 80)
        self.cell(0, 10, "Badar Diagnostics & Medical Equipments")
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_fill_color(0, 51, 102)
        self.rect(10, 265, 190, 15, "F")
        self.set_fill_color(0, 153, 224)
        self.rect(10, 280, 190, 8, "F")
        self.set_y(268)
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", "", 7)
        footer_text = (
            "Lahore Office: D Block Nawab Town, Lahore    "
            "Okara Office: Adjacent Ibn-e-Sina Lab, Opposite DHQ, Okara | "
            "Pindi Office: Commercial Market, Rawalpindi | "
            "Bahawalpur Office: Model Town C, Bahawalpur"
        )
        self.multi_cell(0, 4, footer_text, align="C")
        self.set_y(281)
        self.cell(0, 4, "0300-7303020, 0334-7303020     E-mail: munir.badar1@gmail.com", align="C")

st.title("📄 Professional Invoice / Quotation Generator")

# Sidebar for dynamic content
with st.sidebar:
    st.header("Document Settings")
    terms_input = st.text_area("Terms & Conditions", "1. 80% advance and 20% at the time of delivery.\n2. Prices are subject to change without notice.")
    account_input = st.text_area("Account Details", "Bank Name: \nAccount Title: \nAccount No: ")

if "products" not in st.session_state:
    st.session_state.products = []

doc_type = st.selectbox("Document Type", ["Quotation", "Invoice"])
client_name = st.text_input("Client Name")

st.subheader("Add Product")
p_name = st.text_input("Product Name")
p_desc = st.text_input("Description")
p_qty = st.number_input("Quantity", min_value=1, value=1)
p_price = st.number_input("Unit Price", min_value=0.0)

if st.button("Add Product"):
    st.session_state.products.append({
        "name": p_name, "desc": p_desc, "qty": p_qty, "price": p_price
    })
    st.success("Product Added")

if st.session_state.products:
    st.subheader("Products List")
    for i, p in enumerate(st.session_state.products, 1):
        st.write(f"{i}. {p['name']} - {p['qty']} x {p['price']}")

if st.button("Generate PDF"):
    pdf = InvoicePDF()
    pdf.add_page()
    
    # Header Details
    pdf.set_font("Arial", "", 10)
    number = f"QTR/BD/{random.randint(10000,99999)}"
    pdf.set_xy(15, 45)
    pdf.cell(0, 5, f"No. {number}")
    pdf.set_xy(160, 45)
    pdf.cell(0, 5, f"Date: {date.today().strftime('%d/%m/%Y')}")

    pdf.set_draw_color(0, 153, 224)
    pdf.line(15, 50, 55, 50)
    pdf.line(155, 50, 195, 50)

    pdf.set_xy(15, 58)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 6, f"To: {client_name}")

    pdf.set_xy(0, 68)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(210, 8, doc_type.upper(), align="C")

    # Table
    y = 85
    pdf.set_xy(25, y)
    pdf.set_font("Arial", "B", 9)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(15, 8, "SR #", 1, 0, "C", True)
    pdf.cell(45, 8, "PRODUCT", 1, 0, "C", True)
    pdf.cell(40, 8, "DESCRIPTION", 1, 0, "C", True)
    pdf.cell(15, 8, "QTY", 1, 0, "C", True)
    pdf.cell(25, 8, "PRICE", 1, 0, "C", True)
    pdf.cell(25, 8, "TOTAL", 1, 1, "C", True)

    pdf.set_font("Arial", "", 9)
    grand_total = 0
    for i, p in enumerate(st.session_state.products, 1):
        total = p["qty"] * p["price"]
        grand_total += total
        pdf.set_x(25)
        pdf.cell(15, 8, str(i), 1, 0, "C")
        pdf.cell(45, 8, p["name"], 1)
        pdf.cell(40, 8, p["desc"], 1)
        pdf.cell(15, 8, str(p["qty"]), 1, 0, "C")
        pdf.cell(25, 8, f"{p['price']:.0f}", 1, 0, "C")
        pdf.cell(25, 8, f"{total:.0f}", 1, 1, "C")

    pdf.set_x(125)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(40, 8, "Grand Total", 1, 0, "C", True)
    pdf.cell(25, 8, str(grand_total), 1, 1, "C", True)

    # Left Section: Terms & Account Details
    y_pos = pdf.get_y() + 15
    pdf.set_xy(15, y_pos)
    
    # Terms (Size 12)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "Terms & Conditions:", ln=1)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(100, 7, terms_input)
    
    # Account Details (Size 12)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "Account Details:", ln=1)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(100, 7, account_input)

    # Right Section: Stamp & Signature
    if os.path.exists("stamp.png"):
        pdf.image("stamp.png", x=140, y=y_pos + 10, w=50)
    
    pdf.set_xy(140, y_pos + 65)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(50, 6, "Authorized Signatory", align="C")

    pdf.output("final.pdf")
    with open("final.pdf", "rb") as file:
        st.download_button("📥 Download PDF", file, file_name=f"{doc_type}.pdf", mime="application/pdf")
