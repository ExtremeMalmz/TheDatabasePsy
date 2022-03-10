#Eric Malmström - Informationsarkitektsprogrammet Malmö Universitet - Databasteknik VT2022-DA297A

#gives the current date
from datetime import date
todaysDate = date.today()

def customer_menu_printer(message):
    print("="*20 + '\n' + message + '\n' + "="*20)

def print_All_Products(connection):
    customer_menu_printer("Listing all products")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products")
    records = cursor.fetchall()
    for row in records:
        print("---")
        print("Product ID: ", row[0]),
        print("Product Name:", row[1]),
        print("Baseprice : ", row[2]),
        print("Supplier : ", row[3]),
        print("Quantity : ", row[4])

    cursor.close()

def search_by_ID(connection,date):
    productID = str(input("Enter the ID of the product you wish to find\n"))

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Products WHERE productID = %s AND productID = %s", (productID,productID))
    records = cursor.fetchall()

    if records == []:
        print("Product not found!")
    else:   
        for row in records:
            basePrice = row[2] 
            print("Product ID: ", row[0]),
            print("Product Name:", row[1]),
            print("Baseprice : ", row[2]),
            print("Supplier : ", row[3]),
            print("Quantity : ", row[4])

    cursor.execute("SELECT * FROM discountsAndProducts INNER JOIN discounts ON (discountsAndProducts.discountID = discounts.discountID AND discountsAndProducts.startdate<=%s AND discountsAndProducts.endDate >= %s)",(date, date))
    records = cursor.fetchall()

    if records == []:
        print("No discount for this product")
    else:
        for row in records:
            discountPercent = row[4]
            discountPercent = float(discountPercent)/100
            totalPrice = int(abs(((discountPercent/basePrice) * 100)-basePrice))
        print(f"Discount amount: {discountPercent}%")
        print(f"Total price is {totalPrice}")
        
    cursor.close()

def search_by_name(connection,date):
    productName = str(input("Enter the name of the product you wish to find\n"))

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Products WHERE productName = %s AND productName = %s", (productName,productName))
    records = cursor.fetchall()

    if records == []:
        print("Product not found!")
    else:   
        for row in records:
            basePrice = row[2] 
            print("Product ID: ", row[0]),
            print("Product Name:", row[1]),
            print("Baseprice : ", row[2]),
            print("Supplier : ", row[3]),
            print("Quantity : ", row[4])

    cursor.execute("SELECT * FROM discountsAndProducts INNER JOIN discounts ON (discountsAndProducts.discountID = discounts.discountID AND discountsAndProducts.startdate<=%s AND discountsAndProducts.endDate >= %s)",(date, date))
    records = cursor.fetchall()

    if records == []:
        print("No discount for this product")
    else:
        for row in records:
            discountPercent = row[4]
           
            discountPercent = float(discountPercent)/100
            totalPrice = int(abs(((discountPercent/basePrice) * 100)-basePrice))
            print(f"Discount amount: {discountPercent}%")
            print(f"Total price is {totalPrice}")
    

def search_Discounts(connection,date):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM discountsAndProducts INNER JOIN discounts ON (discountsAndProducts.discountID = discounts.discountID AND discountsAndProducts.startdate<=%s AND discountsAndProducts.endDate >= %s)",(date, date))
    records = cursor.fetchall()
 
    if records == []:
        print("No discounted product found")
    else:
        for row in records:
            print("---\nDISCOUNTED PRODUCT\n---")
            print("product ID: ", row[0]),
            print("product Name: ", row[1]),
            print("Discount name: ", row[3]),
            print("Discount Amount (percentage): ", row[4]),
            print("Start date: ", row[5]),
            print("End date: ", row[6])
            
    cursor.close()

def search_Products(connection,date):
    customer_menu_printer("Search for a product")
    print("1-Search by ID \n2-Search by Product Name \n3-See all ongoing discounts")
    userInput = str(input("Your choice: "))
    
    match userInput:
        case '1':
            search_by_ID(connection,date)
        case '2':
            search_by_name(connection,date)
        case '3':
            search_Discounts(connection,date)

