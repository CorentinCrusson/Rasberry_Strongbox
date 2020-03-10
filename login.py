from tkinter import *
from functools import partial
from main import *


def validateLogin(username, password):
    return username, password


# window
def createWindow():

    tkWindow = Tk()
    tkWindow.geometry('400x150')
    tkWindow.title('Tkinter Login Form - pythonexamples.org')

    # username label and text entry box
    usernameLabel = Label(tkWindow, text="User Name").grid(row=0, column=0)
    username = StringVar()
    usernameEntry = Entry(
        tkWindow, textvariable=username).grid(row=0, column=1)

    # password label and password entry box
    passwordLabel = Label(tkWindow, text="Password").grid(row=1, column=0)
    password = StringVar()
    passwordEntry = Entry(tkWindow, textvariable=password,
                          show='*').grid(row=1, column=1)

    validateLogin = partial(validateLogin, username, password)

    # login button
    loginButton = Button(tkWindow, text="Login",
                         command=validateLogin).grid(row=4, column=0)

    tkWindow.mainloop()
