import Tkinter as tk
import vault_manager
import os
import ttk
import cryptography
import sys
import glob
import serial
import time


class GUI(tk.Tk):
    def __init__(self, mv,md):
        tk.Tk.__init__(self)

        self.welcome = Welcome(self, mv,md)
        self.welcome.pack(fill=tk.BOTH, expand=True)
        self.signup = SignUp(self, mv,md)
        self.login = Login(self, mv,md)
        self.connect = Connect(self, mv,md)
        self.vault = vault_manager.Vault(self, mv)
        self.vault_screen = VaultScreen(self,mv)
        self.title('BioLock')
        self.geometry('960x820')
        icon = tk.PhotoImage(file='graphics/icon.gif')
        self.tk.call('wm', 'iconphoto', self._w, icon)
        self.minsize(width=800, height=800)
        self.protocol('WM_DELETE_WINDOW',lambda: self.on_closing(md))


    def set_welcome(self, _):
        self.signup.pack_forget()
        self.login.pack_forget()
        self.vault_screen.pack_forget()
        self.connect.pack_forget()
        self.welcome.pack(fill=tk.BOTH, expand=True)

    def set_signup(self, _):
        self.welcome.pack_forget()
        self.signup.pack(fill=tk.BOTH, expand=True)

    def set_login(self, _):
        self.welcome.pack_forget()
        self.login.pack(fill=tk.BOTH, expand=True)

    def set_vault(self):
        self.login.pack_forget()
        self.vault_screen.pack(fill=tk.BOTH, expand=True)

    def set_connect(self, _):
        self.welcome.pack_forget()
        self.connect.pack(fill=tk.BOTH, expand=True)

    def on_closing(self,md):
        if md.open:
            md.close()
        self.destroy()


class Welcome(tk.Frame):
    def __init__(self, root, mv,md):

        #create frame
        tk.Frame.__init__(self, root, bg="#bbeaff")

        #create logo
        self.img = tk.PhotoImage(file="graphics/biolock.gif")
        self.logo = tk.Label(self, image=self.img, bg="#bbeaff")

        #create buttons
        self.newBtn = ButtonBL(self, bg="#bbeaff", w=300, h=100, r=100, color="#00afff", hover_color="#5ab7e2",
                                      press_color="#97d8f6", command=lambda x: self.signup(md,root), text="New Vault")
        self.enterBtn = ButtonBL(self, bg="#bbeaff", w=300, h=100, r=100, color="#00afff", hover_color="#5ab7e2",
                                        press_color="#97d8f6", command=lambda x: self.login(md,root), text="Enter Vault")
        self.connectBtn = ButtonBL(self, bg="#bbeaff", w=300, h=100, r=100, color="#00afff", hover_color="#5ab7e2",
                                 press_color="#97d8f6", command=root.set_connect, text="Device")


    def pack(self, **kwargs):
        tk.Frame.pack(self, **kwargs)
        self.logo.pack(side=tk.TOP, pady=(150, 0))
        self.connectBtn.pack(side=tk.TOP, pady=(40, 0))
        self.enterBtn.pack(side=tk.TOP, pady=(10,0))
        self.newBtn.pack(side=tk.TOP, pady=10)

    def login(self,md,root):
        if md.open:
            root.set_login('')

    def signup(self,md,root):
        if md.open:
            root.set_signup('')


