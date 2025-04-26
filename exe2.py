from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json

driver = webdriver.Chrome()
driver.get("https://www.imdb.com/pt/chart/toptv/?ref_=nv_tvv_250")
driver.maximize_window()
time.sleep(2)

# Pegando a lista de séries
tag_ul = driver.find_element(By.XPATH, r'//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul')
lista_series = tag_ul.find_elements(By.TAG_NAME, "li")

# Lista que vai armazenar os dados
series_info = []

def tarefa1():
    for idx, serie in enumerate(lista_series):
        try:
            nome = serie.find_element(By.CLASS_NAME, "ipc-title__text").text
            nota = serie.find_element(By.CLASS_NAME, "ipc-rating-star--rating").text

            metadata = serie.find_element(By.XPATH, './/div[contains(@class, "cli-title-metadata")]')
            dados = metadata.find_elements(By.TAG_NAME, 'span')

            if len(dados) >= 2:
                ano = dados[0].text
                episodios = dados[1].text
            else:
                ano = "Ano não encontrado"
                episodios = "Episódios não encontrados"

            link = serie.find_element(By.CLASS_NAME, "ipc-title-link-wrapper").get_attribute('href')

            serie_data = {
                "Título": nome,
                "Ano de Estreia": ano,
                "Número de Episódios": episodios,
                "Nota do IMDB": nota,
                "Link": link,
                "Popularidade": ""  # Ainda vamos preencher depois
            }

            series_info.append(serie_data)

            print(f"Coletado: {nome}")

        except Exception as e:
            print(f"Erro ao processar uma série: {e}")

def tarefa2():
    for idx, serie in enumerate(series_info):
        try:
            link = serie["Link"]
            print(f"Acessando série {idx + 1}: {link}")

            driver.get(link)
            time.sleep(2)

            # Buscar a popularidade na página da série
            popularidade = driver.find_element(By.CLASS_NAME, "sc-92d56f96-1.iRhOvL").text
            serie["Popularidade"] = popularidade
            print(f"Popularidade: {popularidade}")

        except Exception as e:
            print(f"Erro ao pegar popularidade: {e}")
            serie["Popularidade"] = "Não encontrada"

# Executar as tarefas
tarefa1()
tarefa2()

# Salvar no JSON
with open("series_info.json", "w", encoding="utf-8") as f:
    json.dump(series_info, f, ensure_ascii=False, indent=4)

print("Arquivo 'series_info.json' criado com sucesso!")

time.sleep(3)
driver.quit()
