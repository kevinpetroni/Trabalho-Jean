from bs4 import BeautifulSoup

# Entrada HTML
entrada_html = """
<html> <head> <title> Compiladores </title> </head><body> <p style="color:red;background:blue;" id="abc"> Unipinhal </p> <br> </body></html>
"""

# Analisar o HTML com BeautifulSoup
soup = BeautifulSoup(entrada_html, 'html.parser')

# Função para imprimir uma tag e seus atributos recursivamente
def imprimir_tag(tag, nivel):
    print(f"\n{'  ' * nivel}Tag de abertura: {tag.name}, Nível {nivel}")
    
    for atributo, valor in tag.attrs.items():
        print(f"\n{'  ' * (nivel+1)}Atributo de Tag: {atributo}")
        for i, v in enumerate(valor.split(';')):
            partes = v.split(':')
            if len(partes) == 2:
                nome_css, valor_css = partes
                print(f"\n{'  ' * (nivel+2)}Conteúdo {i + 1} do style: {nome_css.strip()}")
                print(f"\n{'  ' * (nivel+2)}valor conteúdo {i + 1} : {valor_css.strip()}")
    
    if tag.string:
        print(f"\n{'  ' * (nivel+1)}conteúdo da tag: {tag.string.strip()}")

    for filho in tag.find_all(recursive=False):
        imprimir_tag(filho, nivel+1)
    
    if tag.name:
        print(f"\n{'  ' * nivel}Tag de fechamento: {tag.name}")

# Iniciar a análise com a tag HTML raiz
imprimir_tag(soup.html, 0)