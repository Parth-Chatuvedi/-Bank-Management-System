import sys
import matplotlib.pyplot as plt
import mysql.connector as sql
import pandas as pd

conn = sql.connect(host="localhost", user="root", password="YES", database="bank", charset='utf8')
cur = conn.cursor()


def bank_menus():
    print()
    print("1. Add Bank Detail of A Person")
    print("2. Deposit Amount to Bank")
    print("3. Withdrawal Amount from Bank")
    print("4. View Balance")
    print("5. View Statement")
    print("6. Show Graph")
    print("0. Exit")
    choice = int(input('Enter an option: '))
    if choice == 1:
        add_account_detail()
    elif choice == 2:
        deposit()
    elif choice == 3:
        withdrawal()
    elif choice == 4:
        view_balance()
    elif choice == 5:
        view_statement()
    elif choice == 6:
        show_graph()
    else:
        sys.exit()


def add_account_detail():
    print(".....Enter Bank Detail.....")
    print()
    pid = input("Enter Person id: ")
    pid = pid.upper()
    accno = input("Enter Account No: ")
    pname = input("Enter Person Name: ")
    pname = pname.upper()
    doe = input("Enter Date Of Opening: ")
    contactno = input("Enter Contact no.: ")
    gender = input("Enter Gender: ")
    gender = gender.upper()
    bname = input("Enter Bank Name: ")
    bname = bname.upper()
    ifsc = input("Enter Bank IFSC code: ")
    accno = accno.upper()
    opamt = float(input("Enter Opening Amount: "))
    kycinfo = input("Enter KYC Detail: ")
    sq = "INSERT INTO account VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}')".format(pid, accno, pname, doe, contactno, gender, bname, ifsc, opamt, kycinfo)
    cur.execute(sq)
    conn.commit()
    print("....Successfully Recorded.....")
    ans = input("Enter Another Record? (y/n)")
    if ans == 'y':
        add_account_detail()
    else:
        bank_menus()


def deposit():
    print(".....Credit Details......:")
    print()
    pid = input("Enter Person id: ")
    pid = pid.upper()
    sq = "SELECT pid, acc_holder_name, accno, bank_name FROM account WHERE pid='{}'".format(pid)
    cur.execute(sq)
    data = cur.fetchone()
    if data:
        pname = data[1]
        accno = data[2]
        bname = data[3]
        print("Bank Id.......:", pid)
        print("Account Holder Name......:", pname)
        print("Bank Name........:", bname)
        print("_____________________")
        cramt = float(input("Enter Credited Amount: "))
        doc = input("Enter Date of Credit: ")
        sq = "INSERT INTO creditamount VALUES ('{}', '{}', {}, '{}', '{}', '{}')".format(pid, pname, cramt, doc, bname, accno)
        cur.execute(sq)
        conn.commit()
        sq = "UPDATE account SET opening_amount = opening_amount + {} WHERE pid='{}' AND accno='{}' AND bank_name='{}'".format(cramt, pid, accno, bname)
        cur.execute(sq)
        conn.commit()
        print("Recorded...")
        ans = input("Enter Another Record? (y/n)")
        if ans == 'y':
            deposit()
        else:
            bank_menus()
    else:
        print("No record found of this id:")
        ans = input("Try Again? (y/n)")
        if ans == 'y':
            deposit()
        else:
            bank_menus()


def withdrawal():
    print("...... Debit Details...........")
    print()
    pid = input("Enter Person id: ")
    pid = pid.upper()
    sq = "SELECT pid, acc_holder_name, accno, bank_name FROM account WHERE pid='{}'".format(pid)
    cur.execute(sq)
    data = cur.fetchone()
    if cur.rowcount!=-1:
        pname = data[1]
        accno = data[2]
        bname = data[3]
        print("Bank Id... :", pid)
        print("Account Holder Name......: ", pname)
        print("Bank Name.. .:", bname)
        print("___________________________")
        rs = input("Enter Reason................")
        dramt = float(input("Enter Debited Amount......"))
        doc = input("Enter Date of Debit: ")
        sq = 'INSERT INTO debitamount VALUES("' + pid + '","' + pname + '","' + str(dramt) + '","' + rs + '","' + doc + '","' + bname + '","' + accno + '")'

        cur.execute(sq)
        conn.commit()
        sq = "UPDATE account SET opening_amount = opening_amount - {} WHERE pid='{}' AND accno='{}' AND bank_name='{}'".format(dramt, pid, accno, bname)
        cur.execute(sq)
        conn.commit()
        print("Recorded...")
        ans = input("Enter Another Record? (y/n)")
        if ans == 'y':
            withdrawal()
        else:
            bank_menus()
    else:
        print("No record found of this id:")
        ans = input("Try Again? (y/n)")
        if ans == 'y':
            withdrawal()
        else:
            bank_menus()


def view_balance():
    print(". Balance. : ")
    print()
    pid = input("Enter Person id: ")
    pid = pid.upper()
    sq = "SELECT acc_holder_name, bank_name, accno, opening_amount FROM account WHERE pid='{}'".format(pid)
    cur.execute(sq)
    data = cur.fetchone()
    if cur.rowcount!=-1:
        print("Name of Account Holder.......", data[0])
        print("Bank Name.................", data[1])
        print("Bank Account No..............", data[2])
        print(".... Current Balance...........", data[3])
        ans = input("Check Again? (y/n)")
        if ans == 'y':
            view_balance()
        else:
            bank_menus()
    else:
        print("No record found of this id:")
        ans = input("Try Again? (y/n)")
        if ans == 'y':
            view_balance()
        else:
            bank_menus()


def view_statement():
    print("............ Generate Statement.......... : ")
    print()
    pid = input("Enter Person id: ")
    pid = pid.upper()
    tp = input("Debit or Credit Statement: ")
    if tp.upper() == "DEBIT":
        tp = "debitamount"
    elif tp.upper() == "CREDIT":
        tp = "creditamount"
    sq = "SELECT * FROM {} WHERE pid='{}'".format(tp, pid)
    df = pd.read_sql(sq, conn, index_col=['pid'])
    if df.empty:
        print("No Data Available")
    else:
        print(df)
    ans = input("Check Again? (y/n)")
    if ans == 'y':
        view_statement()
    else:
        bank_menus()


def show_graph():
    print("........ Generate Statement. ")
    print()
    pid = input("Enter Person id: ")
    pid = pid.upper()
    tp = input("Debit or Credit Statement: ")
    if tp.upper() == "DEBIT":
        tp = "debitamount"
    elif tp.upper() == "CREDIT":
        tp = "creditamount"
    sq = "SELECT * FROM {} WHERE pid='{}'".format(tp, pid)
    df = pd.read_sql(sq, conn, index_col=['pid'])
    if df.empty:
        print("No Data Available")
    else:
        df.plot(kind='bar', x='doc')
    ans = input("Check Again? (y/n)")
    if ans == 'y':
        view_graph()
    else:
        bank_menus()


bank_menus()
