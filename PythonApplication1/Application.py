import tkinter as tk
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import tkinter.colorchooser as colorPicker
from tkinter import simpledialog
import math

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        master.title("Image Classifier")        
        self.create_widgets()
        self.pack()
        

    def create_widgets(self):

        self.leftFrame = Frame(root)
        self.bottomFrame = Frame(root)
        self.canvasFrame = Frame(root)

        #Botão de escolha de imagem
        self.fileChooserButton = tk.Button(self.bottomFrame)
        self.fileChooserButton["text"] = "Choose File"
        self.fileChooserButton["command"] = self.fileChooserButtonClick
        self.fileChooserButton.pack(side=LEFT)
     
        #Botão de escolha de imagem
        self.classifyButton = tk.Button(self.bottomFrame)
        self.classifyButton["text"] = "Classify"
        self.classifyButton["command"] = self.classifyButtonClick
        self.classifyButton.pack(side=RIGHT)

        self.slider = Scale(self.bottomFrame, from_=0, to=255, orient=HORIZONTAL)
        self.slider.pack(side=RIGHT)

        #canvas onde é mostrada a imagem e onde se pode desenhar
        self.canvas = Canvas(self.canvasFrame)        
        self.canvas.pack(expand = YES, fill = BOTH)

        #canvas onde é mostrada a imagem e onde se pode desenhar
        self.canvasLegenda = Canvas(self.leftFrame)
        self.canvasLegenda["width"] = 150
        self.canvasLegenda["height"] = 300
        self.canvasLegenda["background"] = "#FFFFFF"
        self.canvasLegenda["bd"] = 2
        self.canvasLegenda.pack(expand = YES, fill = BOTH)
        
        #pack dos elementos da tela
        self.bottomFrame.pack(side=BOTTOM)
        self.leftFrame.pack(side=LEFT)
        self.canvasFrame.pack(side = RIGHT)

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
       
        #Variavel que guarda as classes criadas pelo usuario para classificar a
        #imagem
        self.userClasses = []     
        self.classCount = 1

        self.canvasLegenda.create_text(10,10,text = "Legenda", anchor = "w")

    #Escolha do arquivo de imagem, deve ser png ou gif
    def fileChooserButtonClick(self):
        filename = filedialog.askopenfilename(initialdir = "./images",title = "Select Image",filetypes = (("Valid formats","*.png;*gif"),("all files","*.*")))
        if filename != "" :
            self.loadImage(filename)
            
    #Função que carrega a imagem para o canvas e redimensiona o mesmo de acordo
    #com o tamanho da imagem
    def loadImage(self,filename):
        self.img = tk.PhotoImage(file=filename)
        self.imgClassified = self.img.copy()
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
                     "Rgb" : None,
                     "Name": None}

        userClass["Rectangle"] = self.rect
        userClass["Color"] = colorPicker.askcolor()[1]
        userClass["Rgb"] = None
        userClass["Name"] = simpledialog.askstring("Criação de Classe","Nome da Classe:")
        self.userClasses.append(userClass)
        
        self.canvas.itemconfig(userClass["Rectangle"], outline= userClass["Color"])

        self.gap = 10
        self.width = 20
        self.height = 15

        self.canvasLegenda.create_rectangle(self.gap,self.gap*self.classCount+self.height*self.classCount,self.gap+self.width,self.gap*self.classCount+self.height+(self.height*self.classCount),fill=userClass["Color"])
        self.canvasLegenda.create_text(self.gap+self.width+20,self.gap*self.classCount+self.height*self.classCount+7.5,text=userClass["Name"], anchor = "w")
        self.classCount += 1

        pass

    #Função que faz a classificação da imagem
    def classifyButtonClick(self):

        self.gap = 10
        self.width = 20
        self.height = 15

        self.canvasLegenda.create_rectangle(self.gap,self.gap*self.classCount+self.height*self.classCount,self.gap+self.width,self.gap*self.classCount+self.height+(self.height*self.classCount),fill="#000000")
        self.canvasLegenda.create_text(self.gap+self.width+20,self.gap*self.classCount+self.height*self.classCount+7.5,text="Não Classificado", anchor = "w")

        if len(self.userClasses) > 0 :
            for userClass in self.userClasses:
                #variaveis para calcular os valores médios
                r = 0
                g = 0
                b = 0
                total = 0 

                rectCoords = self.canvas.coords(userClass["Rectangle"])
                self.canvas.itemconfig(userClass["Rectangle"],outline="")
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
                  self.imgClassified.put(color,(i,j))
            
            self.canvas.create_image(0,0,anchor=NW,image=self.imgClassified)

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
            if distance <= self.slider.get():               
                distances.append(distance)
                currentClasses.append(userClass)
                
        if len(distances) > 0 :
            indexClass = distances.index(min(distances))            
            return currentClasses[indexClass]["Color"]
        else:
            return "#000000"

    

#Main
root = tk.Tk()
app = Application(master=root)
app.mainloop()
