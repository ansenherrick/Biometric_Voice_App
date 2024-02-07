import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import sounddevice as sd
import numpy as np
import threading
import wavio
import speech_recognition as sr
import json
from PIL import Image, ImageTk
import os
import time
from tkinter import filedialog
from tkinter import PhotoImage
from customtkinter import *
  
def update_mic_status():
    global working_mics
    if working_mics[0] == 1:
        mic1_icon_label.configure(image=mic1_on_image)
    else:
        mic1_icon_label.configure(image=mic1_off_image)

    if working_mics[1] == 1:
        mic2_icon_label.configure(image=mic2_on_image)
    else:
        mic2_icon_label.configure(image=mic2_off_image)

def select_file():
    # This function will be triggered when the button is clicked
    root.filepath = filedialog.askdirectory(initialdir="/", title="Select file")
    print("Selected file:", root.filepath)
    save_variable_to_file('config/filepath.txt', root.filepath)

def read_variable_from_file(file_path):
    with open(file_path, 'r') as file:
        variable = str(file.readline().strip())
    return variable

def save_variable_to_file(file_path, variable):
    with open(file_path, 'w') as file:
        file.write(str(variable))

def open_settings():
    def on_closing():
        print("Window is closing!")
        global mic1_index, mic2_index
        mic1_index = mic1_var.get()
        mic2_index = mic2_var.get() if mic2_var.get() != "No Mic" else None
        print(mic1_index)
        print(mic2_index)
        settings_window.destroy()

    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x200")
    settings_window.protocol("WM_DELETE_WINDOW", on_closing)

    global mic1_var, mic2_var, noisy

    noisy = tk.BooleanVar()

    options_frame = tk.Frame(settings_window)
    options_frame.pack(anchor='center', pady = 10)
    
    mic1_text = ttk.Label(options_frame)
    mic1_text.config(text="Select Microphone 1")
    mic1_text.grid(column=0, row=2, padx=4)

    mic2_text = ttk.Label(options_frame)
    mic2_text.config(text="Select Microphone 2")
    mic2_text.grid(column=0, row=3, padx=4)

    noisy_text = ttk.Label(options_frame)
    noisy_text.config(text="Select Environment")
    noisy_text.grid(column=0, row=0, padx=4)

    path_text = ttk.Label(options_frame)
    path_text.config(text="Select Save Location")
    path_text.grid(column=0, row=1, padx=4) 

    checkbox = ttk.Checkbutton(options_frame, text="Noisy Environment", variable=noisy)
    checkbox.grid(column=1, row=0, pady=5, padx=4) 

    button = tk.Button(options_frame, text="Select File Path", command=select_file)
    button.grid(column=1, row=1, pady=5, padx=4) 

    mic1_var = tk.StringVar()
    mic1_combobox = ttk.Combobox(options_frame, textvariable=mic1_var, values=mic_list)
    mic1_combobox.grid(column=1, row=2, pady=5, padx=4) 
    mic1_combobox.set(mic1_index)  # Set default value

    mic2_var = tk.StringVar()
    mic2_combobox = ttk.Combobox(options_frame, textvariable=mic2_var, values=mic_list)
    mic2_combobox.grid(column=1, row=3, pady=5, padx=4) 
    mic2_combobox.set(mic2_index)  # Set default value

def record_audio(mic_index, filename_td, filename_ti):
    global error, working_mics
    if mic_index is None:
        return  # Do nothing if 'No Mic' is selected

    fs = 44100  # Sample rate
    seconds = 30  # Duration of recording
    ti_seconds = 20

    print(f"Recording from microphone {mic_index} for {seconds} seconds")

    time.sleep(5)
    print("error = " + str(error))

    try:
        myrecording_td = sd.rec(int(seconds * fs), samplerate=fs, channels=2, device=mic_index)
    except Exception as e:
        if mic_index == mic1_index:
            working_mics[0] = 0
        elif mic_index == mic2_index:
            working_mics[1] = 0
        update_mic_status()
        error = 1

    if error == 0:
        working_mics = [1, 1]
        update_mic_status()
    sd.wait()  # Wait until recording is finished
    wavio.write(filename_td, myrecording_td, fs, sampwidth=2)  # Save as WAV file 
    print(f"File written to {filename_td}")
    
    time.sleep(5)

    print(f"Recording from microphone {mic_index} for {ti_seconds} seconds")
    myrecording_ti = sd.rec(int(ti_seconds * fs), samplerate=fs, channels=2, device=mic_index)
    sd.wait()  # Wait until recording is finished
    wavio.write(filename_ti, myrecording_ti, fs, sampwidth=2)  # Save as WAV file 
    print(f"File written to {filename_ti}")

    record_button.place(relx=0.5, rely=0.9, anchor='center') 
    filename_entry.place(relx=0.5, rely=0.83, anchor='center')
    print(threading.current_thread().name + " Stopping")
    return
    
