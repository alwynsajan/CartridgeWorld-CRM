import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image, ImageTk
from customtkinter import CTkImage
import csv
import os
import tkinter.messagebox as messageBox  # For displaying error message
import pandas as pd
from datetime import datetime

from dbClient import DbServer

# Set appearance mode to light
ctk.set_appearance_mode("light")

# Global variable to track if the 'Add Customer' window is open
addCustomerWindow = None
# Global variables to store selected customer details and selection window
selectedCustomerDetails = {}
selectionWindow = None
screen_width = None
screen_height = None
finalProductList = []
currentSLNo = 1

def openAddCustomerWindow(customerEntry,db):
    global addCustomerWindow,selectedCustomerDetails,screen_width,screen_height

    # Check if the window is already open
    if addCustomerWindow is not None and addCustomerWindow.winfo_exists():
        # If it's open, just focus on the existing window
        addCustomerWindow.focus_force()
        addCustomerWindow.lift()  # Bring it to the front
        return

    # Create the new popup window for adding customer details
    addCustomerWindow = ctk.CTkToplevel()  # New top-level window
    addCustomerWindow.title("Add New Customer")

    print("In add cust ",selectedCustomerDetails)

    # Calculate window dimensions
    window_width = int(screen_width * 0.5)
    window_height = int(screen_height * 0.7)

    # Center the window at the top-center of the screen
    xCoordinate = (screen_width - window_width) // 2
    yCoordinate = 50  # Slightly below the top of the screen

    # Set the geometry to center the window
    addCustomerWindow.geometry(f"{window_width}x{window_height}+{xCoordinate}+{yCoordinate}")

    # Disable window maximization
    addCustomerWindow.resizable(False, False)

    # Ensure the window is focused when opened
    addCustomerWindow.focus_force()
    addCustomerWindow.lift()  # Bring the window to the front
    addCustomerWindow.grab_set()  # Grab all events for this window

    # Create a grid layout with labels and entry fields in the same row
    row_index = 0

    # Frame for customer type radio buttons
    customerTypeFrame = ctk.CTkFrame(addCustomerWindow)
    customerTypeFrame.grid(row=row_index, column=0, columnspan=2, padx=10, pady=10, sticky="w")

    orgLabel = ctk.CTkLabel(customerTypeFrame, text="Customer Type:", font=("Times New Roman", 21))
    orgLabel.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # Variable to track the selected customer type (organisation or personal)
    customerTypeVar = tk.StringVar()

    orgRadioButton = ctk.CTkRadioButton(customerTypeFrame, text="Business", variable=customerTypeVar, value="Business",font=("Times New Roman", 21))
    orgRadioButton.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    personalRadioButton = ctk.CTkRadioButton(customerTypeFrame, text="Personal", variable=customerTypeVar, value="Personal",font=("Times New Roman", 21))
    personalRadioButton.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    row_index += 1

    # Customer name field
    nameLabel = ctk.CTkLabel(addCustomerWindow, text="Customer Name:", font=("Times New Roman", 21))
    nameLabel.grid(row=row_index, column=0, padx=10, pady=10, sticky="w")
    nameEntry = ctk.CTkEntry(addCustomerWindow, font=("Times New Roman", 12), width=int(window_width*0.7))  # Increased width
    nameEntry.grid(row=row_index, column=1, padx=10, pady=10, sticky="w")
    row_index += 1

    # Customer address field
    addressLabel = ctk.CTkLabel(addCustomerWindow, text="Address:", font=("Times New Roman", 21))
    addressLabel.grid(row=row_index, column=0, padx=10, pady=10, sticky="w")
    addressEntry = ctk.CTkEntry(addCustomerWindow, font=("Times New Roman", 12), width=int(window_width*0.7))  # Increased width
    addressEntry.grid(row=row_index, column=1, padx=10, pady=10, sticky="w")
    row_index += 1

    # State field
    stateLabel = ctk.CTkLabel(addCustomerWindow, text="State:", font=("Times New Roman", 21))
    stateLabel.grid(row=row_index, column=0, padx=10, pady=10, sticky="w")
    stateEntry = ctk.CTkEntry(addCustomerWindow, font=("Times New Roman", 12), width=int(window_width*0.7))  # Adjusted width
    stateEntry.grid(row=row_index, column=1, padx=10, pady=10, sticky="w")
    row_index += 1

    # Postcode field
    postcodeLabel = ctk.CTkLabel(addCustomerWindow, text="Postcode:", font=("Times New Roman", 21))
    postcodeLabel.grid(row=row_index, column=0, padx=10, pady=10, sticky="w")
    postcodeEntry = ctk.CTkEntry(addCustomerWindow, font=("Times New Roman", 12), width=int(window_width*0.7))  # Adjusted width
    postcodeEntry.grid(row=row_index, column=1, padx=10, pady=10, sticky="w")
    row_index += 1

    # Customer phone field
    phoneLabel = ctk.CTkLabel(addCustomerWindow, text="Phone Number:", font=("Times New Roman", 21))
    phoneLabel.grid(row=row_index, column=0, padx=10, pady=10, sticky="w")
    phoneEntry = ctk.CTkEntry(addCustomerWindow, font=("Times New Roman", 12), width=int(window_width*0.7))  # Increased width
    phoneEntry.grid(row=row_index, column=1, padx=10, pady=10, sticky="w")
    row_index += 1

    # Customer email field
    emailLabel = ctk.CTkLabel(addCustomerWindow, text="Email Address:", font=("Times New Roman", 21))
    emailLabel.grid(row=row_index, column=0, padx=10, pady=10, sticky="w")
    emailEntry = ctk.CTkEntry(addCustomerWindow, font=("Times New Roman", 12), width=int(window_width*0.7))  # Increased width
    emailEntry.grid(row=row_index, column=1, padx=10, pady=10, sticky="w")
    row_index += 1

    # ABN field
    abnLabel = ctk.CTkLabel(addCustomerWindow, text="ABN (if applicable):", font=("Times New Roman", 21))
    abnLabel.grid(row=row_index, column=0, padx=10, pady=10, sticky="w")
    abnEntry = ctk.CTkEntry(addCustomerWindow, font=("Times New Roman", 12), width=int(window_width*0.7))  # Increased width
    abnEntry.grid(row=row_index, column=1, padx=10, pady=10, sticky="w")
    row_index += 1

    # Save button to save the customer info
    saveButton = ctk.CTkButton(addCustomerWindow, text="Save and Exit", font=("Times New Roman", 21),fg_color= "#393939",hover_color="#252523",command=lambda: saveCustomer(customerTypeVar, nameEntry, addressEntry, stateEntry, postcodeEntry, phoneEntry, emailEntry, abnEntry,customerEntry,db),width=int(screen_width * 0.15))
    saveButton.grid(row=row_index, columnspan=2, pady=20)

    def clearAllEntries():
        customerTypeVar.set("")  
        nameEntry.delete(0, tk.END)
        addressEntry.delete(0, tk.END)
        stateEntry.delete(0, tk.END)
        postcodeEntry.delete(0, tk.END)
        phoneEntry.delete(0, tk.END)
        emailEntry.delete(0, tk.END)
        abnEntry.delete(0, tk.END)

    # Clear All button
    clearButton = ctk.CTkButton(addCustomerWindow, text="Clear All", font=("Times New Roman", 21), fg_color= "#e62739",hover_color="#a93226",command=clearAllEntries, width=int(screen_width * 0.15))
    clearButton.grid(row=row_index+1, columnspan=2, pady=20)

