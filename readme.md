# Proyecto de Crawler

**Juan José Roque Cires**

## Como correr el crawler

Para probar el software puede correr run.sh, que crawlea wikipedia y fandom de harry potter, para compararlo contra un documento relacionado con el primer libro de la saga:

* https://es.wikipedia.org/wiki/Harry_Potter 
* https://harrypotter.fandom.com/es/wiki/Harry_Potter
* https://salamandra.info/libro/harry-potter-y-piedra-filosofal 

Para correr un crawler correr python3 crawler -h

Dependencias:

	1. BeautifulSoup 4
 	2. Requests
 	3. Nltk

## Observaciones

Para la construcción de índices limpié el html y lo deje solo en contenido. Luego tokenizé quitando signos de puntuación y luego quité los stopwords.

Para cada documento procese la lista de tokens y lo convertí en un diccionario que guardaba el término contra la frecuencia absoluta de dicho documento.

Ya que no tenemos los stopwords podemos determinar la similitud de los documentos como la suma de las frecuencias absolutas normalizada. 

