from bs4 import BeautifulSoup

# Entrada HTML
entrada_html = """
<html> <head> <title> Compiladores </title> </head><body> <p style="color:red;background:blue;" id="abc"> Unipinhal </p> <br> </body></html>
"""

# Analisar o HTML com BeautifulSoup
soup = BeautifulSoup(entrada_html, 'html.parser')

# Função para imprimir uma tag e seus atributos recursivamente
def print_tag(tag, nivel):
    print(f"\n{'  ' * nivel}Tag de abertura: {tag.name}, Nível {nivel}")
    
    for atributo, valor in tag.attrs.items():
        print(f"\n{'  ' * (nivel+1)}Atributo de Tag: {atributo}")
        valores= enumerate(valor.split(';'))
        if len(valores)>1:
            for i, v in valores:
                partes = v.split(':')
                if len(partes) == 2:
                    nome_css, valor_css = partes
                    print(f"\n{'  ' * (nivel+2)}Conteúdo {i + 1} do style: {nome_css.strip()}")
                    print(f"\n{'  ' * (nivel+2)}valor conteúdo {i + 1} : {valor_css.strip()}")
        else:
            print(f"\n{' ' * (nivel+1)}Valor do atributo: {valor}")
    
    if tag.string:
        print(f"\n{'  ' * (nivel+1)}conteúdo da tag: {tag.string.strip()}")

    for filho in tag.find_all(recursive=False):
        print_tag(filho, nivel+1)
    
    if tag.name:
        print(f"\n{'  ' * nivel}Tag de fechamento: {tag.name}")

# Iniciar a análise com a tag HTML raiz
print_tag(soup.html, 0)

#teste 