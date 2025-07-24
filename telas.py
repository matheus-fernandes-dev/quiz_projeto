import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser
import json
import os
from perguntas import perguntas

# -------------------------
# CORES PADRÕES DA INTERFACE
# -------------------------
cor_background = "#ECECEC"
cor_texto = "#333333"
cor_botao = "#4CAF50"
cor_texto_botao = "#ffffff"
cor_cronometro_bg = "#222222"
cor_cronometro_fg = "#00FF00"

# -------------------------
# VARIÁVEIS GLOBAIS
# -------------------------
janela = None
entrada_nome = None
frame_inicio = None
frame_perguntas = None
frame_final = None
frame_ranking = None
nome_jogador = ""
cronometro_label = None
tempo_restante = 15
indice_pergunta = 0
pontuacao = 0
botoes_resposta = []
cronometro_id = None

# -------------------------
# INICIALIZA A JANELA
# -------------------------
def configurando_janela():
    global janela
    janela = tk.Tk()
    janela.title('Quiz')
    janela.geometry("700x750")
    janela.config(bg=cor_background)
    janela.option_add('*Font', 'Arial')
    try:
        icone = tk.PhotoImage(file="imagens/Icone_canto_esquerdo_superior.png")
        janela.iconphoto(True, icone)
    except:
        pass

# -------------------------
# TELA INICIAL
# -------------------------
def criar_tela_inicial():
    global frame_inicio, entrada_nome
    destruir_frames()
    frame_inicio = tk.Frame(janela, bg=cor_background)
    frame_inicio.pack(fill="both", expand=True)

    try:
        imagem_pil = Image.open("imagens/icone_lixo.png").resize((250, 250))
        imagem_inicial = ImageTk.PhotoImage(imagem_pil)
        imagem_label = tk.Label(frame_inicio, image=imagem_inicial, bg=cor_background)
        imagem_label.image = imagem_inicial
        imagem_label.pack(pady=10)
    except:
        pass

    tk.Label(frame_inicio, text="Desafio do Lixo!", font=("Arial", 18, "bold"), bg=cor_background, fg=cor_texto).pack(pady=10)
    tk.Label(frame_inicio, text="explicação", font=("Arial", 12), bg=cor_background, fg=cor_texto).pack(pady=10)
    tk.Label(frame_inicio, text="Digite seu nome:", bg=cor_background, fg=cor_texto, font=("Arial", 12, "bold")).pack(pady=10)

    entrada_nome = tk.Entry(frame_inicio, font=("Arial", 12))
    entrada_nome.pack(pady=10)

    tk.Button(frame_inicio, text="Começar", width=20, bg=cor_botao, fg=cor_texto_botao,
              font=("Arial", 12, "bold"), command=comecar_jogo).pack(pady=10)
    tk.Button(frame_inicio, text="Jogar Novamente", width=20, bg=cor_botao, fg=cor_texto_botao,
              font=("Arial", 12, "bold"), command=iniciar_novamente_da_pergunta).pack(pady=10)
    tk.Button(frame_inicio, text="Ver Ranking", width=20, bg="#2196F3", fg="white",
              font=("Arial", 12, "bold"), command=lambda: criar_tela_ranking(frame_inicio)).pack(pady=10)

# -------------------------
# DESTROI TELAS ANTERIORES
# -------------------------
def destruir_frames():
    for frame in [frame_inicio, frame_perguntas, frame_final, frame_ranking]:
        if frame:
            frame.pack_forget()

# -------------------------
# INICIAR JOGO
# -------------------------
def comecar_jogo():
    global nome_jogador
    nome = entrada_nome.get().strip()
    if not nome:
        messagebox.showwarning("Aviso", "Digite seu nome para começar!")
        return
    if nome.lower() in [j["nome"].lower() for j in carregar_ranking()]:
        messagebox.showwarning("Aviso", "Esse nome já foi usado. Escolha outro.")
        return
    nome_jogador = nome
    iniciar_quiz_logica()