def add_to_shopping_list(connection,email,date):
    customer_menu_printer("Add to your shopping list")

    newAmount = 0
    productID = int(input("Enter product ID: "))
    productName = str(input("Enter product name: "))
    productAmount = int(input("Enter the amount you'd like to buy: "))

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE productID = %s AND productName = %s",(productID,productName))
    records = cursor.fetchall()
    for row in records:
        originalAmount = row[4]
        newAmount = originalAmount - productAmount
    if newAmount < 0:
        print("Product amount not available")
    else:
        cursor.execute("UPDATE Products SET quantity = %s WHERE productID = %s",(newAmount,productID))
        connection.commit()
        print(f"You have sucessfully ordered {productAmount} of the product {productName}")
        print("Thanks for your purchase and an admin will confirm your order shortly")

    cursor.execute("INSERT INTO orders (useremail,productId,productname,productamount,dateordered,confirmedorder) VALUES (%s,%s,%s,%s,%s,%s)",(email,productID,productName,productAmount,date,'no'))
    connection.commit()

    
    cursor.close()
    
def view_shopping_list(connection,email):
    customer_menu_printer("Displaying shopping list")

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM orders WHERE userEmail = %s AND userEmail = %s",(email,email))
    records = cursor.fetchall()
    for row in records:
        print("Order id: ", row[0]),
        print("Product id: ", row[2]),
        print("Product name: ", row[3]),
        print("Product amount: ", row[4]),
        print("Date ordered: ", row[5]),
        print("Confirmed order status: ", row[6])
        print("---")
    
    
    cursor.execute("SELECT * FROM orders INNER JOIN products ON (orders.productID = products.productID AND useremail = %s AND useremail = %s)",(email,email))
    records = cursor.fetchall()

    totalProductPrice = 0
    for row in records:
        
        productAmount = row[4]
        productPrice = row[9]

        totalProductPrice = (productAmount*productPrice)+totalProductPrice
    print(f"Original cost is: {totalProductPrice}")    
        
    cursor.execute("SELECT * FROM orders INNER JOIN discountsandproducts ON (discountsandproducts.productID = orders.productID AND userEmail = %s AND userEmail = %s AND startDate <= dateOrdered AND endDate >= dateOrdered) INNER JOIN products ON (orders.productID = products.productID)",(email,email))
    records = cursor.fetchall()

    totalDiscountPrice = 0
    for row in records:
        discountProductAmount = row[4]
        discountPercent = row[11]
        price = row[19]

        discountPercent = float(discountPercent)/100
            
        


        totalDiscountPrice = ((discountProductAmount * price)*discountPercent)+totalDiscountPrice  
    print(f"Total discounts are: {totalDiscountPrice}")
    finalPrice = totalProductPrice - totalDiscountPrice
    print(f"Final price is {finalPrice}")

    userInput = str(input("Do you want to pay this price?").upper())
    if userInput == 'YES':
        print("Thanks for paying!")
    else:
        print("Maybe next time")

    cursor.close()

def delete_from_shopping_list(connection,email):
    customer_menu_printer("Delete an Order")

    userInput = int(input("Enter the order ID to cancel it. If the order is confirmed you cant delete it: "))
    
    
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Orders WHERE useremail = %s AND orderID = %s", (email,userInput))
    records = cursor.fetchall()
    for row in records:
        print("Amount of product deleted: ", row[4])

    if records != []:
        cursor.execute("SELECT * FROM orders INNER JOIN products ON (orders.productID = products.productID AND useremail = %s AND orderID = %s)",(email,userInput))
        records = cursor.fetchall()
        for row in records:
            productID = row[2]
            orderProductAmount = row[4]
            totalProductAmount = row[11]
            
        
        totalProductAmount += orderProductAmount

        cursor.execute("UPDATE products SET quantity = %s WHERE productID = %s", (totalProductAmount,productID))
        connection.commit()

        cursor.execute("DELETE FROM orders WHERE orderID = %s AND userEmail = %s AND confirmedOrder = 'no'",(userInput,email))
        connection.commit()

        
        print("Order successfully deleted")
    else:
        print("Unable to delete order")
        

    

    cursor.close()
        
        

def customerMain(connection,email):
    
    print(f"Before you continue please enter the date (Todays date is: {todaysDate})\n OBSERVE: Write the date in numbers only")
    date = str(input("Type here: "))
    print(f"Date: {date}")

    while(True):
        customer_menu_printer("Welcome to the main Customer page")
        print("1- See products \n2- Search products \n3- See discounted products \n4- Add a product to your shopping list \n5- View shopping list\n6- Delete product from shopping list")
        
        userInput = str(input("Your input: "))
        match userInput:
            case '1':
                print_All_Products(connection)
            case '2':
                search_Products(connection,date)
            case '3':
                search_Discounts(connection,date)
            case '4':
                add_to_shopping_list(connection,email,date)
            case '5':
                view_shopping_list(connection,email)
            case '6':
                delete_from_shopping_list(connection,email)
            case _:
                print("I didnt understand that...")