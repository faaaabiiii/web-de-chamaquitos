import requests

url = "https://climate-change-live452.p.rapidapi.com/news"
headers = {
	"X-RapidAPI-Key": "9acd896290mshd7266af432403dcp12ac41jsn0b84bdd47bfa",
	"X-RapidAPI-Host": "climate-change-live452.p.rapidapi.com"
}
response = requests.get(url, headers=headers)
news = response.json()

''' 
Noticias de cambio climático en una lista de diccionarios con llaves 'title' 'url' 'source'

news = [
	{"title": título, "url":url, "source": fuente},
	{"title": título, "url":url, "source": fuente},
 	...
    ]
'''