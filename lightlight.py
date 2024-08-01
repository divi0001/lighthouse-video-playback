"""_summary_: This should display videos on the "lighthouse"-project in Kiel
"""
import time
# import os
import cv2
from pyghthouse import Pyghthouse  # Paket muss ggf. erst installiert werden!
from login import username, token  # In login.py müsst ihr eure Login-Daten eintragen! Mit token (Login.py) ist der API token gemeint, findet man auf der https://www.lighthouse.uni-kiel.de/user/divi Seite
from pytubefix import YouTube
from pytubefix.cli import on_progress

#os.chdir('.')
#28x14 Leinwand

def play_video(video_src: str, p: Pyghthouse, frame_rate: float, is_yt: bool):
    """_summary_ This plays the video, either from a mp4, which you give as a path or 
    downloads from youtube via url. It will be downscaled by a lot, so high resolution
    videos might be hard to recognize in animation.

    Parameters
    ----------
    frames : String
        String of location of mp4 of the video or yt url
    p : Pyghthouse
        The Pyghthouse object, which accesses the API and sets the frames
    frame_rate: Float
        The frame rate you want to set, based on it, the set_image command will be slowed 
        by calling sleep with 1/frame_rate seconds as the delay. Note that this is not perfect,
        therefore the video this is based of might play faster than the animation if played
        at the same time. This depends on your hardware
    isYT: bool
        Indicates, if the given video_src is a file location or url
    """
    #Normally p was created in an outer scope, but i wanted the function to be executable without
    #having to write more than this function execution
    p = Pyghthouse(username, token)
    p.connect()
    Pyghthouse.start(p)
    p.set_frame_rate(frame_rate)
    if not is_yt:
        vidcap = cv2.VideoCapture(video_src)
        success, s_img = vidcap.read()
        count = 0
        while success:
            img = cv2.resize(s_img, (28, 14), interpolation=cv2.INTER_AREA)
            count += 1
            #Uncomment if color conversion is necessary
            # rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            list_img = to_list(img)
            #Uncomment to display info about the dimensions of the downscaled image
            # print(f'The image has {len(list_img)} rows and {len(list_img[0])} cols') 
            Pyghthouse.set_image(p, list_img)
            time.sleep(1.0/frame_rate)
            success, s_img = vidcap.read()
        print(f'The video had {count} frames')
        vidcap.release()
        return
    else:
        name = dl_yt(video_src, dst_path='')
        play_video(f'{name}.mp4', p, frame_rate, False)
    p.close()

def to_list(img):
    """_summary_ Creates the list format needed for Pyghthouse

    Parameters
    ----------
    img : MatLike
        np array or other MatLike to be converted

    Returns
    -------
    list
        The image as a nested list containing a pixel list for [R,G,B] values
    """
    height, width, _ = img.shape
    iml = []
    for y in range(height):
        iml += [[]]
        for x in range(width):
            #uncomment this block and comment the next code line if you want strictly completely 
            # black and white pixels
            # if img[y,x][0] > 0 or img[y,x][1] > 0 or img[y,x][2] > 0: #make black white only
                # iml[y] += [255,255,255]
            # else:
                # iml[y] += [0,0,0]

            iml[y] += [[img[y,x][0],img[y,x][1],img[y,x][2]]]
    return iml



def dl_yt(url, dst_path = '.'):
    """_summary_ Downloads a youtube video from the given URL to the defined dst_path, 
    for this, lowest resolution is chosen because it is downscaled anyway 

    Parameters
    ----------
    url : str
        _description_ The url of the youtube video
    dst_path : str, optional
        _description_, by default '.', the path at which the video shall be saved

    Returns
    -------
    yt.title: str
        The title of the video, which is also the name of the mp4 created
        
    """
    yt = YouTube(url, on_progress_callback= on_progress) #A progress bar for the yt download
    print(yt.title)
    ys = yt.streams.get_lowest_resolution()
    ys.download(output_path=dst_path)
    return yt.title
