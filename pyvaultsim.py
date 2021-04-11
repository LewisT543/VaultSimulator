        
'''This is a program designed to emulate a defi vault, 
in which the rewards are earned in the native token'''


import datetime

class VaultError(Exception):
    pass

global initial_deposit
initial_deposit = 1000

class AUTOBNBVault:

    daily_yield_pct = 0.005
    compound_rewards_target = 10
    fees = 1

    def __init__(self):
        self._balance = initial_deposit
        self._rewards = 0
        # self.history = {}
        self.elapsed_days = 0
        self.usd_in = 0
    
    @property
    def deposits(self):
        return self._balance
    
    @deposits.setter
    def deposits(self, new_balance):
        if self.balance_is_valid(new_balance):
            self._balance = new_balance
        else:
            raise VaultError('New balance number is invalid')
    
    @property
    def rewards(self):
        return self._rewards
    
    @rewards.setter
    def rewards(self, num):
        if isinstance(num, int) and num > 0:
            self._rewards += num
            print(datetime.datetime.now(), ['Rewards Earned', self._rewards])

    @classmethod
    def change_yield(cls, new_yield):
        cls.daily_yield_pct = new_yield

    @classmethod
    def change_rewards_targ(cls, new_targ):
        cls.compound_rewards_target = new_targ
    
    @staticmethod
    def balance_is_valid(balance_num):
        if isinstance(balance_num, int) and balance_num > 0:
            return True
        else:
            print('Balance input not valid.')
            return False

    @staticmethod
    def history_is_valid(hist_item):
        if isinstance(hist_item, dict):
            return True
        else:
            print('History item invalid')
            return False
    
    def get_time_now():
        return datetime.datetime.now().strftime('%m/%d/%Y, %H:%M:%S')

    def add_deposit(self, deposit):
        self._balance += deposit - AUTOBNBVault.fees
        print(AUTOBNBVault.get_time_now(), ['Balance Updated', self._balance])

    def compound(self):
        if self._rewards < AUTOBNBVault.compound_rewards_target:
            self._rewards += (self._balance * (AUTOBNBVault.daily_yield_pct))
        else:
            self.harvest()
            print(AUTOBNBVault.get_time_now(), ['Harvested', self._balance])

    def harvest(self):
        self._balance += self._rewards * 2
        self.usd_in += self._rewards
        self._rewards = 0

    def pretty_print(self):
        print(f'Days Elapsed: {self.elapsed_days}\nInitial Deposit: {initial_deposit}')
        print(f'Final Balance: {self._balance}\nUSD In: {self.usd_in}')
        print(f'Percentage change: {round(((self._balance/initial_deposit) - 1) * 100, 2)}')
    
    # def print_history(self):
    #     for key in self.history:
    #         print(key, '    >>>    ', self.history[key])

    def pass_time(self, days):
        for day in range(days):
            self.compound()
            print(AUTOBNBVault.get_time_now(), '>>>', [f'day: {day}', f'balance {self._balance}'])
            self.elapsed_days += 1

    def reset(self):
        self._balance = initial_deposit
        self._rewards = 0
        self.elapsed_days = 0
        self.usd_in = 0
        print('Reseting Vault')
    

vault = AUTOBNBVault()

vault.pass_time(10)
vault.pretty_print()

results = {}

def prep_results(vault):
    days = round(vault.elapsed_days, 2)
    harvest = AUTOBNBVault.compound_rewards_target
    final = round(vault._balance, 2)
    cost = round(vault.usd_in, 2)
    gain = round(((vault._balance/initial_deposit) - 1) * 100, 2)
    return {'Days': days, 'Harvest@': harvest, 'Final': final, 'Cost': cost, 'Gain': f'{gain}%'}


for harvest_val in range(10, 100, 10):
    vault = AUTOBNBVault()
    vault.change_rewards_targ(harvest_val)
    for days in range(50, 350, 50):
            vault.pass_time(days)
            vault.pretty_print()
            mydict = prep_results(vault)
            save_string = f'{days}:{harvest_val}'
            results[save_string] = mydict
            vault.reset()

for harvest_val in range(10, 100, 10):
    vault = AUTOBNBVault()


for i in results:
    print(results[i])

