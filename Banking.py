
import mysql.connector
import random
from datetime import date

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "Bank"
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE Bank")
# print("Database created !!")

# mycursor.execute("CREATE TABLE Customers (ID INT PRIMARY KEY, FULL_NAME VARCHAR(100), DOB DATE, GENDER VARCHAR(10), MOBILE VARCHAR(12), ADDRESS VARCHAR(255)) ")
# print("Table Created")

# mycursor.execute("CREATE TABLE Accounts (ACCOUNT_NO BIGINT PRIMARY KEY, ID INT , ACCOUNT_TYPE VARCHAR(20), BALANCE DECIMAL(12,2), OPEN_DATE DATE,  FOREIGN KEY (ID) REFERENCES Customers(ID))")
# print("Table created ")

# mycursor.execute("ALTER TABLE Customers MODIFY COLUMN ID INT AUTO_INCREMENT ")
# mycursor.execute("ALTER TABLE Customers AUTO_INCREMENT = 1")
# print("tABLE ALTERED")

while(True):
    print("\n===========================")
    print("Banking Management Syatem")
    print("===========================")
    print("\n1. Crete New Account")
    print("2. Display Account Details")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. Check Balance")
    print("6. Transfer Money")
    print("7. Display All Bank Accounts")
    print("8. Close Bank Account ")
    print("9. Exit")
    
    choice = int(input("Enter Your Choice :"))

    match choice:
        case 1:
            Full_Name = input("Enter Your Full Name:")
            print("\nDOB DATE: in format YYYY-MM-DD")
            Date_OF_Birth = input("Enter the DOB:")
            gender = input("Enter your Gender:")
            Mobile =int(input("Enter Mobile Number:"))
            address = input("Enter your Address:")
            
            sql = "INSERT INTO Customers(FULL_NAME, DOB, GENDER, MOBILE, ADDRESS) VALUES(%s, %s, %s, %s, %s)"
            val = ( Full_Name, Date_OF_Birth, gender,  Mobile, address)
            
            mycursor.execute(sql,val)
            mydb.commit()
            print(mycursor.rowcount,"Customers inserted")

            
            sqql = "Select ID from Customers where MOBILE = %s"
            mycursor.execute(sqql, (Mobile,))
            id = mycursor.fetchone()
            print(f"Your ID:{id[0]}")
            
           
            
            while(True):
                acc_no = random.randint(1000000000,9999999999)
                
                mycursor.execute("SELECT 1 FROM Accounts WHERE ACCOUNT_NO = %s", (acc_no,))
                
                if mycursor.fetchone() is None:
                    break
                
            print(f"Your Account Number:{acc_no}")    
            id =int(input("Enter Your ID:"))
            account_type = input("Enter the Type of account:")
            
            balance = int(input("Enter the Starting Ammount:"))
            open_date = date.today()
            
            
            
            sqls = "INSERT INTO Accounts VALUES(%s, %s, %s, %s, %s)"
            value = (acc_no, id, account_type,  balance, open_date)
            
            mycursor.execute(sqls, value)
            mydb.commit()
            
            print(mycursor.rowcount," Account Created") 

        case 2: 
            acc_no = int(input("Enter Your Account No. :"))
            
            sql = "SELECT Customers.ID, Customers.FULL_NAME, Customers.GENDER, Customers.DOB ,Customers.MOBILE, Customers.ADDRESS, Accounts.ACCOUNT_TYPE, Accounts.ACCOUNT_NO, Accounts.OPEN_DATE FROM Customers JOIN Accounts ON Accounts.ID = Customers.ID  WHERE ACCOUNT_NO = %s"
            val = (acc_no,)
            mycursor.execute(sql, val)
            
            myresult = mycursor.fetchone()
            
            if myresult:
                print("=== Customers Details ===\n")
                print("Customers ID\t:",myresult[0])
                print("Full Name\t:",myresult[1])
                print("Gender\t\t:",myresult[2])
                print("Date Of Birth\t:",myresult[3])
                print("Mobile\t\t:",myresult[4])
                print("Address\t\t:",myresult[5])
                
                print("\n===Account Details===\n")
                print("Account Type\t:",myresult[6])
                print("Account Number\t:",myresult[7])
                print("Open Date\t:",myresult[8])
                
            else:
                print("ACCOUNT NOT FOUND!!")
              
                
        case 3:
            acc_no = int(input("Enter Your Account No :"))
            
            mycursor.execute("SELECT 1 FROM Accounts WHERE ACCOUNT_NO = %s", (acc_no,))
                            
            if mycursor.fetchone() is None:
                print("Account Not Found !!")
                
            else:
                    
                mycursor.execute("SELECT BALANCE FROM Accounts WHERE ACCOUNT_NO = %s", (acc_no,))
                balance = mycursor.fetchone()
                print(f"Your Balance = {balance[0]}")
            
                total = balance[0]
                amount = int(input("\nEnter Depositing Amount:"))
                total += amount
            
                sql = ("UPDATE Accounts SET BALANCE = %s WHERE ACCOUNT_NO = %s")
                val = (total, acc_no)
            
                mycursor.execute(sql, val)
                mydb.commit()
                print("Money Deposited Successfully !!")
            
            
                
                
        case 4:
            acc_no = int(input("Enter Your Account No :"))
             
            mycursor.execute("SELECT 1 FROM Accounts WHERE ACCOUNT_NO = %s", (acc_no,))
                                         
            if mycursor.fetchone() is None:
                print("Account Not Found !!")
             
            else: 
                mycursor.execute("SELECT BALANCE FROM Accounts WHERE ACCOUNT_NO = %s", (acc_no,))
                balance = mycursor.fetchone()
                print(f"Your Balance = {balance[0]}")
            
                total = balance[0]
            
                amount = int(input("\nEnter Withdrawing Amount:"))
            
                if amount > total:
                    print("Insufficient Balance !!")

                else : 
                    total -= amount
            
                    sql = ("UPDATE Accounts SET BALANCE = %s WHERE ACCOUNT_NO = %s")
                    val = (total, acc_no)
            
                    mycursor.execute(sql, val)
                    mydb.commit()
                    print("Money Withdrawed Successfully !!")
                    
        case 5:
            
            acc_no = int(input("Enter Your Account Number:"))
            
            mycursor.execute("SELECT 1 FROM Accounts WHERE ACCOUNT_NO = %s",(acc_no,))
            
            if mycursor.fetchone() is None:
                print("Account Not Found !!")
                
            else:
                mycursor.execute("SELECT BALANCE FROM Accounts WHERE ACCOUNT_NO = %s",(acc_no,))
                myresult = mycursor.fetchone()
                
                
                print(f"BALANCE = {myresult[0]}")
                
        case 6:
            
            user = int(input("Enter Your Account Number:"))
            
            mycursor.execute("SELECT BALANCE FROM Accounts WHERE ACCOUNT_NO = %s",(user,))
            myresult = mycursor.fetchone()
            
            print(f"Your Balance = {myresult[0]}")
            
            receiver = int(input("Enter Receivers Account Number:"))
            amount = int(input("Enter The Amount To Transfer:"))
            
            balance1 = myresult[0]
            
            mycursor.execute("SELECT BALANCE FROM Accounts WHERE ACCOUNT_NO = %s", (receiver,))
            myresult = mycursor.fetchone()
            
            balance2 = myresult[0]
            
            if amount > balance1 :
                print("Insufficient Balance !!")
                
            else :
                balance1 -= amount
                balance2 += amount
                
                sql1 = "UPDATE Accounts SET BALANCE = %s WHERE ACCOUNT_NO = %s"
                value1 = (balance1, user)
                
                sql2 = "UPDATE Accounts SET BALANCE = %s WHERE ACCOUNT_NO = %s"
                value2 = (balance2, receiver)
                
                mycursor.execute(sql1, value1)
                mycursor.execute(sql2, value2)
                mydb.commit()
                
                print("Money Deposited Successfully!!")
                
                
        case 7:
            
            mycursor.execute("SELECT Customers.ID, Customers.Full_Name, Customers.Gender, Accounts.ACCOUNT_NO, Accounts.Open_Date FROM Customers JOIN Accounts ON Accounts.ID = Customers.ID")
            
            myresult = mycursor.fetchall()
            for x in myresult :
                print(x)
                

        case 8:
            id = int(input("Enter Your ID:"))
            
                        
            mycursor.execute("SELECT 1 FROM Customers WHERE ID = %s", (id,))
                                                    
            if mycursor.fetchone() is None:
                print("Account Not Found !!") 
           
            else:
                mycursor.execute("DELETE FROM Accounts WHERE ID = %s", (id,))
                mycursor.execute("DELETE FROM Customers WHERE ID = %s", (id,))
                mydb.commit()
            
                print("Account and Customer Deleted Sucessfully !!")
            
        case 9:
           print("Thank you!")
           print("For Using Our Banking System !!")
           
           break 
                    

            
