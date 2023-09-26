import re

# Texto HTML de entrada
html_input = """
<html> <head> <title> Compiladores </title> </head><body> <p style="color:red;background:blue;" id="abc"> Unipinhal </p> <br> </body></html>
"""

# Padrões regex para tags, atributos e conteúdo
tag_pattern = r'<\s*(\w+)[^>]*>'
attribute_pattern = r'(\w+)\s*=\s*["\']([^"\']+)["\']'
content_pattern = r'>([^<]+)<'

# Nível inicial
level = 0

# Função para imprimir uma linha formatada
def print_line(tag, level, attribute=None, attribute_value=None, content=None):
    indentation = " " * (level * 2)
    if attribute is None:
        print(f"{indentation}Tag de {'abertura' if content is not None else 'fechamento'}: {tag}, Nível {level}")
    elif attribute_value is None:
        print(f"{indentation}Atributo de Tag: {attribute}")
    else:
        print(f"{indentation}Valor atributo {attribute}: {attribute_value}")

# Encontre todas as correspondências de tags, atributos e conteúdo
for match in re.finditer(tag_pattern, html_input):
    tag = match.group(1)
    if '/' not in tag:
        # Tag de abertura
        print_line(tag, level)
        level += 1
    else:
        # Tag de fechamento
        level -= 1
        print_line(tag[1:], level)

    # Encontre atributos dentro da tag
    for attribute_match in re.finditer(attribute_pattern, match.group()):
        attribute = attribute_match.group(1)
        attribute_value = attribute_match.group(2)
        print_line(tag, level, attribute, attribute_value)

    # Encontre conteúdo dentro da tag
    content_match = re.search(content_pattern, match.group())
    if content_match:
        content = content_match.group(1).strip()
        if content:
            print_line(tag, level, content=content)