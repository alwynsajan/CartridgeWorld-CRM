import mysql.connector
import json

class DbServer:
    def __init__(self, configFile='config.json'):
        # Load database credentials from the config.json file
        self.config = self.loadConfig(configFile)

    def loadConfig(self, configFile):
        """Load configuration from JSON file"""
        with open(configFile, 'r') as file:
            return json.load(file)
    
    def connectToDB(self):
        """Establish a connection to the database"""
        return mysql.connector.connect(
            host=self.config["db"]["host"],
            port=self.config["db"]["port"], 
            user=self.config["db"]["user"],
            password=self.config["db"]["password"],
             database=self.config["db"]["database"],
            charset="utf8mb4",
            collation="utf8mb4_general_ci"
        )
    
    def executeQuery(self, query, data):
        """Helper function to execute an insert query and return success/failure response"""
        try:
            conn = self.connectToDB()
            cursor = conn.cursor()
            cursor.execute(query, data)
            conn.commit()
            response = {
                "status": "Success",
                "message": "Query executed successfully."
            }
        except mysql.connector.Error as err:
            response = {
                "status": "Failed",
                "message": f"Error: {err}"
            }
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
        return response

    def addCustomerData(self, customerData):
        """Add customer data to the customerData table"""
        query = """
        INSERT INTO customerData (name, customerType, email, phone, address, state, postcode, ABN)
        VALUES (%s, %s, %s, %s, %s, %s, %s,%s)
        """
        return self.executeQuery(query, (
            customerData['name'],
            customerData['customerType'],
            customerData['email'],
            customerData['phone'],
            customerData['address'],
            customerData['state'],
            customerData['postcode'],
            customerData['ABN']
        ))
    
    def getCustomerName(self):
        """Retrieve all customer IDs and names from the customerData table"""
        query = "SELECT customerID, name FROM customerData"
        
        try:
            conn = self.connectToDB()
            cursor = conn.cursor()
            cursor.execute(query)
            customerList = cursor.fetchall()  # Fetch all results
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            customerList = []  # Return an empty list on failure
        finally:
            cursor.close()
            conn.close()
        
        return customerList  # Returns a list of tuples [(id1, name1), (id2, name2), ...]

    def getCustomerIDByName(self, customerName):
        """Retrieve the customer ID based on the customer's name"""
        query = "SELECT customerID FROM customerData WHERE name = %s"
        
        try:
            conn = self.connectToDB()
            cursor = conn.cursor()
            cursor.execute(query, (customerName,))
            result = cursor.fetchone()
            customerID = result[0] if result else None
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            customerID = None
        finally:
            cursor.close()
            conn.close()
        
        return customerID

    def getCustomerDetails(self, customerID, name):
        """Retrieve customer details based on customer ID and name"""
        query = """
        SELECT customerID, customerType, name, address, state, postcode, phone, email, ABN 
        FROM customerData 
        WHERE customerID = %s AND name = %s
        """
        
        try:
            conn = self.connectToDB()
            cursor = conn.cursor()
            cursor.execute(query, (customerID, name))
            customerDetails = cursor.fetchone()  # Fetch only one result
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            customerDetails = None  # Return None on failure
        finally:
            cursor.close()
            conn.close()

        return customerDetails  # Returns a tuple or None if not found
    
    def addProductData(self, productData):
        """Insert new product into the productData table"""
        query = """
        INSERT INTO productData (name, productType, colour, price)
        VALUES (%s, %s, %s, %s)
        """
        return self.executeQuery(query, (
            productData["name"],
            productData["productType"],
            productData["colour"],
            productData["price"]
        ))
    
    def getProductByName(self, productName):
        """Check if a product with the given name exists in the productData table."""
        query = "SELECT productID FROM productData WHERE name = %s"

        try:
            conn = self.connectToDB()
            cursor = conn.cursor()
            cursor.execute(query, (productName,))
            product = cursor.fetchone()  # Fetch one matching record
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            product = None  # Return None in case of an error
        finally:
            cursor.close()
            conn.close()

        return product  # Returns (productID,) if found, else None


    def getProductDetails(self, productName):
        """Retrieve a product by name from the productData table"""
        query = """
        SELECT name, productType, colour, price
        FROM productdata
        WHERE name = %s
    """
        try:
            conn = self.connectToDB()
            cursor = conn.cursor()
            cursor.execute(query, (productName,))
            product = cursor.fetchone()  # Fetch one product
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            product = None
        finally:
            cursor.close()
            conn.close()

        return product  # Returns tuple (productID, Name, Product_Type, Colour, Price) or None
    
    def getProductNamesAndIds(self):
        """Get all product names and IDs from the database"""
        query = "SELECT productID, Name FROM productdata"
        
        try:
            conn = self.connectToDB()
            cursor = conn.cursor()
            cursor.execute(query)
            products = cursor.fetchall()  # Fetch all results
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            products = []  # Return an empty list on failure
        finally:
            cursor.close()
            conn.close()
        
        return products  # Returns a list of tuples [(id1, name1), (id2, name2), ...]

    def addPerDaySale(self, saleData):
        """Add or update per-day sales data in the PerdaySale table"""
        # Fetch current sales value for the given date
        queryFetch = "SELECT sales FROM PerdaySale WHERE date = %s"
        try:
            conn = self.connectToDB()
            cursor = conn.cursor()
            cursor.execute(queryFetch, (saleData['date'],))
            result = cursor.fetchone()
            
            if result:
                # If there's an existing record, add the current sales to the existing sales
                currentSales = result[0]
                updatedSales = float(currentSales) + float(saleData['sales'])
                queryUpdate = "UPDATE PerdaySale SET sales = %s WHERE date = %s"
                cursor.execute(queryUpdate, (updatedSales, saleData['date']))
                conn.commit()
                response = {
                    "status": "Success",
                    "message": f"Sales updated for {saleData['date']}."
                }
            else:
                # If no record exists, insert a new record
                queryInsert = "INSERT INTO PerdaySale (date, sales) VALUES (%s, %s)"
                cursor.execute(queryInsert, (saleData['date'], saleData['sales']))
                conn.commit()
                response = {
                    "status": "Success",
                    "message": f"New sales record added for {saleData['date']}."
                }
        except mysql.connector.Error as err:
            response = {
                "status": "Failed",
                "message": f"Error: {err}"
            }
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
        
        return response
    
    def getPerDaySalesData(self):
        """Retrieve total sales grouped by date from the database."""
        query = """
        SELECT date, sales AS totalSales
        FROM perdaysale
        ORDER BY date DESC
        """
        try:
            conn = self.connectToDB()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
        except mysql.connector.Error:
            results = []
        finally:
            cursor.close()
            conn.close()
        return results
    

    def addSalesData(self, salesData):
        """Add sales transaction data to the salesData table"""
        query = """
        INSERT INTO salesData (date, customerID, customerName, customerAddress, customerPhone, productName, productType, colour, price, quantity, paymentType)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        return self.executeQuery(query, (
            salesData['date'],
            salesData['customerID'],
            salesData['customerName'],
            salesData['customerAddress'],
            salesData['customerPhone'],
            salesData['productName'],
            salesData['productType'],
            salesData['colour'],
            salesData['price'],
            salesData['quantity'],
            salesData['paymentType']
        ))
    
    def getSalesByCustomerName(self, customerName):
        """Retrieve all sales records for a given customer name."""
        query = """
        SELECT date, customerAddress, customerPhone, productName, productType, colour, price, quantity, paymentType
        FROM salesData
        WHERE customerName = %s
        ORDER BY date DESC
        """

        try:
            conn = self.connectToDB()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, (customerName,))
            sales = cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
            sales = []
        finally:
            cursor.close()
            conn.close()

        return sales
    
    def getCreditSalesData(self):
        """Retrieve all sales transactions with payment type 'Credit'"""
        query = """
        SELECT date, customerName, customerAddress, customerPhone, productName, price, quantity
        FROM salesData WHERE paymentType = 'Credit'
        """
        try:
            conn = self.connectToDB()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            results = cursor.fetchall()
        except mysql.connector.Error:
            results = []
        finally:
            cursor.close()
            conn.close()
        return results


    def updatePaymentType(self, customerName):
        """Update payment type to 'Paid' for a given customer"""
        query = "UPDATE salesData SET paymentType = 'Paid' WHERE customerName = %s AND paymentType = 'Credit'"
        try:
            conn = self.connectToDB()
            cursor = conn.cursor()
            cursor.execute(query, (customerName,))
            conn.commit()
        except mysql.connector.Error:
            conn.rollback()
        finally:
            cursor.close()
            conn.close()


