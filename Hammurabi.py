#!/usr/bin/env python

import random
import argparse # command line arguments are handled in "if __name__" method at end


def main(king_name = None, term=None):

    random.seed()
    
    welcome()
    
    king = Ruler(king_name, term)    

    # Start a 10 year rule:
    while (king.in_office and king.years_ruled<king.term):
        
        king.print_summary()
        # Ask 4 questions
        # Starting with land purchase and sales:

        if king.bushels_in_storage > 0:
            acres_in = ask_land_to_buy(king)
        else:
            print('Oh Great {}, we cannot buy any land this year, as you have no grain.'.format(king.name))
            acres_in = 0
            
        if acres_in == 0:
            if king.acres_of_land > 0:
                acres_out = ask_land_to_sell(king)
            else:
                print('Oh Great {}, we have no land to sell this year.'.format(king.name))
                acres_out = 0
        
        if acres_in > 0:
            land_to_exchange = acres_in
        else:
            land_to_exchange = -acres_out
            
        king.exchange_land(land_to_exchange)    # Do the land transaction (also updates bushels in storage)
        
        # Now ask about how much to feed
        if king.bushels_in_storage > 0:
            bushels_to_feed = ask_how_much_to_feed(king)
        else:
            print('Oh Great {}, we have no grain to feed the people!'.format(king.name))
            bushels_to_feed = 0

        king.feed_people(bushels_to_feed)       # Feed the people (also updates bushels in storage)
        
        # Now ask about planting
        if king.bushels_in_storage > 0:
            acres_planted = ask_how_much_to_plant(king)
        else:
            print('Oh Great {}, we have no grain to plant!'.format(king.name))
            acres_planted = 0
        
        king.plant_seed(acres_planted)          # Plant the acres (also updates bushels in storage)
        
        if not king.update_population():        # Handle starvation, plague, etc.  Returns "False" if failure!
            king.impeach()
        
        king.update_harvest()
        
        king.update_land_price()
        
        king.years_ruled += 1
        
        

    # End of while loop, either 10 years or impeached
    if king.in_office: 
        king.print_final_summary()  # skip if impeached!
        
        avg_starve_rate = king.percentage_death_rate
        avg_land_wealth = king.acres_of_land / king.population
        
        if ((avg_starve_rate > 33) or (avg_land_wealth < 7)):
            print(king.impeach_message)
        elif ((avg_starve_rate > 10) or (avg_land_wealth < 9)):
            print(king.bad_message)
        elif ((avg_starve_rate > 3) or (avg_land_wealth < 10)):
            print(king.so_so_message)
        else:
            print(king.great_message)
        
    input('\nTa ta for now.')


