from bs4 import BeautifulSoup
import requests
import time
import os
import urlparse

base_url = "http://www.lawsofindia.org"
base_dir = "."

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

    return pdfs


def download_pdfs(pdfs, state, headers):
    dir_name = state.lower().replace(" ", "_")
    dir_path = "{}/{}".format(base_dir, dir_name)

    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)

    for pdf in pdfs:
        fname = "{}/{}".format(dir_path, pdf.split('/')[-1])
        if os.path.exists(fname):
            print("{} already downloaded".format(fname))
            continue

        r = requests.get(pdf, headers=headers)

        with open(fname, 'wb') as fp:
            print("writing {}".format(fname))
            fp.write(r.content)


html = requests.get(base_url).text
soup = BeautifulSoup(html, 'html.parser')

state_pages = [(x.string, x['href']) for x in soup.find_all('a') if 'state/' in x['href']]

states = [x[0] for x in state_pages]

for state, url in state_pages[::-1]:
    time.sleep(1)  # Sleep for 1 sec so that you appear human
    state_soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    alpha = [x['href'] for x in state_soup.find_all('a') if 'alpha/' in x['href']][0]
    pdfs = get_pdf_list(state, base_url + alpha)

    headers['Referer'] = url
    download_pdfs(pdfs, state, headers)
