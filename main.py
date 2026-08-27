import tkinter as tk 
from tkinter import messagebox
import random
import pyperclip
#TODO change the file format where the passwords are saved to something more secure 
#like a csv then encrypt it or something (a little ambetious but not impossible) 
#TODO give varaibles better names please    
LABEL_FONT = ("Arial",14,'bold')
app = tk.Tk()
app.title("PassWord Manager")
app.config(padx=20,pady=20)
canvas = tk.Canvas(app,width=200,height=220,highlightthickness=0)
lock_image = tk.PhotoImage(file='logo.png')
canvas.create_image(100,110,image=lock_image)
canvas.grid(column=1,row=0)

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    password_list += [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]

    random.shuffle(password_list)

    password = "".join(password_list)

    #now we take the password to the clipboard and to the password entry 
    input_3.delete(0,tk.END)
    input_3.insert(tk.END,password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_info(website,user,password):
        if len(website) == 0 or len(user) == 0 or len(password) == 0:
            messagebox.showwarning(title="Missing!!",message="One or more of the fields is empty.\n Try again")
            input_1.delete(0,tk.END)
            input_2.delete(0,tk.END) #remove this if you want to put placeholder email
            input_3.delete(0,tk.END)
            return
        #messagebox proceed? plus success
        is_ok = messagebox.askokcancel(title=website,message=f"These are you email and password for this website:\nEmail: {user}\nPassword: {password}")
        if is_ok:
            with open('passwords.txt','a') as file: 
                file.write(f"{website} | {user} | {password}\n")
            messagebox.showinfo("showinfo", "Password was saved successfully") 
            input_1.delete(0,tk.END)
            input_2.delete(0,tk.END) #remove this if you want to put placeholder email
            input_3.delete(0,tk.END)
        else:
            messagebox.showinfo("showinfo", "Canceled") 
            input_1.delete(0,tk.END)
            input_2.delete(0,tk.END) #remove this if you want to put placeholder email
            input_3.delete(0,tk.END)

# ---------------------------- Display PASSWORDS ------------------------------- #
#TODO add some editing capabilities to this window 
#editing passwords usernamenames/emails and webiste names 
#maybe a delete button 

def display():
    with open('passwords.txt','r') as file:
        root = tk.Tk()
        root.config(padx=20,pady=20)
        root.geometry('600x500')
        count = 0
        for line in file.readlines(): 
            # label_info = tk.Label(root,text=line,font=("Arial",20,'bold'))
            # label_info.pack()
            text_pass = tk.Text(root,height=2,borderwidth=0,font=("Arial",15),bg='white')
            text_pass.insert(1.0,line)
            text_pass.pack()
            text_pass.config(state='disabled')
        root.mainloop()

# ---------------------------- UI SETUP ------------------------------- #
#taking website name
label_1 = tk.Label(text='Website:',font=LABEL_FONT)
label_1.grid(column=0,row=1)
input_1 = tk.Entry(width=70)
input_1.grid(column=1,row=1,columnspan=2,sticky="W")
input_1.focus()
#taking userinfo
label_2 = tk.Label(text='Email/Username:',font=LABEL_FONT)
label_2.grid(column=0,row=2)
input_2 = tk.Entry(width=70)
input_2.grid(column=1,row=2,columnspan=2,sticky="W")
#either user inputs password or presses generate button
label_3 = tk.Label(text='Password:',font=LABEL_FONT)
label_3.grid(column=0,row=3)
input_3 = tk.Entry(width=45)
input_3.grid(column=1,row=3,sticky="W")

generator_button = tk.Button(text="Generate Password",width=20,command=generate_password)
generator_button.grid(column=2,row=3,sticky="W")

add_button = tk.Button(text="Add",width=60,command=lambda: save_info(input_1.get(),input_2.get(),input_3.get()))
add_button.grid(column=1,row=4,sticky="W",columnspan=2)
add_button = tk.Button(text="Show Shaved Passwords",width=60,command=display)
add_button.grid(column=1,row=5,sticky="W",columnspan=2)
app.mainloop()