import tkinter as tk
from tkinter import *
from tkinter import filedialog
import math

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
     
        #Botão de escolha de imagem
        self.classifyButton = tk.Button(self)
        self.classifyButton["text"] = "Classify"
        self.classifyButton["command"] = self.classifyButtonClick
        self.classifyButton.pack(side="bottom")

        #canvas onde é mostrada a imagem e onde se pode desenhar
        self.canvas = Canvas(self.master)        
        self.canvas.pack(expand = YES, fill = BOTH)
        #chamada da função de desenhar na tela
        self.canvas.bind("<ButtonPress-1>", self.onMouseLeftClickPress)
        self.canvas.bind("<B1-Motion>", self.onMouseMove)
        self.canvas.bind("<ButtonRelease-1>", self.onMouseLeftClickRelease)
        
        #Variaveis necessarias para a criação do retângulo
        self.x = 0
        self.y = 0
        self.rect = None
        self.startX = None
        self.startY = None   
       
        self.userClasses = []
        self.classCount = 1
       
        self.colors = {0 : "#000000",
           1 : "#0B840D",
           2 : "#E8AE0C",
           3 : "#14A1E8"}

    #Escolha do arquivo de imagem, deve ser png ou gif
    def fileChooserButtonClick(self):
        filename = filedialog.askopenfilename(initialdir = "./images",title = "Select Image",filetypes = (("Valid formats","*.png;*gif"),("all files","*.*")))
        if filename != "" :
            self.loadImage(filename)
            
    #Função que carrega a imagem para o canvas e redimensiona o mesmo de acordo
    #com o tamanho da imagem
    def loadImage(self,filename):
        self.img = tk.PhotoImage(file=filename)
        self.canvas["width"] = self.img.width()
        self.canvas["height"] = self.img.height()
        self.canvas.create_image(0,0,anchor=NW,image=self.img)        
    
    #função de leitura do click do mouse
    def onMouseLeftClickPress(self, event):
        # salva o ponto inicial de onde o mouse começou a ser arrastado
        self.startX = event.x
        self.startY = event.y

       #cria um retangulo se esse já não existir
        self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline="red", width=2)

    #função de movimento do mouse enquanto o mouse estiver precionado
    def onMouseMove(self, event):
        curX, curY = (event.x, event.y)

        #vai aumentando o retangulo conforme se arrasta o mouse
        self.canvas.coords(self.rect, self.startX, self.startY, curX, curY)

    #função de leitura da liberação do click do mouse
    def onMouseLeftClickRelease(self, event):

        userClass = {"Rectangle" : None,
                     "Color" : None,
                     "Rgb" : None}

        userClass["Rectangle"] = self.rect
        userClass["Color"] = self.colors[self.classCount]
        userClass["Rgb"] = None
        self.userClasses.append(userClass)
        self.classCount += 1        
        pass

    #Função que faz a classificação da imagem
    def classifyButtonClick(self):

        r = 0
        g = 0
        b = 0
        total = 0       

        if len(self.userClasses) > 0 :
            for userClass in self.userClasses:
                rectCoords = self.canvas.coords(userClass["Rectangle"])
                for i in range(int(rectCoords[0]),int(rectCoords[2])):
                    for j in range(int(rectCoords[1]),int(rectCoords[3])):
                        rgb = self.img.get(i,j)
                        r+= rgb[0]
                        g+= rgb[1]
                        b+= rgb[2]
                        total+= 1
                rMean = round(r / total)
                gMean = round(g / total)
                bMean = round(b / total)
                userClass["Rgb"] = [rMean,gMean,bMean]
            
            for i in range(self.img.width()):
                for j in range(self.img.height()):
                  color = self.classify(self.img.get(i,j))
                  self.img.put(color,(i,j))

    #Função que compara as classes escolhidas pelo usuario e os pixels da
    #imagem
    def classify(self,rbgImg):
        
        distances = []
        currentClasses = []
        distance = 0
        
        r1 = rbgImg[0]
        g1 = rbgImg[1]
        b1 = rbgImg[2]

        for userClass in self.userClasses:

            r2 = userClass["Rgb"][0]
            g2 = userClass["Rgb"][1]
            b2 = userClass["Rgb"][2]

            distance = math.sqrt(math.pow(r2 - r1,2) + math.pow(g2 - g1,2) + math.pow(b2 - b1,2))
            if distance < 20:               
                distances.append(distance)
                currentClasses.append(userClass)
                
        if len(distances) > 0 :
            indexClass = distances.index(min(distances))            
            return currentClasses[indexClass]["Color"]
        else:
            return self.colors[0]

    

#Main
root = tk.Tk()
app = Application(master=root)
app.mainloop()
