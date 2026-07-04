import streamlit as st
from fpdf import FPDF
from datetime import date
import random
import os

st.set_page_config(page_title="Professional Invoice Generator")

class InvoicePDF(FPDF):
    def header(self):
        # Top blue strips
        self.set_fill_color(0, 51, 102)
        self.rect(10, 8, 22, 8, "F")
        self.set_fill_color(0, 153, 224)
        self.rect(35, 8, 165, 8, "F")
        
        # Logo
        if os.path.exists("logo.png"):
            self.image("logo.png", x=8, y=10, w=30)

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
        footer = (
            "Lahore Office: D Block Nawab Town, Lahore    "
            "Okara Office: Adjacent Ibn-e-Sina Lab, Opposite DHQ, Okara\n"
            "Pindi Office: Commercial Market, Rawalpindi    "
            "Bahawalpur Office: Model Town C, Bahawalpur"
        )
        self.multi_cell(0, 4, footer, align="C")
        self.set_y(281)
        self.cell(0, 4, "0300-7303020, 0334-7303020     E-mail: munir.badar1@gmail.com", align="C")

st.title("📄 Professional Invoice / Quotation Generator")

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
    st.subheader("Products")
    for i, p in enumerate(st.session_state.products, 1):
        st.write(f"{i}. {p['name']} | {p['qty']} x {p['price']}")

if st.button("Generate PDF"):
    pdf = InvoicePDF()
    pdf.add_page()
    
    # Quotation No and Date
    pdf.set_font("Arial", "", 10)
    number = f"QTR/BD/{random.randint(10000,99999)}"
    pdf.set_xy(15, 45)
    pdf.cell(0, 5, f"No. {number}")
    pdf.set_xy(160, 45)
    pdf.cell(0, 5, f"Date: {date.today().strftime('%d/%m/%Y')}")

    # Blue lines
    pdf.set_draw_color(0, 153, 224)
    pdf.line(15, 50, 55, 50)
    pdf.line(155, 50, 195, 50)

    # Client Name
    pdf.set_xy(15, 58)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 6, client_name)

    # Document Title
    pdf.set_xy(0, 65)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(210, 8, doc_type, align="C")

    # Table Header
    y = 82
    pdf.set_xy(30, y)
    pdf.set_font("Arial", "B", 8)
    pdf.cell(15, 8, "SR #", 1, 0, "C")
    pdf.cell(45, 8, "PRODUCT", 1)
    pdf.cell(35, 8, "DESCRIPTION", 1)
    pdf.cell(15, 8, "QTY", 1, 0, "C")
    pdf.cell(25, 8, "PRICE", 1, 0, "C")
    pdf.cell(25, 8, "TOTAL", 1, 1, "C")

    # Products
    pdf.set_font("Arial", "", 8)
    grand_total = 0
    for i, p in enumerate(st.session_state.products, 1):
        total = p["qty"] * p["price"]
        grand_total += total
        pdf.set_x(30)
        pdf.cell(15, 8, str(i), 1, 0, "C")
        pdf.cell(45, 8, p["name"], 1)
        pdf.cell(35, 8, p["desc"], 1)
        pdf.cell(15, 8, str(p["qty"]), 1, 0, "C")
        pdf.cell(25, 8, f"{p['price']:.0f}", 1, 0, "C")
        pdf.cell(25, 8, f"{total:.0f}", 1, 1, "C")

    # Grand Total
    pdf.set_x(120)
    pdf.set_font("Arial", "B", 9)
    pdf.cell(40, 8, "Grand Total", 1, 0, "C")
    pdf.cell(25, 8, str(grand_total), 1, 1, "C")

    # Footer section
    pdf.set_xy(15, 145)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "Terms & Conditions:")
    pdf.set_xy(15, 152)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 6, "80% advance and 20% at the time of delivery.")

    pdf.set_xy(15, 175)
    pdf.set_font("Arial", "", 9)
    pdf.multi_cell(0, 5, "Regards,\nBadar Diagnostics &\nMedical Equipment\nLahore")

    pdf.set_xy(15, 205)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "Account Details :", ln=1)
    pdf.set_font("Arial", "", 9)
    pdf.cell(0, 5, "Badar Diagnostics & Medical Equipment", ln=1)
    pdf.cell(0, 5, "Faysal Bank", ln=1)
    pdf.cell(0, 5, "015500700005585", ln=1)

    pdf.output("final.pdf")
    with open("final.pdf", "rb") as file:
        st.download_button("📥 Download PDF", file, file_name=f"{doc_type}.pdf", mime="application/pdf")
