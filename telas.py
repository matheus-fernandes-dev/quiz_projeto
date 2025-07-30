#FAZENDO OS IMPORTS NECESSÁRIOS
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser
from perguntas import perguntas
from ranking import carregar_ranking, salvar_ranking
import main

#DEFININDO CORES PARA A INTERFACE
cor_background = "#0F7BA6"
cor_texto_principal = "#FCFBFF"
cor_texto_secundario = "#C2D9A0"
cor_botao_principal = "#AFD955"
cor_botao_erro = "#F25C5C"
cor_texto_botao = "#333333"
cor_cronometro_bg = "#222222"
cor_cronometro_fg = "#AFD955"

#VARIAVEIS PARA ARMAZENAR INFORMAÇÕES DA INTERFACE
janela = None
entrada_nome = None
frame_inicio = None
frame_perguntas = None
frame_final = None
frame_ranking = None
cronometro_label = None
botoes_resposta = []


def configurando_janela(): #FUNÇÃO PARA CRIAR A JANELA E DEFINIR ESTILO
    global janela
    janela = tk.Tk()
    janela.title('EcoQuiz')
    janela.geometry("600x670")
    janela.config(bg=cor_background)
    janela.option_add('*Font', 'Arial')
    try:
        icone = tk.PhotoImage(file="imagens/icon_canto_superior_esquerdo_tela_inicio.png")
        janela.iconphoto(True, icone)
    except:
        pass

def destruir_frames(): #FUNÇÃO PARA IGNORAR A TELA ANTERIOR E EXIBIR A ATUAL
    global frame_inicio, frame_perguntas, frame_final, frame_ranking
    for frame in [frame_inicio, frame_perguntas, frame_final, frame_ranking]:
        if frame:
            frame.pack_forget()

def criar_tela_inicial(): #FUNÇÃO PARA INFORMAÇÕES NA TELA INICIAL
    global frame_inicio, entrada_nome
    destruir_frames()
    frame_inicio = tk.Frame(janela, bg=cor_background)
    frame_inicio.pack(fill="both", expand=True)

    try:
        imagem_pil = Image.open("imagens/sticker_tela_inicio.png").resize((220, 220))
        imagem_inicial = ImageTk.PhotoImage(imagem_pil)
        imagem_label = tk.Label(frame_inicio, image=imagem_inicial, bg=cor_background)
        imagem_label.image = imagem_inicial
        imagem_label.pack(pady=10)
    except:
        pass
    tk.Label(frame_inicio, text="Bem vindo ao EcoQuiz!", font=("Arial", 18, "bold"), #TEXTOS DA TELA INICIAL
             bg=cor_background, fg=cor_texto_principal).pack(pady=10)
    tk.Label(frame_inicio, text="“Responda 8 perguntas sobre descarte com 20 segundos para cada desafio.\n"
             "Pontue a cada acerto. Aprenda com as respostas erradas\n" "e veja quem lidera o ranking!”"
             , font=("Arial", 12, "italic"),
             bg=cor_background, fg=cor_texto_secundario).pack(pady=10)
    tk.Label(frame_inicio, text="Digite seu nome abaixo:", bg=cor_background, fg=cor_texto_principal,
             font=("Arial", 12, "bold")).pack(pady=10)
    entrada_nome = tk.Entry(frame_inicio, font=("Arial", 12))
    entrada_nome.pack(pady=10)
    tk.Button(frame_inicio, text="Começar", width=20, bg=cor_botao_principal, fg=cor_texto_botao,#BOTÔES DA TELA INICIAL
              font=("Arial", 12, "bold"), command=main.comecar_jogo).pack(pady=10)
    tk.Button(frame_inicio, text="Jogar Novamente", width=20, bg=cor_botao_principal, fg=cor_texto_botao,
              font=("Arial", 12, "bold"), command=main.iniciar_novamente_da_pergunta).pack(pady=10)
    tk.Button(frame_inicio, text="Ver Ranking", width=20, bg=cor_botao_principal, fg=cor_texto_botao,
              font=("Arial", 12, "bold"), command=lambda: criar_tela_ranking(frame_inicio)).pack(pady=10)

def criar_tela_perguntas(): #FUNÇÃO PARA EXIBIR AS INFORMAÇÕES DA TELA DE PERGUNTAS
    global frame_perguntas, cronometro_label, botoes_resposta
    destruir_frames()
    frame_perguntas = tk.Frame(janela, bg=cor_background)
    frame_perguntas.pack(fill="both", expand=True)
    tk.Label(frame_perguntas, text=f"Bem vindo, jogador(a) {main.nome_jogador}!",
             bg=cor_background, fg=cor_texto_secundario, font=("Arial", 12, "italic")).pack(pady=12)
    tk.Label(frame_perguntas, text=f"Pergunta {main.indice_pergunta + 1} de {len(perguntas)}",
         bg=cor_background, fg=cor_texto_principal, font=("Arial", 12, "bold")).pack(pady=5)
    cronometro_label = tk.Label(frame_perguntas, text="00:00:20", font=("Courier", 20, "bold"),
                                bg=cor_cronometro_bg, fg=cor_cronometro_fg, width=15, pady=20)
    cronometro_label.pack(pady=20)
    pergunta = perguntas[main.indice_pergunta]
    tk.Label(frame_perguntas, text=pergunta[0], wraplength=600, bg=cor_background, fg=cor_texto_principal,
             font=("Arial", 12, "bold")).pack(pady=20)
    botoes_resposta = []
    for i, opcao in enumerate(pergunta[1]):
        botao = tk.Button(frame_perguntas, text=opcao, wraplength=500, width=50,
                          bg=cor_botao_principal, fg=cor_texto_botao, font=("Arial", 10, "bold"),
                          command=lambda i=i: main.verificar_resposta(i))
        botao.pack(pady=8)
        botoes_resposta.append(botao)
    main.iniciar_cronometro()

