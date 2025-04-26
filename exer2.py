from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Inicializar o driver
driver = webdriver.Chrome()
driver.get("https://www.imdb.com/pt/chart/toptv/?ref_=nv_tvv_250")
driver.maximize_window()
time.sleep(2)  # Esperar carregar

# Pegar a lista de séries
tag_ul = driver.find_element(By.XPATH, r'//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul')
lista_series = tag_ul.find_elements(By.TAG_NAME, "li")

# Listas globais
links = []
elencos = []

def tarefa1():
    global links

    for serie in lista_series:
        try:
            # Nome da série
            nome = serie.find_element(By.CLASS_NAME, "ipc-title__text").text

            # Nota da série
            nota = serie.find_element(By.CLASS_NAME, "ipc-rating-star--rating").text

            # Ano e número de episódios
            metadata = serie.find_element(By.XPATH, './/div[contains(@class, "cli-title-metadata")]')
            dados = metadata.find_elements(By.TAG_NAME, 'span')

            if len(dados) >= 2:
                ano = dados[0].text
                episodios = dados[1].text
            else:
                ano = "Ano não encontrado"
                episodios = "Episódios não encontrados"

            # Link da página da série
            link = serie.find_element(By.CLASS_NAME, "ipc-title-link-wrapper").get_attribute('href')
            links.append(link)

            # (opcional) Printar dados
            # print(f"Série: {nome}, Nota: {nota}, Ano: {ano}, Episódios: {episodios}, Link: {link}")

        except Exception as e:
            print(f"Erro ao processar uma série: {e}")

def tarefa2():
    global elencos

    for idx, link in enumerate(links):
        print(f"Acessando série {idx + 1}: {link}")
        driver.get(link)
        time.sleep(2)
        popularidade = driver.find_element(By.CLASS_NAME, "sc-92d56f96-1.iRhOvL").text

        elenco = []

        try:
            # Procurar o botão "Full Cast"
            botao_elenco = driver.find_element(By.XPATH, '//a[contains(@href, "fullcredits")]')
            href_elenco = botao_elenco.get_attribute('href')

            driver.get(href_elenco)
            time.sleep(2)

            # Agora sim: Pegar a lista de atores dentro da tabela de elenco
            atores_tags = driver.find_elements(By.XPATH, '//table[contains(@class,"cast_list")]//tr//td[2]//a')

            for ator_tag in atores_tags:
                ator_nome = ator_tag.text.strip()
                if ator_nome:
                    elenco.append(ator_nome)
            print(f"Popularidade {popularidade}")
            print(f"Elenco ({len(elenco)} atores): {elenco}")

        except Exception as e:
            print(f"Erro ao pegar elenco: {e}")

        elencos.append(elenco)
        print("-" * 40)


# Rodar as tarefas
tarefa1()
tarefa2()

time.sleep(3)
driver.quit()