def saveCustomer(customerTypeVar, nameEntry, addressEntry, stateEntry, postcodeEntry, phoneEntry, emailEntry, abnEntry,customerEntry,db):

    global selectedCustomerDetails

    # Collecting the data from the form fields
    customerType = customerTypeVar.get()  # Get the selected customer type
    name = nameEntry.get()

    # Validate if the name field is empty
    if not name.strip():  # Check if the name is empty or only contains spaces
        messageBox.showerror("Input Error", "Customer Name cannot be empty!")
        return  # Exit the function without saving the data
    
    address = addressEntry.get()
    state = stateEntry.get()
    postcode = postcodeEntry.get()
    phone = phoneEntry.get()
    email = emailEntry.get()
    abn = abnEntry.get()

    selectedCustomerDetails = {"Name":name, "Phone":phone,"Address":address}
    customerEntry.delete(0, "end")
    customerEntry.insert(0, f"Name: {selectedCustomerDetails['Name']}")

    print("Selected Customer details : ",selectedCustomerDetails)

    # Prepare the data to write to the CSV
    customer_data = [customerType, name, address, state, postcode, phone, email, abn]

    # Write data to the CSV file
    try:
        # Define the file path inside the 'Data' folder
        data_folder = "Data"
        file_path = os.path.join(data_folder, "customerDetails.csv")

        # Ensure the 'Data' folder exists
        os.makedirs(data_folder, exist_ok=True)
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Check if the file is empty and write the header if necessary
            if file.tell() == 0:
                writer.writerow(['Customer Type', 'Name', 'Address', 'State', 'Postcode', 'Phone', 'Email', 'ABN'])
            writer.writerow(customer_data)
        print("Customer data saved successfully!")
    except Exception as e:
        print(f"Error saving customer data: {e}")

    # Insert data into the CWdb database using dbClient
    customerDict = {
        "name": name,
        "customerType": customerType if customerType else None,
        "email": email if email else None, 
        "phone": phone if phone else None,  
        "address": address if address else None,
        "state": state if state else None,
        "postcode": postcode if postcode else None,
        "ABN": abn  # Optional ABN
    }

    dbResponse = db.addCustomerData(customerDict)  # Call the database method

    # Display message based on DB operation response
    if dbResponse["status"] == "Success":
        # Close the window after saving the data
        addCustomerWindow.destroy()
        messageBox.showinfo("Success", "Customer added to the database successfully!")
    else:
        messageBox.showerror("Database Error", f"Failed to add customer: {dbResponse['message']}")

    
def updateCustomerListbox(searchEntry, listbox, customerList):
    searchQuery = searchEntry.get().lower()
    listbox.delete(0, tk.END)
    for customer_id, name in customerList:
        if searchQuery in name.lower():
            listbox.insert(tk.END, name)


def showCustomerDetails(selectedCustomer, customerEntry):
    global detailsWindow, screen_width, screen_height

    # Calculate window dimensions
    window_width = int(screen_width * 0.5)
    window_height = int(screen_height * 0.7)

    # Create a new window for customer details
    detailsWindow = ctk.CTkToplevel()
    detailsWindow.title("Customer Details")
    detailsWindow.geometry(f"{window_width}x{window_height}")

    # Center the window at the top-center of the screen
    xCoordinate = (screen_width - window_width) // 2
    yCoordinate = 50  # Slightly below the top of the screen
    detailsWindow.geometry(f"+{xCoordinate}+{yCoordinate}")

    detailsWindow.transient()
    detailsWindow.grab_set()
    detailsWindow.focus_force()

    # Create a frame for details and center it
    detailsFrame = ctk.CTkFrame(detailsWindow)
    detailsFrame.pack(pady=20, padx=20, fill="both", expand=True)  # Centered with `expand=True`

    # Add customer details using separate labels for alignment
    for row, (key, value) in enumerate(selectedCustomer.items()):
        keyLabel = ctk.CTkLabel(detailsFrame, text=f"{key}:", font=("Times New Roman", 21), anchor="w", width=15)
        keyLabel.grid(row=row, column=0, sticky="w", padx=(10, 5), pady=5)

        valueLabel = ctk.CTkLabel(detailsFrame, text=value, font=("Times New Roman", 21), anchor="w")
        valueLabel.grid(row=row, column=1, sticky="w", padx=(5, 10), pady=5)

    # Buttons
    def selectCust():
        global selectedCustomerDetails, selectionWindow
        customerEntry.delete(0, tk.END)
        selectedCustomerDetails = selectedCustomer
        print("Selected Customer details : ",selectedCustomerDetails)
        customerEntry.delete(0, "end")
        customerEntry.insert(0, f"Name: {selectedCustomer['Name']}")
        detailsWindow.destroy()
        selectionWindow.destroy()

    # Create a frame for buttons and center it
    buttonFrame = ctk.CTkFrame(detailsWindow)
    buttonFrame.pack(pady=10, padx=10)  # Centered

    # Add buttons to the same row in the frame
    selectButton = ctk.CTkButton(buttonFrame, text="Select Customer",fg_color= "#393939",hover_color="#252523", width=int(screen_width * .15), font=("Times New Roman", 21), command=selectCust)
    selectButton.grid(row=0, column=0, padx=5, pady=5)

    closeButton = ctk.CTkButton(buttonFrame, text="Close",fg_color= "#e62739",hover_color="#a93226", width=int(screen_width * .15), font=("Times New Roman", 21), command=detailsWindow.destroy)
    closeButton.grid(row=0, column=1, padx=5, pady=5)

    # Adjust the layout to center the frames
    detailsFrame.place(relx=0.5, rely=0.4, anchor="center")
    buttonFrame.place(relx=0.5, rely=0.9, anchor="center")


def selectCustomer(event, customerEntry, listbox, db, customerList):
    selectedName = listbox.get(listbox.curselection())
    customer_id = next((cid for cid, name in customerList if name == selectedName), None)

    if customer_id is None:
        messageBox.showerror("Selection Error", "Failed to retrieve customer ID.")
        return

    try:
        customerDetails = db.getCustomerDetails(customer_id, selectedName)
        if customerDetails:
            customerDict = {
                'Customer Type': customerDetails[1],  # Adjust index based on DB schema
                'Name': customerDetails[2],
                'Address': customerDetails[3],
                'State': customerDetails[4],
                'Postcode': customerDetails[5],
                'Phone': customerDetails[6],
                'Email': customerDetails[7],
                'ABN': customerDetails[8],
            }
            showCustomerDetails(customerDict, customerEntry)
        else:
            messageBox.showerror("Error", "Customer details not found.")
    except Exception as e:
        messageBox.showerror("Database Error", f"Failed to fetch customer details: {e}")