def criar_tela_final():#FUNÇÃO PARA EXIBIR INFORMAÇÕES DA TELA FINAL E ESTILO
    global frame_final
    destruir_frames()
    frame_final = tk.Frame(janela, bg=cor_background)
    frame_final.pack(fill="both", expand=True)
    try:
        imagem_pil = Image.open("imagens/sticker_tela_final.png").resize((220, 220))
        imagem_final = ImageTk.PhotoImage(imagem_pil)
        imagem_label = tk.Label(frame_final, image=imagem_final, bg=cor_background)
        imagem_label.image = imagem_final
        imagem_label.pack(pady=10)
    except:
        pass
    tk.Label(frame_final, text=f"Obrigado por jogar o EcoQuiz!",#TEXTOS DA TELA FINAL
             font=("Arial", 20, "bold"), bg=cor_background, fg=cor_texto_principal).pack(pady=10)
    tk.Label(frame_final, text=f"Você conseguiu {main.pontuacao} acertos.\n Clique em “Ver Ranking” para conferir sua posição.”\n\n“Para saber mais sobre reciclagem em nossa cidade,\n clique no botão “Saiba Mais” e acesse o site oficial da prefeitura.”",
             font=("Arial", 12, "italic"), bg=cor_background, fg=cor_texto_secundario).pack(pady=10)
    salvar_ranking(main.nome_jogador, main.pontuacao)
    tk.Button(frame_final, text="Jogar Novamente", width=25, bg=cor_botao_principal, fg=cor_texto_botao,  #BOTÔES DA TELA FINAL
              font=("Arial", 12, "bold"), command=main.iniciar_novamente_da_pergunta).pack(pady=10)
    tk.Button(frame_final, text="Ver Ranking", width=25, bg=cor_botao_principal, fg=cor_texto_botao,
              font=("Arial", 12, "bold"), command=lambda: criar_tela_ranking(frame_final)).pack(pady=10)
    tk.Button(frame_final, text="Início", width=25, bg=cor_botao_principal, fg=cor_texto_botao,
              font=("Arial", 12, "bold"), command=criar_tela_inicial).pack(pady=10)
    tk.Button(frame_final, text="Saiba Mais", width=25, bg=cor_botao_erro, fg=cor_texto_principal,
              font=("Arial", 12, "bold"), command=abrir_site_informativo).pack(pady=10)

def criar_tela_ranking(frame_anterior):#FUNÇÃO PARA EXIBIR INFORMAÇÕES DA TELA DE RANKING
    global frame_ranking
    frame_anterior.pack_forget()
    frame_ranking = tk.Frame(janela, bg=cor_background)
    frame_ranking.pack(fill="both")
    try:
        imagem_pil = Image.open("imagens/icon_tela_ranking.png").resize((220, 220))
        imagem_trofeu = ImageTk.PhotoImage(imagem_pil)
        img_label = tk.Label(frame_ranking, image=imagem_trofeu, bg=cor_background)
        img_label.image = imagem_trofeu
        img_label.pack(pady=10)
    except:
        pass
    ranking = carregar_ranking()
    if not ranking:
        tk.Label(frame_ranking, text="Ranking ainda não possui informações.", #VERIFICAÇÃO, CASO O RANKING ESTEJA VAZIO
                 font=("Arial", 12), bg=cor_background, fg=cor_texto_principal).pack()
    else:
        ranking_ordenado = sorted(ranking, key=lambda x: x["pontuacao"], reverse=True)#MOSTRANDO O RANKING
        for i, jogador in enumerate(ranking_ordenado):
            posicao = "1." if i == 0 else "2." if i == 1 else "3." if i == 2 else ""
            texto = f"{posicao} {jogador['nome']} - {jogador['pontuacao']} pts"
            tk.Label(frame_ranking, text=texto, font=("Arial", 12), 
                     bg=cor_background, fg=cor_texto_principal).pack()
    tk.Button(frame_ranking, text="Início", width=25, bg=cor_botao_principal, fg=cor_texto_botao,#BOTÕES DA TELA RANKING
              font=("Arial", 12, "bold"), command=criar_tela_inicial).pack(pady=10)
    tk.Label(frame_ranking, text="Para saber mais sobre reciclagem em nossa cidade,\n" #TEXTO DA TELA DO RANKING
                                 "clique no botão “Saiba Mais” e acesse o site oficial da prefeitura.",
             font=("Arial", 12, "italic"), bg=cor_background, fg=cor_texto_secundario).pack(pady=10)
    tk.Button(frame_ranking, text="Saiba Mais", width=25, bg=cor_botao_erro, fg=cor_texto_principal,
              font=("Arial", 12, "bold"), command=abrir_site_informativo).pack(pady=10)

def abrir_site_informativo(): #ABRINDO SITE 
    webbrowser.open("https://paulista.pe.gov.br/2024/dinamico/noticia-detalhe.php?id=8413")
