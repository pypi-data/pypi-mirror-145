import os
from time import sleep
from HackerGprat import basic as b







# -------------------------------------------------------------
# Update HackerGprat PIP Library

def upgradePIP():
    try:
        b.cmd( "pip install HackerGprat -U" )
    except:
        print( "Try To Upgrade HackerGprat PIP Library" )

# upgradePIP()
# -------------------------------------------------------------
        

# -------------------------------------------------------------
# clear screen

def clear( delay=0 ):
    """ it will clear your terminal by default in 0 sec, OR
    clear( delay=3 ) # 3 is second
        youtube:- 
    """
    
    if os.name == 'nt':  # ! for windows
        sleep( delay )
        os.system( "cls" )  # ! cmd uses cls to clear the screen
    else:
        sleep( delay )
        os.system( "clear" ) # ! for linux & mac os
       
# clear(delay=3) 

# -------------------------------------------------------------





# -------------------------------------------------------------
# number input only
# by defualt all input are strings so need to create another one for string

def inputNum( message="Enter Number : "):
    
    """usage
        youtube: - 
        add subtitle in english
    """

    while True:
        try:
            userInt = int( input( message ) )
            return userInt
            break
        except:
            print("NaN")
            
# user = inputNum()    # default print
# user = inputNum("Choose Number : ") # overwrite default value
# print( user )
# -------------------------------------------------------------





# -------------------------------------------------------------
# beautifull view of list

# names = ['ram', 'shyam', 'ghanshyam', 'ravan', 'hari']

def viewList( listName, sep="-" ):

    """ usage i.e.
        viewList( names, "=" )
    """
    for num, name in enumerate( listName ):
        print( num, sep , name )
    
        
# viewList( names, "=" )

# -------------------------------------------------------------





# -------------------------------------------------------------
# cmd

def cmd( command='cd' ):
    """ cmd("dir")
    """
    if os.name == 'nt':
        try:
            os.system("cd")
            print(">> ",command )
            return os.system( command )
        except:
            print("Caught An Error!")
    else:
        try:
            os.system("pwd")
            print(">> ",command )
            return os.system( command )
        except:
            print("Caught An Error!")
       
# print( cmd("cmd") )
# -------------------------------------------------------------


# -------------------------------------------------------------

class Symbol:
    '''Some usefull symbol like heart ❤ etc.

    usage:- 
        symbol = Symbol()
        print( symbol.heart() )  
    '''
    
    def heart(self):
        heart = u'\u2764'
        return heart

    def omega(self):
        omega = u"\u03A9"   # Ω
        return omega
    
    def delta(self):
        return u'\u0394'    # Δ
    
    def sigma(self):
        return u'\u03C3'   # σ
    
    def mu(self):
        return u'\u03BC'    # μ
    
    def epsilon(self):
        return u'\u03B5'    # ε
    
    def degree(self):
        return u'\00B0'     # °
    
    def pi(self):
        return u'\u03C0'    # π	
    
    def theta(self):
        return u'u03F4'     # ϴ
        
    def caret(self):
        return 'a\u0302'    # replace the a with any other to char
    

# s = Symbol()
# print( s.heart() )
# -------------------------------------------------------------

# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------



if __name__ == '__main__':
    pass