class ButtonBL(tk.Canvas):
    def __init__(self, root, bg, w=0, h=0, r=20, color='red', hover_color='blue', press_color='green', command=lambda: None, text="",font="TkDefaultFont 30",fg="white", enabled=True):
        tk.Canvas.__init__(self, root, width=w, height=h,bg=bg,highlightthickness=0)

        self.button_parts = [
            self.create_arc(0, 0, r, r, start=90, extent=90),
            self.create_arc(w - r, 0, w, r, start=0, extent=90),
            self.create_arc(0, h - r, r, h, start=180, extent=90),
            self.create_arc(w - r, h - r, w, h, start=270, extent=90),
            self.create_rectangle(r / 2, 0, w - r / 2, h),
            self.create_rectangle(0, r / 2, w, h - r / 2)
        ]
        self.set_color(color)
        self.create_text(w/2,h/2,font=font,text=text,fill=fg)

        self.color, self.hover_color, self.press_color = color, hover_color, press_color
        self.command = command
        self.set_bindings()

        self.enabled = True
        if not enabled: self.disable()

    def set_color(self, color):
        for i in self.button_parts: self.itemconfig(i, fill=color, outline=color)

    def set_bindings(self):
        self.bind('<Enter>', lambda event: self.set_color(self.hover_color))
        self.bind('<Leave>', lambda event: self.set_color(self.color))

        self.bind('<Button-1>', lambda event: self.set_color(self.press_color))
        self.bind('<ButtonRelease-1>', self.command)

    def disable(self):
        if not self.enabled: return
        self.enabled = False
        self.set_color('#AAAAAA')
        for b in ['<Button-1>', '<ButtonRelease-1>', '<Enter>', '<Leave>']: self.unbind(b)

    def enable(self):
        if self.enabled: return
        self.enabled= True
        self.set_color(self.color)
        self.set_bindings()


class SignUp(tk.Frame):
    def __init__(self, root, mv,md):
        tk.Frame.__init__(self, root, bg="#bbeaff")

        self.logoImg = tk.PhotoImage(file="graphics/biolock.gif")
        self.logo = tk.Label(self, image=self.logoImg, bg="#bbeaff")

        self.f1 = tk.Frame(self, bg="#bbeaff")

        self.e1 = tk.Entry(self.f1, font="TkDefaultFont 18")





        self.t1 = tk.Label(self.f1, text="Vault Name: ", font="TkDefaultFont 18", bg="#bbeaff", justify="left")

        self.var = tk.IntVar()


        self.createBtn = ButtonBL(self, bg="#bbeaff", w=200, h=50, r=50, color="#00afff", hover_color="#5ab7e2",
                                         press_color="#97d8f6", command=lambda x: self.goEntry(md), text="Create Vault",
                                         font="TkDefaultFont 20")

        self.homeImg = tk.PhotoImage(file="graphics/home.gif").subsample(2, 2)
        self.homeBtn = ButtonBL(self, bg="#bbeaff", w=70, h=70, r=20, color="#00afff", hover_color="#5ab7e2",
                                       press_color="#97d8f6", command=root.set_welcome)
        self.homeBtn.create_image(35, 35, image=self.homeImg)
        self.f2 = tk.Frame(self, bg="#bbeaff")
        self.label = tk.Label(self.f2, text='Enter Vault name', bg="#bbeaff", font="TkDefaultFont 20")

    def pack(self, **kwargs):

        tk.Frame.pack(self, **kwargs)
        self.logo.pack(side=tk.TOP, pady=(150, 0))
        self.f1.pack(pady=(90, 0))

        self.t1.pack(side=tk.LEFT)

        self.e1.pack(side=tk.RIGHT)
        self.f2.pack()
        self.label.pack()
        self.createBtn.pack(pady=(20, 0))
        self.homeBtn.pack(anchor=tk.SW, side=tk.BOTTOM, padx=(10, 0), pady=(0, 10))

    def goEntry(self,md):
        stri = self.e1.get()
        if self.valid_input(stri):
            if stri not in [f[:-5] for f in os.listdir(os.getcwd()) if f.endswith('.blvf')]:
                self.label.config(text='Please press finger')
                self.label.update()
                md.led_on()
                while not md.is_press_finger():
                    time.sleep(0.5)
                exists = md.exists()
                if exists:
                    self.label.config(text='Finger is already scanned. Vault created.')
                    self.usekey(md)



                else:
                    self.label.config(text='Remove finger')
                    self.label.update()
                    while md.is_press_finger():
                        time.sleep(0.5)
                    self.label.config(text='Press finger')
                    self.label.update()
                    while not md.is_press_finger():
                        time.sleep(0.5)
                    md.enroll_start()
                    md.enroll1()
                    self.label.config(text='Remove finger')
                    self.label.update()
                    while md.is_press_finger():
                        time.sleep(0.5)
                    self.label.config(text='Press finger')
                    self.label.update()
                    while not md.is_press_finger():
                        time.sleep(0.5)
                    md.enroll2()
                    self.label.config(text='Remove finger')
                    self.label.update()
                    while md.is_press_finger():
                        time.sleep(0.5)
                    self.label.config(text='Press finger')
                    self.label.update()
                    while not md.is_press_finger():
                        time.sleep(0.5)
                    time.sleep(0.5)
                    successful = md.enroll3()
                    if successful:
                        self.usekey(md)
                        self.label.config(text='Remove finger')
                        self.label.update()
                        while md.is_press_finger():
                            time.sleep(0.5)

                        self.label.config(text='Finger captured')
                        self.label.update()
                    else:
                        self.label.config(text='Scan failed. Try again')
                        self.label.update()
            else:
                self.label.config(text='A vault with this name already exists')
                self.label.update()
        else:
            self.label.config(text='Invalid input')
            self.label.update()







    def usekey(self,md):
        stri = self.e1.get()
        newVault = vault_manager.Vault([], stri)
        s = md.identify()
        newVault.lock(s)
        newVault.key = s

    def valid_input(self,user_input):
        for c in user_input:
            if c in '\/*?"<>|':
                return False
        return len(user_input) > 0


