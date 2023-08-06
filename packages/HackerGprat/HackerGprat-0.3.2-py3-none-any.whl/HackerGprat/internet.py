import requests as req
from bs4 import BeautifulSoup as bs



# -------------------------------
# connection_code code
def connection_code( url ):
    '''
    # usage #200 = connected
    # Q. prompt if we are connect

    if (connection_code(url) == 200):
        print("Connected Successfully...")

    '''
    try:
        r = req.get( url )
        return r.status_code
    except:
        return( str( "Error Found in url" ) )

# url = 'https://www.pyathon.org'

# print( connection_code(url) )

# if (connection_code(url) == 200):
#     print("Connected Successfully...")
# else:
#     print("Check Url... Error Found.")
# -------------------------------




# -------------------------------
# check connection print string

def isConnected(url):
    if ( connection_code(url) == 200 ):
        return str("Connected Sucessfully....")
    else:
        error = connection_code(url)
        return str("google -> Error code ", error)


# print( isConnected(url) )

# -------------------------------
# -------------------------------
# -------------------------------


if __name__ == '__main__':
    pass
