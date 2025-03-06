import json
import datetime
import os
from tkinter import messagebox  # Assuming you're using tkinter for messageBox
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Image, Spacer, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle

CONFIG_FILE = "config.json"

def calculateUnitPriceAndGst(total_price, gst_rate=10):
    unit_price = total_price / (1 + gst_rate / 100)
    gst_amount = total_price - unit_price
    return round(unit_price,2), round(gst_amount,2)

def calculateItemPrices(productData):
    calculatedItems = []
    subtotal = 0
    totalGst = 0
    for item in productData:
        itemBrand = item['Brand']
        itemName = item['Name']
        quantity = item['Quantity']
        priceIncGst = item['Price']
        unitPrice, gstAmt = calculateUnitPriceAndGst(priceIncGst, 10)
        totalPrice = round(priceIncGst * quantity, 2)
        subtotal += round(unitPrice * quantity, 2)
        totalGst += round(gstAmt * quantity, 2)
        calculatedItems.append([(itemBrand + " " + itemName), quantity, unitPrice, gstAmt, totalPrice])
    total = subtotal + totalGst
    return calculatedItems, subtotal, totalGst, total

def generateInvoice(customerData, productData, invoiceNo):
    
    # Get the current month and year for the folder name
    current_month_year = datetime.datetime.now().strftime("%B_%Y")  # Example: "July_2025"
    
    # Create the directory for the current month if it doesn't exist
    invoicesDir = os.path.join("Invoices", current_month_year)
    os.makedirs(invoicesDir, exist_ok=True)

    invoiceFilename = os.path.join(invoicesDir, f"invoice_{invoiceNo}.pdf")
    pdf = SimpleDocTemplate(invoiceFilename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    heading = Paragraph(f"<para align='left'><b><font name='Helvetica-Bold' size='25'>K.P.K ASSOCIATES</font></b></para>", styles["Normal"])
    elements.append(heading)
    elements.append(Spacer(1, 0.2 * inch))

    try:
        logo = Image("invoiceLogo.jpeg", width=3 * inch, height=0.75 * inch)
        logo.hAlign = "LEFT"
        elements.append(logo)
    except Exception as e:
        print(f"Error loading image: {e}")

    elements.append(Spacer(1, 0.3 * inch))

    with open(CONFIG_FILE, "r") as file:
        config = json.load(file)

    # Increase the line spacing for the store details
    storeStyle = styles["Normal"]
    storeStyle.leading = 18  # Adjust this value for more space

    storeDetails = [
        [
            Paragraph(f"<b>{config['storeName']}</b><br/>Phone: {config['storePhone']}<br/>A.B.N. {config['storeABN']}", storeStyle),
            Paragraph(f"<b>Tax Invoice</b><br/>Invoice No: {invoiceNo}<br/>Date: {datetime.datetime.now().strftime('%d/%m/%Y %I:%M:%S %p')}", storeStyle),
        ]
    ]
    storeTable = Table(storeDetails, colWidths=[3.25 * inch, 3.25 * inch])
    storeTable.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "LEFT"), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(storeTable)
    elements.append(Spacer(1, 0.3 * inch))

    customerLines = ["Bill To:"]
    customerLines.extend([str(customerData[key]) for key in ["Name", "Address", "State", "Postcode", "Phone"] if customerData.get(key)])

    billData = [[Paragraph("<br/>".join(customerLines), styles["Normal"])]]
    billTable = Table(billData, colWidths=[6.5 * inch])
    billTable.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "LEFT"), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("GRID", (0, 0), (-1, -1), 0.5, colors.black)]))
    elements.append(billTable)
    elements.append(Spacer(1, 0.2 * inch))

    # Define the proportions for the column widths
    total_width = 6.5 * inch  # Total width of the table in inches
    item_column_width = total_width * 0.4  # 40% for the 'Item' column
    other_column_width = total_width * 0.15  # 15% for other columns

    items = [["Item", "Qty", "Unit Price", "GST Amount", "Total Price"]]
    calculatedItems, subtotal, totalGst, total = calculateItemPrices(productData)

    # Wrap the item name in a Paragraph with word wrapping
    for idx, item in enumerate(calculatedItems):
        # Wrap the item name to handle overflow
        item[0] = Paragraph(item[0], styles["Normal"])

    items.extend(calculatedItems)

    # Adjust the item table
    itemsTable = Table(items, colWidths=[item_column_width, other_column_width, other_column_width, other_column_width, other_column_width])

    # Apply the table style
    itemsTable.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),  # Center alignment for all columns
        ("ALIGN", (0, 0), (0, -1), "LEFT"),    # Left align the first column (Item)
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("LINEBELOW", (0, 0), (-1, 0), 1, colors.black),  # Line below header
        ("LINEBELOW", (0, -1), (-1, -1), 1, colors.black),  # Line below last row
        ("GRID", (0, 1), (-1, -1), 0, colors.white),  # White grid lines for readability
        ("VALIGN", (0, 0), (-1, -1), "TOP"),  # Vertically align content at the top
        ("TOPPADDING", (0, 0), (-1, -1), 0),  # Remove top padding
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),  # Remove bottom padding
        ("LEFTPADDING", (0, 0), (-1, -1), 0),  # Remove left padding
        ("RIGHTPADDING", (0, 0), (-1, -1), 0)  # Remove right padding
    ]))

    elements.append(itemsTable)


    centeredStyle = ParagraphStyle(name="centeredStyle", parent=styles["Normal"], alignment=TA_CENTER)

    subtotal_data = [
    [Paragraph("<b>Sub Total ex GST</b>", styles["Normal"]), "", "", Paragraph(f"<b>${subtotal:.2f}</b>", centeredStyle), ""],
    [Paragraph("<b>GST</b>", styles["Normal"]), "", "", Paragraph(f"<b>${totalGst:.2f}</b>", centeredStyle), ""],
    [Paragraph("<b>TOTAL SALE inc GST</b>", styles["Normal"]), "", "", Paragraph(f"<b>${total:.2f}</b>", centeredStyle), ""]
]


    # Set the colWidths to match with the previous table and ensure alignment
    subtotal_table = Table(subtotal_data, colWidths=[item_column_width, other_column_width, other_column_width, other_column_width, other_column_width])

    
    elements.append(subtotal_table)
    elements.append(Spacer(1, 0.2 * inch))  # Adjust the spacing as needed

    # Define a new style with increased line spacing
    footerStyle = styles["Normal"]
    footerStyle.leading = 18  # Adjust this value to increase spacing between lines

    footer_data = [
    [Paragraph("Thank you for shopping with Cartridge World. Please return empty cartridges for our Cartridges for PlanetARK recycling program.", footerStyle)],
    [Paragraph("<b>Payment Details:</b><br/><b>AC Name - K.P.K Associates</b><br/><b>BSB - 036 058</b><br/><b>AC Number - 089452</b>", footerStyle)],
    [Paragraph("OUR VISION: To create environmentally sustainable workplaces where reusing and recycling is the norm.", footerStyle)]
]


    footer_table = Table(footer_data, colWidths=[6.5 * inch])
    footer_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),  # Space below each row
        ("TOPPADDING", (0, 0), (-1, -1), 10)     # Space above each row
    ]))

    elements.append(footer_table)

    pdf.build(elements)
    print(f"Invoice generated: {invoiceFilename}")

    return invoiceFilename


# selectedCustomerDetails = {'Customer ID': 1, 'Customer Type': 'Personal', 'Name': 'Allwyn', 'Address': None, 'State': None, 'Postcode': None, 'Phone': None, 'Email': None, 'ABN': ''}

# finalProductList = [{'Brand': 'Cartridge World HP Cartridge World HP Cartridge World HP', 'Name': 'H768XLC', 'Product Type': None, 'Price': 67.0, 'Quantity': 1},{'Brand': 'CW HP', 'Name': 'H768XLC', 'Product Type': None, 'Price': 67.0, 'Quantity': 1}]

# invoiceFilename = generateInvoice(selectedCustomerDetails, finalProductList, 10)
# # printPDF(invoiceFilename)
