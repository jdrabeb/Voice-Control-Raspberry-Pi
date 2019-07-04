import tkinter as tk
from voiceit2 import VoiceIt2
import base64
import pyaudio
import threading
import wave
import time
import json
import pygame as pg
from control import main


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAMEBARE = "output"
WAVE_FORMAT =".wav"

HEIGHT = 400
WIDTH = 500

#global variables
is_recording = False
counter = 0
thread = None
apiKey ='key_6bd42718c389468e94a8a7f012536e29'
apiTok ='tok_c45d682db2e24504a0a1c5e3660c1e98'
my_voiceit = VoiceIt2(apiKey, apiTok)
usr_id =""
text=""
authorize=False
root = tk.Tk()
root.title("Voice Authorization")
root.geometry(str(WIDTH)+"x"+str(HEIGHT))

def record():
    global is_recording
    global counter
    global text
    global authorize
    global usr_id
    counter = counter+1
    #instantiate pyaudio
    p = pyaudio.PyAudio()

    #open stream
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    message_text.insert(tk.END,"Recording...\n")
    frames = []
    time.sleep(0.500)
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow = False)
        frames.append(data)

    message_text.insert(tk.END,"Done recording...\n")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(WAVE_OUTPUT_FILENAMEBARE+str(counter)+WAVE_FORMAT, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    is_recording = False

    if authorize == False:
        resp = my_voiceit.create_voice_enrollment(usr_id,"en-US",text, WAVE_OUTPUT_FILENAMEBARE+str(counter)+WAVE_FORMAT)
        message_text.insert(tk.END, resp['message']+"\n")
    elif authorize == True:
        pg.mixer.init()
        pg.mixer.music.load("../audio/searching.wav")
        pg.mixer.music.play()
        while pg.mixer.music.get_busy() == True:
            continue
        resp =my_voiceit.voice_verification(usr_id, "en-US", text, WAVE_OUTPUT_FILENAMEBARE+str(counter)+WAVE_FORMAT )
        message_text.insert(tk.END, resp['message']+"\n")
        if resp['responseCode'] == "SUCC":
            authorizedLabel.configure(bg='green')
            pg.mixer.init()
            pg.mixer.music.load("../audio/hello.wav")
            pg.mixer.music.play()
            while pg.mixer.music.get_busy() == True:
                continue
            main()
        else:
            authorizedLabel.configure(bg='red')
            pg.mixer.init()
            pg.mixer.music.load("../audio/who_are_you.wav")
            pg.mixer.music.play()
            while pg.mixer.music.get_busy() == True:
                continue

def create_user():
    global usr_id
    message_text.delete('1.0', tk.END)
    resp = my_voiceit.create_user()
    usr_id = resp['userId']
    userIDLabel['text'] = usr_id
    message_text.insert(tk.END, resp['message'])

def create_user_record():
    global is_recording
    global text
    global authorize
    authorize = False
    message_text.delete('1.0', tk.END)
    if not is_recording:
        print("is recording...")
        resp = my_voiceit.get_phrases("en-US")
        text=resp['phrases'][2]['text']
        message_text.insert(tk.INSERT, text+"\n")
        is_recording = True
        thread = threading.Thread(target=record)
        thread.start()


def authorize_user():
    global authorize
    global is_recording
    authorize = True
    message_text.delete('1.0', tk.END)
    if not is_recording:
        print("is recording...")
        resp = my_voiceit.get_phrases("en-US")
        text=resp['phrases'][2]['text'] +"\n"
        message_text.insert(tk.INSERT, text)
        is_recording = True
        thread = threading.Thread(target=record)
        thread.start()
    pass

rows = 0
while rows < 10:
    root.rowconfigure(rows+1, weight=1)
    root.columnconfigure(rows,weight=1)
    rows += 1



#canvas = tk.Canvas(root,height=HEIGHT, width=WIDTH)
#canvas.pack()
titleLabel = tk.Label(root, text="User Authentication by Voice")
titleLabel.grid(row=1, column=2, columnspan=6)
userLabel = tk.Label(root, text="User: ")
userLabel.grid(row=2, column=3, columnspan=1)
userIDLabel = tk.Label(root, text="...")
userIDLabel.grid(row=2, column=4, columnspan=2, sticky='w')
authorizedLabel = tk.Label(root, text="Authorized", bg='gray')
authorizedLabel.grid(row=3, column=4)

createUser_button = tk.Button(root, text="Create User", command=lambda: create_user())
createUser_button.grid(row=4, column=3)
addEnrollment_button = tk.Button(root, text="Add Recording", command= lambda: create_user_record())
addEnrollment_button.grid(row=4, column=4)
authorize_button = tk.Button(root, text="Authorize User", command= lambda: authorize_user())
authorize_button.grid(row=4, column=5)
messageLabel =  tk.Label(root, text="VoiceIt Messages:")
messageLabel.grid(row=5, column=2, columnspan=6)
message_text = tk.Text(root, height=10, width=60)
message_text.grid(row=6, column=2, columnspan=6)

root.mainloop()

