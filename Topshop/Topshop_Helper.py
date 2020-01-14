from bs4 import BeautifulSoup
import requests

# url = "https://www.topshop.com/en/tsuk/category/clothing-427/dresses-442?currentPage=24"
# page = requests.get(url)
# soup = BeautifulSoup(page.content, 'lxml')
# print(soup.find('div', {"data-product-number": "1"}))

a= "https://www.google.com/search?sxsrf=ACYBGNTHCtlGMsL7kcL7lg3fJIPPzkrmhA:1578997292755&q=food+near+me&npsic=0&rflfq=1&rlha=0&rllag=1531458,103746904,1907&tbm=lcl&ved=2ahUKEwj6sPGl74LnAhUbxzgGHSz_CT8QjGp6BAgMEEc&tbs=lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!1m4!1u16!2m2!16m1!1e1!1m4!1u16!2m2!16m1!1e2!2m1!1e2!2m1!1e16!2m1!1e3!3sIAE,lf:1,lf_ui:9&rldoc=1#rlfi=hd:;si:18340190441292219737,l,Cgxmb29kIG5lYXIgbWUiA5ABAVoUCgRmb29kIgxmb29kIG5lYXIgbWU,y,RKkU8LGXGkQ;mv:[[1.5686444,103.7879111],[1.4573794,103.7061648]] "
b = "https://www.google.com/search?sxsrf=ACYBGNTHCtlGMsL7kcL7lg3fJIPPzkrmhA:1578997292755&q=food+near+me&npsic=0&rflfq=1&rlha=0&rllag=1531458,103746904,1907&tbm=lcl&ved=2ahUKEwj6sPGl74LnAhUbxzgGHSz_CT8QjGp6BAgMEEc&tbs=lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!1m4!1u16!2m2!16m1!1e1!1m4!1u16!2m2!16m1!1e2!2m1!1e2!2m1!1e16!2m1!1e3!3sIAE,lf:1,lf_ui:9&rldoc=1#rlfi=hd:;si:12623288887811360782,l,Cgxmb29kIG5lYXIgbWUiA5ABAUjp1OLDrI-AgAhaGgoEZm9vZBAAGAEYAiIMZm9vZCBuZWFyIG1l,y,bf59heuTdXU;mv:[[1.5686444,103.7879111],[1.4573794,103.7061648]]"