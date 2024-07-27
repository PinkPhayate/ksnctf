"""
以下のURLにダイジェスト認証を行ってログインするプログラム。
http://ctfq.u1tramarine.blue/q9/flag.html

サーバ側は、A1を保存しているので、A1を使ってresponseを計算し、Authorizationヘッダに入れてリクエストを送信する。
A1:= c627e19450db746b739f41b64097d449

Authentication-Infoに記載する項目は以下
- username: q9
- realm: secret
- nonce: リクエストして取得
- uri: /q9/flag.html
- algorithm=MD5
- qop=auth
- nc=00000002
- response=取得したnonce値から算出
- cnonce: 16文字のランダムな文字列?

"""
import hashlib
import string
import random, string
import requests

def randomname(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

def get_reponse(uri, nonce):
    cnonce_org=randomname(1)
    cnonce=hashlib.md5(cnonce_org.encode('utf-8')).hexdigest()
    cnonce = cnonce[:16]
    nc = '00000002'
    qop = 'auth'

    a2 = 'GET:' + uri
    a2_hash = hashlib.md5(a2.encode("utf-8")).hexdigest()

    a1_hash = "c627e19450db746b739f41b64097d449"
    return cnonce, hashlib.md5((a1_hash + ':' + nonce + ':' + nc + ':' + cnonce + ':' + qop + ':' + a2_hash).encode("utf-8")).hexdigest()

# まずリクエストしてnonceを取得する
url = "https://ctfq.u1tramarine.blue/q9/flag.html"
uri = url.split('.blue')[1]
response = requests.get(url)
header = response.headers
# リクエストヘッダに以下の値が入っているので、それを使ってnonceの値を取得する
# {'Server': 'nginx', 'Date': 'Sat, 27 Jul 2024 12:26:51 GMT', 'Content-Type': 'text/html; charset=iso-8859-1', 'Content-Length': '381', 'Connection': 'keep-alive', 'WWW-Authenticate': 'Digest realm="secret", nonce="NDoUvjkeBgA=d45bf0dfd3d2747f1df9b8624828a9698bcef0a9", algorithm=MD5, qop="auth"'}
nonce = header['WWW-Authenticate'].split('nonce="')[1].split('"')[0]

# responseを計算し、その際に使用したcnonceと一緒に取得する
cnonce, response =get_reponse(uri, nonce)

header = 'Digest username="q9", realm="secret", nonce="{}", \
    uri="{}", algorithm=MD5, qop=auth, nc=00000002, response="{}", cnonce="{}"'.format(nonce, uri, response, cnonce)
response = requests.get(url, headers={'Authorization': header})
print(response.text)

