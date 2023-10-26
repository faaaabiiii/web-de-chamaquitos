import http.client

conn = http.client.HTTPSConnection("climate-change-live452.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "9acd896290mshd7266af432403dcp12ac41jsn0b84bdd47bfa",
    'X-RapidAPI-Host': "climate-change-live452.p.rapidapi.com"
}

conn.request("GET", "/news", headers=headers)

res = conn.getresponse()
data = res.read()

news = data.decode("utf-8")

''' 
Noticias de cambio climático en una lista de diccionarios con llaves 'title' 'url' 'source'

news = [
	{"title": título, "url":url, "source": fuente},
	{"title": título, "url":url, "source": fuente},
 	...
    ]
'''