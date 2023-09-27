
import re

html = '<html> <head> <title> Compiladores </title> </head><body> <p style="color:red;background:blue;" id="abc"> Unipinhal </p> <br> </body></html>'

acceptable = {
  "tags": ['html', 'head', 'body', 'title', 'p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'img'],
  "unique_tags": ['br'],
  "attrs": ['id', 'style', 'src', 'width', 'height'],
  "css_attrs": ['width', 'height', 'color', 'font-size', 'background', 'border']
}

useful_pattern= '[^<>\s]+' # serve para evitar conteúdo indesejado dentros das tags: espaços e aberturas de colchetes com sinal
inner_html_pattern= '[^<]*'
attrs_pattern= '\s+([^<>\s]+)="([^<>\s]+)"'
style_attr_pattern= '([^<>\s;]+):([^<>\s;]+);'
regex_patttern= f'({inner_html_pattern})<(\/)?({useful_pattern})(\s+[^<>]+="[^<>]+")*'
level= 0
tokens= []

def has_inner_text(inner_html): 
  if inner_html!='':
    inner_html= inner_html.strip()
    tokens.append(("conteúdo de tag", inner_html))

def handle_tag(closing, tag_name): #Distingue Tags de fechamento, abertura e de única chamada
  global level
  tag_name= tag_name.strip()
  if tag_name in acceptable.get("unique_tags"):  #Verifica se tag é presente na lista de tags sem innerHTML
    tokens.append((f"tag única", tag_name, level)) 
  elif tag_name in acceptable.get("tags"): #Verifica se tag é presente na lista de tags com innerHTML 
    if closing:
      tokens.append((f"tag fechamento", tag_name)) 
      level -= 1
    else:
      tokens.append((f"tag abertura", tag_name, level)) 
      level += 1

def handle_style_attrs(attrs): #atributos de estilo
  count_style_attrs= 0
  for attr in re.finditer(style_attr_pattern, attrs):
    count_style_attrs += 1
    attr_name, attr_value = attr.groups()
    tokens.append((f"conteúdo {count_style_attrs} do style", attr_name)) 
    tokens.append((f"valor conteúdo {count_style_attrs}", attr_value)) 

def handle_attrs(attrs):
  if attrs!='' and attrs is not None:
    for attr in re.finditer(attrs_pattern, attrs):
      attr_name, attr_value = attr.groups()
      if attr_name in acceptable.get("attrs"):
        tokens.append((f"atributo da tag", attr_name)) 
        if attr_name=='style':
          handle_style_attrs(attr_value)
        else:
          tokens.append((f"valor atributo", attr_name, ':', attr_value)) 

def recognizer_html(html):
  content_list= html.strip().split(">")
  for content in content_list:
    content= content.strip()
    search_values =re.search(regex_patttern, content)
    if search_values is not None:
      inner_html, closing, tag_name, attrs = search_values.groups()
      has_inner_text(inner_html) #Avalia se possui conteúdo inícialmente para garantir que o conteúdo não seja registrado na ordem errada, seguindo o padrão estabelecido para a expressão regular
      handle_tag(closing, tag_name)
      handle_attrs(attrs)
    
recognizer_html(html)

for token in tokens:
  print(token)
