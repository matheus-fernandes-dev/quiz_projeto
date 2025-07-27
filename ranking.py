#IMPORTS NECESSÁRIOS
import json 
import os

def salvar_ranking(nome, pontuacao):#FUNÇÃO PARA SALVAR A PONTUAÇÃO E ATUALIZAR NO RANKING
    ranking = carregar_ranking()    
    for jogador in ranking:
        if jogador["nome"].lower() == nome.lower():
            if pontuacao > jogador["pontuacao"]:
                jogador["pontuacao"] = pontuacao
            break
    else:
        ranking.append({"nome": nome, "pontuacao": pontuacao})
    with open("ranking.json", "w", encoding="utf-8") as f: #GERANDO O ARQUIVO COM A INFORMAÇÕES DOS JOGADORES
        json.dump(ranking, f, indent=2, ensure_ascii=False)

def carregar_ranking():#FUNÇÃO PARA CARREGAR AS INFORMAÇÕES DOS JOGADORES NO ARQUIVO E MOSTRAR
    if os.path.exists("ranking.json"):
        with open("ranking.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []
