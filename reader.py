#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import re
import requests
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

group_type=[]
estab_phase=[]
estab_type=[]

estab_type_group=[]
estab_status=[]
estab_phase=[]
estab_type=[]

def reader(file_name, file_html_ref):
	column_names=[]
	try:
		html=requests.get(url).text
		soup=BeautifulSoup(html, 'html.parser')
		link=soup.find(attrs={'data-track':file_html_ref})	  # needs to be done this way rather than with soup.find(data-track="download-data-page|All EduBase data)|download") as HTML 5 attributes like data-* have names that can’t be used as keyword arguments
		link_url=link.get('href')
		link_text=link.get_text()
		print file_name
		print re.findall('[0-9]+[.]*[0-9]*', link_text)[0]+'MB'	   # file size (MB)
		csv_file=requests.get(link_url)
		csv_file=csv_file.iter_lines()	  # is required in order for csv file to be read correctly, without errors caused by new-line characters
		reader=csv.DictReader(csv_file)
		for column in reader.fieldnames:
			column_names.append(column)
		print column_names
		if file_name=='All EduBase data':
			for row in reader:
				if row['EstablishmentTypeGroup (name)'].lower() not in estab_type_group:
					estab_type_group.append(row['EstablishmentTypeGroup (name)'].lower())
				if row['EstablishmentStatus (name)'].lower() not in estab_status:
					estab_status.append(row['EstablishmentStatus (name)'].lower())
				if row['PhaseOfEducation (name)'].lower() not in estab_phase:
					estab_phase.append(row['PhaseOfEducation (name)'].lower())
				if row['TypeOfEstablishment (name)'].lower() not in estab_type:
					estab_type.append(row['TypeOfEstablishment (name)'].lower())
			print estab_type_group
			print estab_status
			print estab_phase
			print estab_type
		if file_name=='Group links':
			for row in reader:
				if row['Group Type'].lower() not in group_type:
					group_type.append(row['Group Type'].lower())
				if row['PhaseOfEducation (name)'].lower() not in estab_phase:
					estab_phase.append(row['PhaseOfEducation (name)'].lower())
				if row['TypeOfEstablishment (name)'].lower() not in estab_type:
					estab_type.append(row['TypeOfEstablishment (name)'].lower())
			print group_type
			print estab_phase
			print estab_type
	except:
		print('Failed to read ' + file_name)
	return

for file in file_list:
	reader(file['name'],file['html_ref']);