def show_sequence():
    try:
        with open('config/sequence.json', 'r') as file:
            sequence = json.load(file)

        for item in sequence:
            if 'image' in item:
                image_path = os.path.join('images', item['image'])
                image = CTkImage(light_image=Image.open(image_path), size=(300,300))
                #image = image.resize((300, 300), Image.LANCZOS)
                #photo = ImageTk.PhotoImage(image)
                image_label.configure(image=image, text="")
                image_label.image = image  # Keep a reference
                image_label.place(relx=0.5, rely=0.45, anchor='center')

            if 'text' in item:
                text_label.configure(text=item['text'])
                text_label.place(relx=0.5, rely=0.15, anchor='center')

            time.sleep(item.get('duration', 5))

            image_label.place_forget()
            text_label.configure(text="")
            
    except Exception as e:
        print(f"Error in show_sequence: {e}")
    
def start_recording():
    global mic1_index, mic2_index, error
    record_button.place_forget()
    filename_entry.place_forget()
    try:
        mic1_var.get()
        mic1_index = mic1_var.get()
        mic2_index = mic2_var.get() if mic2_var.get() != "No Mic" else None
    except NameError:
        mic1_index = 'Microsoft Sound Mapper - Input'
        mic2_index = None

    try:
        noisy.get()
        noisy_boolean = noisy.get()
    except NameError:
        noisy_boolean = False

    folder = "noisy/" if noisy_boolean else "normal/"
    filename1 = read_variable_from_file('config/filepath.txt') + "/text_dependent/" + folder + filename_entry.get() + "_1.wav"
    filename2 = read_variable_from_file('config/filepath.txt') + "/text_dependent/" + folder + filename_entry.get() + "_2.wav"
    filename1_ti = read_variable_from_file('config/filepath.txt') + "/text_independent/" + folder + filename_entry.get() + "_1.wav"
    filename2_ti = read_variable_from_file('config/filepath.txt') + "/text_independent/" + folder + filename_entry.get() + "_2.wav"

    error = 0
    print("error = " + str(error))
    threading.Thread(target=record_audio, args=(mic1_index, filename1, filename1_ti)).start()
    if mic2_index is not None:
        threading.Thread(target=record_audio, args=(mic2_index, filename2, filename2_ti)).start()

    # start recording
    threading.Thread(target=show_sequence).start()

def on_main_closing():
        print("Window is closing!")
        root.destroy()

# Retrieve a list of available microphones
mic_list = sr.Microphone.list_microphone_names()
mic_list.append("No Mic")  # Add the 'No Mic' option

#initializing needed variables
global mic1_index, mic2_index, working_mics
mic1_index = 'Microsoft Sound Mapper - Input'
mic2_index = 'No Mic'
working_mics = [1, 1]

# Setting up the GUI with a themed window
root = CTk()
root.title("Audio Recorder")
root.geometry("800x600")
root.protocol("WM_DELETE_WINDOW", on_main_closing)
set_appearance_mode("light")
base = 800
height = 600

canvas = tk.Canvas(root)
canvas.place(relx=0.5, rely=0.42, anchor="center", width=800, height=700)

# Draw an outline box in the middle
canvas.create_rectangle(10, 10, 790, 690, outline="black", width=3)

settings_icon = CTkButton(root, text="Settings", command=open_settings)
settings_icon.place(relx=0.8, y=20)

record_button = CTkButton(root, text="Start Recording", command=start_recording)
record_button.place(relx=0.5, rely=0.9, anchor='center')

file = tk.StringVar()
filename_entry = CTkEntry(root, placeholder_text="Enter ID Number", width=200)
filename_entry.place(relx=0.5, rely=0.83, anchor='center')

image_label = CTkLabel(root)
text_label = CTkLabel(root, font=('Arial', 20), wraplength=400, justify='center')

mic1_on_image = CTkImage(light_image=Image.open("images/mic1_on.png"), size=(45,40))
mic1_off_image = CTkImage(light_image=Image.open("images/mic1_off.png"), size=(45,40))
mic2_on_image = CTkImage(light_image=Image.open("images/mic2_on.png"), size=(45,40))
mic2_off_image = CTkImage(light_image=Image.open("images/mic2_off.png"), size=(45,40))

# Create Label widgets for microphone status
mic1_icon_label = CTkLabel(root, image=mic1_on_image, text="")
mic1_icon_label.place(anchor='nw', x=10, y=5)

mic2_icon_label = CTkLabel(root, image=mic2_on_image, text="")
mic2_icon_label.place(anchor='nw', x=60, y=5)

# Initial update of microphone status icons
update_mic_status()

root.mainloop()
