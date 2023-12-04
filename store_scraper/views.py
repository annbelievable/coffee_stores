from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import celery_app
from store_scraper.models import CoffeeStore


SCRAPE_URL = "https://zuscoffee.com/category/store/melaka"
state_classes = []


def index(request):
	context = {"title": "Store Scraper"}
	scrape_zus_website.delay()
	return render(request, "store_scraper/index.html", context)


def get_driver_options():
	options = Options()
	options.add_argument('--no-sandbox')
	options.add_argument("--headless")
	options.add_argument('--disable-dev-shm-usage')
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
		try:
			CoffeeStore.objects.update_or_create(
				name=name,
				address=address,
			)
		except:
			print(f"An error occurred: Store name: {name}, Address: {address}")


def get_next_page(driver):
	has_next_page = True
	while has_next_page:
		wait_for_page_load(driver)
		get_page_articles(driver)
		try:
			next_page = driver.find_element(By.CSS_SELECTOR, ".page-numbers.next")
			next_page_url = next_page.get_attribute("href")
			if next_page_url is not None:
				driver.get(next_page_url)
			else:
				has_next_page = False
		except Exception as e:
			has_next_page = False


def get_all_stores(driver):
	for sc in state_classes:
		try:
			wait_for_page_load(driver)
			found_state = driver.find_element(By.CLASS_NAME, sc)
			driver.execute_script("arguments[0].dispatchEvent(new Event('click'));", found_state)
			get_next_page(driver)
		except Exception as e:
			print(f"Page did not load properly: {str(e)}")


@celery_app.task()
def scrape_zus_website():
	driver = prepare_driver()
	driver.get(SCRAPE_URL)
	get_state_classes(driver)
	get_all_stores(driver)
	driver.quit()