class Login(tk.Frame):
    def __init__(self, root, mv,md):
        tk.Frame.__init__(self, root, bg="#bbeaff")
        self.logoImg = tk.PhotoImage(file="graphics/biolock.gif")
        self.logo = tk.Label(self, image=self.logoImg, bg="#bbeaff")
        self.f1 = tk.Frame(self, bg="#bbeaff")
        self.str = tk.StringVar()
        self.str.set("Choose Vault")
        self.menu = ttk.Combobox(self.f1, textvariable=self.str,
                                 width=22, font="TkDefaultFont 14")
        self.menu.option_add("*Font", "TkDefaultFont 18")

        self.t1 = tk.Label(self.f1, text="Vault Name: ", font="TkDefaultFont 18", bg="#bbeaff", justify="left")
        self.openBtn = ButtonBL(self, bg="#bbeaff", w=200, h=50, r=50, color="#00afff", hover_color="#5ab7e2",
                                       press_color="#97d8f6", command= lambda(_): self.verify(root,mv,md), text="Open Vault",
                                       font="TkDefaultFont 20")
        self.img = tk.PhotoImage(file="graphics/home.gif").subsample(2, 2)
        self.homeBtn = ButtonBL(self, bg="#bbeaff", w=70, h=70, r=20, color="#00afff", hover_color="#5ab7e2",
                                       press_color="#97d8f6", command=root.set_welcome)
        self.homeBtn.create_image(35, 35, image=self.img)
        self.f2 = tk.Frame(self, bg="#bbeaff")
        self.label = tk.Label(self.f2, text='Choose vault', bg="#bbeaff")

    def pack(self, **kwargs):
        tk.Frame.pack(self, **kwargs)
        self.logo.pack(side=tk.TOP, pady=(150, 0))
        self.f1.pack()
        self.t1.pack(side=tk.LEFT)
        self.menu.pack_forget()
        self.menu = ttk.Combobox(self.f1, textvariable=self.str, values=[f[:-5] for f in os.listdir(os.getcwd()) if f.endswith('.blvf')],
                                 width=22, font="TkDefaultFont 14")
        self.menu.option_add("*Font", "TkDefaultFont 18")
        self.menu.pack(side=tk.RIGHT)
        self.openBtn.pack(pady=(20, 0))
        self.f2.pack()
        self.label.pack()
        self.homeBtn.pack(anchor=tk.SW, side=tk.BOTTOM, padx=(10, 0), pady=(0, 10))



    def verify(self,root,mv,md):

        user_input = self.menu.get()
        if user_input in [f[:-5] for f in os.listdir(os.getcwd()) if f.endswith('.blvf')]:
            vault_path = user_input + ".blvf"
            vault_file = open(vault_path, "r")
            self.label.config(text='Please press finger')
            self.label.update()
            md.led_on()
            while not md.is_press_finger():
                time.sleep(0.5)
            v = md.identify()
            mv.update_name(user_input)
            mv.key = v

            if mv.try_unlock(v):
                mv.unlock(v)
                root.vault_screen.makeTree(mv)
                root.set_vault()
            md.led_off()
        else:
            self.label.config(text='Invalid input')
            self.label.update()


