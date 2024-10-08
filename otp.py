import os
import random
import smtplib
from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk


# Function to center the window on the screen
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    window.geometry(f'{width}x{height}+{position_right}+{position_top}')

# Function to send OTP
def send_otp():
    global OTP, otp_window
    OTP = random.randint(100000, 999999)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        password = ""  # App password
        server.login("", password)  # email

        body = f"Dear {name_entry.get()},\n\nYour OTP is {OTP}."
        subject = "OTP Verification using Python"
        message = f'Subject: {subject}\n\n{body}'

        server.sendmail("techskill121@gmail.com", email_entry.get(), message)
        server.quit()

        messagebox.showinfo("Success", "OTP has been sent to your email!")

        open_otp_verification_window()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to send OTP: {str(e)}")

# Function to open OTP verification window
def open_otp_verification_window():
    global otp_entry, otp_window

    otp_window = Toplevel(root)
    otp_window.title("OTP Verification")
    center_window(otp_window, 300, 250)

    Label(otp_window, text="Enter the OTP sent to your email:", font=("Arial", 12)).pack(pady=10)
    otp_entry = Entry(otp_window, width=20, font=("Arial", 12), bd=5, relief=GROOVE, cursor="xterm")
    otp_entry.pack(pady=5)

    create_button(otp_window, "Verify OTP", verify_otp, 12, 15, 10)
    
    # Adding Resend OTP button
    create_button(otp_window, "Resend OTP", send_otp, 12, 15, 5, bg="#FFC107")  # Amber color

    # Adding Back button
    create_button(otp_window, "Back", otp_window.destroy, 12, 15, 5, bg="#F44336")  # Red color

# Function to verify OTP
def verify_otp():
    entered_otp = otp_entry.get()

    if entered_otp == str(OTP):
        messagebox.showinfo("Success", "OTP Verified!")
        otp_window.destroy()
    else:
        messagebox.showerror("Error", "Invalid OTP, please try again.")

# Function to create a button with rounded corners
def create_button(parent, text, command, font_size, width, pady, bg="#4CAF50"):
    button_frame = Frame(parent, bg=bg, bd=0)  
    button_frame.pack(pady=pady)

    button = Button(button_frame, text=text, command=command, font=("Arial", font_size),
                    bg=bg, fg="white", bd=0, width=width, cursor="hand2")
    button.pack(fill=BOTH, expand=True)

    # Hover effects
    button.bind("<Enter>", lambda e: button_frame.config(bg="#2196F3"))  
    button.bind("<Leave>", lambda e: button_frame.config(bg=bg))  

    # Click effect
    button.bind("<ButtonPress-1>", lambda e: button_frame.config(bg="#1976D2"))
    button.bind("<ButtonRelease-1>", lambda e: button_frame.config(bg="#2196F3"))  

# Setting up the GUI
root = Tk()
root.title("OTP Verification System")
center_window(root, 500, 500)  
root.config(bg="#f0f0f0")

Label(root, text="OTP Verification", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=20)

# Load and place the image
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "otp_image.png")

try:
    otp_image = Image.open(image_path)
    otp_image = otp_image.resize((100, 100), Image.Resampling.LANCZOS)
    otp_photo = ImageTk.PhotoImage(otp_image)

    Label(root, image=otp_photo, bg="#f0f0f0").pack(pady=10)
except FileNotFoundError:
    messagebox.showerror("Error", "Image file not found! Please check the file path.")
except Exception as e:
    messagebox.showerror("Error", f"Unable to load image: {str(e)}")

Label(root, text="Enter Your Name:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
name_entry = Entry(root, width=30, font=("Arial", 12), bd=5, relief=GROOVE, cursor="xterm")
name_entry.pack()

Label(root, text="Enter Your Email:", font=("Arial", 12), bg="#f0f0f0").pack(pady=10)
email_entry = Entry(root, width=30, font=("Arial", 12), bd=5, relief=GROOVE, cursor="xterm")
email_entry.pack()

create_button(root, "Send OTP", send_otp, 12, 15, 20)

# Running the GUI application
root.mainloop()
