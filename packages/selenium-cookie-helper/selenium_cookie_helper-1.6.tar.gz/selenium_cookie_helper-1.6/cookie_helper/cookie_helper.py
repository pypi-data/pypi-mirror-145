from selenium import webdriver
import json


def save_cookies(driver):
	input('Press [Return] to save cookies now! \n')
	all_cookies = driver.get_cookies()
	json_string = json.dumps(all_cookies)

	with open('custom_cookies.json', 'w') as f:
		f.write(json_string)

	print(f'Ok.! {len(all_cookies)} cookies written to file (custom_cookies.json)')

	driver.quit()


def load_cookies(driver, url):
	driver.get(url)

	with open('custom_cookies.json') as f:
		all_cookies = json.load(f)

	for cookie in all_cookies:
		driver.add_cookie(cookie)

	driver.refresh()
	
	return driver


''' ========================== EXAMPLE USAGE ==========================
driver = webdriver.Chrome()
save_cookies(driver)
driver = load_cookies(driver, 'https://www.discogs.com')
    =================================================================== '''
