import socket
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
import os

# Configuration
HOST = '127.0.0.1'
PORT = 6555
received_files_directory = 'received_files'

if not os.path.exists(received_files_directory):
    os.makedirs(received_files_directory)

# Create a socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Initialize the GUI
root = tk.Tk()
root.title("File Transfer Client")
root.geometry("800x600")
root.resizable(False, False)

# Textbox for displaying messages
message_box = scrolledtext.ScrolledText(root, wrap=tk.WORD)
message_box.pack(fill=tk.BOTH, expand=True)
message_box.config(state=tk.DISABLED)

# Function to add a message to the textbox
def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)

# Function to connect to the server
def connect():
    try:
        client.connect((HOST, PORT))
        add_message("Connected to the server")
    except Exception as e:
        messagebox.showerror("Connection Error", f"Unable to connect to server: {e}")

# Function to send a file to the server
def send_file():
    filename = filedialog.askopenfilename()
    if filename:
        file_name = os.path.basename(filename)
        client.send(file_name.encode())
        with open(filename, 'rb') as file:
            file_data = file.read(1024)
            while file_data:
                client.send(file_data)
                file_data = file.read(1024)
        client.send(b"END_OF_FILE")

# Function to handle incoming messages
def listen_for_messages():
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                add_message(message)
            else:
                messagebox.showerror("Error", "Message received from server is empty")
        except Exception as e:
            print(f"Error while receiving message: {e}")
            break

# Start listening for incoming messages
listen_thread = threading.Thread(target=listen_for_messages)
listen_thread.daemon = True
listen_thread.start()

# Connect to the server
connect_button = tk.Button(root, text="Connect to Server", command=connect)
connect_button.pack()

# Send a file to the server
send_file_button = tk.Button(root, text="Send File to Server", command=send_file)
send_file_button.pack()

# Main loop
root.mainloop()
