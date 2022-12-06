from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from termcolor import colored, cprint
import datetime
import csv
import argparse
import numexpr		

def initSession(drv = 'Firefox'):
	if drv == 'Chrome':
		from selenium.webdriver.chrome.options import Options
		from selenium.webdriver.chrome.service import Service as ChromeService
		from webdriver_manager.chrome import ChromeDriverManager
		chromeOptions = Options()
		chromeOptions.headless = True
		chromeOptions.add_argument("--disable-gpu")
		chromeOptions.add_argument(
			"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
		driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chromeOptions)
	
	elif drv == 'Firefox':
		from selenium.webdriver.firefox.options import Options
		from selenium.webdriver.firefox.service import Service as FirefoxService
		from webdriver_manager.firefox import GeckoDriverManager
		firefoxOptions = Options()  
		firefoxOptions.add_argument("--headless") 
		firefoxOptions.add_argument("--window-size=1920,1080")
		firefoxOptions.add_argument('--start-maximized')
		firefoxOptions.add_argument('--disable-gpu')
		firefoxOptions.add_argument('--no-sandbox')
		driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefoxOptions)
	else:
		driver = None
	return driver

def FAIRChecker(d, res):
	"""
	Author(s):
	- Thomas Rosnet (thomas.rosnet@france-bioinformatique.fr)
	- Alban Gaignard (alban.gaignard@univ-nantes.fr)
	- Marie-Dominique Devignes (marie-dominique.devignes@loria.fr)
	
	Source: https://fair-checker.france-bioinformatique.fr/about
	"""
	FAIRChecker_score = {
		'resource': res[0],
		'tool': 'FAIR-Checker',
		'F': '',
		'A': '',
		'I': '',
		'R': '',
		'report_url': '',
		'datetime': str(datetime.datetime.today()),
		'status':'success'
	}
	try:
		cprint('  FAIR-Checker: Starting...', 'white', attrs=[], end='\r')
		
		d.get('https://fair-checker.france-bioinformatique.fr/check')
		input = d.find_element(By.XPATH,'//*[@id="url"]')
		input.send_keys(res)
		sleep(2)
		d.find_element(By.XPATH, '//*[@id="btn_test_all"]').click()

		WebDriverWait(d, 60).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '.vcenter .is-loading')))
	except Exception as e:
		print(e)
		FAIRChecker_score['status'] = 'fail'
		cprint('FAIR-Checker: FAILED     ', 'red', attrs=['bold'])
	else:
		sleep(3)
		FAIR = {
			'F': ['#row_status_FC_0', '#row_status_FC_1', '#row_status_FC_2', '#row_status_FC_3'],
			'A': ['#row_status_FC_4'],
			'I': ['#row_status_FC_5', '#row_status_FC_6', '#row_status_FC_7'],
			'R': ['#row_status_FC_8', '#row_status_FC_9', '#row_status_FC_10']
		}
		f,a,i,r = 0,0,0,0
		for fair_F in FAIR['F']:
			if d.find_element(By.CSS_SELECTOR, fair_F).text == 'Success':
				f += 1
		for fair_A in FAIR['A']:
			if d.find_element(By.CSS_SELECTOR, fair_A).text == 'Success':
				a += 1
		for fair_I in FAIR['I']:
			if d.find_element(By.CSS_SELECTOR, fair_I).text == 'Success':
				i += 1
		for fair_R in FAIR['R']:
			if d.find_element(By.CSS_SELECTOR, fair_R).text == 'Success':
				r += 1

		FAIRChecker_score['F'] = '{}/{}'.format(f, len(FAIR['F']))
		FAIRChecker_score['A'] = '{}/{}'.format(a, len(FAIR['A']))
		FAIRChecker_score['I'] = '{}/{}'.format(i, len(FAIR['I']))
		FAIRChecker_score['R'] = '{}/{}'.format(r, len(FAIR['R']))
		cprint('\r  FAIR-Checker: Finished!  ', 'white', attrs=[])
	return FAIRChecker_score

