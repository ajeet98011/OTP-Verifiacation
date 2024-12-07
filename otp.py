import os
import random
import smtplib
from tkinter import *
from tkinter import filedialog, messagebox

from PIL import Image, ImageTk

# Global variable to store user data
user_data = {}

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    window.geometry(f'{width}x{height}+{position_right}+{position_top}')

def send_otp():
    global OTP, otp_window, timer_label, time_left
    OTP = random.randint(100000, 999999)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        password = ""  #app password
        server.login("", password)  #email
        body = f"Dear {name_entry.get()},\n\nYour OTP is {OTP}."
        subject = "OTP Verification using Python"
        message = f'Subject: {subject}\n\n{body}'

        server.sendmail("", email_entry.get(), message)  #email
        server.quit()
        messagebox.showinfo("Success", "OTP has been sent to your email!")
        open_otp_verification_window()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to send OTP: {str(e)}")

def open_otp_verification_window():
    global otp_entry, otp_window, timer_label, time_left, verify_button
    otp_window = Toplevel(root)
    otp_window.title("OTP Verification")
    center_window(otp_window, 400, 350)

    otp_frame = Frame(otp_window, bg="#f9f9f9", padx=20, pady=20)
    otp_frame.pack(fill=BOTH, expand=True)

    Label(otp_frame, text="Enter the OTP sent to your email:", font=("Arial", 14), bg="#f9f9f9").pack(pady=10)
    otp_entry = Entry(otp_frame, width=25, font=("Arial", 14), bd=5, relief=GROOVE, justify=CENTER)
    otp_entry.pack(pady=5)

    timer_label = Label(otp_frame, text="", font=("Arial", 12), bg="#f9f9f9")
    timer_label.pack(pady=5)

    verify_button = create_custom_button(otp_frame, "Verify OTP", verify_otp, 14, "#4CAF50", "#45a049")
    create_custom_button(otp_frame, "Resend OTP", send_otp, 14, "#FFC107", "#ffb300")
    create_custom_button(otp_frame, "Back", otp_window.destroy, 14, "#F44336", "#f33a2e")

    time_left = 60  #Time in seconds
    start_countdown()

def start_countdown():
    global time_left
    if time_left > 0:
        mins, secs = divmod(time_left, 60)
        timer_label.config(text=f"Time left: {mins:02d}:{secs:02d}")
        time_left -= 1
        otp_window.after(1000, start_countdown)
    else:
        timer_label.config(text="OTP expired! Please resend OTP.")
        verify_button.config(state=DISABLED)

def verify_otp():
    entered_otp = otp_entry.get()
    if entered_otp == str(OTP) and time_left > 0:
        messagebox.showinfo("Success", "OTP Verified!")
        otp_window.destroy()
        open_profile_upload_window()
    else:
        messagebox.showerror("Error", "Invalid OTP or OTP has expired, please try again.")

def create_custom_button(parent, text, command, font_size, bg_color, hover_color):
    button = Button(parent, text=text, command=command, font=("Arial", font_size), bg=bg_color, fg="white",
                    bd=0, relief=FLAT, cursor="hand2", activebackground=hover_color, activeforeground="white")
    button.pack(pady=10, padx=20)

    button.bind("<Enter>", lambda e: button.config(bg=hover_color))
    button.bind("<Leave>", lambda e: button.config(bg=bg_color))
    return button

def typing_effect(target_text, label, index=0):
    if index < len(target_text):
        current_text = label.cget("text") + target_text[index]
        label.config(text=current_text)
        root.after(100, typing_effect, target_text, label, index + 1)

def start_typing_animation():
    typing_effect("OTP Verification", title_label)

