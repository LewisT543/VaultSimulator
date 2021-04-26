
import datetime
import pandas as pd
import numpy as np

class Vault:

    '''Vault must have a balance, a yield and a method to increment 
        the current balance by the vaults yield'''
    
    fees = 0.50 # Depends on current Binance Smart Chain gas fees

    def __init__(self, daily_yield, start_balance, numdays):
        self.balance = start_balance
        self.daily_yield = daily_yield
        self.farm_time = numdays
        self.rewards = 0
        self.deposits = 0
        self.fees_paid = 0
    
    def add_rewards(self):
        self.rewards += (self.balance * self.daily_yield)

    def harvest(self):
        rews = self.rewards
        self.rewards = 0
        self.pay_fees()
        self.compound(rews)
    
    def compound(self, harvest_amt):
        self.deposits += harvest_amt
        self.balance += (2 * harvest_amt)
        self.pay_fees()
        # Extra one to account for missing PancakeSwap trade
        self.pay_fees() 

    def pay_fees(self):
        self.fees_paid += Vault.fees

        

    #methods:
    # deposit
    # Increment balance
    # Harvest (reset rewards)