class Connect(tk.Frame):
    def __init__(self, root, mv,md):
        tk.Frame.__init__(self, root, bg="#bbeaff")
        self.logoImg = tk.PhotoImage(file="graphics/biolock.gif")
        self.logo = tk.Label(self, image=self.logoImg, bg="#bbeaff")
        self.f1 = tk.Frame(self, bg="#bbeaff")
        self.str = tk.StringVar()
        self.str.set("Choose port")
        self.menu = ttk.Combobox(self.f1, textvariable=self.str, width=22, font="TkDefaultFont 14")
        self.menu.option_add("*Font", "TkDefaultFont 18")
        self.t1 = tk.Label(self.f1, text="Port: ", font="TkDefaultFont 18", bg="#bbeaff", justify="left")
        self.open_button = ButtonBL(self, bg="#bbeaff", w=200, h=50, r=50, color="#00afff", hover_color="#5ab7e2",
                                    press_color="#97d8f6", command=lambda x: self.ok(md), text="Connect",
                                    font="TkDefaultFont 20")
        self.close_button = ButtonBL(self, bg="#bbeaff", w=200, h=50, r=50, color="#00afff", hover_color="#5ab7e2",
                                    press_color="#97d8f6", command=lambda x: self.close(md), text="Disconnect",
                                    font="TkDefaultFont 20")
        self.img = tk.PhotoImage(file="graphics/home.gif").subsample(2, 2)
        self.home_button = ButtonBL(self, bg="#bbeaff", w=70, h=70, r=20, color="#00afff", hover_color="#5ab7e2",
                                    press_color="#97d8f6", command=root.set_welcome)
        self.home_button.create_image(35, 35, image=self.img)
        self.f2 = tk.Frame(self, bg="#bbeaff")
        self.label = tk.Label(self.f2, text='please connect', bg="#bbeaff")
        self.connected = False
        self.port = None

    def pack(self, **kwargs):
        tk.Frame.pack(self, **kwargs)
        self.logo.pack(side=tk.TOP, pady=(150, 0))
        self.f1.pack()
        self.t1.pack(side=tk.LEFT)
        self.menu.pack_forget()
        self.menu = ttk.Combobox(self.f1, textvariable=self.str, values=self.serial_ports(),
                                 width=22, font="TkDefaultFont 14")
        self.menu.option_add("*Font", "TkDefaultFont 18")
        self.menu.pack(side=tk.RIGHT)
        self.f2.pack()
        self.label.pack()
        self.open_button.pack(pady=(20, 0))
        self.close_button.pack(pady=(10, 0))
        self.home_button.pack(anchor=tk.SW, side=tk.BOTTOM, padx=(10, 0), pady=(0, 10))

    def serial_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result


    def ok(self, md):
        if not self.connected:
            p = self.menu.get()
            if p == 'Choose port':
                self.label.config(text='Choose a port before trying to connect')
                self.label.update()
            elif p in self.serial_ports():
                self.label.config(text='connecting to: ' + p)
                self.label.update()
                md.start(port=p)
                self.connected = True
                self.port = p
                self.label.config(text='connected to ' + p)
            else:
                self.label.config(text='Invalid input')
                self.label.update()
        else:
            self.label.config(text='Please disconnect from %s before connecting' %self.port)
            self.label.update()
    def close(self, md):
        if self.connected:
            self.label.config(text='disconnecting from: ' + self.port)
            self.label.update()
            md.close()
            self.connected = False
            self.port = None
        self.label.config(text='please connect')


