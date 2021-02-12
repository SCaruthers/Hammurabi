#!/usr/bin/env python

import random
#import string

def main():
    king = Ruler()
    welcome()
    king.print_summary()
    
    # Start a 10 year rule:
    for i in range(1):
        # reset variables:
        acres_in = 0
        acres_out = 0
        bushels_eaten = 0
        
        # Ask 4 questions
        # Starting with land purchase and sales:

        if king.bushels_in_storage > 0:
            acres_in = ask_land_to_buy(king)
        else:
            print('You cannot buy any land this year, as you have no grain.')
            
        if acres_in == 0:
            if king.acres_of_land > 0:
                acres_out = ask_land_to_sell(king)
            else:
                print('You have no land to sell this year.')
        
        if acres_in > 0:
            land_to_exchange = acres_in
        else:
            land_to_exchange = -acres_out
    
        bushels_eaten = ask_how_much_to_feed(king)
    
def welcome():
    message = '''Congratulations, you are the newest ruler of ancient Samaria, elected
for a ten year term of office. Your duties are to dispense food, direct
farming, and buy and sell land as needed to support your people. Watch
out for rat infestiations and the plague! Grain is the general currency,
measured in bushels. The following will help you in your decisions:

  * Each person needs at least 20 bushels of grain per year to survive.

  * Each person can farm at most 10 acres of land.

  * It takes 2 bushels of grain to farm an acre of land.

  * The market price for land fluctuates yearly.

Rule wisely and you will be showered with appreciation at the end of
your term. Rule poorly and you will be kicked out of office!
'''
    print(message)

def input_int(prompt = ''):
    number = None
    while number == None:
        try:
            number = int(input(prompt))
        except:
            pass
    return number
     
def ask_land_to_buy(ruler):
    if ruler.bushels_in_storage < 1: return 0
    acres = -1
    while acres < 0:
        acres = input_int('How many acres of land do you want to buy? : ')
        if acres < 0: print('Negative numbers are not allowed.')
        if (acres * ruler.price_of_land) > (ruler.bushels_in_storage):
            print('You do not have enough grain to buy {} acres.'.format(acres))
            acres = -1
    return acres

def ask_land_to_sell(ruler):
    if ruler.acres_of_land < 1: return 0    #have none to sell!
    acres = -1
    while acres < 0:
        acres = input_int('How many acres of land do you want to sell? : ')
        if acres < 0: print('Negative numbers are not allowed.')
        if acres > ruler.acres_of_land:
            print('You can sell only up to {} acres.'.format(ruler.acres_of_land))
            acres = -1
    return acres
    
def ask_how_much_to_feed(ruler):
    if ruler.bushels_in_storage < 1: return 0
    food = -1
    while food < 0:
        food = input_int('How much grain do you want to feed to the people? : ')
        if food < 0: print('Negative numbers are not allowed.')
        if food > ruler.bushels_in_storage:
            print('You don\'t have {} bushels to feed.'.format(food))
            food = -1
    return food
    
class Ruler():
    """A class for the ruler of ancient Samaria."""
    
    def __init__(self, name=None):
        if name is None:
            self.name = 'Hammurabi'
        else:
            self.name = name
        self.bushels_in_storage = 2800
        self.harvested_bushels_per_acre = 3
        self.population = 100
        self.acres_of_land = 1000
        self.price_of_land = 19            #bushels / acre
        self.acres_planted = 1000
        self.years_ruled = 0
        self.num_immigrants = 5
        self.num_deaths = 0
        self.bushels_rats_ate = 200
        
    
    def print_summary(self):
        print('O great {}!'.format(self.name))
        print('You are in year {} of your ten year rule.'.format(1+self.years_ruled))
        print('In the previous year {} people starved to death.'.format(self.num_deaths))
        print('In the previous year {} people entered the kingdom.'.format(self.num_immigrants))
        print('The population is now {}.'.format(self.population))
        print('We harvested {} bushels at {} bushels per acre.'.format(self.harvested_bushels_per_acre*self.acres_planted, self.harvested_bushels_per_acre))
        print('Rats destroyed {} bushels, leaving {} bushels in storage.'.format(self.bushels_rats_ate, self.bushels_in_storage))
        print('The city owns {} acres of land.'.format(self.acres_of_land))
        print('Land is currently worth {} bushels per acre.'.format(self.price_of_land))
        print('')


if __name__ == "__main__":
    main()