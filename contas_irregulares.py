from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import csv
import re
        
driver = webdriver.Firefox()

def remover_primeira_linha_csv(nome_arquivo):
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()

    # Descartando a primeira linha (índice 0)
    linhas_restantes = linhas[1:]
    
    # Juntando as linhas novamente em uma única string
    novo_conteudo = ''.join(linhas_restantes)

    # Escrevendo o novo conteúdo de volta no arquivo
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write(novo_conteudo)
        
def tirar_aspas(nome_arquivo):
    pattern = r'[\"\n]'
    
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    
    linha_modificada = []
    for linha in linhas:
        if re.match(pattern, linha):
            linha = re.sub(pattern, '', linha)
        linha_modificada.append(linha)
    
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.writelines(linha_modificada)
        

driver.get("https://contasirregulares.tcu.gov.br/ordsext/f?p=105:2:0::NO:RP:P2_MOSTRAR_LISTA:1")
line = []
while True:
    try:
        sleep(1.5)
        dados = driver.find_element(By.CLASS_NAME, "a-IRR-tableContainer")
        html = dados.get_attribute("innerHTML")
        soup = BeautifulSoup(html,"html.parser")
        table = soup.select_one('table')
        data = [d for d in table.select("tr")]
        for d in data:
            linha = ""
            dado = d.select("td")[1:]
            for t in dado:
                linha = linha + t.text+";"
                if linha.startswith(";") or linha.startswith("."):
                    linha = linha[1:]
            line.append(linha)
        proxima_pagina = driver.find_element(By.XPATH,'/html/body/form/div[1]/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div[2]/div[2]/div[5]/div[2]/ul/li[3]/button')
        proxima_pagina.click() 
    except NoSuchElementException:
        break   

df = pd.DataFrame(line)
df.to_csv("dados_contas_irregulares.csv", index=False)
csv = 'dados_contas_irregulares.csv'
remover_primeira_linha_csv(csv)
tirar_aspas(csv)







     
    