class VaultScreen(tk.Frame):
    def __init__(self, master, mv):
        tk.Frame.__init__(self, master, bg="#bbeaff")

        self.mv = mv
        self.master = master

        self.tree = ttk.Treeview(self, show='headings', selectmode=tk.BROWSE)
        self.tree['columns'] = ['b', 'c', 'd']
        self.tree.heading('b', text='Title')
        self.tree.heading('c', text='Username')
        self.tree.heading('d', text='Password')


        self.sidebar = tk.Frame(self, bg='#bbeaff')
        self.sidebar.pack(fill=tk.BOTH, side=tk.LEFT)

        self.new_entry = ButtonBL(self.sidebar, bg="#bbeaff", w=330, h=70, r=20, color="#00afff",
                                  hover_color="#5ab7e2",
                                  press_color="#97d8f6", command=lambda event: EntryPopup(self, 'New Entry'),
                                  text="New Entry")
        self.edit_entry = ButtonBL(self.sidebar, bg="#bbeaff", w=330, h=70, r=20, color="#00afff",
                                   hover_color="#5ab7e2",
                                   press_color="#97d8f6",
                                   command=lambda event: EntryPopup(self, 'Edit Entry', True),
                                   text="Edit Entry")
        self.delete_entry = ButtonBL(self.sidebar, bg="#bbeaff", w=330, h=70, r=20, color="#00afff",
                                     hover_color="#5ab7e2",
                                     press_color="#97d8f6", command=self.deleteEntry, text="Delete Entry")

        self.copyTitle = ButtonBL(self.sidebar, bg="#bbeaff", w=330, h=70, r=20, color="#00afff",
                                  hover_color="#5ab7e2",
                                  press_color="#97d8f6", command=self.copytitle, text="Copy Title")
        self.copyUsername = ButtonBL(self.sidebar, bg="#bbeaff", w=330, h=70, r=20, color="#00afff",
                                     hover_color="#5ab7e2",
                                     press_color="#97d8f6", command=self.copyusername, text="Copy Username")
        self.copyPassword = ButtonBL(self.sidebar, bg="#bbeaff", w=330, h=70, r=20, color="#00afff",
                                     hover_color="#5ab7e2",
                                     press_color="#97d8f6", command=self.copypassword, text="Copy Password")
        self.lock = ButtonBL(self.sidebar, bg="#bbeaff", w=330, h=70, r=20, color="#00afff",
                             hover_color="#5ab7e2",
                             press_color="#97d8f6", command=self.locksave, text="Lock")

    def deleteEntry(self, _):
        if self.tree.selection():
            a = self.tree.item(self.tree.selection()[0], 'values')[0]
            b = self.tree.item(self.tree.selection()[0], 'values')[1]
            c = self.tree.item(self.tree.selection()[0], 'values')[2]
            ent = vault_manager.Entry(a, b, c)
            self.mv.remove(ent)
            self.update_tree(self.mv)

    def copytitle(self, _):
        if self.tree.selection():
            cryptography.copyToClipboard(self.tree.item(self.tree.selection()[0], 'values')[0])

    def copyusername(self, _):
        if self.tree.selection():
            cryptography.copyToClipboard(self.tree.item(self.tree.selection()[0], 'values')[1])

    def copypassword(self, _):
        if self.tree.selection():
            cryptography.copyToClipboard(self.tree.item(self.tree.selection()[0], 'values')[2])

    def locksave(self, _):
        self.mv.lock(self.mv.key)
        self.mv.entry_list = []
        self.tree.delete(*self.tree.get_children())
        self.master.set_welcome("k")


    def pack(self, **kwargs):
        tk.Frame.pack(self, **kwargs)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.new_entry.pack(pady=(60, 5), padx=7)
        self.edit_entry.pack(pady=5, padx=7)
        self.delete_entry.pack(pady=5, padx=7)
        self.copyTitle.pack(pady=5, padx=7)
        self.copyUsername.pack(pady=5, padx=7)
        self.copyPassword.pack(pady=5, padx=7)
        self.lock.pack(pady=5, padx=7)

    def makeTree(self, mv):
        for i in mv.entry_list:
            self.tree.insert('', tk.END, values=(i.title, i.username, i.password))

    def update_tree(self, mv):
        self.tree.delete(*self.tree.get_children())
        self.makeTree(mv)


    def insert_entry(self, title, un, pw, edit_selected=False):
        if not edit_selected:
            # self.tree.insert('', tk.END, values=(title, un, pw))
            self.mv.insert(vault_manager.Entry(title, un, pw))
            self.update_tree(self.mv)
            return
        old_e = vault_manager.Entry(*self.tree.item(self.tree.selection()[0], 'values'))
        new_e = vault_manager.Entry(title, un, pw)
        self.mv.edit(old_e, new_e)
        self.tree.item(self.tree.selection()[0], values=(title, un, pw))


