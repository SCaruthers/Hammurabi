
import tkinter as tk
import Hammurabi

## First Class is for getting player's name

BUY = +1
SELL = -1

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
        self.quitButton = tk.Button(self.frame, text = 'Quit', command = self.close_windows)
        self.l1.pack(pady=5)
        self.l2.pack()
        self.my_name.pack()
        self.button1.pack(padx = 10, pady=10, side = tk.LEFT, fill = tk.X, expand = True)
        self.quitButton.pack(padx = 10, pady=10, side = tk.RIGHT, fill = tk.X, expand = True)
        self.frame.pack(pady = 10)
        
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
        self.Ruler = Hammurabi.Ruler(ruler_name)
        
        self.master.protocol("WM_DELETE_WINDOW", self.close_windows)
        self.master.geometry("400x510")
        self.master.minsize(340, 250)
        self.master.maxsize(500,600)
        
        # Set up some string variables to use as active labels
        self.yio = tk.StringVar()    #years in office
        self.pop = tk.StringVar()    #population
        self.grn = tk.StringVar()    #grain in storage
        self.acr = tk.StringVar()    #acres owned
        self.ppa = tk.StringVar()    #price per acres
        self.update_labels()
        
        self.bs = tk.IntVar()        # value state for buying / selling land
        self.bs.set(BUY)             # BUY is +1, SELL is -1 to increase or decrease acreage
        
        self.oracle_text = tk.StringVar()   # Message to be displayed in bottom frame
        self.oracle_text.set(Hammurabi.welcome(to_print=False))
        
        # top frame for data output
        self.frame_top = tk.LabelFrame(self.master, 
                                       width = 400, height = 150,
                                       text = "Ruler: "+self.Ruler.name,
                                       )  
        # middle frame for entry fields
        self.frame_mid = tk.LabelFrame(self.master,
                                       width = 400, height = 200,
                                       text = "Make your commands:"
                                       ) 
        
        # bottom frame for report message        
        self.frame_bot = tk.LabelFrame(self.master,
                                       width = 400, height = 300,
                                       text = "Message from Oracle:")  
        self.frame_top.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.frame_mid.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.frame_bot.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)
        
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
        self.val_feed = tk.Spinbox(self.frame_mid, width=5, from_=0, to=self.grn.get(), increment=5, repeatinterval=20)
        self.digit_validation = self.frame_mid.register(self.validate_digit)
        self.val_feed.config(validate='all', validatecommand = (self.digit_validation, '%P','%W'))
        self.lbl_feed2 = tk.Label(self.frame_mid, text="bushels of grain")
        
        self.lbl_plant = tk.Label(self.frame_mid, text="Plant ")
        self.val_plant = tk.Spinbox(self.frame_mid, width=5, from_=0, to=self.get_plant_max())
        self.val_plant.config(validate='all', validatecommand = (self.digit_validation, '%P','%W'))
        self.lbl_plant2 = tk.Label(self.frame_mid, text="acres")
        
        self.goButton = tk.Button(self.frame_mid, 
                                  text = ' GO ', 
                                  width = 8,
                                  activebackground='green',
                                  highlightcolor='green',
                                  cursor='hand2',
                                  command = self.close_windows
                                  )
        
        self.lbl_landcost.grid(row=0, column=0, columnspan = 4, sticky = tk.E + tk.N)
        self.val_landcost.grid(row=0, column=4, sticky = tk.W + tk.N)
        self.rbn_buy.grid(row=1, column=0, sticky=tk.W)
        self.rbn_sell.grid(row=1, column=1, sticky=tk.W)
        self.val_landsale.grid(row=1, column=2, sticky=tk.E)
        self.lbl_landsale.grid(row=1, column=3, sticky=tk.W)
        self.lbl_feed.grid(row=2, column=0, columnspan=2, sticky=tk.E)
        self.val_feed.grid(row=2, column=2, sticky=tk.W)
        self.lbl_feed2.grid(row=2, column=3, columnspan=2, sticky=tk.W)
        self.lbl_plant.grid(row=3, column=0, columnspan=2, sticky=tk.E)
        self.val_plant.grid(row=3, column=2, sticky=tk.W)
        self.lbl_plant2.grid(row=3, column=3, sticky=tk.W)
        self.goButton.grid(row=4, column=6, sticky=tk.E, padx=5, pady=5)
        

        # Fill in Bottom frame:
        self.lbl_oracle_msg = tk.Label(self.frame_bot, 
                                       textvariable = self.oracle_text,
                                       fg = '#40f',
                                       wraplength=400, 
                                       justify=tk.LEFT
                                       )
        
        self.lbl_oracle_msg.grid(row=0, column=0, sticky=tk.N+tk.W)
        #self.quitButton = tk.Button(self.frame_bot, text = 'Quit', command = self.close_windows)


        #self.quitButton.pack(side=tk.RIGHT)

        
    def close_windows(self):
        self.master.destroy()
        self.parent.deiconify()
        
        
    def update_labels(self):
        self.yio.set('{:3d}'.format(self.Ruler.years_ruled))        #years in office
        self.pop.set(self.Ruler.population)         #population
        self.grn.set(self.Ruler.bushels_in_storage) #grain in storage
        self.acr.set(self.Ruler.acres_of_land)      #acres owned
        self.ppa.set(self.Ruler.price_of_land)      #price per acres
        
        
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
            self.val_feed.config(to=maxval)
        except ValueError:
            pass
            
        # set planting limits
        self.val_plant.config(to=self.get_plant_max())
        
        
    def get_plant_max(self):
        # the max allowed to plant is the least of 
        # 1. population * 10
        # 2. acres owned
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
    


def main(): 
    root = tk.Tk()
    app = Welcome(root)
    root.mainloop()

if __name__ == '__main__':
    main()
