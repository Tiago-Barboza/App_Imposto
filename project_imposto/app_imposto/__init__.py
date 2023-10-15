from bs4 import BeautifulSoup
import requests

from project_imposto.settings import prodList


class Produto:
    def __init__(self, nome, tributacao):
        self.nome = nome
        self.tributacao = tributacao


url = 'https://impostometro.com.br/home/relacaoprodutos'
r = requests.get(url)

soup = BeautifulSoup(r.text, 'lxml')
divTables = soup.find("div", class_="editor")

prodTrib = divTables.find_all("tr")
for i in prodTrib:
    td_elements = i.find_all("td")
    if len(td_elements) >= 2:
        nome = td_elements[0].get_text(strip=True)
        tributo = td_elements[1].get_text(strip=True)
        prod = Produto(nome, tributo)
        prodList.append(prod)