def openSales(selectedName, db):
    global screen_width, screen_height

    # Fetch sales details for the selected customer from the database
    customer_sales = db.getSalesByCustomerName(selectedName)

    if not customer_sales:
        messageBox.showinfo("No Data", f"No sales details found for {selectedName}.")
        return

    # Create the sales details window
    salesWindow = ctk.CTkToplevel()
    salesWindow.title(f"Sales Details - {selectedName}")

    # Window size and position
    window_width = int(screen_width * 0.5)
    window_height = int(screen_height * 0.8)
    xCoordinate = (screen_width - window_width) // 2
    yCoordinate = 50
    salesWindow.geometry(f"{window_width}x{window_height}+{xCoordinate}+{yCoordinate}")
    salesWindow.resizable(False, False)
    salesWindow.transient()
    salesWindow.grab_set()
    salesWindow.focus_force()

    # Main frame for customer and product details
    mainFrame = ctk.CTkFrame(salesWindow)
    mainFrame.pack(fill="both", expand=True, padx=10, pady=10)

    # Scrollable canvas for product details
    canvas = tk.Canvas(mainFrame)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ctk.CTkScrollbar(mainFrame, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    contentFrame = ctk.CTkFrame(canvas)
    canvas.create_window((0, 0), window=contentFrame, anchor="n")  # Align content at the top center

    # Display customer details at the top
    customerDetailsFrame = ctk.CTkFrame(contentFrame)
    customerDetailsFrame.pack(pady=20)  # Add padding to center the frame in the window

    first_sale = customer_sales[0]  # Get the first record to extract customer details

    customerDetails = f"""
    Customer Name: {selectedName}
    Address: {first_sale['customerAddress']}
    Phone: {first_sale['customerPhone']}
    """
    customerDetailsLabel = ctk.CTkLabel(customerDetailsFrame, text=customerDetails, font=("Times New Roman", 20), anchor="center")
    customerDetailsLabel.pack(padx=10, pady=5)

    # Group sales by date
    grouped_sales = {}
    for sale in customer_sales:
        date = sale["date"]
        if date not in grouped_sales:
            grouped_sales[date] = []
        grouped_sales[date].append(sale)

    # Loop through grouped sales and display products under the same date
    for date, sales in grouped_sales.items():
        # Calculate total price for that date
        total_price = sum(float(sale["price"]) * int(sale["quantity"]) for sale in sales)

        # Create a frame for the date
        dateFrame = ctk.CTkFrame(contentFrame, width=window_width * 0.9)
        dateFrame.pack(pady=20)

        # Date label (Bold)
        dateLabel = ctk.CTkLabel(dateFrame, text=f"Date: {date}", font=("Times New Roman", 20, "bold"), anchor="center")
        dateLabel.pack(pady=5)

        # Loop through each sale and display product details under the same date
        for sale in sales:
            productDetails = f"""
            Product Name: {sale['productName']}
            Product Type: {sale['productType']}
            Colour: {sale['colour']}
            Price: ${sale['price']}
            Quantity: {sale['quantity']}
            Payment Type: {sale['paymentType']}
            """
            productLabel = ctk.CTkLabel(dateFrame, text=productDetails, font=("Times New Roman", 18), anchor="center")
            productLabel.pack(padx=10, pady=2)

        # Display total price for all purchases on that date
        totalPriceLabel = ctk.CTkLabel(
            dateFrame, 
            text=f"Total Price: ${total_price:.2f}", 
            font=("Times New Roman", 18, "bold"),  # Bold total price
            anchor="center", 
            text_color="red"
        )
        totalPriceLabel.pack(pady=5)

    # Close Button
    closeButton = ctk.CTkButton(salesWindow, text="Close", font=("Times New Roman", 18), command=salesWindow.destroy, fg_color="#e62739", hover_color="#a93226")
    closeButton.pack(pady=20)


def openCustomerSelection(customerEntry,flag,db):
    global selectionWindow, screen_width, screen_height
    if selectionWindow and selectionWindow.winfo_exists():
        selectionWindow.lift()
        return

    # Fetch customer names and IDs from the database
    try:
        customerList = db.getCustomerName()  # Fetches (id, name) tuples
    except Exception as e:
        messageBox.showerror("Database Error", f"Failed to fetch customers: {e}")
        return

    if not customerList:
        messageBox.showinfo("No Customers", "No customer records found.")
        return
    
    print("customerList : ", customerList)

    selectionWindow = ctk.CTkToplevel()
    selectionWindow.title("Select Customer")

    window_width = int(screen_width * 0.5)
    window_height = int(screen_height * 0.9 )

    # Position the window at the top center
    xCoordinate = (screen_width - window_width) // 2
    yCoordinate = 50  # Slightly below the top of the screen
    selectionWindow.geometry(f"{window_width}x{window_height}+{xCoordinate}+{yCoordinate}")

    # Disable window maximization
    selectionWindow.resizable(False, False)
    selectionWindow.transient()
    selectionWindow.grab_set()
    selectionWindow.focus_force()

    # Search label and entry
    searchLabel = ctk.CTkLabel(selectionWindow, text="Search by Name:", font=("Times New Roman", 21))
    searchLabel.pack(pady=10)
    
    searchEntry = ctk.CTkEntry(selectionWindow, width=int(window_width - 20 ))
    searchEntry.pack()

    # Frame for listbox and scrollbar
    listboxFrame = ctk.CTkFrame(selectionWindow)
    listboxFrame.pack(pady=10, fill="both", expand=True)

    listboxWithScrollbarFrame = ctk.CTkFrame(listboxFrame)
    listboxWithScrollbarFrame.pack(fill="both", expand=True, padx=10, pady=10)

    # Adjust listbox size dynamically based on the window size
    listbox_width = int(window_width * 0.8 // 10)  # Approximate scaling for width
    listbox_height = int(window_height * 0.4 // 18)  # Approximate scaling for height

    customerListbox = tk.Listbox(listboxWithScrollbarFrame, width=listbox_width, height=listbox_height, font=("Times New Roman", 21))
    customerListbox.pack(side="left", pady=10, fill="both", expand=True)

    # Scrollbar
    scrollbar = tk.Scrollbar(listboxWithScrollbarFrame, orient="vertical", command=customerListbox.yview, width=25 )
    scrollbar.pack(side="right", fill="y")

    customerListbox.config(yscrollcommand=scrollbar.set)

    # Bind search functionality
    searchEntry.bind("<KeyRelease>", lambda e: updateCustomerListbox(searchEntry, customerListbox, customerList))
    updateCustomerListbox(searchEntry, customerListbox, customerList)

    if flag == "selectCustomer":
        customerListbox.bind("<Double-1>", lambda e: selectCustomer(e, customerEntry, customerListbox, db, customerList))
    else:
        customerListbox.bind("<Double-1>", lambda e: openSales(customerListbox.get(customerListbox.curselection()),db))

    # Close button at the bottom center
    closeButton = ctk.CTkButton(selectionWindow, text="Close", fg_color= "#e62739",hover_color="#a93226", text_color="white", font=("Times New Roman", 18),command=selectionWindow.destroy)
    closeButton.pack(pady=10)

def removeProduct(productEntry):
    global screen_width, screen_height, finalProductList

    if finalProductList == []:
        messageBox.showwarning("No Selection", "No products selected to remove.")
        return

    # Create a new window for removing products
    removeWindow = ctk.CTkToplevel()
    removeWindow.title("Remove Product")

    # Set window dimensions and position
    window_width = int(screen_width * 0.5)
    window_height = int(screen_height * 0.8)
    xCoordinate = (screen_width - window_width) // 2
    yCoordinate = 50  # Slightly below the top of the screen
    removeWindow.geometry(f"{window_width}x{window_height}+{xCoordinate}+{yCoordinate}")

    # Disable resizing
    removeWindow.resizable(False, False)
    removeWindow.transient()
    removeWindow.grab_set()
    removeWindow.focus_force()

    # Frame for product list
    productFrame = ctk.CTkFrame(removeWindow)
    productFrame.pack(fill="both", expand=True, padx=10, pady=10)

    # Create a dictionary to hold checkbox variables
    productCheckboxVars = {}

    # Fetch data from the tree and display it with checkboxes
    for index, item in enumerate(productEntry.get_children()):
        product = productEntry.item(item, "values")  # Get product details from the tree
        checkboxVar = tk.BooleanVar()
        productCheckboxVars[item] = checkboxVar

        checkboxText = f"{product[0]} - {product[1]} x{product[2]} {product[3]}"
        ctk.CTkCheckBox(productFrame, text=checkboxText, variable=checkboxVar, font=("Times New Roman", 18)).pack(anchor="w", padx=10, pady=5)

    def rebuild_serial_numbers():
        global currentSLNo
        currentSLNo = 1  # Reset serial number
        for item in productEntry.get_children():
            values = productEntry.item(item, "values")
            productEntry.item(item, values=(currentSLNo, *values[1:]))
            currentSLNo += 1

    # Buttons
    def removeSelectedProducts():
        selectedItems = [item for item, var in productCheckboxVars.items() if var.get()]  # Get selected items
        for item in selectedItems:
            # Get product details of the selected item
            product = productEntry.item(item, "values")
            # Find and remove the corresponding product from finalProductList
            for prod in finalProductList:
                if (prod["Name"] == product[1] and int(prod["Quantity"]) == int(product[2])):
                    finalProductList.remove(prod)
                    break

            print(f"Removed from finalProductList: {product}")
            productEntry.delete(item)  # Remove the selected items from the tree

        rebuild_serial_numbers()
        removeWindow.destroy()
        

    # Buttons frame
    buttonFrame = ctk.CTkFrame(removeWindow)
    buttonFrame.pack(pady=10)

    removeButton = ctk.CTkButton(buttonFrame,text="Remove",fg_color= "#e62739",hover_color="#a93226", width=int(screen_width * 0.15),font=("Times New Roman", 21),command=removeSelectedProducts)
    removeButton.grid(row=0, column=0, padx=10)

    closeButton = ctk.CTkButton(buttonFrame,text="Close",fg_color= "#393939",hover_color="#252523", width=int(screen_width * 0.15),font=("Times New Roman", 21),command=removeWindow.destroy,)
    closeButton.grid(row=0, column=1, padx=10)

def addToProductEntry(productEntry, name, quantity, unit_price):
    global currentSLNo  # Use the global variable to track serial numbers

    try:
        # Validate inputs
        if not name.strip():
            messageBox.showwarning("Input Error", "Product Name cannot be empty.")
            return

        # Calculate total price
        total_price = quantity * unit_price

        # Insert data into the Treeview
        productEntry.insert(
            "",  # Parent item (root level)
            "end",  # Position to insert
            values=(currentSLNo, name, quantity, f"${unit_price:.2f}", f"${total_price:.2f}")
        )

        # Increment the serial number
        currentSLNo += 1

    except Exception as e:
        messageBox.showerror("Error", f"An error occurred: {e}")

def openAddProductWindow(productEntry, db):
    # Create a new window for adding product details
    global screen_width, screen_height
    addProductWindow = ctk.CTkToplevel()
    addProductWindow.title("Add Product")

    # Set window dimensions
    window_width = int(screen_width * 0.5)
    window_height = int(screen_height * 0.6)
    xCoordinate = (screen_width - window_width) // 2
    yCoordinate = 50
    addProductWindow.geometry(f"{window_width}x{window_height}+{xCoordinate}+{yCoordinate}")
    addProductWindow.transient()
    addProductWindow.grab_set()
    addProductWindow.focus_force()

    # Create a frame for the form
    formFrame = ctk.CTkFrame(addProductWindow)
    formFrame.pack(pady=20, padx=20, fill="both", expand=True)

    # Labels and Entry Fields for Product Details
    labels = ["Name", "Product Type", "Colour", "Price", "Quantity"]  # Quantity only used in CRM
    entries = {}

    for row, label in enumerate(labels):
        lbl = ctk.CTkLabel(formFrame, text=f"{label}:", font=("Times New Roman", 21), anchor="w")
        lbl.grid(row=row, column=0, padx=(10, 5), pady=5, sticky="w")

        entry = ctk.CTkEntry(formFrame, font=("Times New Roman", 21), width=int(window_width * 0.7))
        entry.grid(row=row, column=1, padx=(5, 10), pady=5, sticky="ew")
        entries[label] = entry

    # Save Product Button
    def saveProductDetails(productEntry):
        global finalProductList
        
        try:
            productDetails = {
                "name": entries["Name"].get(),
                "productType": entries["Product Type"].get(),
                "colour": entries["Colour"].get(),
                "price": float(entries["Price"].get()),
            }
            quantity = int(entries["Quantity"].get())  # Quantity for CRM only

            # Check if the product already exists in the database
            existingProduct = db.getProductByName(productDetails["name"])
            
            if not existingProduct:
                # Insert new product into the database
                try:
                    db.addProductData(productDetails)
                    messageBox.showinfo("Success", "Product added to Database successfully!")
                except Exception as e:
                    messageBox.showwarning("Database Error", f"Failed to add product: {e}")

            # Check if the product already exists in the finalProductList
            for product in finalProductList:
                if product['Name'].lower() == productDetails['name'].lower():
                    # Update the quantity and price for the existing product
                    product['Quantity'] += quantity
                    product['Price'] = productDetails["price"]  # Update unit price

                    # Update the corresponding row in the TreeView
                    for child in productEntry.get_children():
                        values = productEntry.item(child, 'values')
                        if values[1].lower() == productDetails['name'].lower():  # Match product name
                            # Update quantity and total price in TreeView
                            total_price = product['Quantity'] * product['Price']
                            productEntry.item(child, values=(values[0], values[1], product['Quantity'], 
                                                            f"${product['Price']:.2f}", f"${total_price:.2f}"))
                            break
                    
                    # Close the details window
                    print("finalProductList:", finalProductList)
                    addProductWindow.destroy()
                    return

            # Add the product to the finalProductList
            productDetails['Quantity'] = quantity
            finalProductList.append(productDetails)
            print("finalProductList:", finalProductList)

            # Update the TreeView in CRM
            addToProductEntry(productEntry, productDetails["name"], quantity, productDetails["price"])

        except ValueError:
            messageBox.showerror("Input Error", "Provide valid input for Name, Quantity, and Price!")
        except Exception as e:
            messageBox.showerror("Error", f"Failed to save product: {e}")

    # Exit Button
    def closeWindow():
        addProductWindow.destroy()

    # Clear All Button Function
    def clearAllFields():
        for entry in entries.values():
            entry.delete(0, tk.END)

    # Save and Exit Buttons
    buttonFrame = ctk.CTkFrame(addProductWindow)
    buttonFrame.pack(pady=10)

    saveButton = ctk.CTkButton(buttonFrame, text="Save", fg_color= "#393939",hover_color="#252523", command=lambda: saveProductDetails(productEntry), width=int(screen_width * 0.15), font=("Times New Roman", 21))
    saveButton.grid(row=0, column=0, padx=10, pady=5)

    exitButton = ctk.CTkButton(buttonFrame, text="Exit", fg_color= "#393939",hover_color="#252523", command=closeWindow, width=int(screen_width * 0.15), font=("Times New Roman", 21))
    exitButton.grid(row=0, column=1, padx=10, pady=5)

    clearButton = ctk.CTkButton(buttonFrame, text="Clear All", fg_color= "#e62739",hover_color="#a93226", text_color="white", command=clearAllFields, width=int(screen_width * 0.15), font=("Times New Roman", 21))
    clearButton.grid(row=0, column=2, padx=10, pady=5)

def showProductDetails(selectedProduct, productEntry):
    global detailsWindow, screen_width, screen_height

    # Calculate window dimensions
    window_width = int(screen_width * 0.5)
    window_height = int(screen_height * 0.7)

    # Create a new window for product details
    detailsWindow = ctk.CTkToplevel()
    detailsWindow.title("Product Details")
    detailsWindow.geometry(f"{window_width}x{window_height}")

    # Center the window at the top-center of the screen
    xCoordinate = (screen_width - window_width) // 2
    yCoordinate = 50  # Slightly below the top of the screen
    detailsWindow.geometry(f"+{xCoordinate}+{yCoordinate}")

    detailsWindow.transient()
    detailsWindow.grab_set()
    detailsWindow.focus_force()

    # Create a frame for details and center it
    detailsFrame = ctk.CTkFrame(detailsWindow)
    detailsFrame.pack(pady=20, padx=20, fill="both", expand=True)

    # Add product details using separate labels for alignment
    for row, (key, value) in enumerate(selectedProduct.items()):
        keyLabel = ctk.CTkLabel(detailsFrame, text=f"{key}:", font=("Times New Roman", 21), anchor="w", width=15)
        keyLabel.grid(row=row, column=0, sticky="w", padx=(10, 5), pady=5)

        valueLabel = ctk.CTkLabel(detailsFrame, text=value, font=("Times New Roman", 21), anchor="w")
        valueLabel.grid(row=row, column=1, sticky="w", padx=(5, 10), pady=5)

    # Add Quantity entry
    quantityLabel = ctk.CTkLabel(detailsFrame, text="Quantity:", font=("Times New Roman", 21), anchor="w", width=15)
    quantityLabel.grid(row=row + 1, column=0, sticky="w", padx=(10, 5), pady=5)

    quantityEntry = ctk.CTkEntry(detailsFrame, font=("Times New Roman", 21))
    quantityEntry.grid(row=row + 1, column=1, sticky="w", padx=(5, 10), pady=5)

    quantityEntry.insert(0, "1")  # Default quantity is 1

    # Price entry
    priceLabel = ctk.CTkLabel(detailsFrame, text="Price:", font=("Times New Roman", 21), anchor="w", width=15)
    priceLabel.grid(row=row + 2, column=0, sticky="w", padx=(10, 5), pady=5)

    priceEntry = ctk.CTkEntry(detailsFrame, font=("Times New Roman", 21))
    priceEntry.grid(row=row + 2, column=1, sticky="w", padx=(5, 10), pady=5)

    priceEntry.insert(0, selectedProduct['Price'])  # Set the price in the price entry field

    # Buttons
    def selectPDT():
        global selectionWindow,finalProductList

        try:
            selectedProduct["Quantity"] = int(quantityEntry.get())
            selectedProduct["Price"] = float(priceEntry.get())

            print("selectedProduct in select PDDT : ",selectedProduct)

            # Check if the product already exists in the finalProductList
            for product in finalProductList:
                if product['Name'].lower() == selectedProduct['Name'].lower():
                    # Update the quantity and price for the existing product
                    product['Quantity'] += selectedProduct["Quantity"]
                    product['Price'] = selectedProduct["Price"]  # Update unit price (if applicable)

                    # Update the corresponding row in the Treeview
                    for child in productEntry.get_children():
                        values = productEntry.item(child, 'values')
                        if values[1].lower() == selectedProduct['Name'].lower():  # Match product name
                            # Update quantity and total price in Treeview
                            total_price = product['Quantity'] * product['Price']
                            productEntry.item(child, values=(values[0], values[1], product['Quantity'], 
                                                            f"${product['Price']:.2f}", f"${total_price:.2f}"))
                            break

                    # Close the details window
                    detailsWindow.destroy()
                    print("finalProductList : ",finalProductList)
                    return

            finalProductList.append(selectedProduct)
            print("finalProductList : ",finalProductList)

            addToProductEntry(productEntry,selectedProduct['Name'],selectedProduct['Quantity'],selectedProduct['Price'])
            detailsWindow.destroy()

            if selectedProduct['Quantity'] <= 0 or selectedProduct['Price'] <= 0:
                messageBox.showwarning("Input Error", "Quantity and Unit Price must be positive.")
                return
        except Exception as e:
            print(f"Error saving product details: {e}")
            messageBox.showwarning("Input Error", "Provide Valid inputs.")
            return

    # Create a frame for buttons and center it
    buttonFrame = ctk.CTkFrame(detailsWindow)
    buttonFrame.pack(pady=10, padx=10)

    # Add buttons to the frame
    selectButton = ctk.CTkButton(buttonFrame, text="Select Product",fg_color= "#393939",hover_color="#252523", width=int(screen_width * .15), font=("Times New Roman", 21), command=selectPDT)
    selectButton.grid(row=0, column=0, padx=5, pady=5)

    closeButton = ctk.CTkButton(buttonFrame, text="Close",fg_color= "#e62739",hover_color="#a93226", width=int(screen_width * .15), font=("Times New Roman", 21), command=detailsWindow.destroy)
    closeButton.grid(row=0, column=1, padx=5, pady=5)

    # Adjust the layout to center the frames
    detailsFrame.place(relx=0.5, rely=0.4, anchor="center")
    buttonFrame.place(relx=0.5, rely=0.9, anchor="center")

def selectProduct(event, productEntry, listbox, db):

    selectedName = listbox.get(listbox.curselection())

    # Fetch product details based on the selected name
    try:
        product_details = db.getProductDetails( selectedName)  # No ID, searching by name
    except Exception as e:
        messageBox.showerror("Error", f"Error fetching product details: {str(e)}")
        return
    
    if not product_details:
        messageBox.showerror("Error", f"Product '{selectedName}' not found.")
        return
    
    selectedProduct = {
        "Name": product_details[0],
        "Product Type": product_details[1],
        "Colour": product_details[2],
        "Price": product_details[3] if product_details[3] is not None else 0
    }

    showProductDetails(selectedProduct, productEntry)

def updateListbox(searchEntry, productListbox, products):

    """Update the listbox with filtered product names"""
    search_query = searchEntry.get().lower()
    filtered_products = [product for product in products if search_query in product[1].lower()]
    productListbox.delete(0, tk.END)  # Clear existing entries
    for product in filtered_products:
        productListbox.insert(tk.END, product[1])  # Insert product name

def openSelectProductWindow(productEntry,db):

    global selectionWindow, screen_width, screen_height
    if selectionWindow and selectionWindow.winfo_exists():
        selectionWindow.lift()
        return

    try:
        # Get product names and IDs from the database
        products = db.getProductNamesAndIds()
    except Exception as e:
        messageBox.showerror("Error", f"Error fetching product data: {str(e)}")
        return

    selectionWindow = ctk.CTkToplevel()
    selectionWindow.title("Select Products")

    # Calculate 50% of the screen size
    window_width = int(screen_width * 0.5)
    window_height = int(screen_height * 0.9)

    # Position the window at the top center
    xCoordinate = (screen_width - window_width) // 2
    yCoordinate = 50  # Slightly below the top of the screen
    selectionWindow.geometry(f"{window_width}x{window_height}+{xCoordinate}+{yCoordinate}")

    # Disable window maximization
    selectionWindow.resizable(False, False)
    selectionWindow.transient()
    selectionWindow.grab_set()
    selectionWindow.focus_force()

    # Search label and entry
    searchLabel = ctk.CTkLabel(selectionWindow, text="Search by Name:", font=("Times New Roman", 21))
    searchLabel.pack(pady=10)
    
    searchEntry = ctk.CTkEntry(selectionWindow, width=int(window_width - 20 ))
    searchEntry.pack()

    # Frame for listbox and scrollbar
    listboxFrame = ctk.CTkFrame(selectionWindow)
    listboxFrame.pack(pady=10, fill="both", expand=True)

    listboxWithScrollbarFrame = ctk.CTkFrame(listboxFrame)
    listboxWithScrollbarFrame.pack(fill="both", expand=True, padx=10, pady=10)

    # Adjust listbox size dynamically based on the window size
    listbox_width = int(window_width * 0.8 // 10)  # Approximate scaling for width
    listbox_height = int(window_height * 0.4 // 18)  # Approximate scaling for height

    productListbox = tk.Listbox(listboxWithScrollbarFrame, width=listbox_width, height=listbox_height, font=("Times New Roman", 21))
    productListbox.pack(side="left", pady=10, fill="both", expand=True)

    # Scrollbar
    scrollbar = tk.Scrollbar(listboxWithScrollbarFrame, orient="vertical", command=productListbox.yview, width=25 )
    scrollbar.pack(side="right", fill="y")

    productListbox.config(yscrollcommand=scrollbar.set)

    # Bind search functionality
    searchEntry.bind("<KeyRelease>", lambda e: updateListbox(searchEntry, productListbox, products))
    updateListbox(searchEntry, productListbox, products)

    # Double-click to select a customer
    productListbox.bind("<Double-1>", lambda e: selectProduct(e, productEntry, productListbox, db))


    # Close button at the bottom center
    closeButton = ctk.CTkButton(selectionWindow, text="Close", fg_color= "#e62739",hover_color="#a93226", text_color="white", font=("Times New Roman", 18),command=selectionWindow.destroy)
    closeButton.pack(pady=10)

def addNewProductToSystem(productName, productPrice, db):
    """Add a new product to the system and database"""

    if productName.strip() == "":
        messageBox.showwarning("Input Error", "Name of the product not specified!")
        return

    try:
        # Check if the product already exists in the database
        existingProduct = db.getProductByName(productName)  # Fetch the product ID by name
        if existingProduct:
            messageBox.showwarning("Duplicate Product", f"Product '{productName}' already exists in the system!")
            return

        # Insert new product into the database
        productData = {
            "name": productName,
            "productType": None,
            "colour": None,
            "price": productPrice
        }
        db.addProductData(productData)  # Call method to insert data into the DB

        messageBox.showinfo("Success", f"Product '{productName}' added to the Data Base successfully!")

    except Exception as e:
        messageBox.showerror("Error", f"An error occurred while adding the product: {e}")



def openMiscellaneousWindow(productEntry,db):
    global finalProductList,screen_width,screen_height

    # Create a new window
    miscWindow = ctk.CTkToplevel()
    miscWindow.title("Add Miscellaneous Product")

    # Set window dimensions
    window_width = int(screen_width * 0.5)
    window_height = int(screen_height * 0.6)
    xCoordinate = (screen_width - window_width) // 2
    yCoordinate = 50
    miscWindow.geometry(f"{window_width}x{window_height}+{xCoordinate}+{yCoordinate}")

    # Disable resizing
    miscWindow.resizable(False, False)
    miscWindow.transient()
    miscWindow.grab_set()
    miscWindow.focus_force()

    # Main frame to center all elements
    mainFrame = ctk.CTkFrame(miscWindow)
    mainFrame.pack(padx=20, pady=20, fill="both", expand=True)

    # Entry Frame for all inputs
    entryFrame = ctk.CTkFrame(mainFrame)
    entryFrame.pack(pady=20)

    # Name Entry
    nameLabel = ctk.CTkLabel(entryFrame, text="Product Name:", font=("Times New Roman", 21))
    nameLabel.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    nameEntry = ctk.CTkEntry(entryFrame,width= int(window_width*.60), font=("Times New Roman", 18))
    nameEntry.grid(row=0, column=1, padx=10, pady=10)

    # Quantity Entry
    quantityLabel = ctk.CTkLabel(entryFrame, text="Quantity:", font=("Times New Roman", 21))
    quantityLabel.grid(row=1, column=0, padx=10, pady=10, sticky="e")
    quantityEntry = ctk.CTkEntry(entryFrame, width= int(window_width*.60), font=("Times New Roman", 18))
    quantityEntry.grid(row=1, column=1, padx=10, pady=10)

    # Price Entry
    priceLabel = ctk.CTkLabel(entryFrame, text="Price ($):", font=("Times New Roman", 21))
    priceLabel.grid(row=2, column=0, padx=10, pady=10, sticky="e")
    priceEntry = ctk.CTkEntry(entryFrame, width= int(window_width*.60), font=("Times New Roman", 18))
    priceEntry.grid(row=2, column=1, padx=10, pady=10)

    # Add Product Functionality
    def addMiscProduct(productEntry):
        try:
            productName = nameEntry.get()
            productQuantity = int(quantityEntry.get().strip())
            productPrice = float(priceEntry.get().strip())

            if productName == "":
                messageBox.showwarning("Input Error", "Name of the product not specified!.")
                return
            if productQuantity <= 0 or productPrice <= 0:
                messageBox.showwarning("Input Error", "Quantity and Price must be positive."); return

            # Add the product to finalProductList
            productDict = {
                "Product Type": "Miscellaneous",
                "Colour": "N/A",
                "Name": productName,
                "Price": productPrice,
                "Quantity": productQuantity
            }
            finalProductList.append(productDict)
            print("finalProductList ",finalProductList)

            addToProductEntry(productEntry,productName,productQuantity,productPrice)

            # Clear the entries
            nameEntry.delete(0, "end")
            quantityEntry.delete(0, "end")
            priceEntry.delete(0, "end")

        except ValueError:
            messageBox.showwarning("Input Error", "Please provide valid numerical inputs for Quantity and Price.")

    # Buttons
    buttonFrame = ctk.CTkFrame(mainFrame)
    buttonFrame.pack(pady=20)

    addButton = ctk.CTkButton(buttonFrame, text="Add Product to Checkout", width=int(screen_width * 0.15),
                              font=("Times New Roman", 21), command=lambda: addMiscProduct(productEntry),
                              fg_color= "#393939",hover_color="#252523")
    addButton.grid(row=0, column=0, padx=10)

    closeButton = ctk.CTkButton(buttonFrame, text="Close", width=int(screen_width * 0.15),
                                font=("Times New Roman", 21), command=miscWindow.destroy,
                                fg_color= "#e62739",hover_color="#a93226",)
    closeButton.grid(row=0, column=1, padx=10)

    addToSysButton = ctk.CTkButton(buttonFrame, text="Add Product to System", width=int(screen_width * 0.10),
                              font=("Times New Roman", 21), fg_color= "#393939",hover_color="#252523", command=lambda: addNewProductToSystem(nameEntry.get().strip(),priceEntry.get().strip(),db))
    addToSysButton.grid(row=0, column=2, padx=10)


# Define the function
def writeSalesDetails(db, paymentType="efpos"):
    global finalProductList, selectedCustomerDetails

    # Prepare customer details
    customerName = selectedCustomerDetails.get('Name', 'N/A')
    customerAddress = selectedCustomerDetails.get('Address', 'N/A')
    customerPhone = selectedCustomerDetails.get('Phone', 'N/A')

    # Retrieve customerID from the database using the customer's name (if applicable)
    customerID = db.getCustomerIDByName(customerName) if customerName != 'N/A' else None

    # Get the current date
    sale_date = datetime.now().strftime('%Y-%m-%d')

    # Insert sales details into the database
    for product in finalProductList:
        salesData = {
            "date": sale_date,
            "customerID": customerID,
            "customerName": customerName,
            "customerAddress": customerAddress,
            "customerPhone": customerPhone,
            "productName": product['Name'],
            "productType": product['Product Type'],
            "colour": product['Colour'],
            "price": product['Price'],
            "quantity": product['Quantity'],
            "paymentType": paymentType
        }

        response = db.addSalesData(salesData)

        # Log the response message
        print(response["message"])


def writePerDaySales(db):
    global finalProductList

    # Calculate total price from finalProductList
    total_price = sum(item['Price'] * item['Quantity'] for item in finalProductList if not pd.isna(item['Price']))

    # Get today's date in YYYY-MM-DD format
    today_date = datetime.today().strftime('%Y-%m-%d')

    # Prepare sales data for the database
    saleData = {
        "date": today_date,
        "sales": total_price
    }

    # Call the database function to add/update the sales record
    response = db.addPerDaySale(saleData)

    # Log response message
    print(response["message"])

def generateInvoice(db):
    global screen_width, screen_height, finalProductList, selectedCustomerDetails

    if finalProductList == []:
        messageBox.showwarning("Input Error", "Please add a product!")
        return

    # Open a window for selecting payment type (25% of the screen size)
    paymentWindow = ctk.CTkToplevel()
    paymentWindow.title("Select Payment Type")
    
    # Window size and position (25% of the screen size)
    window_width = int(screen_width * 0.25)
    window_height = int(screen_height * 0.25)
    xCoordinate = (screen_width - window_width) // 2
    yCoordinate = (screen_height - window_height) // 2
    paymentWindow.geometry(f"{window_width}x{window_height}+{xCoordinate}+{yCoordinate}")
    paymentWindow.resizable(False, False)
    paymentWindow.transient()
    paymentWindow.grab_set()
    paymentWindow.focus_force()

    # Variable to store selected payment type
    payment_type = tk.StringVar(value="")  # Default value is empty string

    # Create radio buttons for payment types
    cashRadio = ctk.CTkRadioButton(paymentWindow, text="Cash", variable=payment_type, value="Cash", font=("Times New Roman", 16))
    efposRadio = ctk.CTkRadioButton(paymentWindow, text="Efpos", variable=payment_type, value="Efpos", font=("Times New Roman", 16))
    creditRadio = ctk.CTkRadioButton(paymentWindow, text="Credit", variable=payment_type, value="Credit", font=("Times New Roman", 16))
    bankTransferRadio = ctk.CTkRadioButton(paymentWindow, text="Bank Transfer", variable=payment_type, value="Bank Transfer", font=("Times New Roman", 16))

    # Pack radio buttons into the window
    cashRadio.pack(anchor="w", pady=5,padx= 10)
    efposRadio.pack(anchor="w", pady=5,padx= 10)
    creditRadio.pack(anchor="w", pady=5,padx= 10)
    bankTransferRadio.pack(anchor="w", pady=5,padx= 10)

    # Button to confirm payment type selection
    def onConfirm():
        selected_payment = payment_type.get()
        if not selected_payment:
            messageBox.showwarning("Input Error", "Please select a payment type.")
            return
        
        # Proceed with sales processing
        writePerDaySales(db)
        writeSalesDetails(db,selected_payment)
        
        # Close the payment window
        paymentWindow.destroy()

    confirmButton = ctk.CTkButton(paymentWindow, text="Confirm", command=onConfirm, font=("Times New Roman", 16))
    confirmButton.pack(pady=10)

def openPerDaySalesWindow(db):
    global screen_width, screen_height

    salesData = db.getPerDaySalesData()
    if not salesData:
        messageBox.showinfo("No Data", "No sales data found.")
        return

    salesWindow = ctk.CTkToplevel()
    salesWindow.title("Per Day Sales Summary")

    window_width = int(screen_width * 0.5)
    window_height = int(screen_height * 0.8)
    xCoordinate = (screen_width - window_width) // 2
    yCoordinate = 50
    salesWindow.geometry(f"{window_width}x{window_height}+{xCoordinate}+{yCoordinate}")
    salesWindow.resizable(False, False)
    salesWindow.transient()
    salesWindow.grab_set()
    salesWindow.focus_force()

    mainFrame = ctk.CTkFrame(salesWindow)
    mainFrame.pack(fill="both", expand=True, padx=10, pady=10)

    searchFrame = ctk.CTkFrame(mainFrame)
    searchFrame.pack(fill="x", padx=10, pady=5)

    searchLabel = ctk.CTkLabel(searchFrame, text="Search by Date:", font=("Times New Roman", 16))
    searchLabel.pack(side="left", padx=5)

    searchEntry = ctk.CTkEntry(searchFrame, font=("Times New Roman", 16))
    searchEntry.pack(side="left", fill="x", expand=True, padx=5)

    canvas = tk.Canvas(mainFrame)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ctk.CTkScrollbar(mainFrame, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    contentFrame = ctk.CTkFrame(canvas)
    canvas_window = canvas.create_window((0, 0), window=contentFrame, anchor="n")

    def displaySales(filteredData):
        for widget in contentFrame.winfo_children():
            widget.destroy()
        
        for sale in filteredData:
            salesFrame = ctk.CTkFrame(contentFrame, width=window_width * 0.9, height=100)
            salesFrame.pack(pady=5)
            salesFrame.pack_propagate(False)

            salesDetails = f"""
            Date: {sale['date']}
            Total Sales: ${sale['totalSales']:.2f}
            """
            salesLabel = ctk.CTkLabel(salesFrame, text=salesDetails, font=("Times New Roman", 18), anchor="center")
            salesLabel.pack(padx=10, pady=5)
    
    displaySales(salesData)

    def onSearchChange():
        query = searchEntry.get().strip().lower()
        filteredData = [sale for sale in salesData if query in str(sale['date']).lower()]
        displaySales(filteredData)
    
    searchEntry.bind("<KeyRelease>", lambda event: onSearchChange())

    closeButton = ctk.CTkButton(salesWindow, text="Close", width=int(screen_width * 0.15), fg_color= "#e62739",hover_color="#a93226", 
                                 font=("Times New Roman", 21, "bold"), 
                                command=salesWindow.destroy)
    closeButton.pack(pady=20)



def creditWindow(db):
    global screen_width, screen_height

    def refreshWindow():
        creditWin.destroy()
        creditWindow(db)

    creditSales = db.getCreditSalesData()
    if not creditSales:
        messageBox.showwarning("No Credit Data", "No credit sales data found.")
        return

    creditWin = ctk.CTkToplevel()
    creditWin.title("Credit Sales")
    windowWidth = int(screen_width * 0.5)
    windowHeight = int(screen_height * 0.8)
    xCoordinate = (screen_width - windowWidth) // 2
    yCoordinate = (screen_height - windowHeight) // 2
    creditWin.geometry(f"{windowWidth}x{windowHeight}+{xCoordinate}+{yCoordinate}")
    creditWin.resizable(False, False)
    creditWin.transient()
    creditWin.grab_set()
    creditWin.focus_force()

    mainFrame = ctk.CTkFrame(creditWin)
    mainFrame.pack(fill="both", expand=True, padx=10, pady=10)

    searchFrame = ctk.CTkFrame(mainFrame)
    searchFrame.pack(fill="x", padx=10, pady=5)

    searchEntry = ctk.CTkEntry(searchFrame, placeholder_text="Search by Name or Date...")
    searchEntry.pack(fill="x", padx=5, pady=5)

    canvas = tk.Canvas(mainFrame)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar = ctk.CTkScrollbar(mainFrame, orientation="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    contentFrame = ctk.CTkFrame(canvas)
    canvas_window = canvas.create_window((0, 0), window=contentFrame, anchor="n")

    def onFrameConfigure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    contentFrame.bind("<Configure>", onFrameConfigure)

    def updateList():
        query = searchEntry.get().lower()
        for widget in contentFrame.winfo_children():
            widget.destroy()
        
        filteredSales = [sale for sale in creditSales if query in sale['customerName'].lower() or query in str(sale['date'])]
        
        customers = {}
        for sale in filteredSales:
            name = sale['customerName']
            date = sale['date']
            
            if name not in customers:
                customers[name] = {"address": sale['customerAddress'], "phone": sale['customerPhone'], "purchases": {}, "total": 0}
            
            if date not in customers[name]["purchases"]:
                customers[name]["purchases"][date] = []
            
            customers[name]["purchases"][date].append(sale)
            customers[name]["total"] += sale['price'] * sale['quantity']

        for customer, details in customers.items():
            customerFrame = ctk.CTkFrame(contentFrame, width=windowWidth * 0.9)
            customerFrame.pack(pady=10, padx=10, fill="x")
            
            customerLabel = ctk.CTkLabel(
                customerFrame,
                text=f"Customer: {customer}\nAddress: {details['address']}\nPhone: {details['phone']}\nTotal Credit: ${details['total']:.2f}",
                font=("Times New Roman", 18, "bold"),
                anchor="center"
            )
            customerLabel.pack(padx=windowWidth * 0.4, pady=5)

            for date, products in details['purchases'].items():
                dateLabel = ctk.CTkLabel(customerFrame, text=f"Date: {date}", font=("Times New Roman", 16, "bold"), anchor="w")
                dateLabel.pack(padx=10, pady=5)
                
                for product in products:
                    productLabel = ctk.CTkLabel(customerFrame, text=f"    Product: {product['productName']}\n    Price: ${product['price']}\n    Quantity: {product['quantity']}", font=("Times New Roman", 16), anchor="w")
                    productLabel.pack(padx=10, pady=5)

            paidVar = tk.BooleanVar()
            paidRadio = ctk.CTkRadioButton(customerFrame, text="Mark as Paid", variable=paidVar, value=True)
            paidRadio.pack(pady=5)
            
            submitButton = ctk.CTkButton(
                customerFrame,
                text="Submit",
                fg_color="green",
                command=lambda name=customer: (db.updatePaymentType(name), refreshWindow()) if paidVar.get() else None
            )
            submitButton.pack(pady=5)

    searchEntry.bind("<KeyRelease>", lambda event: updateList())
    updateList()

    closeButton = ctk.CTkButton(creditWin, text="Close", width=int(screen_width * 0.15), fg_color= "#e62739",hover_color="#a93226", 
                                 font=("Times New Roman", 21, "bold"), 
                                command=creditWin.destroy)
    closeButton.pack(pady=20)
    canvas.update_idletasks()
    creditWin.mainloop()




def main():

    global screen_width,screen_height,finalProductList

    # Initialize the dbServer class
    db = DbServer()

    # Create the main window with updated dimensions (10% increased)
    root = ctk.CTk()  # Use customtkinter CTk instead of tk.Tk
    root.title("Cartridge World")
    
    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Set the window width and height 
    window_width = int(screen_width)
    window_height = int(screen_height)

    # Set the geometry of the window with the calculated coordinates
    root.geometry(f"{screen_width}x{screen_height}+{0}+{0}")
    
    # Disable window maximization
    root.resizable(False, False)

    # Create the navigation frame on the left side (10% increased) 
    navigationFrame = ctk.CTkFrame(root, width=int(screen_width * 0.25), height=int(screen_height), corner_radius=0, fg_color="#393939")
    navigationFrame.grid(row=0, column=0, sticky="ns")

    # Home button in the navigation frame (highlighted as selected, 10% increased size)
    def clear_data():
        global selectedCustomerDetails,finalProductList,currentSLNo
        # Clear the data in customerEntry and productEntry
        customerEntry.delete(0, tk.END)  # Clears customer entry field
        for item in productEntry.get_children():
            productEntry.delete(item)
        selectedCustomerDetails = {}
        finalProductList = []
        currentSLNo = 1

    # Home button - Now enabled and clears data
    homeButton = ctk.CTkButton(navigationFrame, text="Home", width=int(screen_width * 0.15),fg_color= "#dfd8c8",hover_color="#252523", text_color="black", font=("Times New Roman", int(21), "bold"), command=clear_data)
    homeButton.grid(row=0, column=0, padx=5, pady=20)

    salesButton = ctk.CTkButton(navigationFrame, text="Sales", width=int(screen_width * 0.15),fg_color= "#dfd8c8",hover_color="#252523", text_color="black", font=("Times New Roman", int(21), "bold"),command=lambda:openCustomerSelection(customerEntry,"sales",db))
    salesButton.grid(row=1, column=0, padx=5, pady=20)

    miscellaneousButton = ctk.CTkButton(navigationFrame, text="Miscellaneous", width=int(screen_width * 0.15),fg_color= "#dfd8c8",hover_color="#252523", text_color="black", font=("Times New Roman", int(21), "bold"),command=lambda:openMiscellaneousWindow(productEntry,db))
    miscellaneousButton.grid(row=2, column=0, padx=5, pady=20)

    salesPerDayButton = ctk.CTkButton(navigationFrame, text="Sales Per Day", width=int(screen_width * 0.15),fg_color= "#dfd8c8",hover_color="#252523", text_color="black", font=("Times New Roman", int(21), "bold"),command=lambda:openPerDaySalesWindow(db))
    salesPerDayButton.grid(row=3, column=0, padx=5, pady=20)

    creditButton = ctk.CTkButton(navigationFrame, text="Credits", width=int(screen_width * 0.15),fg_color= "#dfd8c8",hover_color="#252523", text_color="black", font=("Times New Roman", int(21), "bold"),command=lambda:creditWindow(db))
    creditButton.grid(row=4, column=0, padx=5, pady=20)

    # Create the main content frame on the right side, starting from the second column
    mainContentFrame = ctk.CTkFrame(root, width=int(screen_width * 0.75 ),fg_color="#dfd8c8")
    mainContentFrame.grid(row=0, column=1, sticky="nsew")

    # Add a frame to hold the text
    textFrame = ctk.CTkFrame(mainContentFrame, fg_color="#dfd8c8")
    textFrame.pack(pady=20, fill="both", expand=True)

    textLabel = ctk.CTkLabel(textFrame, text="K.P.K ASSOCIATES", font=("Times New Roman", int(window_height * 0.05), "bold"))
    textLabel.pack(pady=20, padx=20, anchor="center")

    # Customer section in a black-bordered box (10% increased sizes)
    customerFrame = ctk.CTkFrame(mainContentFrame, fg_color="#dfd8c8")
    customerFrame.pack(padx=int(20 * 1.5), fill="x")  # 10% increased padding

    # Adding empty rows for spacing
    customerSpacerTop = ctk.CTkLabel(customerFrame, text="", font=("Times New Roman", int(12 * 1.5)))
    customerSpacerTop.grid(row=0, column=0, pady=int(5 * 1.5))

    customerLabel = ctk.CTkLabel(customerFrame, text="Customer:", font=("Times New Roman", int(21)))
    customerLabel.grid(row=1, column=0, padx=int(5 * 1.5), pady=int(5 * 1.5), sticky="w")

    customerEntry = ctk.CTkEntry(customerFrame, width=int(screen_width * .73 ), font=("Times New Roman", int(12 * 1.5)))
    customerEntry.grid(row=1, column=1, padx=int(5 * 1.5), pady=int(5 * 1.5), sticky="w")

    # Create a new frame for customer buttons (10% increased sizes)
    customerButtonFrame = ctk.CTkFrame(mainContentFrame, fg_color="#dfd8c8")
    customerButtonFrame.pack(pady=int(2 * 1.5), padx=int(20 * 1.5), fill="x")  # 10% increased padding

    # Move buttons to customerButtonFrame
    selectCustomerButton = ctk.CTkButton(customerButtonFrame, text="Select Customer", width=int(screen_width * .15),fg_color= "#393939",hover_color="#252523", font=("Times New Roman", int(21)), command=lambda: openCustomerSelection(customerEntry,"selectCustomer",db))  # Increased width
    selectCustomerButton.grid(row=0, column=0, padx=int(5 * 1.5), pady=int(5 * 1.5))

    addCustomerButton = ctk.CTkButton(customerButtonFrame, text="Add New Customer", width=int(screen_width * .15),fg_color= "#393939",hover_color="#252523",  font=("Times New Roman", int(21)), command=lambda:openAddCustomerWindow(customerEntry,db))  # Increased width
    addCustomerButton.grid(row=0, column=1, padx=int(5 * 1.5), pady=int(5 * 1.5), sticky="w")

    # Function to clear the entry widget
    def clearEntry():
        global selectedCustomerDetails
        selectedCustomerDetails = {}
        customerEntry.delete(0, "end") 

    clearCustomerButton = ctk.CTkButton(customerButtonFrame, text="Clear", width=int(screen_width * .15), font=("Times New Roman", int(21)),fg_color= "#e62739",hover_color="#a93226", command=clearEntry)  # Increased width
    clearCustomerButton.grid(row=0, column=2, padx=int(5 * 1.5), pady=int(5 * 1.5), sticky="w")

    # Adding empty row below customer section
    customerSpacerBottom = ctk.CTkLabel(customerFrame, text="", font=("Times New Roman", int(12 * 1.5)))
    customerSpacerBottom.grid(row=3, column=0, pady=int(5 * 1.5))

    # Spacer Frame for spacing before Product Frame
    spacerFrame = tk.Frame(mainContentFrame, height=int(10 * 1.5))
    spacerFrame.pack(pady = 10)

    # Product section in a black-bordered box with Text widget and scrollbar (10% increased sizes)
    productFrame = ctk.CTkFrame(mainContentFrame, fg_color="#dfd8c8")
    productFrame.pack(padx=int(20 * 1.5), fill="x")  # 10% increased padding

    productLabel = ctk.CTkLabel(productFrame, text="Selected Products:", font=("Times New Roman", int(21)))
    productLabel.grid(row=1, column=0, padx=int(5 * 1.5), pady=int(5 * 1.5), sticky="w")

    # Create a Treeview widget with a vertical scrollbar
    treeFrame = ctk.CTkFrame(productFrame)  # A subframe to contain the Treeview and scrollbar
    treeFrame.grid(row=2, column=0, columnspan=2, padx=int(5 * 1.5), pady=int(5 * 1.5), sticky="nsew")

    productEntry = ttk.Treeview(
        treeFrame,
        columns=("Sl.No", "Name", "Quantity", "Unit Price", "Total Price"),
        show="headings",
        height=int(screen_height * 0.01),  # Approximate row height
    )

    # Set the column widths proportionally
    productEntry.column("Sl.No", width=int(screen_width * 0.05), anchor="center")
    productEntry.column("Name", width=int(screen_width * 0.58), anchor="w")
    productEntry.column("Quantity", width=int(screen_width * 0.1), anchor="center")
    productEntry.column("Unit Price", width=int(screen_width  * 0.1), anchor="center")
    productEntry.column("Total Price", width=int(screen_width * 0.15), anchor="center")

    # # Add column headers
    productEntry.heading("Sl.No", text="Sl.No")
    productEntry.heading("Name", text="Name")
    productEntry.heading("Quantity", text="Quantity")
    productEntry.heading("Unit Price", text="Unit Price")
    productEntry.heading("Total Price", text="Total Price")

    # Configure alternating row colors with tags
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview", font=("Times New Roman", 18), rowheight=30)  # Row height and font
    style.configure("Treeview.Heading", font=("Times New Roman", 16, "bold"))
    style.map("Treeview", background=[("selected", "#d3d3d3")])
    productEntry.tag_configure("oddrow", background="white")
    productEntry.tag_configure("evenrow", background="white")

    # Add vertical scrollbar for Treeview
    scrollbar = ttk.Scrollbar(treeFrame, orient="vertical", command=productEntry.yview)
    productEntry.configure(yscroll=scrollbar.set)

    # Pack Treeview and Scrollbar
    scrollbar.pack(side="right", fill="y")
    productEntry.pack(side="left", fill="both", expand=True)

    # Create a new frame for product buttons (10% increased sizes)
    productButtonFrame = ctk.CTkFrame(mainContentFrame, fg_color="#dfd8c8")
    productButtonFrame.pack(pady=int(2 * 1.5), padx=int(20 * 1.5), fill="x")  # 10% increased padding

    # Move buttons to productButtonFrame
    selectProductButton = ctk.CTkButton(productButtonFrame, text="Select Product", width=int(screen_width * .15), fg_color= "#393939",hover_color="#252523", font=("Times New Roman", int(21)),command=lambda: openSelectProductWindow(productEntry,db))  # Increased width
    selectProductButton.grid(row=0, column=0, padx=int(5 * 1.5), pady=int(5 * 1.5))

    removeProductButton = ctk.CTkButton(productButtonFrame, text="Remove Product", width=int(screen_width * .15), fg_color= "#e62739",hover_color="#a93226",font=("Times New Roman", int(21)),command=lambda: removeProduct(productEntry))  # Increased width
    removeProductButton.grid(row=0, column=1, padx=int(5 * 1.5), pady=int(5 * 1.5))

    addProductButton = ctk.CTkButton(productButtonFrame, text="Add New Product", width=int(screen_width * .15),fg_color= "#393939",hover_color="#252523",  font=("Times New Roman", int(21)),command=lambda:openAddProductWindow(productEntry,db))  
    addProductButton.grid(row=0, column=2, padx=int(5 * 1.5), pady=int(5 * 1.5), sticky="w")

    # Adding empty row below product section
    productSpacerBottom = ctk.CTkLabel(productFrame, text="", font=("Times New Roman", int(12 * 1.5)))
    productSpacerBottom.grid(row=3, column=0, pady=int(5 * 1.5))

    # Action buttons (10% increased sizes)
    actionFrame = ctk.CTkFrame(mainContentFrame, fg_color="#dfd8c8")
    actionFrame.pack(pady=int(20 * 1.5))

    # Increased button size (10% increase)
    generateInvoiceButton = ctk.CTkButton(actionFrame, text="Generate Invoice", width=int(screen_width * .15),fg_color= "#393939",hover_color="#252523",  font=("Times New Roman", int(21)),command = lambda:generateInvoice(db))
    generateInvoiceButton.grid(row=0, column=0, padx=int(10 * 1.5), pady=int(5 * 1.5))

    printInvoiceButton = ctk.CTkButton(actionFrame, text=" Print Invoice ", width=int(screen_width * .15),fg_color= "#393939",hover_color="#252523",  font=("Times New Roman", int(21)))
    printInvoiceButton.grid(row=0, column=1, padx=int(10 * 1.5), pady=int(5 * 1.5))

    clearAllButton = ctk.CTkButton(actionFrame, text=" Clear All ", width=int(screen_width * .15),fg_color= "#e62739",hover_color="#a93226",  font=("Times New Roman", int(21)), command = clear_data)
    clearAllButton.grid(row=0, column=2, padx=int(10 * 1.5), pady=int(5 * 1.5))


    # Run the application
    root.mainloop()

# Run the main function to initialize the application
main()