# -------------------------
# LÓGICA DO QUIZ
# -------------------------
def iniciar_quiz_logica():
    global indice_pergunta, pontuacao
    destruir_frames()
    indice_pergunta = 0
    pontuacao = 0
    criar_tela_perguntas()

# -------------------------
# CRONÔMETRO
# -------------------------
def iniciar_cronometro():
    global tempo_restante, cronometro_id
    tempo_restante = 15
    if cronometro_id:
        janela.after_cancel(cronometro_id)
    atualizar_cronometro()

def atualizar_cronometro():
    global tempo_restante, cronometro_id
    minutos = tempo_restante // 60
    segundos = tempo_restante % 60
    cronometro_label.config(text=f"00:{minutos:02d}:{segundos:02d}")
    if tempo_restante > 0:
        tempo_restante -= 1
        cronometro_id = janela.after(1000, atualizar_cronometro)
    else:
        proxima_pergunta()

# -------------------------
# TELA DE PERGUNTAS
# -------------------------
def criar_tela_perguntas():
    global frame_perguntas, cronometro_label, botoes_resposta
    destruir_frames()
    frame_perguntas = tk.Frame(janela, bg=cor_background)
    frame_perguntas.pack(fill="both", expand=True)

    tk.Label(frame_perguntas, text=f"Jogador(a): {nome_jogador}", bg=cor_background, fg=cor_texto,
             font=("Arial", 12, "italic")).pack(pady=12)

    cronometro_label = tk.Label(frame_perguntas, text="00:00:15", font=("Courier", 20, "bold"),
                                bg=cor_cronometro_bg, fg=cor_cronometro_fg, width=15, pady=20)
    cronometro_label.pack(pady=10)

    pergunta = perguntas[indice_pergunta]
    tk.Label(frame_perguntas, text=pergunta[0], wraplength=600, bg=cor_background, fg=cor_texto,
             font=("Arial", 12, "bold")).pack(pady=20)

    botoes_resposta = []
    for i, opcao in enumerate(pergunta[1]):
        botao = tk.Button(frame_perguntas, text=opcao, wraplength=500, width=50,
                          bg=cor_botao, fg=cor_texto_botao, font=("Arial", 10, "bold"),
                          command=lambda i=i: verificar_resposta(i))
        botao.pack(pady=8)
        botoes_resposta.append(botao)

    iniciar_cronometro()

# -------------------------
# VERIFICAR RESPOSTA
# -------------------------
def verificar_resposta(indice):
    global pontuacao
    pergunta = perguntas[indice_pergunta]
    correta = pergunta[2]
    info = pergunta[3]
    selecionada = pergunta[1][indice]

    if selecionada == correta:
        pontuacao += 1
        proxima_pergunta()
    else:
        botoes_resposta[indice].config(bg='red')
        for i, texto in enumerate(pergunta[1]):
            if texto == correta:
                botoes_resposta[i].config(bg='green')
        messagebox.showinfo("Resposta incorreta", info)
        proxima_pergunta()

# -------------------------
# PRÓXIMA PERGUNTA
# -------------------------
def proxima_pergunta():
    global indice_pergunta
    indice_pergunta += 1
    if indice_pergunta < len(perguntas):
        criar_tela_perguntas()
    else:
        criar_tela_final()

