#!/usr/bin/env python
import tkinter as tk
import tkinter.font as tkFont
from tkinter import scrolledtext
from tkinter import messagebox
import Hammurabi
import random

## First Class is for getting player's name

BUY = +1
SELL = -1

WIN_W = 370
WIN_H = 510

class Welcome:
    '''Class to start the Hammurabi game, asking the user for the Ruler's name.'''
    def __init__(self, master):
        self.master = master
        self.master.geometry("300x150")
        self.master.minsize(275, 135)
        self.master.title("Welcome to Babylon!")
        self.frame = tk.Frame(self.master)
        self.l1 = tk.Label(self.frame, 
                           text='Oh great Ruler, welcome to Babylon.',
                           font=('Arial',13))
        self.l2 = tk.Label(self.frame, 
                           text='What is your name?',
                           font=('Arial',10))
        self.currentRuler = tk.StringVar()
        self.currentRuler.set('Hammurabi')
        self.my_name = tk.Entry(self.frame, textvariable = self.currentRuler, width = 20)
        self.button1 = tk.Button(self.frame, text = "Start", command = self.game_window)
        self.helpBtn1 = tk.Button(self.frame, text = "Help", command = self.show_start_help)
        self.quitButton = tk.Button(self.frame, text = 'Quit', command = self.close_windows)
        self.l1.pack(pady=5)
        self.l2.pack()
        self.my_name.pack()
        self.button1.pack(padx = 5, pady=10, side = tk.LEFT, fill = tk.X, expand = True)
        self.helpBtn1.pack(padx = 5, pady=10, side = tk.LEFT, fill = tk.X, expand = True)
        self.quitButton.pack(padx = 5, pady=10, side = tk.RIGHT, fill = tk.X, expand = True)
        self.frame.pack(pady = 10)
    
    def show_start_help(self):
        msg = '''        To play the game of Hammurabi,
        Type your name in the box and click "Start".
        
        You will serve your term in office buying & selling land, 
        planting & harvesting seed, and feeding your people.
        
        The default term is 10 years. If you want a different 
        term, append it to the name with a # mark, followed 
        by the number of years, as in Hammurabi#15'''
        messagebox.Message(parent=self.master,title='Help',message=msg).show()
        
    def game_window(self):
        self.gameWindow = tk.Toplevel(self.master)
        self.gameWindow.title('Oracle of Babylon')
        self.master.withdraw()
        self.master.title("Welcome Back!")
        self.app = GoPlay(self.gameWindow, self.master, self.currentRuler.get())
        
    def close_windows(self):
        self.master.destroy()

