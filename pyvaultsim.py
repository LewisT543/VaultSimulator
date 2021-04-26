        
'''This is a program designed to emulate a defi vault, 
in which the rewards are earned in the native token'''


import pandas as pd

class VaultError(Exception):
    pass

global initial_deposit
initial_deposit = 2000

class AUTOBNBVault:

    daily_yield_pct = 0.0041
    compound_rewards_target = 10
    fees = 1.1
    default_days = 90

    def __init__(self):
        self.balance = initial_deposit
        self.rewards = 0
        self.elapsed_days = 0
        self.usd_in = 0
        self.fees_paid = 0

    @classmethod
    def change_yield(cls, new_yield):
        cls.daily_yield_pct = new_yield

    @classmethod
    def change_rewards_targ(cls, new_targ):
        cls.compound_rewards_target = new_targ

    @classmethod
    def change_default_days(cls, new_days):
        cls.default_days = new_days

    def pay_fees(self):
        self.fees_paid += AUTOBNBVault.fees

    def compound(self):
        if self.rewards < AUTOBNBVault.compound_rewards_target:
            self.rewards += (self.balance * (AUTOBNBVault.daily_yield_pct))
        else:
            self.pay_fees()
            self.harvest()

    def harvest(self):
        self.usd_in += self.rewards
        self.balance += self.rewards * 2
        self.rewards = 0
    
    def pass_time(self, days):
        for i in range(days):
            self.elapsed_days += 1
            self.compound()

    def reset(self):
        self.balance = initial_deposit
        self.rewards = 0
        self.elapsed_days = 0
        self.usd_in = 0
        self.fees_paid = 0


class Simulate:
    '''
    sim_length_range = (start, stop, step)
    '''

    def __init__(self, sim_length_range, harvest_level_range=None):
        self.time_range = sim_length_range
        self.harvest_range = harvest_level_range

    def prep_results(self, vault):
        days = round(vault.elapsed_days, 2)
        harvest = AUTOBNBVault.compound_rewards_target
        final = round(vault.balance, 2)
        cost = round(vault.usd_in, 2)
        gain = round(((vault.balance / initial_deposit) - 1) * 100, 2)
        fees = round(vault.fees_paid, 2)
        return {'Days': days,'Harvest_targ': harvest,'Final': final, 'Cost': cost,'Gain': gain, 'Fees': fees}
    
    def test_X_numdays(self, start, stop, step):
        all_results = []
        vault = AUTOBNBVault()
        for days in range(start, stop, step):
            vault.pass_time(days)
            all_results.append(self.prep_results(vault))
            vault.reset()
        df = pd.DataFrame(all_results, columns=['Days', 'Harvest_targ', 'Final', 'Cost', 'Gain', 'Fees'])
        return df
    
    def test_X_harvest(self, start, stop, step):
        all_results = []
        for harvest_targ in range(start, stop, step):
            AUTOBNBVault.change_rewards_targ(harvest_targ)
            vault = AUTOBNBVault()
            vault.pass_time(AUTOBNBVault.default_days)
            all_results.append(self.prep_results(vault))
            vault.reset()
        df = pd.DataFrame(all_results, columns=['Days', 'Harvest_targ', 'Final', 'Cost', 'Gain', 'Fees'])
        return df

    def optimise_harvest_days(self, tup, tup2):
        hstart, hstop, hstep = tup[0], tup[1], tup[2]
        dstart, dstop, dstep = tup2[0], tup2[1], tup2[2]
        all_results = []
        for harvest_targ in range(hstart, hstop, hstep):
            AUTOBNBVault.change_rewards_targ(harvest_targ)
            vault = AUTOBNBVault()
            for days in range(dstart, dstop, dstep):
                vault.pass_time(days)
                all_results.append(self.prep_results(vault))
                vault.reset()
        df = pd.DataFrame(all_results, columns=['Days', 'Harvest_targ', 'Final', 'Cost', 'Gain', 'Fees'])
        return df
            

my_sim = Simulate((10, 200, 10))
# opti = my_sim.optimise_harvest_days((10, 100, 5), (10, 100, 10))
# pd.set_option('display.max_rows', None)
#print(opti.sort_values(by='Final'))
# print(opti.sort_values(by='Days'))
'''
results: At a first glance this data displays that a longer hold time between 
compounds is an advantageous decision when using BNB-AUTO
'''
# Target = 10 to 200 in steps of 5.

# Maximum returns for a 30 day period:
# max = 29.95%, biased towards 145-125 and 95-85, min = $150 with 15%, optimal = $95 value with 3 harvests => ~once every 10 days

# Maximum returns for a 60 day period:
# max = 68.44%, biased towards 165-95, min = $5 with 34.78%, optimal = $130 value with 5 harvests => ~once every 12 days

# Maximum returns for a 90 day period:
# max = 117.12%, baised towards 115+, min = $5 with 56.48%, optimal = $190 value with 6 harvests => ~once every 15 days


all_test_res = []
for days in range(30, 360, 2):
    AUTOBNBVault.change_default_days(days)
    results = my_sim.test_X_harvest(100,1000,50)
    all_test_res.append(results)

highest = []
for df in all_test_res:
    sorted_df = df.sort_values(by='Final')
    highest.append([sorted_df['Days'].iloc[-1], sorted_df['Harvest_targ'].iloc[-1], sorted_df['Gain'].iloc[-1]])

net_results_df = pd.DataFrame(highest, columns=['Days', 'Optimum_harvest_targ', 'Gain_%'])   
print(net_results_df)
net_results_df.to_csv('Optimised_results.csv')


'''
Results:
Days              30.0
Harvest_targ     290.0
Final           2580.0
Cost             290.0
Gain              29.0
Fees               1.1

Days              60.00
Harvest_targ     130.00
Final           3368.75
Cost             684.37
Gain              68.44
Fees               5.50

Days              90.00
Harvest_targ     190.00
Final           4342.44
Cost            1171.22
Gain             117.12
Fees               6.60
'''
