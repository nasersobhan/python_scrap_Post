from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pickle
import os
import random
import math
import yaml
import sys
import argparse

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)

driver = webdriver.Chrome(cfg['WebDriverPath'])

def login_and_search(tuser, tpassword):	
	#open login page
	driver.get('https://team.website.com/#/projects/405949/time')
	#enter username
	email = driver.find_element_by_xpath('//*[@id="loginemail"]')
	email.send_keys(tuser) # change it to your username
	#enter password
	password = driver.find_element_by_xpath('//*[@id="loginpassword"]')
	password.send_keys(tpassword) #change it to your password
	#click login
	login = driver.find_element_by_xpath('//*[@id="app"]/div[1]/section/div[2]/div[2]/div/div/div/form/div[2]/button')
	login.click()


	return driver
def login_and_search_slack(suser, spassword):	
	#open login page
	driver_slack.get('https://mycompany.slack.com/')
	#maximize the window
	#driver.maximize_window()
	#enter username
	email = driver_slack.find_element_by_xpath('//*[@id="email"]')
	email.send_keys(suser) # change it to your username
	#enter password
	password = driver_slack.find_element_by_xpath('//*[@id="password"]')
	password.send_keys(spassword) #change it to your password
	#click login
	login = driver_slack.find_element_by_xpath('//*[@id="signin_btn"]')
	login.click()


	return driver
def get_page_links(linkz, itemnumber, CBList = 0):

	driver.get(linkz)
	time.sleep(10)
	soup = BeautifulSoup(driver.page_source, 'lxml')
	print('Collecting Information...')
	data = []
	table = soup.find_all('table', attrs={'class':'w-time-grid'})
	#table_body = table.find('tbody')
	project = soup.find('h1', attrs={'class':'w-header-titles__project-name'}).text.strip()
	listdate = soup.find_all('h4', attrs={'class':'gridHeading subTitle'})
	listdate = listdate[itemnumber].text.strip()
	rows = table[itemnumber].find_all('tr')
	tasks = []
	del rows[0]
	for row in rows:
		cols = row.find_all('td')
		tasks.append(cols[1].text.strip())
		cols = [ele.text.strip() for ele in cols]
		data.append([ele for ele in cols if ele])
	#print(data)
	table2 = soup.find_all('table', attrs={'class':'w-time-list__totals-table'})
	rows = table2[itemnumber].find_all('tr')
	data2 = []
	for row in rows:
		cols = row.find_all('td')
		cols = [ele.text.strip() for ele in cols]
		data2.append([ele for ele in cols if ele])
	print('cleaning Information...')
	texttopost = '*' + listdate + '*\n'
	texttopost = texttopost + '*_' + project + '_*\n'
	texttopost = texttopost + '+++ ' + '\n+++ '.join(tasks) + '\n'
	texttopost = texttopost + 'Total: `' + rows[0].find_all('td')[1].text.strip() + '`\n'
	texttopost = texttopost + 'None Billable: `' + rows[2].find_all('td')[1].text.strip() + '`\n'
	texttopost = texttopost + 'Billable: `' + rows[3].find_all('td')[1].text.strip() + '`\n'
	totalhours = float(rows[0].find_all('td')[2].text.strip())
	if CBList != 0:
		listCBitems = CBList.split(',') # ['Drupal','Wordpress','Android','Server','Youtube Intergration']
	if  totalhours < 8:
		CBhours = str(float(8 - totalhours))
		Numbx = CBhours.split('.')
		d, i = (Numbx[1], Numbx[0]) #math.modf(CBhours)
		minu = str(int(0.6 * int(d)))
		hour = str(int(i))
		randomtitle = ''
		if listCBitems:
			randomtitle = '+++ ' + str(listCBitems[random.randrange(len(listCBitems))]) + ' '
		texttopost = texttopost + '*_Capacity building_*\n' + randomtitle + ' `' + hour  + ' Hours And ' + minu[:2]  + ' Minutes`\n' 
	print('Generating Text...')
	print(texttopost)
	return texttopost

def post_toslack(linkz, texttopost):
	print('openings Channel...')
	driver_slack.get(linkz)
	time.sleep(20)
	print('Posting Text...')
	boxx = driver_slack.find_element_by_xpath('//*[@id="undefined"]')
	boxx.send_keys(texttopost) # change it to your username


########################################### MAIN ###################################

print('Opening TeamWork...')
login_and_search(cfg['teamuser'],cfg['teampassword'])
time.sleep(20)
print('Going to Time Page...')
texttopost = get_page_links(cfg['projectURL'], cfg['ListNumber'], cfg['RandomCBSubjects'])
driver.quit()
print('TeamWork Closed.')
print('Opening Slack...')
driver_slack = webdriver.Chrome(cfg['WebDriverPath'])
#time.sleep(10)
print('Login Slack...')
login_and_search_slack(cfg['slackuser'],cfg['slackpassword'])
#time.sleep(20)
post_toslack(cfg['slackchannelURL'], texttopost)
#driver.quit()

####################################################################################


