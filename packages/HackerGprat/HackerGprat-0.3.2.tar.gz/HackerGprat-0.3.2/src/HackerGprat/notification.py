# from plyer import notification
from plyer import notification

def desktop_notification( title="Title", message="Enter Your Message", timeout=10 ):
    notification.notify(
                title = title,
                message = message,
                timeout = 10
            )
    
