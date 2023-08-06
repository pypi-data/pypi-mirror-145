full_name = input( "Enter Your Name : " ).split()

def shortName( full_name ):
    short_name = ''
    words = len( full_name )

    if words >= 3:
        
        for word in full_name[ : (words -1) ]:
            
            short_name += word[0].upper() + "."
        
        short_name += full_name[ -1 ].capitalize()
        
        return short_name

# print( short_name )
        
print( shortName(full_name) )