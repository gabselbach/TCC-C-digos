!pip install selenium
import nltk
import re
import sys
import pandas as pd
import urllib.request
from nltk.tokenize import word_tokenize
from urllib.request import urlopen
from bs4 import BeautifulSoup
from collections import defaultdict
from google.colab import files
from selenium import webdriver
from urllib.error import HTTPError
!apt-get update # to update ubuntu to correctly run apt install
!apt install chromium-chromedriver
!cp /usr/lib/chromium-browser/chromedriver /usr/bin
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
wd.get("https://educacao.uol.com.br/bancoderedacoes/")
element = wd.find_element_by_class_name('btn-primary')
while not element == None:
  try:
    wd.execute_script("arguments[0].click();", element)
    element = wd.find_element_by_class_name('btn-primary')
  except Exception as e:
    break
linksProposta=[]
linksRedacao=[]
DataRedacoes= []
redacoes=[]
data =[]
contRedacao=0
cont= 0
items.pop(0)
for i in items:  
  linksProposta.append(i.get('href'))
  linkprop = i.get('href')
  if(cont<850):
    try:
      html = urlopen(linkprop)
      soup = BeautifulSoup(html.read(),'html5lib')
      tituloProposta = soup.find('i',{'class': 'custom-title'}).get_text()
      textoMotivador = soup.find('div',{'class': 'text'})
      val = soup.find_all('div', {'class': 'rt-line-option'})
      if val != [] :
        for j in val:
          linkRedacao = j.find('a', href=re.compile("https://educacao.uol.com.br/bancoderedacoes/redacoes/")).get('href')
          print(linkRedacao)
          try:
            html2 = urlopen(linkRedacao)
            soup2 = BeautifulSoup(html2.read(),'html5lib')
            tituloRedacao = soup2.find('h2').get_text()
            notaFinal = soup2.find('span', {'class': 'mark'})
            notaComp1 = soup2.find('span', {'class': 'points'})
            textoComTag = soup2.find('div', {'class': 'text-composition'})
            textoResposta = soup2.find('div',{'class':'text'})
            textoSemTag = re.sub('<span style="color:#00b050.>.*?<\/span>', '', str(textoComTag))
            ano = re.sub('<[^>]+?>', '', str(soup2.find('i', {'class': 'kicker'})))
            temp = {
              'ano': '2019',
              'tituloProposta':re.sub('<[^>]+?>', '', str(tituloProposta)),
              'linkProposta':linkprop,
              'textosMotivadores':re.sub('<[^>]+?>', '', str(textoMotivador)),
              'tituloRedacao':tituloRedacao,
              'linkRedacao':linkRedacao,
              'notaFinal':re.sub('<[^>]+?>', '', str(notaFinal)),
              'notaComp':re.sub('<[^>]+?>', '', str(notaComp1)),
              'textoTotal':textoComTag,
              try:
                'correcao': PegaCorrecao(textoComTag),
              except HTTPError as e:
                'correcao': 'NAN',
              'textoSemTag': re.sub('<[^>]+?>', '', str(textoSemTag)),
              'textoResposta':re.sub('<[^>]+?>', '', str(textoResposta))
            }
            data.append(dict(temp))
          except HTTPError as e:
            content = e.read()
    except HTTPError as e:
      content = e.read()
  cont=cont+1         
df = pd.DataFrame(data, columns= ['ano', 'tituloProposta','linkProposta','textosMotivadores','tituloRedacao','linkRedacao','notaFinal','notaComp','textoTotal','correcao','textoSemTag','textoResposta'])
df.to_csv('CrawlerUOL.csv')