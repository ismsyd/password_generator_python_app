import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Treeview,Scrollbar
import random,json
import pyperclip
FILE_NAME = "data.json"
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
    input_password.delete(0, tk.END)
    input_password.insert(tk.END, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_info(website,user,password):
        if len(website) == 0 or len(user) == 0 or len(password) == 0:
            messagebox.showwarning(title="Missing!!",message="One or more of the fields is empty.\n Try again")
            input_website.delete(0, tk.END)
            input_user.delete(0, tk.END) #remove this if you want to put placeholder email
            input_password.delete(0, tk.END)
            return
        #messagebox proceed? plus success
        is_ok = messagebox.askokcancel(title=website,message=f"These are you email and password for this website:\nEmail: {user}\nPassword: {password}")

        info_dict = {
            website: {
                'email': user,
                'password': password,
            }
        }
        if is_ok:
            try:
                with open(FILE_NAME,'r') as file:
                    data = json.load(file)
                    data.update(info_dict)
                with open(FILE_NAME,'w') as file:
                    json.dump(data,file,indent=4)
            except json.decoder.JSONDecodeError,FileNotFoundError:
                with open(FILE_NAME,'w') as file:
                    json.dump(info_dict,file,indent=4)
            finally:
                messagebox.showinfo("showinfo", "Password was saved successfully")
                input_website.delete(0, tk.END)
                input_user.delete(0, tk.END) #remove this if you want to put placeholder email
                input_password.delete(0, tk.END)
        else:
            messagebox.showinfo("showinfo", "Canceled")
            input_website.delete(0, tk.END)
            input_user.delete(0, tk.END) #remove this if you want to put placeholder email
            input_password.delete(0, tk.END)

# ---------------------------- Search PASSWORDS ------------------------------- #
def search(website):
    #read file check arg with webname from json.load
    try:
        with open(FILE_NAME,'r') as file:
            data = json.load(file)
            finding = data[website]
            message_output = f"Website: {website}\nUsername/Email: {finding['email']}\nPassword: {finding['password']}"
            messagebox.showinfo(message=message_output)
            return message_output
    except KeyError:
        messagebox.showerror(message="Website not found\nTry again...")
    except json.JSONDecodeError,FileNotFoundError:
        with open(FILE_NAME,'w') as file:
            choice = messagebox.askokcancel(title=f"{FILE_NAME} is missing or empty",message=f"No File {FILE_NAME} was found.\n Save ?")
            if choice:
                save_info(input_website.get(),input_user.get(),input_password.get())
            else:
                messagebox.showinfo(message="Quiting")
                input_website.delete(0, tk.END)
                input_user.delete(0, tk.END)  # remove this if you want to put placeholder email
                input_password.delete(0, tk.END)
# ---------------------------- Display PASSWORDS ------------------------------- #
#TODO add some editing capabilities to this window
#editing passwords usernamenames/emails and webiste names
#maybe a delete button
#TODO change from the txt to json
def change_data_formate():
    '''goes into data.json '''
    try:
        file = open(FILE_NAME,'r')
    except FileNotFoundError as e:
        messagebox.showerror(title='No info' ,message=f"No information was found try adding something")

    else:
        data_b = json.load(file) #b for before changing it
        data_a = [] # a for after change
        for web_name in data_b.keys():
            tpl = (web_name,data_b[web_name]['email'],data_b[web_name]['password'])
            data_a.append(tpl)
        return data_a



def display():
    root = tk.Tk()
    root.config(padx=20, pady=20)
    root.geometry('600x500')
    #TODO create scroll bar object
    #create table widget
    user_info_table = Treeview(root) #using ttk
    #define columns
    user_info_table['columns'] = ('Website','Email/Username','Password')
    #Format columns
    user_info_table.column('#0', width=0, stretch=tk.NO)
    user_info_table.column('Website', anchor=tk.W, width=150)
    user_info_table.column('Email/Username', anchor=tk.W, width=200)
    user_info_table.column('Password', anchor=tk.W, width=150)
    #Create headings
    user_info_table.heading('#0', text='', anchor=tk.W)
    user_info_table.heading('Website', text='Name', anchor=tk.W)
    user_info_table.heading('Email/Username', text='Email/Username', anchor=tk.W)
    user_info_table.heading('Password', text='Password', anchor=tk.W)
    data = change_data_formate()
    user_info_table.tag_configure('oddrow', background='#E8E8E8')
    user_info_table.tag_configure('evenrow', background='#FFFFFF')
    # Add data with alternating row colors
    for i in range(len(data)):
        if i % 2 == 0:
            user_info_table.insert(parent='', index=i, values=data[i], tags=('evenrow',))
        else:
            user_info_table.insert(parent='', index=i, values=data[i], tags=('oddrow',))
    # Pack the table
    user_info_table.pack(expand=True, fill=tk.BOTH)
    root.mainloop()

# ---------------------------- UI SETUP ------------------------------- #
#taking website name
label_website = tk.Label(text='Website:', font=LABEL_FONT)
label_website.grid(column=0, row=1)
input_website = tk.Entry(width=50)
input_website.grid(column=1, row=1, columnspan=1, sticky="W")
input_website.focus()
search_button = tk.Button(text="Search",width=15,command=lambda : search(input_website.get()))
search_button.grid(column=2,row=1)
#taking userinfo
label_user = tk.Label(text='Email/Username:', font=LABEL_FONT)
label_user.grid(column=0, row=2)
input_user = tk.Entry(width=70)
input_user.grid(column=1, row=2, columnspan=3, sticky="W")
#either user inputs password or presses generate button
label_password = tk.Label(text='Password:',font=LABEL_FONT)
label_password.grid(column=0,row=3)
input_password = tk.Entry(width=50)
input_password.grid(column=1, row=3, sticky="W")

generator_button = tk.Button(text="Generate Password",width=15,command=generate_password)
generator_button.grid(column=2,row=3)

add_button = tk.Button(text="Add", width=60, command=lambda: save_info(input_website.get(), input_user.get(), input_password.get()))
add_button.grid(column=1,row=4,sticky="W",columnspan=2)
show_button = tk.Button(text="Show Shaved Passwords",width=60,command=display)
show_button.grid(column=1,row=5,sticky="W",columnspan=2)
app.mainloop()