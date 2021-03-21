import shutil
import urllib.request

import requests
from bs4 import BeautifulSoup


def download_fmi_pdf(url):
    schedule_name = 'new_' + url.split('/')[-1]
    with urllib.request.urlopen(url) as response, open('resources/' + schedule_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    return schedule_name


def get_fmi_pdf(option='latest'):
    """
    :param option: ['latest', 's1', 's2'] - PDF to downlaod
    :return name of the downloaded file
    """
    page = requests.get("https://fmi.unibuc.ro/orar/")
    soup = BeautifulSoup(page.content, 'html.parser')

    nav_info = soup.find_all(class_="nv-content-wrap entry-content")[0]
    links_a_element = nav_info.find_all("a")
    links = [(link.get_text(), link['href']) for link in links_a_element]

    s1_link = ""
    s2_link = ""
    for link in links:
        if 'orar_grupe' in link[1]:
            if 's1' in link[1]:
                s1_link = link[1]
            elif 's2' in link[1]:
                s2_link = link[1]

    if option == 's1':
        if s1_link:
            return download_fmi_pdf(s1_link)
    elif option == 's2':
        if s2_link:
            return download_fmi_pdf(s2_link)
    else:
        if s2_link:
            return download_fmi_pdf(s2_link)
        elif s1_link:
            return download_fmi_pdf(s1_link)
    return "LinksNotFound"
