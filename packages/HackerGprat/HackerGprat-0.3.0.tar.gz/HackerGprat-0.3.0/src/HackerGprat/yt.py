from HackerGprat import clear
from pytube import YouTube
import os

def yt_download(videourl, path="./Output"):

    clear()
    
    print("Connecting...")
    
    yt = YouTube(videourl)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    
    if not os.path.exists(path):
        print("Creating Folder...")
        os.makedirs(path)

    print("Downloading...")
    yt.download(path)
    print("SucessFully Downloaded...")



# url = 'https://www.youtube.com/watch?v=r2giUilvkBQ&list=PLC3y8-rFHvwg2-q6Kvw3Tl_4xhxtIaNlY&index=45'
# yt_download( url )

# urls = []


def yt( videoUrl, path="./Output"):
    
    if type( videoUrl ) == str:
        yt_download(videourl)
        
    elif type( videoUrl ) == list:
        for link in videoUrl:
            yt_download( link )
    else:
        print("See The Docs & Try Again")



