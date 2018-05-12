#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import urllib
from urlparse import urljoin
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

def reader(file_name, file_html_ref):
    try:
        html=requests.get(url).text
        soup=BeautifulSoup(html, 'html.parser')
        link=soup.find(attrs={'data-track':file_html_ref})      # needs to be done this way rather than with soup.find(data-track="download-data-page|All EduBase data)|download") as HTML 5 attributes like data-* have names that can’t be used as keyword arguments
        link_url=link.get('href')
        link_text=link.get_text()
        print float(re.findall("\w+[^\w\s]\w", link_text)[0])       # file size (MB)
        csv_file=requests.get(link_url)
        csv_file=csv_file.iter_lines()      # is required in order for csv file to be read correctly, without errors caused by new-line characters
        reader=csv.DictReader(csv_file)
        for row in reader:
            print row
    except:
        print('Failed to read ' + file_name)
    return

for file in file_list:
    reader(file['name'],file['html_ref']);
