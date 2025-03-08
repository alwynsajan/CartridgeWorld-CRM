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

    heading = Paragraph(f"<para align='left'><b><font name='Helvetica-Bold' size='28'>K.P.K ASSOCIATES</font></b></para>", styles["Normal"])
    elements.append(heading)
    elements.append(Spacer(1, 0.3 * inch))

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
    storeStyle.leading = 12  # Adjust this value for more space

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

    # Billing Information Table
    billToStyle = ParagraphStyle(name="billToStyle", parent=styles["Normal"], fontSize=10, spaceAfter=5)

    customerDetails = []
    if customerData.get("Name"):
        customerDetails.append(customerData['Name'])
    if customerData.get("Address"):
        customerDetails.append(f" {customerData['Address']}, {customerData['State']}")
    if customerData.get("ABN"):
        customerDetails.append(f"Customer ABN: {customerData['ABN']}")

    billData = [
        [Paragraph("<b>Bill To:</b>", billToStyle)],  # First row: "Bill To"
        [Paragraph("<br/>".join(customerDetails), styles["Normal"])]  # Second row: Customer details
    ]

    billTable = Table(billData, colWidths=[6.5 * inch], rowHeights=[0.3 * inch, 0.7 * inch])  # Fixed row sizes
    billTable.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("VALIGN", (0, 1), (-1, -1), "TOP")
    ]))

    elements.append(billTable)
    elements.append(Spacer(1, 0.2 * inch))  # Adjust spacing below the bill-to section


    # Define the proportions for the column widths
    total_width = 6.5 * inch  # Total width of the table in inches
    item_column_width = total_width * 0.4  # 40% for the 'Item' column
    other_column_width = total_width * 0.15  # 15% for other columns

    # Define a custom paragraph style with reduced line spacing
    customItemStyle = ParagraphStyle(
        name="customItemStyle",
        parent=styles["Normal"],
        leading=12  # Reduce line spacing
    )

    items = [["Item", "Qty", "Unit Price", "GST Amount", "Total Price"]]
    calculatedItems, subtotal, totalGst, total = calculateItemPrices(productData)

    # Wrap the item name with the new paragraph style
    for idx, item in enumerate(calculatedItems):
        item[0] = Paragraph(item[0], customItemStyle)  # Apply custom style to reduce spacing

    items.extend(calculatedItems)


    # Adjust the item table
    itemsTable = Table(items, colWidths=[item_column_width, other_column_width, other_column_width, other_column_width, other_column_width])

    # Apply table styles with increased header spacing and thicker lines
    itemsTable.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("LINEABOVE", (0, 1), (-1, 1), 1, colors.black),
        ("LINEBELOW", (0, -1), (-1, -1), 1, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 1), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 1), (-1, -1),2.5 )
    ]))

    elements.append(itemsTable)
    elements.append(Spacer(1, 0.1 * inch))

    centeredStyle = ParagraphStyle(name="centeredStyle", parent=styles["Normal"], alignment=TA_CENTER)

    subtotal_data = [
    [Paragraph("<b>Sub Total ex GST</b>", styles["Normal"]), "", "", Paragraph(f"<b>${subtotal:.2f}</b>", centeredStyle), ""],
    [Paragraph("<b>GST</b>", styles["Normal"]), "", "", Paragraph(f"<b>${totalGst:.2f}</b>", centeredStyle), ""],
    [Paragraph("<b>TOTAL SALE inc GST</b>", styles["Normal"]), "", "", Paragraph(f"<b>${total:.2f}</b>", centeredStyle), ""]
]

    subtotal_table = Table(subtotal_data, colWidths=[item_column_width, other_column_width, other_column_width, other_column_width, other_column_width])
    subtotal_table.setStyle(TableStyle([
        ("TOPPADDING", (0, 0), (-1, -1), 0),  # Reduce top padding
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0)  # Reduce bottom padding
    ]))

    elements.append(subtotal_table)
    elements.append(Spacer(1, 0.3 * inch))  # Adjust the spacing as needed

    # Define a new style with increased line spacing
    footerStyle = styles["Normal"]
    footerStyle.leading = 16  # Adjust this value to increase spacing between lines

    footer_data = [
    [Paragraph("Thank you for shopping with Cartridge World.<br/>Please return empty cartridges for our Cartridges for PlanetARK recycling program.", footerStyle)],
    [Paragraph("<b>Payment Details:</b><br/><b>AC Name - K.P.K Associates</b><br/><b>BSB - 036 058</b><br/><b>AC Number - 089452</b>", footerStyle)],
    [Paragraph("OUR VISION: To create environmentally sustainable workplaces where reusing and recycling is the norm.", footerStyle)]
]


    footer_table = Table(footer_data, colWidths=[6.5 * inch])
    footer_table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),  # Space below each row
        ("TOPPADDING", (0, 0), (-1, -1), 2.5)     # Space above each row
    ]))

    elements.append(footer_table)

    pdf.build(elements)
    print(f"Invoice generated: {invoiceFilename}")

    return invoiceFilename


# selectedCustomerDetails = {'Customer ID': 4, 'Customer Type': 'Business', 'Name': 'Coles', 'Address': 'Subi Street', 'State': 'WA', 'Postcode': '12234', 'Phone': '2345678', 'Email': 'coles@subi.com', 'ABN': '1234567'}

# finalProductList = [{'Brand': 'Cartridge World HP Cartridge World HP Cartridge World HP', 'Name': 'H768XLC', 'Product Type': None, 'Price': 67.0, 'Quantity': 1},{'Brand': 'CW HP', 'Name': 'H768XLC', 'Product Type': None, 'Price': 67.0, 'Quantity': 1}]

# invoiceFilename = generateInvoice(selectedCustomerDetails, finalProductList, 10)


