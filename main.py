import re

# Entrada HTML
html = """
<html> <head> <title> Compiladores </title> </head><body> <p style="color:red;background:blue;" id="abc"> Unipinhal </p> <br> </body></html>
""".strip()

tag_name_pattern= '([^<>]+)'
attr_name_pattern= '(\w|\d|[^<>])+'
attr_value_pattern= '[^<>]+'
attrs_pattern= f'(\s({attr_name_pattern})="({attr_value_pattern})")*'
tag_pattern= rf'<{tag_name_pattern}{attrs_pattern}>(.*)<\/(\1)>'
single_tag_pattern= rf'<{tag_name_pattern}{attrs_pattern}\/?>'
tokens= []

def has_closing_tag(inner_html, tag_name):
  return re.match(rf'<\/{tag_name}>', inner_html)

def fetch_single_tag(inner_html, level):
  unique_tag= ["br"]
  has_single_tag= False
  for match in re.finditer(single_tag_pattern, inner_html):
    op_tag= match.group(1).strip() # tag de abertura
    if not has_closing_tag(inner_html, op_tag):
      for ut in unique_tag: # valida se está na lista de tags únicas que não tem terminação
        if op_tag==ut:
          has_single_tag= True
          tokens.append(('Tag única', op_tag, level))
  return has_single_tag


def fetch_tag(html, level= 0):
  count_tag= 0 # serve para impedir que o conteúdo de innerHTML que possui HTML seja impresso
  for match in re.finditer(tag_pattern, html):
    count_tag+=1;
    op_tag= match.group(1).strip() # tag de abertura
    inner_html= match.group(6).strip()
    tokens.append(('Tag de abertura', op_tag, level))
    has_tag= fetch_tag(inner_html, level+1)==0
    has_single_tag= fetch_single_tag(inner_html, level+1)
    if has_tag and not has_single_tag:
      tokens.append(('conteúdo de tag', inner_html))
    tokens.append(('Tag de fechamento', op_tag, level))
  return count_tag


fetch_tag(html)

for token in tokens:
  print(token)