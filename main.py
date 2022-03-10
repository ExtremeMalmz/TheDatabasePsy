#TODO : tests to see if everything works. Congrats on getting the thing done! 02/28/2022 23:07 - 675 lines of code 
#Eric Malmström - Informationsarkitektsprogrammet Malmö Universitet - Databasteknik VT2022-DA297A

from sqlite3 import OperationalError
import psycopg2

#Dont forget to save the file!
from Customer_main import *
from Admin_main import *

def connectToServer():
    '''connects to the mau pgserver, makes sure you have wifi'''
    #make sure you got wifi ha ha
    try:
        connection = psycopg2.connect(
            user="aj0363",
            password="tpdengsq",
            host="pgserver.mau.se",
            database="aj0363"
        )
        return connection
    except psycopg2.OperationalError:
        print("Your internet is off...turn it on!")
        exit()

def menu_printer(message):
    '''prints a message inbetween 10 -
    Args: Message - the indata recieved'''
    print("-"*10 + '\n' + message + '\n' + "-"*10)

def printAllProducts(connection):
    menu_printer("VIEW OUR PRODUCTS")

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

def searchProductName(connection):
    productName = str(input("Enter the name of the product you wish to find\n"))

    cursor = connection.cursor()

    #Who made this a thing which uses tuples? Only works with two values at the end
    cursor.execute("SELECT * FROM Products WHERE productname = %s AND productname = %s", (productName,productName))
    records = cursor.fetchall()
    if records == []:
        print("Product not found!")
    else:
        for row in records:
            print("Product ID: ", row[0]),
            print("Product Name:", row[1]),
            print("Baseprice : ", row[2]),
            print("Supplier : ", row[3]),
            print("Quantity : ", row[4])
            print("log in to see discounts!")
    
    cursor.close()

def searchProductPrice(connection):
    print("You will search for a product between 2 prices")
    lowestAmount = int(input("Enter the lowest price: "))
    highestAmount = int(input("Enter the highest price: "))

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products WHERE baseprice >= %s AND  baseprice <= %s", (lowestAmount,highestAmount))
    records = cursor.fetchall()
    if records == []:
        print("Product not found!")
    else:
        for row in records:
            print("Product ID: ", row[0]),
            print("Product Name:", row[1]),
            print("Baseprice : ", row[2]),
            print("Supplier : ", row[3]),
            print("Quantity : ", row[4])
            print("log in to see discounts!")

    cursor.close()

def searchProducts(connection):
    menu_printer("SEARCH OUR PRODUCTS")
    userInput = str(input("1-Search by name \n2- Search by price \nREMINDER: You have to be logged in to see discounts! \n"))

    match userInput:
        case '1':
            searchProductName(connection)
        case '2':
            searchProductPrice(connection)

def logIn(connection):
    '''logs the user into her account'''
    email = str(input("Enter Email: "))
    password = str(input("Enter Password: "))
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE useremail = %s AND userpassword = %s", (email,password))
    records = cursor.fetchall()
    if records == []:
        menu_printer("!!! The information you entered was incorrect !!!") 
    for row in records:
        print("*"*20)
        print("Welcome to the store,", row[1] + ' ' + row[2]) #for name just add + row[2]
        print("Your role is:", row[5])
        print("*"*20)
        if row[5] == 'Admin':            
            adminMain(connection)
        else:
            customerMain(connection,email)

    cursor.close()

def createCustomer(connection):
    '''Creates a Customer ''' 
    firstName = str(input("Enter your first name: "))
    lastName = str(input("Enter your last name: "))
    userPassword = str(input("Enter your password: "))
    userEmail = str(input("Enter your email: "))
    userRole = 'Customer'

    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (firstname,lastname,userpassword,useremail,userrole) VALUES (%s,%s,%s,%s,%s)", (firstName, lastName, userPassword, userEmail, userRole))
    connection.commit()

    cursor.close()
    
def main():
    connection = connectToServer()

    while(True):
        menu_printer("Welcome to the Online Game store")

        userInput = input(("1-See Products \n2-Search for products \n3-Log in \n4- Create a customer account \n"))
        match userInput:
            case '1':
                printAllProducts(connection)
            case '2':
                searchProducts(connection)
            case '3':
                logIn(connection)
            case '4':
                createCustomer(connection)
            case _:
                print("no understand")

if __name__ == '__main__':
    main()