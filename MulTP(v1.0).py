from tkinter import *
import youtube_dl as ytd

def mp3Download():
    
    link_address = E.get()

    # seeks video info
    video_info = ytd.YoutubeDL().extract_info(url = link_address, download = False)
    # filename = f"{video_info['title']}.mp3"
    options = {
            'format': 'bestaudio/best',
            'outtmpl': 'C:/Users/Lenovo/Downloads/audio_files/%(title)s.%(ext)s',
            'keepvideo' : False,
            'postprocessors': [{
            'key':'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320'
            }]
            }

    # file download
    with ytd.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    output.insert(END, 'Download complete!\n')
    E.delete(0, 1000)

# MAIN
# Creating object of tkinter class 
root = Tk()

# Setting the title, background color  
# and size of the tkinter window and  
# disabling the resizing property 
root.geometry('400x200')
root.resizable(False, False) 
root.title('Mp3 Downlaoder')
root.config(background="#1C1A18")

E = Entry(root, width = 50, bg="#FFE2C7")
E.pack(anchor = CENTER)

B = Button(root, text = "Download", bg="#FFBA00", command = mp3Download)
output = Text(root, width=40, height=8, bg="#FFE2C7")
B.pack(anchor = S)
output.pack()


root.mainloop()