def F_UJI(d, res):
	"""
	Author(s):
	- Anusuriya Devaraju
	- Robert Huber
	
	Source: https://www.f-uji.net/index.php?action=about
	"""
	FUJI_score = {
		'resource': res[0],
		'tool': 'F-UJI',
		'F': '',
		'A': '',
		'I': '',
		'R': '',
		'report_url': '',
		'datetime': str(datetime.datetime.today()),
		'status':'success'
	}
	try:
		cprint('  F-UJI: Starting...', 'white', attrs=[], end='\r')
		d.get('https://www.f-uji.net/index.php?action=test')
		input = d.find_element(By.XPATH,'//*[@id="pid"]')
		input.send_keys(res)
		sleep(2)
		d.find_element(By.XPATH, '//*[@id="assessment_form"]/div/form/div[4]/button').click()
		WebDriverWait(d, 60).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '#loader')))
	except Exception as e:
		# print(e)
		FUJI_score['status'] = 'fail'
		cprint('\r  F-UJI: FAILED!     ', 'red', attrs=['bold'])
	else:
		sleep(1)
		FAIR = {
			'F': '//*[@id="fujiresults"]/div[4]/div[2]/table/tbody/tr[2]/td[1]',
			'A': '//*[@id="fujiresults"]/div[4]/div[2]/table/tbody/tr[3]/td[1]',
			'I': '//*[@id="fujiresults"]/div[4]/div[2]/table/tbody/tr[4]/td[1]',
			'R': '//*[@id="fujiresults"]/div[4]/div[2]/table/tbody/tr[5]/td[1]'
		}
		FUJI_score['F'] = str(d.find_element(By.XPATH, FAIR['F']).text).replace(' of ', '/')
		FUJI_score['A'] = str(d.find_element(By.XPATH, FAIR['A']).text).replace(' of ', '/')
		FUJI_score['I'] = str(d.find_element(By.XPATH, FAIR['I']).text).replace(' of ', '/')
		FUJI_score['R'] = str(d.find_element(By.XPATH, FAIR['R']).text).replace(' of ', '/')
		cprint('\r  F-UJI: Finished!  ', 'white', attrs=[])
	return FUJI_score

