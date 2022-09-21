import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

web = 'https://twitter.com/search?q=python&src=typed_query'
path = '/path/to/driver'
driver = webdriver.Chrome(path)
driver.get(web)
driver.maximize_window()

def get_tweet(element):
    try:
        user = element.find_element_by_xpath(".//span[contains(text(),'@')]").text
        text = element.find_element_by_xpath(".//div[@lang]").text
        text = " ".join(text.split())
        tweets_data = [user, text]
    except:
        tweets_data = ["user","text"]
    return tweets_data

user_data = []
text_data = []
tweet_ids = set()

scrolling = True
while scrolling:
    tweets = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located(By.XPATH, "//article[@role='article']")
    )

    for tweet in tweets:
        tweet_list = get_tweet(tweet)
        tweet_id = ''.join(tweet_list)
        if tweet_id not in tweet_ids:
            tweet_ids.add(tweet_id)
            user_data.append(tweet_list[0])
            text_data.append(tweet_list[1])
    
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHieght")
        if new_height == last_height:
            scrolling = False
            break
        else:
            last_height = new_height
            break

driver.quit()
df = pd.DataFrame({"user": user_data, "text": text_data})
df.to_csv("tweets.csv", index=False)