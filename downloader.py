#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urllib
from bs4 import BeautifulSoup

url='https://get-information-schools.service.gov.uk/Downloads'
file_list=(
    {
        'name':'All EduBase data',
        'html_ref':'download-data-page|All EduBase data)|download'
    },
    {
        'name':'Links',
        'html_ref':'download-data-page|All EduBase data links)|download'
    },
    {
        'name':'Group links',
        'html_ref':'download-data-page|Academy sponsor and trust links)|download'
    }
)

def downloader(file_name, file_html_ref):
    try:
        html=requests.get(url).text
        soup=BeautifulSoup(html, 'html.parser')
        link=soup.find(attrs={'data-track':file_html_ref})      # needs to be done this way rather than with soup.find(data-track="download-data-page|All EduBase data)|download") as HTML 5 attributes like data-* have names that can’t be used as keyword arguments
        link_url=link.get('href')
        link_filename=link_url.rsplit('/', 1)[-1]
        file=urllib.URLopener()
        file.retrieve(link_url, link_filename)
    except:
        print('Failed to download ' + file_name)
    return

for file in file_list:
    downloader(file['name'],file['html_ref']);
