from django.shortcuts import render
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


SCRAPE_URL = "https://zuscoffee.com/category/store/melaka"
state_classes = []


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
	driver.get(SCRAPE_URL)
	found_states = driver.find_elements(By.CLASS_NAME, "state")
	for fs in found_states:
		state_class = fs.get_attribute("class")
		state_class = state_class.split(" ")[1]
		state_classes.append(state_class)


def scrape_zus_website():
	driver = prepare_driver()
	get_state_classes(driver)
	wait = WebDriverWait(driver, 10)

	for sc in state_classes:
		try:
			loaded_url = driver.current_url
			wait.until(EC.url_to_be(loaded_url))

			found_state = driver.find_element(By.CLASS_NAME, sc)
			found_state.click()
		except Exception as e:
			print(f"Page did not load properly: {str(e)}")

	driver.quit()
