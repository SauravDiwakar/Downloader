import youtube_dl as ytd
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
from tkinter import messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from threading import *
import validators

driver_location = 'D:\python projects\chromedriver\chromedriver'

def isLinkValid(link_address):
    extractors = ytd.extractor.gen_extractors()
    for e in extractors:
        if e.suitable(link_address) and e.IE_NAME != 'generic':
            return True
    return False

def downloadMp4Thread():
    thread = Thread(target = downloadMp4)
    thread.start()

def downloadMp4():   
    link_address = paste_link.get()
    if validators.url(link_address):
        if isLinkValid(link_address):
            try:
                video_info = ytd.YoutubeDL().extract_info(url = link_address, download = False)
                options = {
                    'format': 'bestvideo+bestaudio[ext=m4a]/best',
                    'outtmpl': f'{directory}/%(title)s.%(ext)s',
                    'audioquality': '0'
                    }
                output.insert(END, 'Download starting..\n')
                # download video file
                with ytd.YoutubeDL(options) as ydl:
                    ydl.download([video_info['webpage_url']])

                pgbar['value'] = 100
                output.insert(END, 'Download complete!\n')
            except NameError:
                output.insert(END, 'Select path first..\n')
        else:
            output.insert(END, 'Incompatible URL!!\n')
    else:
        output.insert(END, 'Not a URL!!!\n')

def downloadMp3Thread():
    thread = Thread(target = downloadMp3)
    thread.start()

def downloadMp3():    
    link_address = paste_link.get()
    if validators.url(link_address):
        if isLinkValid(link_address):
            try:    
                # seeks video info
                video_info = ytd.YoutubeDL().extract_info(url = link_address, download = False)
                # filename = f"{video_info['title']}.mp3"
                options = {
                        'format': 'bestaudio/best',
                        'outtmpl': f'{directory}/%(title)s.%(ext)s',
                        'keepvideo' : False,
                        'postprocessors': [{
                        'key':'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '320'
                        }]
                        }
                output.insert(END, 'Download starting..\n')
                # file download
                with ytd.YoutubeDL(options) as ydl:
                    ydl.download([video_info['webpage_url']])

                pgbar['value'] = 100
                output.insert(END, 'Download complete!\n')
            except NameError:
                output.insert(END, 'Select path first..\n')       
        else:
            output.insert(END, 'Incompatible URL!!\n')
    else:
        output.insert(END, 'Not a URL!!!\n')

def chooseDirThread():
    thread = Thread(target = chooseDir)
    thread.start()

def chooseDir():
    global directory
    directory = tk.filedialog.askdirectory()
    dir_select.delete(0, 1000)
    dir_select.insert(END, directory)

def searchYouTubeThread():
    thread = Thread(target = searchYouTube)
    thread.start()

def searchYouTube():
    content = search_item.get()
    if len(content):
        driver = webdriver.Chrome(driver_location)
        driver.get('https:\www.youtube.com')
        driver.maximize_window()

        time.sleep(1)
        assert 'YouTube' in driver.title
        search_btn = driver.find_element_by_name('search_query')
        search_btn.clear()
        search_btn.send_keys(content)
        search_btn.send_keys(Keys.RETURN)
    else:
        output.insert(END, 'Empty Search bar!\n')

def searchGoogleThread():
    thread = Thread(target = searchGoogle)
    thread.start()

def searchGoogle():
    content = search_item.get()
    if len(content):
        driver = webdriver.Chrome(driver_location)
        driver.get('https:\www.google.com')
        driver.maximize_window()

        time.sleep(1)
        assert 'Google' in driver.title
        search_btn = driver.find_element_by_class_name('gLFyf')
        search_btn.clear()
        search_btn.send_keys(content)
        search_btn.send_keys(Keys.RETURN) 
    else:
        output.insert(END, 'Empty Search bar!\n')

def clearAll():
    output.delete('1.0', END)
    pgbar['value'] = 0
        
if __name__ == '__main__':
    # Creating object of tkinter class 
    root = Tk()

    # Setting the title, background color  
    # and size of the tkinter window and  
    # disabling the resizing property 
    root.geometry('400x400')
    root.resizable(False, False) 
    root.title('MulTP(v2.0)')
    root.config(background="#0C3B2E")

    # SEARCH SECTION 
    search_item = tk.Entry(root, 
        width = 50, 
        bg="#FFFFFF"
    )
    search_item.place(x = 35, y = 30)
    
    # will clear the search bar
    cross_btn = tk.Button(root,
        text = 'x',
        command = lambda:search_item.delete(0, 1000),
        bg="#B46617",
        activebackground = '#6D9773',
        activeforeground = '#FFFFFF',
        height = 1
    ).place(x = 350, y = 28)

    search_google_btn = tk.Button(root,
        text = 'Search Google',
        bg="#FFBA00",
        activebackground = '#6D9773',
        activeforeground = '#FFFFFF',
        command = searchGoogleThread
    ).place(x = 80, y = 70)

    search_youtube_btn = tk.Button(root,
        text = 'Search YouTube',
        bg="#FFBA00",
        activebackground = '#6D9773',
        activeforeground = '#FFFFFF',
        command = searchYouTubeThread
    ).place(x = 210, y = 70)

    # DOWNLOAD SECTION 
    paste_link = tk.Entry(root, 
        width = 50, 
        bg="#FFFFFF"
    )
    paste_link.place(x = 35, y = 120)

    clear_link_btn = tk.Button(root,
        text = 'x',
        command = lambda:paste_link.delete(0, 1000),
        bg="#B46617",
        activebackground = '#6D9773',
        activeforeground = '#FFFFFF',
        height = 1
    ).place(x = 350, y = 118)

    dir_select = tk.Entry(root,
        width = 50,
        bg = '#FFFFFF'
    )
    dir_select.place(x = 35, y = 155)

    dir_select_btn = tk.Button(root,
        text = '..',
        command = chooseDirThread,
        bg="#B46617",
        activebackground = '#6D9773',
        activeforeground = '#FFFFFF',
        height = 1
    ).place(x = 350, y = 153)

    mp3_btn = tk.Button(root, 
        text = "Download Mp3", 
        bg="#FFBA00", 
        command = downloadMp3Thread,
        activebackground = '#6D9773',
        activeforeground = '#FFFFFF'
    )
    mp3_btn.place(x = 70, y = 190)

    mp4_btn = tk.Button(root, 
        text = "Download Mp4", 
        bg="#FFBA00", 
        command = downloadMp4Thread,
        activebackground = '#6D9773',
        activeforeground = '#FFFFFF'
    )
    mp4_btn.place(x = 210, y = 190)

    # PROGRESS SECTION 
    pgbar = Progressbar(
        root,
        length = 380,
        orient = HORIZONTAL,
        maximum = 100,
        value = 0,
        mode = 'determinate'
    )
    pgbar.place(x = 10, y = 230)

    # OUTPUT SECTION 
    output = Text(root, 
        width=47, 
        height=6, 
        bg="#FFFFFF"
    )
    output.place(x = 10, y = 260)

    clear_all_btn = tk.Button(root,
        text = 'Clear All',
        command = clearAll,
        bg="#B46617",
        activebackground = '#6D9773',
        activeforeground = '#FFFFFF',
        height = 1,
        width = 50
    ).place(x = 20, y = 370)

    root.mainloop()