def welcome():
    message = '''
\n\n\n
Congratulations, you have been elected the ruler of ancient 
Samaria. Your duties are to dispense food, direct farming,
and buy and sell land as needed to support your people. Watch
out for rat infestations and the plague! Grain is the general currency,
measured in bushels. The following will help you in your decisions:

  * Each person needs at least 20 bushels of grain per year to survive.

  * Each person can farm at most 10 acres of land.

  * It takes 1/2 bushel of grain to farm an acre of land.

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

def get_non_neg_int(prompt):
    ans = -1
    while ans < 0:
        ans = input_int(prompt)
        if ans < 0: print('Negative numbers are not allowed.')
    return ans

     
def ask_land_to_buy(ruler):
    if ruler.bushels_in_storage < 1: return 0
    acres = None
    while acres is None:
        acres = get_non_neg_int('How many acres of land do you want to buy? : ')
        if (acres * ruler.price_of_land) > (ruler.bushels_in_storage):
            print('Oh Great {}, we do not have enough grain to buy {} acres.'.format(ruler.name, acres))
            acres = None
    return acres

def ask_land_to_sell(ruler):
    if ruler.acres_of_land < 1: return 0    #have none to sell!
    acres = None
    while acres is None:
        acres = get_non_neg_int('How many acres of land do you want to sell? : ')
        if acres > ruler.acres_of_land:
            print('Oh Great {}, we can sell only up to {} acres.'.format(ruler.name, ruler.acres_of_land))
            acres = None
    return acres
    
def ask_how_much_to_feed(ruler):
    if ruler.bushels_in_storage < 1: return 0
    food = None
    while food is None:
        food = get_non_neg_int('How much grain do you want to feed to the people? : ')
        if food > ruler.bushels_in_storage:
            print('Oh Great {}, we don\'t have {} bushels to feed.'.format(ruler.name, food))
            food = None
    return food

def ask_how_much_to_plant(ruler):
    if ruler.bushels_in_storage < 1: return 0
    bushels_per_acre = 0.5
    acres_per_person = 10
    acres = None
    while acres is None:
        acres = get_non_neg_int('How many acres do you want to plant? : ')
        if acres > ruler.acres_of_land: 
            print('Oh Great {}, we have only {} acres to plant'.format(ruler.name, ruler.acres_of_land))
            acres = None
        elif (acres * bushels_per_acre) > ruler.bushels_in_storage:
            print('Oh Great {}, we have enough seed for only {} acres'.format(ruler.name, int(ruler.bushels_in_storage/bushels_per_acre)))
            acres = None
        elif acres > (ruler.population * acres_per_person):
            print('Oh Great {}, there are only enough people to plant {} acres'.format(ruler.name, int(ruler.population*acres_per_person)))
            acres = None
    return acres

    
class Ruler():
    """A class for the ruler of ancient Samaria."""
    
    impeach_message ='Due to this extreme mismanagement you have not only\nbeen impeached and thrown out of office, but you have\nalso been declared "National Fink" !!'
    great_message = 'A fantastic performance!!!  Charlemange, Disraeli, and \nJefferson combined could not have done better!'
    so_so_message = 'Your performance could have been somewhat better, but\nreally wasn\'t too bad at all. '+str(random.randint(2,14))+' people would\ndearly like to see you assassinated but we all have our\ntrivial problems.'
    bad_message = 'Your heavy-handed performance smacks of Nero and Ivan IV.\nThe people (remaining) find you an unpleasant ruler, \nand, frankly, hate your guts!'
    
    def __init__(self, name=None, term=None):
        if name is None:
            self.name = 'Hammurabi'
        else:
            self.name = name
        if term is None:
            self.term = 10
        else:
            self.term = term
        self.bushels_in_storage = 2800
        self.harvested_bushels_per_acre = 3
        self.population = 100
        self.acres_of_land = 1000
        self.price_of_land = 19            #bushels / acre
        self.acres_planted = 1000
        self.years_ruled = 0
        self.in_office = True
        self.num_immigrants = 5
        self.bushels_fed = 0
        self.num_deaths = 0
        self.total_num_deaths = 0
        self.percentage_death_rate = 0
        self.bushels_rats_ate = 200
        self.plague_flag = False
        
    def __str__(self):
        message = '{}: Member of Ruler class.'.format(self.name)
        if self.in_office:
            message = '\n'.join([message, 'Has been in office for {} years.'.format(self.years_ruled)])
        else:
            message = '\n'.join([message, 'Currently, is not in office'])
        return message
        
    
    def print_summary(self):
        print('\nO great {}!'.format(self.name))
        print('You are in year {} of your {} year rule.'.format(1+self.years_ruled, self.term))
        if self.plague_flag: 
            print('There was a terrible plague and half the population died.')
        self.print_pop_summary()
        print('We harvested {} bushels at {} bushels per acre.'.format(self.harvested_bushels_per_acre*self.acres_planted, self.harvested_bushels_per_acre))
        print('Rats destroyed {} bushels, leaving {} bushels in storage.'.format(self.bushels_rats_ate, self.bushels_in_storage))
        print('The city owns {} acres of land.'.format(self.acres_of_land))
        print('Land is currently worth {} bushels per acre.'.format(self.price_of_land))
        print('')
    
    def print_pop_summary(self):
        print('In the previous year {} people starved to death,'.format(self.num_deaths))
        print('and {} people entered the kingdom.'.format(self.num_immigrants))
        print('The population is now {}.'.format(self.population))
    
    def print_final_summary(self):
        print('\nO great {},'.format(self.name))
        self.print_pop_summary()
        print('\nIn your {}-year term of office, {:.1f} percent of the'.format(self.years_ruled,self.percentage_death_rate))
        print('population starved per year on average, i.e., ')
        print('a total of {} people starved!'.format(self.total_num_deaths))
        print('You started with 10.0 acres per person and ended with')
        print('{:.1f} acres per person.\n'.format(self.acres_of_land/self.population))
        
    def update_bushels_in_storage(self, amount):
        self.bushels_in_storage = int(self.bushels_in_storage+amount)
        
    def exchange_land(self, land_to_buy):
        # land_to_buy is positive if buying, negative if selling
        self.acres_of_land += land_to_buy      
        self.update_bushels_in_storage( -land_to_buy*self.price_of_land )
        
    def feed_people(self, bushels):
        # reduce storage by amount eaten
        self.update_bushels_in_storage(-bushels)
        self.bushels_fed = bushels
        
    def plant_seed(self, acres):
        # it takes 1/2 bushels per acre to plant
        bushels_per_acre = -0.5
        self.update_bushels_in_storage(bushels_per_acre*acres)
        self.acres_planted = acres

    def is_plague(self):
        if random.randint(0,99) < 15:
            self.plague_flag = True
        else:
            self.plague_flag = False
        return self.plague_flag
        
    def rat_infestation(self):
        if random.randint(0,99) < 40:
            return True
        else:
            return False

    def update_population(self):
        # Is there a plague? Happens 15% of the time, then 1/2 people die
        # Did anyone starve?  Each person needs 20 bushels.
        ## If 45% of the people starve, end the game!! (return False)
        # How many immigrants?
        ## If anyone starved, no immigrants
        ## else (20 * number of acres you have + amount of grain you have in storage) / (100 * population) + 1
        #return True, unless you starved too many
        
        # Plague
        if self.is_plague():
            self.population = int(self.population / 2)
        
        # Starvation:
        
        num_fully_fed = int(self.bushels_fed / 20)
        if num_fully_fed >= self.population:
            self.num_deaths = 0
        else:
            self.num_deaths = self.population - num_fully_fed
        if self.num_deaths > int(0.45 * self.population):
            return False        # You starved too many, Impeach immediately!
        else:
            self.population -= self.num_deaths
            self.total_num_deaths += self.num_deaths
        
        self.update_death_rate()
        
        # Immigration
        if self.num_deaths > 0:
            self.num_immigrants = 0
        else:
            self.num_immigrants = int((20 * self.acres_of_land + self.bushels_in_storage) / (100 * self.population) + 1)
        self.population += self.num_immigrants
        
        return True # end of update population with success
    
    def update_death_rate(self):
        self.percentage_death_rate = (self.years_ruled * self.percentage_death_rate + 100 * self.num_deaths/self.population) / (self.years_ruled+1)
        
    def update_harvest(self):
        yield_range = {'min':1, 'max':8}
        self.harvested_bushels_per_acre = random.randint(yield_range['min'],yield_range['max'])
        self.update_bushels_in_storage(self.harvested_bushels_per_acre * self.acres_planted)
        
        if self.rat_infestation(): # eat between 1/10 - 3/10 of the grain
            self.bushels_rats_ate = int(self.bushels_in_storage * random.randint(1,3) / 10)
        else:
            self.bushels_rats_ate = 0
        self.update_bushels_in_storage(-self.bushels_rats_ate)
            
    def update_land_price(self):
        land_price_range = {'min':17, 'max':26}
        self.price_of_land = random.randint(land_price_range['min'],land_price_range['max'])
        
    def impeach(self):
        print('\n\n{}, You starved {} people in one year!!!'.format(self.name, self.num_deaths))
        print(Ruler.impeach_message)
        self.in_office = False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    description = 'Hammurabi Game -- Rule Ancient Samaria in this text-based strategy game')
    parser.add_argument('-n', '--name', 
                        help='The name of the ruler, defaults to "Hammurabi"', 
                        default = None)
    parser.add_argument('-t','--term', 
                        type=int,
                        help='The duration of reign, defaults to 10 years', 
                        default=None)
    args = parser.parse_args()
    main(king_name=args.name, term=args.term)