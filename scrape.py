from bs4 import BeautifulSoup
import requests
import time
import os
import subprocess
import shlex
import urlparse

base_url = "http://www.lawsofindia.org"

cookie = {"PHPSESSID": "c9fb7f2770f39540a098ea285189b456"}

headers = {
    "Host": " www.lawsofindia.org",
    "User-Agent": " Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0",
    "Accept": " text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": " gzip, deflate",
    "DNT": " 1",
    "Referer": " http://www.lawsofindia.org/state/27/West%20Bengal.html",
    "Cookie": " PHPSESSID=25c803c8f07e5915de1af871ca2936c2",
    "Connection": " keep-alive",
}

def get_pdf_url(href):
    query = urlparse.urlparse(href).query
    return "{}/pdf/{}".format(base_url, urlparse.parse_qs(query)['file'][0])


def get_pdf_list(state, url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    pdfs = [get_pdf_url(base_url + x['href']) for x in soup.find_all('a') if '.pdf' in x['href']]

    with open("{}.txt".format(state), 'w') as fp:
        fp.write("\n".join(pdfs))


def download_pdfs(state, headers):
    infile = "{}.txt".format(state)
    dir = state.lower().replace(" ", "_")

    cmd = "aria2c -i {} -d {}".format(infile, dir)
    subprocess.call(shlex.split(cmd))

html = requests.get(base_url).text
soup = BeautifulSoup(html, 'html.parser')

state_pages = [(x.string, x['href']) for x in soup.find_all('a') if 'state/' in x['href']]

states = [x[0] for x in state_pages]

for state, url in state_pages[::-1]:
    time.sleep(1)  # Sleep for 1 sec so that you appear human
    state_soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    alpha = [x['href'] for x in state_soup.find_all('a') if 'alpha/' in x['href']][0]
    get_pdf_list(state, base_url + alpha)

    headers['Referer'] = url
    download_pdfs(state, headers)





# TODO: setup python auto completion
