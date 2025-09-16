
from urllib.request import urlopen, Request
import re

ua = "Mozilla/5.0 (compatible; Konqueror/3.5.8; Linux)"
h = {"User-Agent": ua}
r = Request("https://www.abc.es/rss/2.0/espana/andalucia/", headers=h)
file = urlopen(r)

noticias = []

class Noticia:
    def __init__(self, titulo,link,fecha):
        self.titulo = titulo
        self.link = link
        self.fecha = fecha

    def show(self):
        return f"Titulo: {self.titulo}. Link: {self.link}, Fecha: {self.fecha}"

    def __str__(self):
        return self.show()

    def __repr__(self):
        return self.show()
        

coincidencias = re.findall("<item>.*?</item>", file.read().decode('utf-8'), re.DOTALL)

for i in coincidencias:
    titulo = re.findall("<title>(.*?)</title>", i, re.DOTALL)[0]
    link = re.findall("<link>(.*?)</link>", i, re.DOTALL)[0]
    puDate = re.findall("<pubDate>(.*?)</pubDate>", i, re.DOTALL)[0]
    nuevaNoticia = Noticia(titulo, link, puDate)
    noticias.append(nuevaNoticia)

print(noticias)