class EntryPopup(tk.Toplevel):
    def __init__(self, master, title, edit=False): #(t, un, pw)=(None, None, None)
        tk.Toplevel.__init__(self, master)
        if self.master.tree.selection() or not edit:
            self.master = master
            self.title(title)
            self.geometry('400x150')
            self.resizable(width=False, height=False)
            self.bind_all('<Return>', self.okpressed)
            self.config(bg='#bbeaff')
            self.edit = edit

            frame = tk.Frame(self, bg="#bbeaff")
            entries = tk.Frame(frame, bg="#bbeaff")
            labels = tk.Frame(frame, bg="#bbeaff")
            buttons = tk.Frame(self, bg="#bbeaff")

            self.e_title = tk.Entry(entries, font="TkDefaultFont 18")
            tk.Label(labels, text="Title:", font="TkDefaultFont 18", bg="#bbeaff", anchor=tk.E).pack(fill=tk.X)

            self.e_username = tk.Entry(entries, font="TkDefaultFont 18")
            tk.Label(labels, text="Username:", font="TkDefaultFont 18", bg="#bbeaff", anchor=tk.E).pack(fill=tk.X)

            self.e_password = tk.Entry(entries, font="TkDefaultFont 18")
            tk.Label(labels, text="Password:", font="TkDefaultFont 18", bg="#bbeaff", anchor=tk.E).pack(fill=tk.X)


            if edit:
                t,un,pw = self.master.tree.item(self.master.tree.selection()[0], 'values')

                self.e_title.insert(0, t)
                self.e_username.insert(0, un)
                self.e_password.insert(0, pw)

            tk.Button(buttons, text="Cancel", command=self.destroy).pack(side=tk.RIGHT, padx=2)
            tk.Button(buttons, text="OK", command=self.okpressed).pack(side=tk.RIGHT, padx=2)

            frame.pack(pady=5)
            entries.pack(side=tk.RIGHT, fill=tk.BOTH)
            labels.pack(side=tk.LEFT, fill=tk.BOTH)

            self.e_title.pack()
            self.e_title.focus_force()
            self.e_username.pack()
            self.e_password.pack()
            buttons.pack(fill=tk.X)
        else:
            self.destroy()

    def okpressed(self, _=None):
        self.master.insert_entry(self.e_title.get(), self.e_username.get(), self.e_password.get(), self.edit)
        self.destroy()
