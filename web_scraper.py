
from ctypes import c_void_p
import os
#from msilib.schema import CreateFolder
from selenium import webdriver 
import time
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from uuid import uuid4
import json
import urllib
import pandas as pd

class WebScrape:
    '''
    This class is used to to webscrape. 

    Attributres:
    web URL to Ted Baker website.    
    '''
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
        '''
        Accepts cookies on the Ted Baker website.

        Returns
            .......
            'Cookies accepted' once button is clicked
        '''

        time.sleep(2) # Wait a couple of seconds, so the website doesn't suspect you are a bot
        try:
            # driver.switch_to_frame('gdpr-consent-notice') # This is the id of the frame
            accept_cookies_button = self.driver.find_element(By.XPATH, '//*[@id="consent_prompt_submit"]')
            accept_cookies_button.click()
            print('Cookies accepted')

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
        '''
        Closes promotion pop-up on the Ted Baker website

        Returns
           .......

        '''
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
        except TimeoutException:
            print('No pop up found')

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
        '''
        Clicks on shirt from men's shirt section of website

        Returns
           .......
           prints links of each shirt on the page
        '''

        time.sleep(5)
        shirt_click = self.driver.find_element(By.XPATH, '//*[@id="plp-container"]/a[3]')
        link = shirt_click.get_attribute('href')
        print(link)
        self.driver.get(link)

    def page_scroll(self):
        '''
        Scrolls down page of website

        Returns
           .......
           prints links of each shirt on the page
        '''

        time.sleep(5)
        self.driver.execute_script("window.scrollTo(0, 1400)")
        print('page scrolled!') 


    def extract_page_links(self): # method to extract hrefs from webpage
        '''
        Extracts page links for all shirts on the mens site

        It does this by iterating through all the a tags in the
        containter of the site, getting the 'href' attribute, 
        then appending this to a list

        Returns
           .......
           prints the list of all the href's of each shirt and 
           prints the length of the list, to check if all of the
           shirts have been extracted 
        '''
    
    
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
        '''
        Clicks on each shirt, extracts all the necessary info

        Returns:
           .......
           a list of dictionaries, with each dictionary having the 
           following keys: price, product code, description, UUID
           and image links
        '''
        product_page_list = self.extract_page_links()
        # all_prices = []
        # all_product_names = []
        # all_product_descriptions = []
        product_information = []
        #product_unique_uuid = []
        for product_page in product_page_list[:3]:
            product_information_dictionary = dict()
            self.driver.get(product_page)
            self.close_pop_up()

            try:
                price = self.driver.find_element(By.XPATH, '//h2[@class="product-pricesstyled__Price-sc-1hhcrv3-1 hJwDit"]').text
                # print(price)
                # all_prices.append(price)
            except:
                price = self.driver.find_element(By.XPATH, '//h2[@class="product-pricesstyled__Price-sc-1hhcrv3-1 fArSfN"]').text
                # print(price)
                # all_prices.append(price)
            product_information_dictionary['price'] = price
            
            product_names = self.driver.find_element(By.XPATH, '//h1[@class="product-detailsstyled__ProductName-tuq96a-0 dnwiVs"]').text
            # print(product_names)
            # all_product_names.append(product_names)
            product_information_dictionary['name'] = product_names
            
            product_descriptions = self.driver.find_element(By.XPATH, '//h2[@class="product-detailsstyled__ProductDescription-tuq96a-2 bbToXQ"]').text
            # print(product_descriptions)
            # all_product_descriptions.append(product_descriptions)
            product_information_dictionary['description'] = product_descriptions
            product_information.append(product_information_dictionary)

            current_URL = self.driver.current_url.split('/')[-1]
            print(str(uuid4()))
            product_information_dictionary['product_code'] = self.get_product_code()
            product_information_dictionary['uuid'] = self.get_unique_id()
            product_information_dictionary['image_link'] = self.get_images()
            product_information.append(product_information_dictionary)
        # print(all_product_names)
        # print(all_prices)
        # print(all_product_descriptions)
        # info_dictionary = dict(zip(product_descriptions, all_product_names))
        # print(info_dictionary)
        # df = pd.DataFrame.from_dict(product_information_dictionary)
        print(product_information)
        # print(df)
        return product_information

    def save_locally(self):
        '''
        saves data in json file
        '''
        directory = "raw_data"
        parent_dir = "/home/Documents/"
        path = os.path.join(parent_dir, directory)
        product_dictionary_list = self.retrieve_info()
        with open('data.json') as json_file:
            json.dump(product_dictionary_list, json_file)

    def get_images(self):
        '''
        gets image links for all shirts
        '''
        img_link = self.driver.find_element(By.XPATH, '//div[@data-swiper-slide-index="0"]//img').get_attribute('src')
        print(img_link)
        return img_link

    def get_product_code(self):
        '''
        extracts product code from item URL

        Returns:
           .......
           product code: the last unique part of the URL for
           each item
        '''
        product_code = self.driver.current_url.split('/')[-1]
        print(product_code)
        return product_code
        






        # jbag = self.retrieve_info()
        # json = json.dumps(jbag)
        # f = open("dict.jbag", "w")
        # f.write(json)
        # f.close()

        
        # with open('filename', "w") as f:



    # def retrieve_names(self): 
    #     product_page_list = self.extract_page_links()
    #     all_product_names = []
    #     for product_page in product_page_list[:6]:
    #         self.driver.get(product_page)
    #         self.close_pop_up()
    #         product_names = self.driver.find_element(By.XPATH, '//h1[@class="product-detailsstyled__ProductName-tuq96a-0 dnwiVs"]').text
    #         print(product_names)
    #         all_product_names.append(product_names)
    #     print(all_product_names)



    # def collect_page_info(self):
    #     product_dict = dict()
    #     product_dict["product_name"] = self.driver.find_element(By.XPATH, '//*[data-testid="pdp-product-name"]').text
    #     #do the identical for description and price


    def get_details(self): 
        '''
        
        '''
        all_pages_list = [] 
        list_of_links = self.extract_page_links() 
        for item in list_of_links[:6]: 
            self.driver.get(item) 
            all_pages_list.append(self.collect_page_info()) 
            self.save_json(all_pages_list, "raw-data") 
    

    def get_product_code(self):
        product_code = self.driver.current_url.split('/')[-1]
        print(product_code)
        return product_code

    def get_unique_id(self):
        uuid = str(uuid4())
        return uuid

    


        
    



        

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
    ted_baker_scrape.retrieve_info()
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
#%%
from timeit import timeit

result = timeit(stmt='total=sum(range(1000))', number=5000)
print(result/5000)
# %%
def count_ways(n: int) -> int:
    # If the number of steps 
    if (n == 1 or n == 0) :
        return 1
    elif (n == 2) :
        return 2
    else :
        return count_ways(n - 3) + count_ways(n - 2) + count_ways(n - 1)
 
 
# Driver code
n = 4
print(count_ways(n))
# %%
