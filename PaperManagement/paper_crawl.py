from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

'''
Crawl Paper's Information using Selenium
'''

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://www.arxiv.com")
time.sleep(2)
machine_learning = driver.find_element(By.XPATH, value='//*[@id="stat.ML"]')
time.sleep(2)
machine_learning.click()

first_paper = driver.find_element(
    By.XPATH, value='//*[@id="dlpage"]/dl[1]/dt[1]/span/a[1]')
first_paper.click()
time.sleep(3)

related_button = driver.find_element(
    By.XPATH, value='//*[@id="labstabs"]/div/label[4]')
related_button.click()
time.sleep(2)

title = driver.find_element(By.XPATH, value='//*[@id="abs"]/h1').text
abstract = driver.find_element(
    By.XPATH, value='//*[@id="abs"]/blockquote').text

paper_id = driver.find_element(
    By.XPATH, value='//*[@id="header"]/div[1]').text
paper_id = paper_id.split(':')[1]

submitted_date = driver.find_element(
    By.XPATH, value='//*[@id="abs"]/div[1]').text
submitted_date = submitted_date.split('on')[1][1:-1]

domain = driver.find_element(
    By.XPATH, value='//*[@id="abs-outer"]/div[1]/div[1]/h1').text

paper_url = driver.find_element(
    By.XPATH, value='//*[@id="abs-outer"]/div[2]/div[1]/ul/li[1]/a').get_attribute("href")

author_list = driver.find_element(
    By.XPATH, value='//*[@id="abs"]/div[2]').find_elements(by=By.TAG_NAME, value='a')

for a in author_list:
    print('author link: ', a.get_attribute("href"))
    print('author name: ', a.text)

print('----------')

recommend_switch_1 = driver.find_element(
    By.XPATH, value='//*[@id="labstabs"]/div/div[4]/div[1]/div[1]/div[1]/label/span[1]')
recommend_switch_1.click()
time.sleep(1)
recommend_switch_2 = driver.find_element(
    By.XPATH, value='//*[@id="labstabs"]/div/div[4]/div[1]/div[2]/div[1]/label/span[1]')
recommend_switch_2.click()
time.sleep(1)
recommend_switch_3 = driver.find_element(
    By.XPATH, value='//*[@id="labstabs"]/div/div[4]/div[1]/div[3]/div[1]/label/span[1]')
recommend_switch_3.click()
time.sleep(5)

related_papers = driver.find_element(
    By.XPATH, value='//*[@id="coreRecommender-tab1"]/ul').find_elements(by=By.TAG_NAME, value='li')

print('paper id: ', paper_id)
print('----------')
print('submitted date: ', submitted_date)
print('----------')
print('title: ', title)
print('----------')
print('abstract: ', abstract)
print('----------')
print('domain: ', domain)
print('----------')
print('paper url: ', paper_url)
print('----------')


for i, paper in enumerate(related_papers):
    print(f'related paper name {i}: ', paper.text)
    a_tag = paper.find_element(By.TAG_NAME, 'a')
    href_value = a_tag.get_attribute('href')
    print(f'related paper url {i}: ', href_value)

driver.quit()
