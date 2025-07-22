import tkinter as tk
import random as ran
from perguntas import perguntas 
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image, ImageTk

cor_background= "#ECECEC"
cor_texto= "#333333"
cor_botao= "#4CAF50"
cor_texto_botao= "#ffffff"

janela= tk.Tk()
janela.title('Quiz')
janela.geometry("700x750")
janela.config(bg=cor_background)
janela.option_add('*Font', 'Arial')

icone = tk.PhotoImage(file="imagens/recycle-bin.png")
janela.iconphoto(True, icone)

imagem_pil = Image.open("imagens/icone_lixo.png")
imagem_pil = imagem_pil.resize((250, 250))
imagem_inicial = ImageTk.PhotoImage(imagem_pil)
imagem_label = tk.Label(janela, image=imagem_inicial, bg=cor_background)
imagem_label.pack(pady=10)

perguntas_label= tk.Label(janela, text="Perguntas", wraplength=380, bg=cor_background, fg=cor_texto, font=("Arial", 12, "bold"))
perguntas_label.pack(pady=20)
resposta_correta= tk.StringVar()

#Estlizando os botões
botao_opcao1= tk.Button(janela, text="", width=30, bg= cor_botao, fg=cor_texto_botao, state=tk.DISABLED, font=("Arial", 10, "bold"))
botao_opcao1.pack(pady=10)

botao_opcao2= tk.Button(janela, text="", width=30, bg= cor_botao, fg=cor_texto_botao, state=tk.DISABLED, font=("Arial", 10, "bold"))
botao_opcao2.pack(pady=10)

botao_opcao3= tk.Button(janela, text="", width=30, bg= cor_botao, fg=cor_texto_botao, state=tk.DISABLED, font=("Arial", 10, "bold"))
botao_opcao3.pack(pady=10)

botao_opcao4= tk.Button(janela, text="", width=30, bg= cor_botao, fg=cor_texto_botao, state=tk.DISABLED, font=("Arial", 10, "bold"))
botao_opcao4.pack(pady=10)

janela.mainloop()




