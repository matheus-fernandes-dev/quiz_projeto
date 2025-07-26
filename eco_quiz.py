#FAZENDO OS IMPORTS NECESSÁRIOS
import tkinter as tk 
from tkinter import messagebox 
from perguntas import perguntas 
from ranking import carregar_ranking
import telas 
import random 

#VARIAVÉIS
nome_jogador = "" 
tempo_restante = 20 
indice_pergunta = 0 
pontuacao = 0 
cronometro_id = None 

# FUNÇÕES DO QUIZ
def comecar_jogo(): #FUNÇÃO PARA VERIFICAR SE O NOME FOI PREENCHIDO E SE É ÚNICO
    global nome_jogador
    nome = telas.entrada_nome.get().strip()
    if not nome:
        messagebox.showwarning("Aviso", "Digite seu nome para começar!")
        return
    if nome.lower() in [j["nome"].lower() for j in carregar_ranking()]:
        messagebox.showwarning("Aviso", "Esse nome já foi usado. Escolha outro.")
        return
    nome_jogador = nome
    iniciar_quiz_logica() #INICIANDO O JOGO COM AS PERGUNTAS

def embaralhar_perguntas():#FUNÇÃO PARA EMBARALHAR A ORDEM DAS PERGUNTAS E A ORDEM DAS ALTERNATIVAS
    global perguntas
    random.shuffle(perguntas)  
    for pergunta in perguntas:
        random.shuffle(pergunta[1])

def iniciar_quiz_logica():#FUNÇÃO QUE MOSTRA A TELA DE PERGUNTAS
    global indice_pergunta, pontuacao
    telas.destruir_frames()
    indice_pergunta = 0
    pontuacao = 0
    embaralhar_perguntas() 
    telas.criar_tela_perguntas()

def iniciar_cronometro():#FUNÇÃO DO CRONOMETRO PARA CADA TELA
    global tempo_restante, cronometro_id
    tempo_restante = 20
    if cronometro_id:
        telas.janela.after_cancel(cronometro_id)
    atualizar_cronometro()

def atualizar_cronometro():#FUNÇÃO DO CRONOMETRO PARA PASSAR PARA A PROXIMA PERGUNTA AO FIM DO TEMPO.
    global tempo_restante, cronometro_id
    minutos = tempo_restante // 60
    segundos = tempo_restante % 60
    telas.cronometro_label.config(text=f"00:{minutos:02d}:{segundos:02d}")
    if tempo_restante > 0:
        tempo_restante -= 1
        cronometro_id = telas.janela.after(1000, atualizar_cronometro)
    else:
        proxima_pergunta()

def verificar_resposta(indice):#FUNÇÃO PARA VERIFICAR A RESPOSTA CERTA E DAR FEEDBACK COM MESSAGEBOX
    global pontuacao
    pergunta = perguntas[indice_pergunta]
    correta = pergunta[2]
    info = pergunta[3]
    selecionada = pergunta[1][indice]
    if selecionada == correta:
        pontuacao += 1
        telas.botoes_resposta[indice].config(bg="#ABE358")
        proxima_pergunta()
    else:
        telas.botoes_resposta[indice].config(bg="#F25C5C")
        for i, texto in enumerate(pergunta[1]):
            if texto == correta:
                telas.botoes_resposta[i].config(bg="#ABE358")
        messagebox.showinfo("Resposta incorreta", info) #MOSTRANDO O FEEDBACK
        proxima_pergunta()

def proxima_pergunta(): #FUNÇÃO PARA A PRÓXIMA PERGUNTA
    global indice_pergunta
    indice_pergunta += 1
    if indice_pergunta < len(perguntas):
        telas.criar_tela_perguntas()
    else:
        telas.criar_tela_final()

def iniciar_novamente_da_pergunta(): #FUNÇÃO PARA JOGAR NOVAMENTE E VERIFICAÇÕES DO NOME
    global nome_jogador
    nome = telas.entrada_nome.get().strip()
    if not nome:
        messagebox.showwarning("Aviso", "Digite seu nome para jogar novamente!")
        return
    ranking = carregar_ranking()
    nomes_ranking = [j["nome"].lower() for j in ranking]
    if nome.lower() not in nomes_ranking:
        messagebox.showinfo("Nome não encontrado", "Nome não cadastrado. Verifique seu nome no ranking.")
        telas.criar_tela_inicial()
        return
    nome_jogador = nome
    iniciar_quiz_logica()

def iniciar_quiz(): #FUNÇÃO PARA EXIBIR A TELA INICIAL
    telas.configurando_janela()
    telas.criar_tela_inicial()
    telas.janela.mainloop()

if __name__ == "__main__": #EXECUTANDO O QUIZ
    iniciar_quiz()
