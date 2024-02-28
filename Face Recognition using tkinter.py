import cv2
import tkinter as tk
from tkinter import *
from tkinter import StringVar, messagebox
import customtkinter
from PIL import Image, ImageTk
import face_recognition

# Initialize Tkinter
root = tk.Tk()
root.title('Face Recognition Login')

# Set background color
bg_colour = '#3d6466'

# Create frames
f1 = tk.Frame(root, width=1024, height=720, bg=bg_colour)
f1.pack(expand=True, fill='both')
f2 = tk.Frame(root, bg=bg_colour)

# Declare global variables
un = StringVar()
pw = StringVar()
label = None  # Initialize label as None

# Function to clear widgets in a frame
def clear_widgets(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# Load frame 1
def load_f1():
    global un, pw, label  # Declare global variables
    clear_widgets(f1)
    f2.pack_forget()  # Hide frame 2
    f1.pack_propagate(False)  # Prevent child from modifying parent
    
    #logoimage
    img = Image.open("C:/Users/sumat/OneDrive/Desktop/Practice/PROJECT/logo.png").resize((400,400))
    logo_img=ImageTk.PhotoImage(img)
    logo_widget=tk.Label(f1,image=logo_img,bg=bg_colour)
    logo_widget.image=logo_img
    logo_widget.pack(side='left')

    l1 = tk.Label(f1, text="Face Recognition Login", bg=bg_colour, fg="white", font=("AmarilloUSAF", 20, "bold"))
    l1.pack(pady=20)

    button = customtkinter.CTkButton(f1, text="login",font=('TkHeadingFont', 20),fg_color=('#badee2',bg_colour), command=load_f2)
    button.place(x=650, y=475)
##    tk.Button(f1,text='login',font=('TkHeadingFont', 20),
##              bg='#28393a',fg='white',cursor='hand2',
##              activebackground='#badee2',activeforeground='black',
##              command=load_f2).place(x=670, y=475)

    img = Image.open("C:/Users/sumat/OneDrive/Desktop/Practice/PROJECT/USER.png").resize((200,200))
    logo_img=ImageTk.PhotoImage(img)
    logo_widget=tk.Label(f1,image=logo_img,bg=bg_colour)
    logo_widget.image=logo_img
    logo_widget.place(x=600, y=205)

    l2=tk.Label(f1)
    e1 = Entry(f1,textvariable=un,bg='#badee2').place(x=675, y=285,width=110,height=25)

    img = Image.open("C:/Users/sumat/OneDrive/Desktop/Practice/PROJECT/PASS.png").resize((200,200))
    logo_img=ImageTk.PhotoImage(img)
    logo_widget=tk.Label(f1,image=logo_img,bg=bg_colour)
    logo_widget.image=logo_img
    logo_widget.place(x=600, y=355,height=100)

    l3=tk.Label(f1)
    e2 = Entry(f1, width=20, textvariable=pw, show="*",bg='#badee2').place(x=675, y=400,width=115,height=25)

    img = Image.open("C:/Users/sumat/OneDrive/Desktop/Practice/PROJECT/LOGIN.png").resize((100,100))
    logo_img=ImageTk.PhotoImage(img)
    logo_widget=tk.Label(f1,image=logo_img,bg=bg_colour)
    logo_widget.image=logo_img
    logo_widget.place(x=650, y=100,height=150)


# Load frame 2 (face recognition)
def load_f2():
    global un, pw, label  # Access global variables
    f1.pack_forget()  # Hide frame 1
    f2.pack(expand=True, fill='both')

    label = tk.Label(f2)  # Initialize label in frame 2
    label.pack()  # Pack label

    # Open the webcam using OpenCV
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def recognize_face(frame):
        # Resize frame to speed up face recognition
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        # Load the known face images and their corresponding names
        known_face_encodings = []
        known_face_names = ["Viki"]

        # Load the known face image for Viki
        viki_image = face_recognition.load_image_file("Viki.jpeg")
        viki_face_encoding = face_recognition.face_encodings(viki_image)[0]
        known_face_encodings.append(viki_face_encoding)

        for face_encoding in face_encodings:
            # See if the face matches any known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            return name

    def update_frame():
        ret, frame = cap.read()
        if not ret:
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        recognized_name = recognize_face(frame)

        if un.get() == "ABC" and pw.get() == "123" and recognized_name == "Viki":
            messagebox.showinfo("Login Successful", "Welcome, Viki!")
            
            # Load the image after successful login
            img = Image.open("C:/Users/sumat/OneDrive/Desktop/Practice/PROJECT/side-img.png").resize((400, 400))
            logo_img = ImageTk.PhotoImage(img)
            logo_widget = tk.Label(f2, image=logo_img, bg=bg_colour)
            logo_widget.image = logo_img
            logo_widget.pack(side='left')
    
            # Add an exit button
            exit_button = tk.Button(f2, text='Exit', font=('TkHeadingFont', 20),
                                    bg='#28393a', fg='white', cursor='hand2',
                                    activebackground='#badee2', activeforeground='black',
                                    command=close_frame2)
            exit_button.place(x=670, y=475)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials or unrecognized face.")
            print("Login Failed")

        cv2.putText(frame, recognized_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img_tk = ImageTk.PhotoImage(img)

        label.config(image=img_tk)
        label.image = img_tk
        f2.after(10, update_frame)  # Continuously update the frame

    def close_frame2():
        cap.release()
        f2.pack_forget()

    update_frame()

# Bind the Escape key to close the app
root.bind('<Escape>', lambda e: root.destroy())

# Load frame 1 by default
load_f1()

# Start the Tkinter event loop
root.mainloop()
