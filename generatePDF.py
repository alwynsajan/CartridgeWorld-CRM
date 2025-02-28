import json
import datetime
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Image, Spacer, Table, TableStyle, Paragraph
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

CONFIG_FILE = "config.json"

def getInvoiceNumber():
    # Load configuration
    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)
    
    invoiceNo = config.get("invoiceNumber", 1000)  # Default if not found
    newInvoiceNo = invoiceNo + 1
    
    # Update config with new invoice number
    config["invoiceNumber"] = newInvoiceNo
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)
    
    return invoiceNo

# Function to calculate item prices
def calculateItemPrices(productData):
    calculatedItems = []
    subtotal = 0
    totalGst = 0
    for item in productData:
        itemBrand = item['Brand']
        itemName = item['Name']
        quantity = item['Quantity']
        pricePerUnit = item['Price']
        gst = round(pricePerUnit * 0.10, 2)
        unitPrice = round(pricePerUnit - gst, 2)
        totalPrice = round((unitPrice + gst) * quantity, 2)
        subtotal += unitPrice * quantity
        totalGst += gst * quantity
        calculatedItems.append([(itemBrand + " "+ itemName), quantity, unitPrice, gst, totalPrice])
    total = subtotal + totalGst
    return calculatedItems, subtotal, totalGst, total

# Function to generate invoice
def generateInvoice(customerData, productData):
    invoiceNo = getInvoiceNumber()
    
    # Ensure the 'Invoices' directory exists
    invoicesDir = "Invoices"
    os.makedirs(invoicesDir, exist_ok=True)

    invoiceFilename = os.path.join(invoicesDir, f"invoice_{invoiceNo}.pdf")
    pdf = SimpleDocTemplate(invoiceFilename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # Store details
    heading = Paragraph(
        f"<para align='left'><b><font name='Helvetica-Bold' size='20'>K.P.K ASSOCIATES</font></b></para>",
        styles["Normal"]
    )
    elements.append(heading)
    elements.append(Spacer(1, 0.2 * inch))

    # Add Logo
    logoPath = "invoiceLogo.jpeg"  # Ensure this file exists
    try:
        logo = Image(logoPath, width=3 * inch, height=0.75 * inch)
        logo.hAlign = "LEFT"
        elements.append(logo)
    except Exception as e:
        print(f"Error loading image: {e}")

    elements.append(Spacer(1, 0.3 * inch))

    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)

    # Store and Invoice Details
    storeDetails = [
        [
            Paragraph(f"<b>{config['storeName']}</b><br/>Phone: {config['storePhone']}<br/>A.B.N. {config['storeABN']}", styles["Normal"]),
            Paragraph(f"<b>Tax Invoice</b><br/>Invoice No: {invoiceNo}<br/>Date: {datetime.datetime.now().strftime('%d/%m/%Y %I:%M:%S %p')}", styles["Normal"]),
        ]
    ]
    storeTable = Table(storeDetails, colWidths=[3.25 * inch, 3.25 * inch])
    storeTable.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP")
    ]))
    elements.append(storeTable)
    elements.append(Spacer(1, 0.3 * inch))

    # Customer Details (Skipping empty lines)
    customerLines = ["Bill To:"]
    customerLines.extend([str(customerData[key]) for key in ["Name", "Address", "State", "Postcode", "Phone"] if customerData.get(key)])
    
    billData = [[Paragraph("<br/>".join(customerLines), styles["Normal"])] ]
    billTable = Table(billData, colWidths=[6.5 * inch])
    billTable.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(billTable)
    elements.append(Spacer(1, 0.2 * inch))

    # Itemized Details
    items = [["Item", "Quantity", "Unit Price", "GST Amount", "Total Price"]]
    calculatedItems, subtotal, totalGst, total = calculateItemPrices(productData)
    items.extend(calculatedItems)
    itemsTable = Table(items, colWidths=[2 * inch, 1 * inch, 1 * inch, 1 * inch, 1.5 * inch])
    itemsTable.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("LINEBELOW", (0, 0), (-1, 0), 1, colors.black),
        ("LINEBELOW", (0, -1), (-1, -1), 1, colors.black),
        ("GRID", (0, 1), (-1, -1), 0, colors.white),
    ]))
    elements.append(itemsTable)
    subtotal_data = [["Sub Total ex GST", "", "", Paragraph(f"<b>${subtotal:.2f}</b>", styles["Normal"]), ""],
                     [Paragraph(f"<b>GST</b>",styles["Normal"]), "", "", Paragraph(f"<b>${totalGst:.2f}</b>", styles["Normal"]), ""],
                     [Paragraph(f"<b>TOTAL SALE inc GST</b>",styles["Normal"]), "", "", Paragraph(f"<b>${total:.2f}</b>", styles["Normal"]), ""]]
    subtotal_table = Table(subtotal_data, colWidths=[2 * inch, 1 * inch, 1 * inch,1 * inch, 1.5 * inch])
    subtotal_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("LINEBELOW", (0, 0), (-1, -1), 1, colors.white),
    ]))
    elements.append(subtotal_table)
    elements.append(Spacer(1, 0.2 * inch))
    
    # Footer Table
    footer_data = [
        [Paragraph("Thank you for shopping with Cartridge World. Please return empty cartridges for our Cartridges for PlanetARK recycling program.", styles["Normal"])],
        ["Payment Details:\nAC Name - K.P.K Associates\nBSB - 036 058\nAC Number - 089452"],
        [Paragraph("OUR VISION: To create environmentally sustainable workplaces where reusing and recycling is the norm.", styles["Normal"]) ]
    ]
    footer_table = Table(footer_data, colWidths=[6.5 * inch])
    footer_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    elements.append(footer_table)

    # Build the PDF
    pdf.build(elements)
    print(f"Invoice generated: {invoiceFilename}")

    return invoiceFilename

