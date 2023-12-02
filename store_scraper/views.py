from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


SCRAPE_URL = "https://zuscoffee.com/category/store/melaka"
state_classes = []
stores = []


# Create your views here.
def index(request):
	context = {"title": "Store Scraper"}
	print("Starting scraping")
	scrape_zus_website()
	print("Finished scraping")
	return render(request, "store_scraper/index.html", context)
def get_driver_options():
	# configure webdriver
	options = Options()
	options.headless = True
	options.add_argument("--window-size=1920,1080")
	options.add_argument("start-maximized")
	return options


def prepare_driver():
	options = get_driver_options()
	driver = webdriver.Chrome(options=options)
	return driver


def get_state_classes(driver):
	found_states = driver.find_elements(By.CLASS_NAME, "state")
	for fs in found_states:
		state_class = fs.get_attribute("class")
		state_class = state_class.split(" ")[1]
		state_classes.append(state_class)


def wait_for_page_load(driver):
	wait = WebDriverWait(driver, 10)
	wait.until(EC.visibility_of_element_located((By.ID, "fc_frame")))


def get_page_articles(driver):
	articles = driver.find_elements(By.TAG_NAME, "article")
	for article in articles:
		article_details = article.find_elements(By.CSS_SELECTOR, ".elementor-widget-container p")
		name = article_details[0].text
		address = article_details[1].text
		stores.append({name: name, address:address})


def get_next_page(driver):
	has_next_page = True
	while has_next_page:
		wait_for_page_load(driver)
		print(f"SCRAPE: {driver.current_url}")
		get_page_articles(driver)
		#try:
		try:
			next_page = driver.find_element(By.CSS_SELECTOR, ".page-numbers.next")
			next_page_url = next_page.get_attribute("href")
			if next_page_url is not None:
				driver.get(next_page_url)
				print("NEXT PAGE")
			else:
				has_next_page = False
		except Exception as e:
			has_next_page = False
			print(f"NO NEXT PAGE")


def get_all_stores(driver):
	for sc in state_classes:
		try:
			print(f"CURRENT PAGE: {driver.current_url}, GOING TO {sc}")
			wait_for_page_load(driver)
			found_state = driver.find_element(By.CLASS_NAME, sc)
			driver.execute_script("arguments[0].dispatchEvent(new Event('click'));", found_state)
			get_next_page(driver)
		except Exception as e:
			print(f"Page did not load properly: {str(e)}")


def scrape_zus_website():
	driver = prepare_driver()
	driver.get(SCRAPE_URL)
	get_state_classes(driver)
	get_all_stores(driver)
	driver.quit()