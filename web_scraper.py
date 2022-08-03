
from ctypes import c_void_p
from os import mkdir
#from msilib.schema import CreateFolder
from selenium import webdriver 
import time
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import test_with_Blair
from uuid import uuid4
import json
import urllib
class WebScrape:
    def __init__(self, URL) -> None:
        self.driver = webdriver.Chrome()
        self.URL = URL
        URL = "https://www.tedbaker.com/uk/c/mens/clothing/shirts/680"
        self.driver.get(URL)
        # element = self.driver.find.element[By.XPATH, '//*[@id=smc-v5-overlay-83316]']
        # self.driver.execute_script("""
        # var element = arguments[0];
        # element.parentNode.removeChild(element);
        # """, element)
        # time.sleep(10)
        # pass

    def accept_cookies(self):

        time.sleep(2) # Wait a couple of seconds, so the website doesn't suspect you are a bot
        try:
            # driver.switch_to_frame('gdpr-consent-notice') # This is the id of the frame
            accept_cookies_button = self.driver.find_element(By.XPATH, '//*[@id="consent_prompt_submit"]')
            accept_cookies_button.click()
            print('try')

        except AttributeError: # If you have the latest version of Selenium, the code above won't run because the "switch_to_frame" is deprecated
            # driver.switch_to.frame('gdpr-consent-notice') # This is the id of the frame
            accept_cookies_button = self.driver.find_element(By.XPATH, '//*[@id="consent_prompt_submit"]')
            accept_cookies_button.click()
            print('Attribute Error')
        except:
            pass # cookies did not show

        # return self.driver()


# this is for the 10% sale pop-up, which happens randomly
# // find all elements, then * means any
    def close_pop_up(self) -> webdriver.Chrome:
        try:
        #    time.sleep(5)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="smc-v5-overlay-73228"]')))
            element = self.driver.find_element(By.XPATH, '//*[@id="smc-v5-overlay-73228"]')
            self.driver.execute_script("""
            var element = arguments[0]
            if (element)
                element.parentNode.removeChild(element);
            """, element
            )

            # self.driver.execute_script("""
            # var element = document.querySelector(By.XPATH, '//*[@id="smc-v5-overlay-73228"]');
            # if (element)
            #     element.parentNode.removeChild(element);
            # """)
            print('pop up gone!')
        except Exception as e:
            print(e)

        # delay = 10 # 
        # try:
        #     time.sleep(4)
        #     # WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="smc-animated smc-fadeInRight smc-animDelay4 smc-closer"]')))
        #     # print("Frame Ready!")
        #     # # self.driver.switch_to.frame('gdpr-consent-notice')
        #     close_pop_up = self.driver.execute_script('return document.querySelector("#smc-v5-overlay-83316 > smc-bg > smc-overlay-outer > smc-overlay-inner > smc-close > a")')
        #     close_pop_up = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@class="smc-animated smc-fadeInRight smc-animDelay4 smc-closer"]/a')))
        #     print("Accept Cookies Button Ready!")
        #     close_pop_up.click()
        # except TimeoutException:
        #     print("Loading took too much time!")

        # return self.driver 
    
    def click_shirt(self):

        time.sleep(5)
        shirt_click = self.driver.find_element(By.XPATH, '//*[@id="plp-container"]/a[3]')
        link = shirt_click.get_attribute('href')
        print(link)
        self.driver.get(link)

    def page_scroll(self):
        time.sleep(5)
        self.driver.execute_script("window.scrollTo(0, 1400)")
        print('page scrolled!') 

    def extract_page_links(self): # method to extract hrefs from webpage
        page_link_list = []
        page_container = self.driver.find_elements(By.XPATH, '//div[@data-testid="plp-grid"]//a')
        #print(page_container) # print a list of selenium web elements

        for item in page_container:
            link_to_page = item.get_attribute('href')
            print(link_to_page)
            #iterating and adding to the empty list
            page_link_list.append(link_to_page)

        print(page_link_list)
        print(len(page_link_list))
        return page_link_list

    def retrieve_info(self): 
        product_page_list = self.extract_page_links()
        all_prices = []
        all_product_names = []
        all_product_descriptions = []
        product_information = []
        #product_unique_uuid = []
        for product_page in product_page_list[:6]:
            product_information_dictionary = dict()
            self.driver.get(product_page)
            self.close_pop_up()
            try:
                price = self.driver.find_element(By.XPATH, '//h2[@class="product-pricesstyled__Price-sc-1hhcrv3-1 hJwDit"]').text
                print(price)
                all_prices.append(price)
            except:
                price = self.driver.find_element(By.XPATH, '//h2[@class="product-pricesstyled__Price-sc-1hhcrv3-1 fArSfN"]').text
                print(price)
                all_prices.append(price)
            product_information_dictionary['price'] = price
            
            product_names = self.driver.find_element(By.XPATH, '//h1[@class="product-detailsstyled__ProductName-tuq96a-0 dnwiVs"]').text
            print(product_names)
            all_product_names.append(product_names)
            product_information_dictionary['name'] = product_names
            
            product_descriptions = self.driver.find_element(By.XPATH, '//h2[@class="product-detailsstyled__ProductDescription-tuq96a-2 bbToXQ"]').text
            print(product_descriptions)
            all_product_descriptions.append(product_descriptions)
            product_information_dictionary['description'] = product_descriptions
            product_information.append(product_information_dictionary)

            current_URL = self.driver.current_url.split('/')[-1]
            print(str(uuid4()))
            product_information_dictionary['uuid'] = str(uuid4())
            product_information.append(product_information_dictionary)
        # print(all_product_names)
        # print(all_prices)
        # print(all_product_descriptions)
        # info_dictionary = dict(zip(product_descriptions, all_product_names))
        # print(info_dictionary)
        print(product_information)
        return product_information

    def save_locally(self):
        directory = "raw_data"
        parent_dir = "/home/Documents/"
        path = os.path.join(parent_dir, directory)
        mkdir()
        product_dictionary_list = self.retrieve_info()
        with open('data.json') as json_file:
            json.dump(product_dictionary_list, json_file)

    def 






        # jbag = self.retrieve_info()
        # json = json.dumps(jbag)
        # f = open("dict.jbag", "w")
        # f.write(json)
        # f.close()

        
        # with open('filename', "w") as f:



    def retrieve_names(self): 
        product_page_list = self.extract_page_links()
        all_product_names = []
        for product_page in product_page_list[:6]:
            self.driver.get(product_page)
            self.close_pop_up()
            product_names = self.driver.find_element(By.XPATH, '//h1[@class="product-detailsstyled__ProductName-tuq96a-0 dnwiVs"]').text
            print(product_names)
            all_product_names.append(product_names)
        print(all_product_names)



    def collect_page_info(self):
        product_dict = dict()
        product_dict["product_name"] = self.driver.find_element(By.XPATH, '//*[data-testid="pdp-product-name"]').text
        #do the identical for description and price


    def get_details(self): 
        all_pages_list = [] 
        list_of_links = self.extract_page_links() 
        for item in list_of_links[:6]: 
            self.driver.get(item) 
            all_pages_list.append(self.collect_page_info()) 
            self.save_json(all_pages_list, "raw-data") 
    

    def get_unique_id(self):
        current_URL = self.driver.current_url.split('/')[-1]
        print(current_URL)
        print(str(uuid4()))


        
    



        