def open_profile_upload_window():
    global profile_pic_label, phone_entry, address_entry
    profile_window = Toplevel(root)
    profile_window.title("User Profile")
    center_window(profile_window, 500, 600)

    profile_frame = Frame(profile_window, bg="#f9f9f9", padx=20, pady=20)
    profile_frame.pack(fill=BOTH, expand=True)

    Label(profile_frame, text="Upload Profile Picture:", font=("Arial", 14), bg="#f9f9f9").pack(pady=10)

    profile_pic_label = Label(profile_frame, bg="#f9f9f9", width=15, height=7, relief=SOLID)
    profile_pic_label.pack(pady=10)

    create_custom_button(profile_frame, "Upload Picture", upload_profile_picture, 14, "#2196F3", "#1976D2")

    Label(profile_frame, text="Enter Your Phone Number:", font=("Arial", 12), bg="#f9f9f9").pack(pady=10)
    phone_entry = Entry(profile_frame, width=30, font=("Arial", 12), bd=3, relief=GROOVE)
    phone_entry.pack(pady=5)

    Label(profile_frame, text="Enter Your Address:", font=("Arial", 12), bg="#f9f9f9").pack(pady=10)
    address_entry = Entry(profile_frame, width=30, font=("Arial", 12), bd=3, relief=GROOVE)
    address_entry.pack(pady=5)

    create_custom_button(profile_frame, "Save Details", save_details, 14, "#4CAF50", "#45a049")
    create_custom_button(profile_frame, "Open User Page", open_user_page, 14, "#009688", "#00796D")

def upload_profile_picture():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        try:
            img = Image.open(file_path)
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            profile_pic_label.config(image=photo)
            profile_pic_label.image = photo
            user_data['profile_picture'] = photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image: {str(e)}")

def save_details():
    user_data['phone'] = phone_entry.get()
    user_data['address'] = address_entry.get()
    messagebox.showinfo("Success", "User details saved successfully!")

def open_user_page():
    user_page_window = Toplevel(root)
    user_page_window.title("User Page")
    center_window(user_page_window, 400, 400)

    user_info_frame = Frame(user_page_window, bg="#f9f9f9", padx=20, pady=20)
    user_info_frame.pack(fill=BOTH, expand=True)

    Label(user_info_frame, text="User Profile Details", font=("Arial", 16), bg="#f9f9f9").pack(pady=10)
    Label(user_info_frame, text=f"Phone: {user_data.get('phone', 'N/A')}", font=("Arial", 12), bg="#f9f9f9").pack(pady=5)
    Label(user_info_frame, text=f"Address: {user_data.get('address', 'N/A')}", font=("Arial", 12), bg="#f9f9f9").pack(pady=5)

    if 'profile_picture' in user_data:
        profile_pic_display = Label(user_info_frame, image=user_data['profile_picture'], bg="#f9f9f9")
        profile_pic_display.pack(pady=10)

#Initialize the main window
root = Tk()
root.title("OTP Verification")
center_window(root, 500, 500)  #Set the window size to 500x500

# Add app icon
try:
    root.iconphoto(False, PhotoImage(file='otp_image.png'))  #Load the app logo
except Exception as e:
    print(f"Error loading icon: {str(e)}")

#Main layout
main_frame = Frame(root, bg="#f9f9f9", padx=20, pady=20)
main_frame.pack(fill=BOTH, expand=True)

#Add app logo
try:
    logo_image = Image.open("otp_image.png")  #Load the app logo
    logo_image = logo_image.resize((100, 100), Image.Resampling.LANCZOS)  #Resize the image
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = Label(main_frame, image=logo_photo, bg="#f9f9f9")
    logo_label.pack(pady=10)  #Add logo at the top
except Exception as e:
    print(f"Error loading logo: {str(e)}")

#Animated title
title_label = Label(main_frame, text="", font=("Arial", 24), bg="#f9f9f9", fg="#2196F3")
title_label.pack(pady=10)

#Start typing animation after a delay
root.after(500, start_typing_animation)

# Input fields
Label(main_frame, text="Enter Your Name:", font=("Arial", 14), bg="#f9f9f9").pack(pady=10)
name_entry = Entry(main_frame, width=30, font=("Arial", 12), bd=3, relief=GROOVE)
name_entry.pack(pady=5)

Label(main_frame, text="Enter Your Email:", font=("Arial", 14), bg="#f9f9f9").pack(pady=10)
email_entry = Entry(main_frame, width=30, font=("Arial", 12), bd=3, relief=GROOVE)
email_entry.pack(pady=5)

create_custom_button(main_frame, "Send OTP", send_otp, 14, "#2196F3", "#1976D2")

#Run the main loop
root.mainloop()
