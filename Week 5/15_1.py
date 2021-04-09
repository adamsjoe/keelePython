# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 19:20:21 2021

@author: Joseph
"""

class BankAccount(object):
    def __init__(self):            # Constructor DUNDER method
        self._balance = 0           # Called AUTOMATICALLY by
                                   # BankAccount()
            
    def withdraw(self, amount):
            accountBalance = self.get_balance()
            if amount > accountBalance:
                print("insufficient funds")
            else:
                self._balance -= amount     # balance is a PRIVATE member variable
                return self._balance   
            
    def deposit(self, amount):
        self._balance += amount
        return self._balance
    
    def get_balance(self):
        return self._balance
    
c = BankAccount()
c.deposit(1000)
print(c.get_balance())
c.withdraw(300)
print(c.get_balance())
c.withdraw(900)