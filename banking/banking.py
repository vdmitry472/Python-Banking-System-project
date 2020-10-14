
import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS card')
conn.commit()
cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
conn.commit()

class CreditCard:
    all_cards = []

    def __init__(self):
        id = int()
        pin = str()
        num = str()
        for i in range(4):
            pin = pin + str(random.randint(0, 9))
        self.pin = pin
        self.balance = 0
        for x in range(9):
            num = num + str(random.randint(0, 9))
        count = 0
        sum = 0
        number = str(400000) + num
        while count <= 14:
            if (count + 1) % 2 != 0:
                x = int(number[count])
                x = x * 2
                if x > 9:
                    x = x - 9
                sum += x
            else:
                sum += int(number[count])
            count += 1
        check = 10
        while check < sum:
            check += 10
        checksum = check - sum
        res = number + str(checksum)
        self.number = res
        CreditCard.all_cards.append(self)
        cur.execute("INSERT INTO card (number, pin) VALUES ('{}', '{}')".format(res, pin))
        conn.commit()

def create (number, pin, balance):
    card = CreditCard()
    card.number = number
    card.pin = pin
    card.balance = balance
    return card


def start_menu():
    i = 2
    while i > 0:
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
        choice = int(input())
        if choice == 1:
            create_card()
        elif choice == 2:
            log()
        else:
            print("Bye!")
            exit()

def create_card():
    new_card = CreditCard()
    print("")
    print("Your card has been created")
    print("Your card number:")
    print(new_card.number)
    print("Your card PIN:")
    print(new_card.pin)

def log():
    num = input("Enter your card number:")
    pin = input("Enter your PIN:")
    cur.execute("SELECT number, pin, balance FROM card")
    for row in cur:
        if num.strip() == row[0] and pin.strip() == row[1]:
            print("You have successfully logged in")
            card = create(row[0], row[1], row[2])
            logged_menu(card)
            is_logged = True
        else:
            is_logged = False
    if is_logged == False:
        print("Wrong card number or PIN!")

def is_luhn_validated(number):
    count = 0
    sum = 0
    while count <= 14:
        if (count + 1) % 2 != 0:
            x = int(number[count])
            x = x * 2
            if x > 9:
                x = x - 9
            sum += x
        else:
            sum += int(number[count])
        count += 1
    check = 10
    while check < sum:
        check += 10
    checksum = check - sum
    return checksum


def transfer(card):
    print("Transfer")
    res_number = input("Enter card number:").strip()
    check = is_luhn_validated(res_number)
    if res_number[0] != "4":
        print("Such a card does not exist.")
        logged_menu(card)
    if str(check) != res_number[15]:
        print("Probably you made a mistake in the card number. Please try again!")
        logged_menu(card)
    cur.execute("SELECT number FROM card")
    is_exist = False
    for row in cur:
        if res_number == row[0]:
            is_exist = True
    if res_number == card.number:
        print("You can't transfer money to the same account!")
        logged_menu(card)
    elif is_exist == False:
        print("Such a card does not exist.")
        logged_menu(card)
    if is_exist:
        print("Enter how much money you want to transfer:")
    transaction = int(input())
    if card.balance < transaction:
        print("Not enough money!")
        logged_menu(card)
    else:
        cur.execute("UPDATE card SET balance = balance + {} WHERE number = {}".format(transaction, res_number))
        cur.execute("UPDATE card SET balance = balance - {} WHERE number = {}".format(transaction, card.number))
        conn.commit()
        card.balance -= transaction
        print("Success!")






def logged_menu(card):
    i = 2
    while i > 0:
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")
        choice = int(input())
        if choice == 1:
            print("Balance: " + str(card.balance))
        elif choice == 2:
            print("Enter income:")
            inc = int(input())
            cur.execute("UPDATE card SET balance = balance + {} WHERE number = {}".format(inc,card.number))
            conn.commit()
            print("Income was added!")
            card.balance += inc
        elif choice == 3:
            transfer(card)
        elif choice == 4:
            cur.execute("DELETE FROM card WHERE number = '{}'".format(card.number))
            conn.commit()
            print("The account has been closed!")
            start_menu()
        elif choice == 5:
            print("You have successfully logged out!")
            start_menu()
        else:
            print("Bye!")
            exit()


start_menu()




