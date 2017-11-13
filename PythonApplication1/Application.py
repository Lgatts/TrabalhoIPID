import tkinter as tk
from tkinter import *
from tkinter import filedialog

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        #Botão de escolha de imagem
        self.fileChooserButton = tk.Button(self)
        self.fileChooserButton["text"] = "Choose File"
        self.fileChooserButton["command"] = self.fileChooserButtonClick
        self.fileChooserButton.pack(side="top")
     
        #canvas onde é mostrada a imagem e onde se pode desenhar
        self.canvas = Canvas(self.master)        
        self.canvas.pack(expand = YES, fill = BOTH)
        self.canvas.bind( "<B1-Motion>", self.paint )

    def fileChooserButtonClick(self):
        filename = filedialog.askopenfilename(initialdir = "./images",title = "Select Image",filetypes = (("Valid formats","*.png;*gif"),("all files","*.*")))
        self.loadImage(filename)

    def loadImage(self,filename):
        self.img = tk.PhotoImage(file=filename)
        self.canvas["width"] = self.img.width()
        self.canvas["height"] = self.img.height()
        self.canvas.create_image(0,0,anchor=NW,image=self.img)        
        
    def paint(self, event ):
        python_green="#604a42"
        #python_green = "#476042"
        x1, y1 = ( event.x - 1 ), ( event.y - 1 )
        x2, y2 = ( event.x + 1 ), ( event.y + 1 )
        self.canvas.create_oval( x1, y1, x2, y2, fill = python_green )

 
root = tk.Tk()
app = Application(master=root)
app.mainloop()
