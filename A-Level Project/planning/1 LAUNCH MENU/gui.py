from tkinter import *
import winsound

class LaunchWindow(Tk):
    def __init__(self):
        super().__init__()
        self.WIDTH,self.HEIGHT=1280,720
        self.title('Tank Game Launcher')
        self.geometry('1280x720+0+0')
        self.minsize(320,180)
        self.config(bg='white')
        #self.iconbitmap('assets//jack.ico')
        mediumFont=('Calibri Light',12)
        inputFont=('Calibri Light',10)
        self.usernameLabel=Label(text='Username',font=mediumFont)
        self.usernameEntry=Entry(fg='black',bg='white',font=inputFont)
        self.passwordLabel=Label(text='Password',font=mediumFont)
        self.passwordEntry=Entry(fg='black',bg='white',show='•',font=inputFont) 
        # relx = relx - 1/2 of relwidth
        # rely = rely - 1/2 of relheight
        self.usernameLabel.place(relx=7/16,rely=7/40,relwidth=1/8,relheight=1/30)
        self.usernameEntry.place(relx=7/16,rely=9/40,relwidth=1/8,relheight=1/20)
        self.passwordLabel.place(relx=7/16,rely=27/40,relwidth=1/8,relheight=1/30)
        self.passwordEntry.place(relx=7/16,rely=29/40,relwidth=1/8,relheight=1/20)


        self.update()
    def update(self):
        self.UpdateFontSize(self.usernameLabel,mediumFont)
        self.UpdateFontSize(self.passwordLabel,mediumFont)
        self.after(1000,self.update)

    def UpdateFontSize(self,label,font):
        width=self.winfo_width()
        fontName,fontSize=font
        fontSize=round((fontSize/1280)*width)
        label.config(font=(fontName,fontSize))
window=LaunchWindow()
window.mainloop()