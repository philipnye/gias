#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import re
import json
import requests
import datetime
from bs4 import BeautifulSoup

url='https://get-information-schools.service.gov.uk/Downloads'
file_list=(
	{
		'name':'edubasealldata',
		'html_ref':'download-data-page|All EduBase data)|download'
	},
	{
		'name':'links',
		'html_ref':'download-data-page|All EduBase data links)|download'
	},
	{
		'name':'grouplinks',
		'html_ref':'download-data-page|Academy sponsor and trust links)|download'
	}
)

estab_phase=[]
estab_type=[]
estab_type_group=[]
estab_status=[]
group_type=[]

def reader(file_name, file_html_ref):
	column_names=[]
	column_names=data_structure[file_name]['columns'].split('; ')
	html=requests.get(url).text
	soup=BeautifulSoup(html, 'html.parser')
	link=soup.find(attrs={'data-track':file_html_ref})		# needs to be done this way rather than with soup.find(data-track='download-data-page|All EduBase data)|download') as HTML 5 attributes like data-* have names that can’t be used as keyword arguments
	link_url=link.get('href')
	link_text=link.get_text()
	prev_file_size=data_structure[file_name]['size']
	file_size=re.findall('[0-9]+[.]*[0-9]*', link_text)[0] + 'MB'
	if float(file_size[:-2])<float(prev_file_size[:-2]):
		log.write(file_name + ' file is smaller than previous version: ' + file_size + ' versus ' + prev_file_size + '\n')
	data_structure[file_name]['size']=file_size
	csv_file=requests.get(link_url)
	csv_file=csv_file.iter_lines()		# is required in order for csv file to be read correctly, without errors caused by new-line characters
	reader=csv.DictReader(csv_file)
	for column in reader.fieldnames:
		if column not in column_names:
			log.write('New column in ' + file_name + ' file: ' + column + '\n')
			column_names.append(column)
			data_structure[file_name]['columns']='; '.join(str(x) for x in column_names)
	if file_name=='edubasealldata':
		for row in reader:
			if row['EstablishmentTypeGroup (name)'].lower() not in estab_type_group:
				log.write('New estab_type_group: ' + row['EstablishmentTypeGroup (name)'] + '\n')
				estab_type_group.append(row['EstablishmentTypeGroup (name)'].lower())
			if row['EstablishmentStatus (name)'].lower() not in estab_status:
				log.write('New estab_status: ' + row['EstablishmentStatus (name)'] + '\n')
				estab_status.append(row['EstablishmentStatus (name)'].lower())
			if row['PhaseOfEducation (name)'].lower() not in estab_phase:
				log.write('New estab_phase: ' + row['PhaseOfEducation (name)'] + '\n')
				estab_phase.append(row['PhaseOfEducation (name)'].lower())
			if row['TypeOfEstablishment (name)'].lower() not in estab_type:
				log.write('New estab_type: ' + row['TypeOfEstablishment (name)'] + '\n')
				estab_type.append(row['TypeOfEstablishment (name)'].lower())
	if file_name=='grouplinks':
		for row in reader:
			if row['Group Type'].lower() not in group_type:
				log.write('New group_type: ' + row['Group Type'] + '\n')
				group_type.append(row['Group Type'].lower())
			if row['PhaseOfEducation (name)'].lower() not in estab_phase:
				log.write('New estab_phase: ' + row['PhaseOfEducation (name)'] + '\n')
				estab_phase.append(row['PhaseOfEducation (name)'].lower())
			if row['TypeOfEstablishment (name)'].lower() not in estab_type:
				log.write('New estab_type: ' + row['TypeOfEstablishment (name)'] + '\n')
				estab_type.append(row['TypeOfEstablishment (name)'].lower())
	return

with open('log.txt', 'a') as log:
	log.write('\n'+ '\n'+str(datetime.datetime.now())+ '\n')
	with open('data_structure.json', 'r+ ') as data_structure_json:
		data_structure=json.load(data_structure_json)
		with open('allowable_values.json', 'r+ ') as allowable_values_json:
			allowable_values=json.load(allowable_values_json)
			estab_type_group=allowable_values['estab_type_group'].split('; ')
			estab_status=allowable_values['estab_status'].split('; ')
			estab_phase=allowable_values['estab_phase'].split('; ')
			estab_type=allowable_values['estab_type'].split('; ')
			group_type=allowable_values['group_type'].split('; ')
			for file in file_list:
				reader(file['name'],file['html_ref'])
			estab_type_group.sort()
			estab_status.sort()
			estab_phase.sort()
			estab_type.sort()
			group_type.sort()
			data_structure_json.seek(0)		# needed to fend off a python 2.7 error when opening a file for reading *and* writing
			json.dump(data_structure,data_structure_json,indent=2,sort_keys=True)
			allowable_values['estab_type_group']='; '.join(str(x) for x in estab_type_group)
			allowable_values['estab_status']='; '.join(str(x) for x in estab_status)
			allowable_values['estab_phase']='; '.join(str(x) for x in estab_phase)
			allowable_values['estab_type']='; '.join(str(x) for x in estab_type)
			allowable_values['group_type']='; '.join(str(x) for x in group_type)
			allowable_values_json.seek(0)
			json.dump(allowable_values,allowable_values_json,indent=2,sort_keys=True)
