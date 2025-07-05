# Requirements
# Provide user login and register
# Provide user access to add balance, view balance and withdraw balance after login
# User's should be only able to work with their own balance data only

# Important - Use oop(Better program structure), File handling(Data storage), Git and Github for Version Control

import json
import os

DATA_FILE = 'users.json'

class User:
    def __init__(self, username, password, balance=0.0):
        self.username = username
        self.password = password
        self.balance = balance

    def to_dict(self):
        return {
            'username': self.username,
            'password': self.password,
            'balance': self.balance
        }

class BankSystem:
    def __init__(self):
        self.users = {}  
        self.current_user = None
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                for user_data in data:
                    user = User(
                        username = user_data['username'],
                        password = user_data['password'],
                        balance = user_data.get('balance', 0.0)
                    )
                    self.users[user.username] = user
        else:
            self.users = {}

    def save_data(self):
        with open(DATA_FILE, 'w') as f:
            json.dump([user.to_dict() for user in self.users.values()], f, indent=4)

    def register(self, username, password):
        if username in self.users:
            print("Username already exists.")
            return False
        self.users[username] = User(username, password)
        self.save_data()
        print("Registration successful.")
        return True

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.password == password:
            self.current_user = user
            print(f"Logged in as {username}")
            return True
        print("Invalid username or password.")
        return False

    def add_balance(self, amount):
        if self.current_user:
            self.current_user.balance += amount
            self.save_data()
            print(f"Balance updated. New balance: {self.current_user.balance}")
        else:
            print("Please login first.")

    def view_balance(self):
        if self.current_user:
            print(f"Your current balance is: {self.current_user.balance}")
        else:
            print("Please login first.")

    def withdraw_balance(self, amount):
        if self.current_user:
            if amount > self.current_user.balance:
                print("Insufficient balance.")
            else:
                self.current_user.balance -= amount
                self.save_data()
                print(f"Withdrawal successful. New balance: {self.current_user.balance}")
        else:
            print("Please login first.")

    def logout(self):
        self.current_user = None
        print("Logged out.")

def main():
    system = BankSystem()

    while True:
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your  choice: ")

        if choice == '1':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            system.register(username, password)

        elif choice == '2':
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            if system.login(username, password):
                while True:
                    print("1. View Balance")
                    print("2. Add Balance")
                    print("3. Withdraw Balance")
                    print("4. Logout")
                    user_choice = input("Enter your choice: ")

                    if user_choice == '1':
                        system.view_balance()
                    elif user_choice == '2':
                        amount = float(input("Enter amount to add: "))
                        system.add_balance(amount)
                    elif user_choice == '3':
                        amount = float(input("Enter amount to withdraw: "))
                        system.withdraw_balance(amount)
                    elif user_choice == '4':
                        system.logout()
                        break
                    else:
                        print("Invalid choice.")
        elif choice == '3':
            print("Goodbiieeeeee!!")
            break
        else:
            print("Invalid choice.")
if __name__ == "__main__":
    main()