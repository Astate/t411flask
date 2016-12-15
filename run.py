#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, redirect, url_for, request
from flask import render_template
import requests
import re
from bs4 import BeautifulSoup
from flask_cache import Cache

app = Flask(__name__)
cache = Cache(app,config={'CACHE_TYPE': 'simple'})

def getHeaders():
	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'
	}
	return headers



@app.route('/',methods =['POST', 'GET'])
def index():
	query = request.args.get('recherche')
	if query:
		print(query)
		return redirect(url_for('torrent_list', query=query))
	else:
		return render_template('index.html')

@app.route('/r/<query>')
def torrent_list(query):

	r = requests.get('http://www.t411.li/torrents/search/?search=%40name+'+query+'+&order=added&type=desc+&submit=Recherche&order=added&type=desc',headers=getHeaders())
	table = torrent_srch(r)
	return render_template('query.html', query=query,  table=table)

@cache.cached(timeout=3600)
@app.route('/top100')
def torrent_top():

	r = requests.get('http://www.t411.li/top/100/',headers=getHeaders())
	query = 'top100'
	table = torrent_srch(r)

	return render_template('query.html', query=query, table=table)


def torrent_srch(r):
	seriestv = 'category - spline - video - tv - series'
	comics = 'category - spline - ebook - comics'
	soup = BeautifulSoup(r.content, "html.parser")
	a = [a.get('href') for a in soup.find_all('a', href=re.compile(r'www\.t411\.li/torrents/'))]
	href = [q[23:] for q in a]
	c = ['http://www.t411.li' + b.get('href') for b in soup.find_all('a', href=re.compile(r'.*\?id\=\d{4,8}'))]
	href2 = [re.sub(r'nfo', r'download', q) for q in c]

	dls = [td.text for td in soup.find_all('td', {'align': 'center'})]



	bi = 0
	size = []
	seed = []
	for i in range(0, len(dls)):
		if i % 6 == 0:
			size.append(dls[bi + 2])
			seed.append(dls[bi + 4])
		bi = bi + 1

	table = [[str(i + 1) if (i + 1) % 2 == 0 else i + 1,
			  href[i] if (i + 1) % 2 == 0 else href[i],
			  href2[i] if (i + 1) % 2 == 0 else href2[i],
			  size[i] if (i + 2) % 2 == 0 else size[i],
			  seed[i] if (i + 2) % 2 == 0 else seed[i]] for i in range(len(href))]
	return table

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)
