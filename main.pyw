# Import the required libraries
from tkinter import *
from pystray import MenuItem as item
import pystray
from PIL import Image
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import pynput
from pynput import keyboard

# Create an instance of tkinter frame or window
win=Tk()

win.title("System Tray Application")
# Set the size of the window
win.geometry("700x350")

# Define a function for quit the window
def quit_window(icon, item):
   icon.stop()
   win.destroy()

# Define a function to show the window again
def show_window(icon, item):
   icon.stop()
   win.after(0,win.deiconify())

# Hide the window and show on the system taskbar
def hide_window():
   win.withdraw()
   image=Image.open("favicon.ico")
   menu=(item('Quit', quit_window), item('Show', show_window))
   icon=pystray.Icon("name", image, "My System Tray Icon", menu)
   icon.run()

win.protocol('WM_DELETE_WINDOW', hide_window)
sessions = AudioUtilities.GetAllSessions()

def helloCallBack():
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "Spotify.exe":
            print("volume.GetMasterVolume(): %s" % volume.GetMasterVolume())
            if (volume.GetMasterVolume() + .1 > 1.0):
                print("would be")
            else:
                volume.SetMasterVolume(volume.GetMasterVolume()+.1, None)

B = Button(win, text="hello", command=helloCallBack)

# The key combination to check
COMBINATIONS = [
    {keyboard.Key.shift, keyboard.Key.f7}, # for volume down
    {keyboard.Key.shift, keyboard.Key.f8} # for voume up
]

# The currently active modifiers
current = set()

def executeDown():
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "Spotify.exe":
            print("volume.GetMasterVolume(): %s" % volume.GetMasterVolume())
            if (volume.GetMasterVolume()-.05 > 0):
                volume.SetMasterVolume(volume.GetMasterVolume()-.05, None)

def executeUp():
    for session in sessions:
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        if session.Process and session.Process.name() == "Spotify.exe":
            print("volume.GetMasterVolume(): %s" % volume.GetMasterVolume())
            if (volume.GetMasterVolume()+.05 < 1):
                volume.SetMasterVolume(volume.GetMasterVolume()+.05, None)



def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if all(k in current for k in {keyboard.Key.shift, keyboard.Key.f8}):
            executeUp()
        if all(k in current for k in {keyboard.Key.shift, keyboard.Key.f7}):
            executeDown()            

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        try:
            current.remove(key)
        except:
            print("error somewhere")

listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

B.pack()
win.mainloop()