class GoPlay:
    '''Class to run the Hammurabi game in a window.'''
    def __init__(self, master, parent, ruler_name):
        global BUY
        global SELL
        self.master = master
        self.parent = parent
        try:
            rulerTerm = int(float(ruler_name.split('#')[1]))
        except:
            rulerTerm = 10
        self.Ruler = Hammurabi.Ruler(ruler_name.split('#')[0], rulerTerm)
        
        self.master.protocol("WM_DELETE_WINDOW", self.close_windows)
        self.master.geometry('x'.join((str(WIN_W),str(WIN_H))))
        self.master.minsize(340, 250)
        self.master.maxsize(500,600)
        
        # History Window will keep a running total of actions and results
        # Be sure red 'X' doesn't destroy the window!
        self.historyWin = tk.Toplevel(self.master)
        self.historyWin.title("{}'s Record as Ruler".format(self.Ruler.name))
        self.historyWin.protocol("WM_DELETE_WINDOW", self.historyWin.withdraw)
        self.historyWin.geometry('x'.join((str(WIN_W+65),str(WIN_H-265))))
        self.historyWin.minsize(WIN_W+50, WIN_H-320)
        self.historyWin.maxsize(500,600)
        hist_head = ('\t\t\t ----- G R A I N -----'+
                    '\nYear\tPop\tAcres\tStored\t Fed \tHarvest'+
                    '\n----\t---\t-----\t------\t-----\t-------')
        
        # Set up some string variables to use as active labels
        self.yio = tk.StringVar()    #years in office
        self.pop = tk.StringVar()    #population
        self.grn = tk.StringVar()    #grain in storage
        self.acr = tk.StringVar()    #acres owned
        self.ppa = tk.StringVar()    #price per acres
        self.plt = tk.StringVar()    #amount to plant
        self.plt.set('0')
        self.hist = tk.StringVar()    #text for running history window
        self.hist.set(hist_head)
        
        self.update_labels()
        
        self.bs = tk.IntVar()        # value state for buying / selling land
        self.bs.set(BUY)             # BUY is +1, SELL is -1 to increase or decrease acreage
        
        self.oracle_text = tk.StringVar()   # Message to be displayed in bottom frame
        self.oracle_text.set(Hammurabi.welcome(to_print=False))
        
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=10)
        
        # top frame for data output
        self.frame_top = tk.LabelFrame(self.master, 
                                       width = WIN_W, height = 150,
                                       text = "Ruler: "+self.Ruler.name,
                                       )  
        # middle frame for entry fields
        self.frame_mid = tk.LabelFrame(self.master,
                                       width = WIN_W, height = 200,
                                       text = "Make your commands:"
                                       ) 
        
        # bottom frame for report message        
        self.frame_bot = tk.LabelFrame(self.master,
                                       width = WIN_W, height = 300,
                                       text = "Message from Oracle:")  
        
        self.frame_top.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=False)
        self.frame_mid.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=False)
        self.frame_bot.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=False)
        
        
        # Fill in Top frame, then put items
        self.lbl_years = tk.Label(self.frame_top, text = "Years Served:")
        self.val_years = tk.Label(self.frame_top, textvar = self.yio)
        self.lbl_pop = tk.Label(self.frame_top, text = "Population:")
        self.val_pop = tk.Label(self.frame_top, textvar = self.pop)
        self.lbl_grain = tk.Label(self.frame_top, text = "Bushels of Grain:")
        self.val_grain = tk.Label(self.frame_top, textvar = self.grn)
        self.lbl_acres = tk.Label(self.frame_top, text = "Acres of Land:")
        self.val_acres = tk.Label(self.frame_top, textvar = self.acr)
                                  

        self.lbl_years.grid(row=0, column=0, sticky = tk.E)
        self.val_years.grid(row=0, column=1, sticky = tk.W)
        self.lbl_grain.grid(row=0, column=2, sticky = tk.E)
        self.val_grain.grid(row=0, column=3, sticky = tk.W)
        self.lbl_pop.grid(row=1, column=0, sticky = tk.E)
        self.val_pop.grid(row=1, column=1, sticky = tk.W)
        self.lbl_acres.grid(row=1, column=2, sticky = tk.E)
        self.val_acres.grid(row=1, column=3, sticky = tk.W)
        
        # Fill in Middle frame:
        self.lbl_landcost = tk.Label(self.frame_mid, text = "Price of land in bushels per acre:")
        self.val_landcost = tk.Label(self.frame_mid, textvar = self.ppa)
        
        self.rbn_buy = tk.Radiobutton(self.frame_mid, text="Buy", var=self.bs, value=BUY, command = self.bs_range)
        self.rbn_sell = tk.Radiobutton(self.frame_mid, text="Sell", var=self.bs, value=SELL, command = self.bs_range)
        maxval = int(self.Ruler.bushels_in_storage / self.Ruler.price_of_land)
        self.val_landsale = tk.Spinbox(self.frame_mid, width=5, from_=0, to=maxval, command = self.bs_range)
        self.sale_validation = self.frame_mid.register(self.validate_sale)
        self.val_landsale.config(validate='all', validatecommand = (self.sale_validation, '%P'))
        self.lbl_landsale = tk.Label(self.frame_mid, text="acres")
        
        self.lbl_feed = tk.Label(self.frame_mid, text="Feed the people ")
        self.val_feed = tk.Spinbox(self.frame_mid, width=5, from_=0, to=self.grn.get(), increment=5, repeatinterval=20, command = self.bs_range)
        self.digit_validation = self.frame_mid.register(self.validate_digit)
        self.val_feed.config(validate='all', validatecommand = (self.digit_validation, '%P','%W'))
        self.lbl_feed2 = tk.Label(self.frame_mid, text="bushels of grain")
        
        self.lbl_plant = tk.Label(self.frame_mid, text="Plant ")
        self.val_plant = tk.Spinbox(self.frame_mid, textvar = self.plt, width=5, from_=0, to=self.get_plant_max(), command = self.bs_range)
        self.val_plant.config(validate='all', validatecommand = (self.digit_validation, '%P','%W'))
        self.lbl_plant2 = tk.Label(self.frame_mid, text="acres")
        
        self.goButton = tk.Button(self.frame_mid, 
                                  text = ' GO ', 
                                  width = 8,
                                  activebackground='green',
                                  highlightcolor='green',
                                  cursor='hand2',
                                  command = self.go_action
                                  )
        
        self.quitButton = tk.Button(self.frame_mid, 
                          text = 'End', 
                          width = 8,
                          activebackground='red',
                          highlightcolor='red',
                          cursor='hand2',
                          command = self.close_windows
                          )
        
        self.lbl_landcost.grid(row=0, column=0, columnspan = 4, sticky = tk.E + tk.N)
        self.val_landcost.grid(row=0, column=4, sticky = tk.W + tk.N)
        self.rbn_buy.grid(row=1, column=0, sticky=tk.W)
        self.rbn_sell.grid(row=1, column=1, sticky=tk.W)
        self.val_landsale.grid(row=1, column=2, sticky=tk.W)
        self.lbl_landsale.grid(row=1, column=3, sticky=tk.W)
        self.lbl_feed.grid(row=2, column=0, columnspan=2, sticky=tk.E)
        self.val_feed.grid(row=2, column=2, sticky=tk.W)
        self.lbl_feed2.grid(row=2, column=3, columnspan=2, sticky=tk.W)
        self.lbl_plant.grid(row=3, column=0, columnspan=2, sticky=tk.E)
        self.val_plant.grid(row=3, column=2, sticky=tk.W)
        self.lbl_plant2.grid(row=3, column=3, sticky=tk.W)
        self.goButton.grid(row=4, column=4, sticky=tk.E, padx=5, pady=5)
        self.quitButton.grid(row=4, column=5, sticky=tk.E, padx=5, pady=5)
        

        # Fill in Bottom frame:
        self.lbl_oracle_msg = tk.Label(self.frame_bot, 
                                       textvariable = self.oracle_text,
                                       fg = '#40f',
                                       wraplength=400,
                                       font=('TkDefaultFont',8),
                                       justify=tk.LEFT
                                       )
        
        self.lbl_oracle_msg.grid(row=0, column=0, sticky=tk.N+tk.W)
        
        # Set up History Window with a frame and text for hist variable
        self.label_hist = tk.Label(self.historyWin, 
                                   text = "History for Ruler: "+self.Ruler.name,
                                   font = ('TkDefaultFont',15)
                                  )
        hist_font = tkFont.nametofont('TkFixedFont')
        self.hist_text_area = scrolledtext.ScrolledText(self.historyWin,
                                                        width = 50,
                                                        height = 10,
                                                        font = hist_font,
                                                       )
        self.hist_text_area.insert('end',self.hist.get())
        self.historyWin.grid_columnconfigure(0,weight=1)
        self.historyWin.grid_rowconfigure(1,weight=1)
        self.historyWin.resizable(width = True, height = True)
        self.label_hist.grid(column=0,row=0, padx=10, pady=10, sticky=tk.W)
        self.hist_text_area.grid(column=0, row=1, padx=10, pady=10, sticky=tk.W+tk.N+tk.E+tk.S)
        self.hist_text_area.configure(state="disabled")
        self.historyWin.withdraw()

        # Create a menu so user can pull up the History Window
        self.menubar = tk.Menu(self.master)
        self.filemenu = tk.Menu(self.menubar,tearoff=0)
        self.filemenu.add_command(label="View History", command=self.historyWin.deiconify)
        self.filemenu.add_command(label="Quit Reign", command=self.close_windows)
        self.filemenu.add_command(label="Quit Game", command=self.parent.destroy)
        self.helpmenu = tk.Menu(self.menubar,tearoff=0)
        self.helpmenu.add_command(label="Help", command=self.show_reign_help)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)
        self.master.config(menu=self.menubar)
        
        

    def show_reign_help(self):
        self.reignHelpWin = tk.Toplevel(self.master)
        self.reignHelpWin.title("Rules...")
        self.historyWin.geometry('x'.join((str(WIN_W),str(WIN_H-265))))
        self.historyWin.minsize(WIN_W, WIN_H-265)
        self.historyWin.maxsize(WIN_W, WIN_H-265)
        self.playHelpLbl = tk.Label(self.reignHelpWin, text = Hammurabi.welcome(to_print=False)).pack(padx=5,pady=5)
        
    def close_windows(self):
        self.master.destroy()
        self.parent.deiconify()
        
        
    def update_labels(self):
        self.yio.set('{:3d}'.format(self.Ruler.years_ruled))        #years in office
        self.pop.set(self.Ruler.population)         #population
        self.grn.set(self.Ruler.bushels_in_storage) #grain in storage
        self.acr.set(self.Ruler.acres_of_land)      #acres owned
        self.ppa.set(self.Ruler.price_of_land)      #price per acres
                    #  yio   pop   acr   grn    fed   harvest
        hist_line = "\n{:3}\t{:5}\t{:5}\t{:6}\t{!s:5}\t{!s:5}".format(self.yio.get(),self.pop.get(),self.acr.get(),self.grn.get(),self.Ruler.bushels_fed, (self.Ruler.harvested_bushels_per_acre*self.Ruler.acres_planted))
        
        self.hist.set(self.hist.get() + hist_line)
        
    def update_history_text(self):
        self.hist_text_area.configure(state="normal")
        self.hist_text_area.replace(1.0,'end',self.hist.get())
        self.hist_text_area.configure(state="disabled")
        
    def bs_range(self):
        # set land sale limits accordingly, ignore feed and plant
        if self.bs.get() == BUY:
            maxval = int(int(self.grn.get()) / int(self.ppa.get()))
        else:
            maxval = int(self.acr.get())
        self.val_landsale.config(to=maxval)
        
        # set feed limits accordingly, ignore plant
        try:
            maxval = int(self.grn.get()) - (int(self.bs.get()) * int(self.val_landsale.get()) * int(self.ppa.get()))
            if maxval <= 0:
                #self.val_feed.set('0')
                self.val_feed.config(to=0)
            else:
                self.val_feed.config(to=maxval)
        except ValueError:
            pass
            
        # set planting limits
        tmp = self.get_plant_max()
        if tmp == 0:
            self.plt.set('0')
        self.val_plant.config(to=tmp)
        
        
    def get_plant_max(self):
        # the max allowed to plant is the least of 
        # 1. population * 10
        # 2. acres owned (+/- current sale)
        # 3. (total bushels available * 2 acres / bushel ) where total is storage +/- sale - feed
        m1 = int(self.pop.get()) * 10
        try:
            m2 = int(self.acr.get()) + (int(self.bs.get()) * int(self.val_landsale.get()))
        except:
            m2 = m1
        try:
            tot_grn = int(self.grn.get()) - (int(self.bs.get())*int(self.val_landsale.get())*int(self.ppa.get())) - int(self.val_feed.get())
            m3 = tot_grn * 2
        except:
            m3 = m1
        
        return max(0,min(m1,m2,m3))
    
    
    def validate_sale(self, user_input):
        # first, make sure scrollbox limits are up to date:
        self.bs_range()
        # ensure input is number
        if user_input.isdigit():
            minval = int(self.frame_mid.nametowidget(self.val_landsale).config('from')[4])
            maxval = int(self.frame_mid.nametowidget(self.val_landsale).config('to')[4])
                
            if int(user_input) not in range(minval,maxval+1):
                return False
            return True
            
        elif user_input is "":
            return True
            
        else:
            return False
    
    
    def validate_digit(self, user_input, W):
        # first, make sure scrollbox limits are up to date:
        self.bs_range()
        if user_input.isdigit():
            minval = int(self.frame_mid.nametowidget(W).config('from')[4])
            maxval = int(self.frame_mid.nametowidget(W).config('to')[4])

            if int(user_input) not in range(minval,maxval+1):
                return False
            return True
            
        elif user_input is "":
            return True
        else:
            return False
    

    def final_check(self):
        msg = None
        # check that there is no blank entry
        if self.val_landsale.get()=='' or self.val_feed.get()=='' or self.plt.get()=='':
            msg = 'O great {}, please make sure each item has a value!'.format(self.Ruler.name)
            return msg
        cashOnHand = int(self.grn.get())
        # check land sale
        ## Is there enough acreage to sell?
        ## Is there enough bushels to pay?
        if self.bs.get() == BUY:
            if cashOnHand < (int(self.ppa.get()) * int(self.val_landsale.get())):
                msg = 'O great {}, you do not have enough grain to buy {} acres.'.format(self.Ruler.name, self.val_landsale.get())
                return msg
            cashOnHand -= int(self.ppa.get()) * int(self.val_landsale.get())
        else:
            if int(self.acr.get()) < int(self.val_landsale.get()):
                msg = 'O great {}, you do not have enough land to sell {} acres.'.format(self.Ruler.name, self.val_landsale.get())
                return msg
            cashOnHand += int(self.ppa.get()) * int(self.val_landsale.get())
        # check feed
        ## Is there enough bushels to feed?
        if cashOnHand < int(self.val_feed.get()):
            msg = 'O great {}, you do not have enough grain to feed {} bushels.'.format(self.Ruler.name, self.val_feed.get())
            return msg
        cashOnHand -= int(self.val_feed.get())
        # check planting
        ## Is there enough land to plant
        ## Is there enough seed to plant
        ## Is population enough to plant
        if (int(self.acr.get()) + (int(self.bs.get()) * int(self.val_landsale.get()))) < int(self.plt.get()):
            msg = 'O great {}, you do not have enough land to plant {} acres.'.format(self.Ruler.name, self.plt.get())
        elif (int(self.grn.get()) * 2) < int(self.grn.get()):
            msg = 'O great {}, you do not have enough grain to plant {} acres.'.format(self.Ruler.name, self.plt.get())
        elif (int(self.pop.get()) * 10) < int(self.plt.get()):
            msg = 'O great {}, you do not have enough people to plant {} acres.'.format(self.Ruler.name, self.plt.get())
        return msg
    
    def go_action(self):
        #msg = "You hit the GO button\nLand Exchange: {}\nFeed: {}\nPlant: {}".format(str(int(self.val_landsale.get())*int(self.bs.get())),self.val_feed.get(),self.plt.get())
        #self.oracle_text.set(msg)
        
        self.lbl_oracle_msg.config(font=('TkDefaultFont',10))
        
        msg = self.final_check()
        if msg != None:
            self.oracle_text.set(msg+'\n')
            return
        
        # Obviously passed final check
        # Process all the calls for the year in office
        self.Ruler.exchange_land(int(self.bs.get()) * int(self.val_landsale.get()))

        self.Ruler.feed_people(int(self.val_feed.get()))
        
        self.Ruler.plant_seed(int(self.plt.get()))
        
        if not self.Ruler.update_population():
            # update_pop returns False if you starved too many
            self.oracle_text.set(self.Ruler.impeach(quiet=True))
            self.end_reign()
        
        self.Ruler.update_harvest()
        self.Ruler.update_land_price()
        self.Ruler.years_ruled += 1
        
        # Update the "dashboard" values and
        # Reset the choices back to 0's
        self.update_labels()
        self.update_history_text()
        self.re_init_vals()
        
        # set the appropriate text, which depends on 
        # if still in office or not.
        if self.Ruler.in_office:
            if int(self.yio.get()) < self.Ruler.term:
                msg = self.summarize_year()
                self.oracle_text.set(msg)
            else: 
                msg = self.Ruler.print_final_summary(mode='return')
                msg += '\n'+self.get_final_score()
                self.oracle_text.set(msg)
                self.end_reign()
        else:
            self.end_reign()
            
    def re_init_vals(self):
        self.bs.set(BUY)
        self.val_landsale.delete(0,tk.END)
        self.val_landsale.insert(0,'0')
        self.val_feed.delete(0,tk.END)
        self.val_feed.insert(0,'0')
        self.val_plant.delete(0,tk.END)
        self.val_plant.insert(0,'0')
        
        
    def summarize_year(self):
        return self.Ruler.print_summary(mode='return')
        
    
    def get_final_score(self):
        avg_starve_rate = self.Ruler.percentage_death_rate
        avg_land_wealth = self.Ruler.acres_of_land / self.Ruler.population
        
        if ((avg_starve_rate > 33) or (avg_land_wealth < 7)):
            return self.Ruler.impeach_message
        elif ((avg_starve_rate > 10) or (avg_land_wealth < 9)):
            return self.Ruler.bad_message
        elif ((avg_starve_rate > 3) or (avg_land_wealth < 10)):
            return self.Ruler.so_so_message
        else:
            return self.Ruler.great_message

    
    
    def end_reign(self):
        # Disable all the widgets, especially "GO" button
        # Setting the oracle_text is not the responsibility of this function!
        self.parent.bell()
        self.goButton.config(state=tk.DISABLED)

def main(): 
    random.seed()
    root = tk.Tk()
    app = Welcome(root)
    root.mainloop()

if __name__ == '__main__':
    main()
