# READ ME
## Decision Tree

**1º passo:** Correr o ficheiro arvore_decisao.py através do seguinte comando "python3 arvore_decisao.py" ou "python arvore_decisao.py" dependendo da sua versão do Python.

**2º passo:** Indicar qual o dataset a analisar no formato <nome>.csv, por exemplo, "weather.csv".
          De seguida, será gerada a correspondente árvore de decisão segundo o esquema fornecido no enunciado do trabalho.

**3º passo:** Aparecerá também a opção de classificar um exemplo (externo ou não), para tal deve colocar y/Y no terminal. Caso não o pretenda fazer pode apenas colocar n/N e o programa terminará.

**4º passo:** Uma vez dada a indicação de que se quer classificar exemplos será pedido para indicar quntos quer devendo o seu input ser um inteiro, ex: 2.

**5º passo:** Após indicados quantos os exemplos a classificar ser-lhe-á pedido para os indicar um a um com a respetiva ordem do dataset e separados por vírgulas (ver exemplos no campo observações).

**6º passo:** Para cada exemplo inserido é lhe fornecido o respetivo output que indica qual a classe a que pertence o seu exemplo.

**Observações:**
  O dataset pretendido deve estar guardado no mesmo diretório que o ficheiro python.  
  Caso o seu exemplo tenha dados que não fazem parte do dataset obterá como output um aviso dizendo "Valor do atributo <atributo> não encontrado na árvore. Classe prevista: <classe>".  
      Por exemplo:  
      input: 3,sunny,90,90,FALSE  
      output: Valor do atributo Temp não encontrado na árvore. Classe prevista: yes  

  Exemplos (para dataset weather.csv):  
          1,sunny,85,85,FALSE  
          2,sunny,80,90,TRUE  
          3,overcast,83,86,FALSE  
          4,rainy,70,96,FALSE  
          5,rainy,68,80,FALSE  
          6,rainy,65,70,TRUE  
          7,overcast,64,65,TRUE  
          8,sunny,72,95,FALSE  
          9,sunny,69,70,FALSE  
          10,rainy,75,80,FALSE  
          11,sunny,75,70,TRUE  
          12,overcast,72,90,TRUE  
          13,overcast,81,75,FALSE  
          14,rainy,71,91,TRUE
