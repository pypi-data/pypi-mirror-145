

def numToText( listOfNumbers, space=32, specialChar=95 ):
    """ if a = 1, b = 2, c = 3 and " " = 27 and "_" = 28
    example "bad " = 2 1 4 27 
    
    below is example how to use
    test = [23, 5, 12, 12, 27, 20, 8, 5, 27, 6, 12, 1,]
    print( assciToText( test, space=27, specialChar=28 ) )
    
    tutorial
    youtube:- 
    """

    text = ""

    for num in listOfNumbers:
        if num == space:
            text += " "
        elif num == specialChar:
            text += "_"
        else:
            text += chr( num + 96 )

    return text


if __name__ == '__main__':
    pass

