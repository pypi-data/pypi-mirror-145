from HackerGprat import clear
from pytube import YouTube
import os

def yt(videourl, path="./Output"):
    """
        single you tube video downloder, with custom path [ by default path = current path ]
    """
    clear()
    
    print("🔌Connecting...🔐 \n")
    
    yt = YouTube(videourl)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    
    if not os.path.exists(path):
        print("Creating Folder...\n")
        os.makedirs(path)

    print("⏬ Downloading...⏳\n")
    yt.download(path)
    print("✅ SucessFully Downloaded...\n")



# url = 'https://www.youtube.com/watch?v=r2giUilvkBQ&list=PLC3y8-rFHvwg2-q6Kvw3Tl_4xhxtIaNlY&index=45'
# yt_download( url )

# urls = []


def yt_download( url, folderName="Youtube_videos" ):
    """
        youtube downloader no matter single or a list
    """
    
    if type( url ) == str:
        yt( url, folderName )
        
    elif type( url ) == list:

        # todo - detected links : 
        # todo - total file going to be downladed
        # downloading {i} 
        
        for link in url:
            yt( link )
    else:
        print("See The Docs & Try Again")