def FAIREnough(d, res):
	"""
	Author(s): Institute of Data Science at Maastricht University 2020.
	
	Source: https://fair-enough.semanticscience.org/about
	"""
	FAIREnough_score = {
		'resource': res[0],
		'tool': 'FAIR-Enough',
		'F': '',
		'A': '',
		'I': '',
		'R': '',
		'report_url': '',
		'datetime': str(datetime.datetime.today()),
		'status':'success'
	}
	try:
		d.get('https://fair-enough.semanticscience.org/')
		d.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/form/div[1]/div[1]/div/div').click()
		WebDriverWait(d, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="menu-"]/div[3]/ul')))
		WebDriverWait(d, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="menu-"]/div[3]/ul/li[1]')))
	except Exception as e:
		print(e)
	else:
		d.find_element(By.XPATH, '//*[@id="menu-"]/div[3]/ul/li[1]').click()

	try:
		cprint('  FAIR-Enough: Starting...', 'white', attrs=[], end='\r')
		input = d.find_element(By.XPATH,'//*[@id="urlToEvaluate"]')
		input.send_keys(res)
		sleep(2)
		d.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div/form/button').click()
		WebDriverWait(d, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div/div/div[3]')))
	except Exception as e:
		# print(e)
		FAIREnough_score['status'] = 'fail'
		cprint('\r  FAIR-Enough: FAILED!     ', 'red', attrs=['bold'])
	else:
		sleep(1)
		FAIR = {
			'F': '//*[@id="root"]/div/div/div/div/div[4]/div[2]//h6/*[name()="svg" and @data-testid="CheckCircleIcon"]',
			'A': '//*[@id="root"]/div/div/div/div/div[5]/div[2]//h6/*[name()="svg" and @data-testid="CheckCircleIcon"]',
			'I': '//*[@id="root"]/div/div/div/div/div[6]/div[2]//h6/*[name()="svg" and @data-testid="CheckCircleIcon"]',
			'R': '//*[@id="root"]/div/div/div/div/div[7]/div[2]//h6/*[name()="svg" and @data-testid="CheckCircleIcon"]'
		}
		
		FAIREnough_score['F'] = '{}/{}'.format(len(d.find_elements(By.XPATH, FAIR['F'])), '6')
		FAIREnough_score['A'] = '{}/{}'.format(len(d.find_elements(By.XPATH, FAIR['A'])), '3')
		FAIREnough_score['I'] = '{}/{}'.format(len(d.find_elements(By.XPATH, FAIR['I'])), '5')
		FAIREnough_score['R'] = '{}/{}'.format(len(d.find_elements(By.XPATH, FAIR['R'])), '2')
		FAIREnough_score['report_url'] = d.current_url
		cprint('\r  FAIR-Enough: Finished!  ', 'white', attrs=[])
	return FAIREnough_score

def isFAIR():
	parser = argparse.ArgumentParser()
	parser.add_argument("resource", help="CSV list or url")
	parser.add_argument('-drv', '--driver', default='Firefox', help='Driver type - Chrome or Firefox')
	args = parser.parse_args()
	
	driver = initSession(args.driver)
	reports = []
	reports_aggregated = []
	if '.csv' in args.resource:
		with open(args.resource, mode='r') as resources_list:
			resources = list(csv.reader(resources_list, delimiter=';'))
	else:
		resources = [args.resource]
		print(resources)

	for i,resource in enumerate(resources):
		score = {}
		try:
			cprint('[ ASSESSING RESOURCE ' + str(i+1) + '/' + str(len(resources)) + ' ]', 'white', attrs=['bold'])
			cprint('  URL: ' + str(resource[0]), 'white', attrs=[])
			
			score['FAIRChecker'] =  FAIRChecker(driver, resource)
			score['F-UJI'] = F_UJI(driver, resource)
			score['FAIREnough'] = FAIREnough(driver, resource)
			
			reports.append(score['FAIRChecker'])
			reports.append(score['F-UJI'])
			reports.append(score['FAIREnough'])
			
			if 'fail' not in {score['FAIRChecker']['status'], score['F-UJI']['status'],score['FAIREnough']['status']}:
				report = {
					'resource': str(resource[0]),
					'F': round((numexpr.evaluate(score['FAIRChecker']['F']) + numexpr.evaluate(score['F-UJI']['F']) + numexpr.evaluate(score['FAIREnough']['F']))/3, 2),
					'A': round((numexpr.evaluate(score['FAIRChecker']['A']) + numexpr.evaluate(score['F-UJI']['A']) + numexpr.evaluate(score['FAIREnough']['A']))/3, 2),
					'I': round((numexpr.evaluate(score['FAIRChecker']['I']) + numexpr.evaluate(score['F-UJI']['I']) + numexpr.evaluate(score['FAIREnough']['I']))/3, 2),
					'R': round((numexpr.evaluate(score['FAIRChecker']['R']) + numexpr.evaluate(score['F-UJI']['R']) + numexpr.evaluate(score['FAIREnough']['R']))/3, 2),
					'FAIR_score': '',
					'datetime': str(datetime.datetime.today())
				}
				report['FAIR_score'] = report['F'] + report['A'] + report['I'] + report['R']
				reports_aggregated.append(report)
			
			print('\n')
		except Exception as e:
			print(e)
		sleep(1)

	try:
		with open('./reports/' + str(datetime.datetime.now().strftime("%d-%m-%Y %H%M")) + '.csv', 'w') as csvReport:
			r = csv.DictWriter(csvReport, fieldnames= ['resource','tool','F','A','I','R','report_url','datetime','status'])
			r.writeheader()
			for item in reports:
				r.writerow(item)
	
		with open('./reports/aggr_' + str(datetime.datetime.now().strftime("%d-%m-%Y %H%M")) + '.csv', 'w') as csvReport:
			r = csv.DictWriter(csvReport, fieldnames= ['resource','F','A','I','R','FAIR_score','datetime'])
			r.writeheader()
			for item in reports_aggregated:
				r.writerow(item)
	except Exception as e:
		print(e)

	driver.close()
	cprint('[ DONE ] Report name: ' + str(datetime.datetime.now().strftime("%d-%m-%Y %H%M")) + '.csv', 'green', attrs=['bold'])

if __name__ == "__main__":
	isFAIR()