# Need to create a crawler to get link of all different shirts

# this is for the 10% sale pop-up, which happens randomly

#time.sleep(2) # Wait a couple of seconds, so the website doesn't suspect you are a bot
# driver = webdriver.Chrome() 
# try:
#     driver.switch_to_frame('gdpr-consent-notice') # This is the id of the frame
#     cancel_pop_up = driver.find_element(By.XPATH, '//*[@class="smc-animated smc-fadeInRight smc-animDelay4 smc-closer"]')
#     cancel_pop_up.click()
#     print('try')

#    smc-animated smc-fadeInRight smc-animDelay4 smc-closer

if __name__ == '__main__':
    ted_baker_scrape = WebScrape("https://www.tedbaker.com/uk/c/mens/clothing/shirts/680")
    ted_baker_scrape.accept_cookies()
    ted_baker_scrape.close_pop_up()
  #  ted_baker_scrape.click_shirt()
    #ted_baker_scrape.close_pop_up()
    # ted_baker_scrape.page_scroll()
    # ted_baker_scrape.click_shirt()
    # ted_baker_scrape.close_pop_up()
    #ted_baker_scrape.extract_page_links()
    #ted_baker_scrape.get_details()
    #ted_baker_scrape.retrieve_info()
    #ted_baker_scrape.retrieve_names()
    #ted_baker_scrape.get_unique_id()


# %%
# element = driver.find_element_by_class_name('classname')
# driver.execute_script("""
# var element = arguments[0];
# element.parentNode.removeChild(element);
# """, element)


# c_void_p

# def extract_page_links(self, container_xpath): 
#     ''' method to extract the hrefs from a page ''' 
#     page_link_list = [] page_container = self.driver.find_elements(By.XPATH, container_xpath)
#      print(page_container) for item in page_container:
#       link_to_page = item.get_attribute('href') 

# Iterating and adding the link to the empty list 

# page_link_list.append(link_to_page)
# print(page_link_list)
# print(len(page_link_list))
# return page_link_list 

# def get_details(self): 
#     all_pages_list = [] 
#     list_of_links = self.extract_page_links('//div[@data-testid="plp-card"]') 
#     for item in list_of_links: 
#         self.driver.get(item) 
#         all_pages_list.append(self.collect_page_info()) 
#         self.save_json(all_pages_list, "raw-data") 