import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.headless = False
#options.add_argument('window-size=1920x1080')

web = 'https://www.audible.com/search'
path = '/path/to/driver'
driver = webdriver.Chrome(path, options=options)
driver.get(web)
driver.maximize_window()

# pagination
pagination = driver.find_element_by_xpath('//ul[contains(@class,"pagingElements")]')
pages = pagination.find_elements_by_tag_name('li')
last_page = int(pages[-2].text)

current_page = 1

book_title = []
book_author = []
book_length = []

while current_page <= last_page:

    container = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
        (By.CLASS_NAME, 'adbl-impression-container')
    ))

    #container = driver.find_element_by_class_name('adbl-impression-container')
    products = WebDriverWait(container, 5).until(EC.presence_of_all_elements_located(
        (By.XPATH, './li')
    ))
    #products = container.find_elements_by_xpath('./li')

    for product in products:
        book_title.append(product.find_element_by_xpath('.//h3[contains(@class, "bc-heading")]').text)
        book_author.append(product.find_element_by_xpath('.//li[contains(@class, "authorLabel")]').text)
        book_length.append(product.find_element_by_xpath('.//li[contains(@class, "runtimeLabel")]').text)

    current_page += 1

    try:
        next_page = driver.find_element_by_xpath('//span[contains(@class,"nextButton")]')
        next_page.click()
    except:
        pass

driver.quit()

df_books = pd.DataFrame({"title": book_title, "author": book_author, "length": book_length})
df_books.to_csv("books.csv", index=False)