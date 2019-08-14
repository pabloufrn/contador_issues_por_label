# como usar
digite no terminal linux `source myenv/bin/activate`, depois `python main.py`.
Case queira fazer as requisições da api novamente, delete o main_cache.sqlite.
# resultados de exemplo
o arquivo `kibana_pulls.txt` tem todas as pulls listadas com os seguintes críterios:
- Cada pull tem pelo menos uma das label listadas em `labels_kibana.txt`.
- Nenhuma pull é listada mais de uma vez. 

A mesma coisa acontece para os arquivos do projeto cas.  
  
<br>  

A contagem obtida nessa amostra foi a seguinte:  
- 3458 issues no repositório kibana  
- 959 pulls no repositório kibana 
- 0 issues no repositório cas 
- 243 pulls no repositório cas 
  
obs .: Como cada pull request é uma issue, podemos ter a contagem de issues total somando as issues com as pulls requests.