# -------------------------
# TELA FINAL
# -------------------------
def criar_tela_final():
    global frame_final
    destruir_frames()
    frame_final = tk.Frame(janela, bg=cor_background)
    frame_final.pack(fill="both", expand=True)

    try:
        imagem_pil = Image.open("imagens/icon_canto_esquerdo_superior.png").resize((100, 100))
        imagem_final = ImageTk.PhotoImage(imagem_pil)
        imagem_label = tk.Label(frame_final, image=imagem_final, bg=cor_background)
        imagem_label.image = imagem_final
        imagem_label.pack(pady=10)
    except:
        pass

    tk.Label(frame_final, text=f"Fim do Quiz!\nPontuação: {pontuacao}", font=("Arial", 20, "bold"),
             bg=cor_background, fg=cor_texto).pack(pady=10)

    salvar_ranking(nome_jogador, pontuacao)

    tk.Button(frame_final, text="Jogar Novamente", width=25, bg=cor_botao, fg=cor_texto_botao,
              font=("Arial", 12, "bold"), command=iniciar_novamente_da_pergunta).pack(pady=10)
    tk.Button(frame_final, text="Ver Ranking", width=25, bg="#2196F3", fg="white",
              font=("Arial", 12, "bold"), command=lambda: criar_tela_ranking(frame_final)).pack(pady=10)
    tk.Button(frame_final, text="Início", width=25, bg=cor_botao, fg=cor_texto_botao,
              font=("Arial", 12, "bold"), command=criar_tela_inicial).pack(pady=10)
    tk.Button(frame_final, text="Ver Informações", width=25, bg="#FF9800", fg="white",
              font=("Arial", 12, "bold"), command=abrir_site_informativo).pack(pady=10)

# -------------------------
# JOGAR NOVAMENTE
# -------------------------
def iniciar_novamente_da_pergunta():
    global nome_jogador
    nome = entrada_nome.get().strip()
    if not nome:
        messagebox.showwarning("Aviso", "Digite seu nome!")
        return

    ranking = carregar_ranking()
    nomes_ranking = [j["nome"].lower() for j in ranking]

    if nome.lower() not in nomes_ranking:
        messagebox.showinfo("Nome não encontrado", "Nome não cadastrado. Verifique seu nome no ranking.")
        criar_tela_inicial()
        return

    nome_jogador = nome
    iniciar_quiz_logica()

# -------------------------
# TELA DE RANKING
# -------------------------
def criar_tela_ranking(frame_anterior):
    global frame_ranking
    frame_anterior.pack_forget()
    frame_ranking = tk.Frame(janela, bg=cor_background)
    frame_ranking.pack(fill="both", expand=True)

    try:
        imagem_pil = Image.open("imagens/icon_ranking.png").resize((120, 120))
        imagem_trofeu = ImageTk.PhotoImage(imagem_pil)
        img_label = tk.Label(frame_ranking, image=imagem_trofeu, bg=cor_background)
        img_label.image = imagem_trofeu
        img_label.pack(pady=10)
    except:
        pass

    ranking = carregar_ranking()
    if not ranking:
        tk.Label(frame_ranking, text="Ranking ainda não possui informações.", font=("Arial", 12),
                 bg=cor_background, fg=cor_texto).pack()
    else:
        ranking_ordenado = sorted(ranking, key=lambda x: x["pontuacao"], reverse=True)
        for i, jogador in enumerate(ranking_ordenado):
            emoji = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else ""
            texto = f"{emoji} {jogador['nome']} - {jogador['pontuacao']} pts"
            tk.Label(frame_ranking, text=texto, font=("Arial", 12), bg=cor_background, fg=cor_texto).pack()

    tk.Button(frame_ranking, text="Início", width=25, bg=cor_botao, fg=cor_texto_botao,
              font=("Arial", 12, "bold"), command=criar_tela_inicial).pack(pady=20)

# -------------------------
# SALVAR/CARREGAR RANKING - JSON
# -------------------------
def salvar_ranking(nome, pontuacao):
    ranking = carregar_ranking()
    for jogador in ranking:
        if jogador["nome"].lower() == nome.lower():
            if pontuacao > jogador["pontuacao"]:
                jogador["pontuacao"] = pontuacao
            break
    else:
        ranking.append({"nome": nome, "pontuacao": pontuacao})

    with open("ranking.json", "w", encoding="utf-8") as f:
        json.dump(ranking, f, indent=2, ensure_ascii=False)

def carregar_ranking():
    if os.path.exists("ranking.json"):
        with open("ranking.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# -------------------------
# ABRIR SITE
# -------------------------
def abrir_site_informativo():
    webbrowser.open("https://www.exemplo.com.br")

# -------------------------
# EXECUTAR O JOGO
# -------------------------
def iniciar_quiz():
    configurando_janela()
    criar_tela_inicial()
    janela.mainloop()