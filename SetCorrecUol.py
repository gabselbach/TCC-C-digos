#Funcao para pegar apenas as correções de acentuação grafica
def PegaCorrecao2(txt):
  palavras=[]
  p1 =''
  p2=''
  PalavrasEscritas = re.findall(r'<strong>(.*?)</strong>(.*?)<span style=\"color:#00b050\">(.*?)</span>',txt)
  r = PalavrasEscritas.copy()
  novo = []
  val =[]
  v=0
  acento = re.compile('à|[á-ú]|ê|ô|ã|õ|í') 
  outro = re.compile("[,|:|?]")
  espaço = re.compile("^[[a-z]+\s.]$")
  for palavra in r:
    p1 = re.sub(' ','',palavra[0])
    p2 = re.sub(' ','',palavra[2])
    conteudo = nlp(palavra[0])
    valores1 = conteudo.text.split()
    conteudo = nlp(palavra[2])
    valores2 = conteudo.text.split()
    if(len(valores1)==len(valores2)):
      i=0
      for x in valores2:
        if(distance(x,valores1[i])==1 and (acento.search(str(x))) and (not acento.search(str(valores1[i]))) ):
          norm = normalize('NFKD',str(x)).encode('ASCII', 'ignore').decode('ASCII').lower()
          palavras.append(str(x))   
        i=i+1
  return palavras
#código principal
UOL = pd.read_csv('TodasReds.csv')
SetUol=[]
SetUol2=[]
def isdigit(s):
    comp = re_compile("^\d+?\.\d+?$")
    if comp.match(s) is None:
        return s.isdigit()
    return True
for (i,row) in UOL.iterrows():
  if(i<15):
    qtd=0
    red = row['textoTotal']
    redSotexto = row['textoSemTag']
    manual = []
    manual =PegaCorrecao2(red)
    conteudo = nlp(redSotexto)
    palavras = conteudo.text.split()
    copytexto = palavras.copy()
    palavrasComuns = {'atração','acontece','antigas','pertence','pais','muita','econômico','sofre','ideia','coloca','mídia','para','correta','pública','integra','julga','justifica','mais','pela','fica','favorece','reforça','larga','esta','significa','disse','corte','começa','espera','merece','parece','formas','esquece'	}
    for x in copytexto:
      if(len(x) < 2 or (x in palavrasComuns)):
        palavras.remove(x)
    Novo = []
    l=0
    for j in palavras:
      
      pnorm = normalize('NFKD',str(j)).encode('ASCII', 'ignore').decode('ASCII').lower()
      temp={
        'correc': 0,
        'palavra': j
      }
      copymanual = manual.copy();
      Novo.append(temp)
      for k in copymanual:
        pNormManual = normalize('NFKD',str(k)).encode('ASCII', 'ignore').decode('ASCII').lower()
        if(pnorm == pNormManual and distance(str(j),str(k))==1 and len(str(j))>2):
          Novo[l]["correc"]=1
          qtd +=1
          manual.remove(k)
          break
      l +=1
    Novo = pd.DataFrame(Novo)
    temp2 = {
      'texto': redSotexto,
      'palavrasCorrec': Novo.copy(),
      'qtd':qtd
    }
    SetUol2.append(temp2)
  else:
    break
SetUol2 = pd.DataFrame(SetUol2)
SetUol2.to_excel('setCorrecUol100Certo.xlsx', sheet_name='analiseRedações')