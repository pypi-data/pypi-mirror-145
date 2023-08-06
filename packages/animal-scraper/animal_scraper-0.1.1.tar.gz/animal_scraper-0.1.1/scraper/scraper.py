from matplotlib import container
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os
from tqdm import tqdm
import urllib.request
import boto3

class Scraper:
    def __init__(self, url, headless=False):
        self.url = url
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument("--window-size=1024,768")
        if headless:
            options.add_argument('--headless')
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        else:
            self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(self.url)


'''
This module contains the scraper class and its methods.
'''
class AnimalScraper(Scraper):
    '''
    This class will help you scrape images from animal.
    Pass the name of the animal you want to scrape and
    the scraper will be initialized
    '''
    def __init__(self, animal, headless=False, url='https://all-free-download.com/free-photos/') -> None:
        self.animal = animal
        self.url = url + animal
        super().__init__(self.url, headless)
        
        # aws_key_id = input('Enter your AWS key ID please: ')
        # aws_secret_key = input('Enter your AWS secret key please: ')
        # aws_region = input('Enter your AWS region: ')
        # self.client = boto3.client('s3', 
        #             aws_access_key_id=aws_key_id,
        #             aws_secret_access_key=aws_secret_key,
        #             region_name=aws_region)
        # options = webdriver.ChromeOptions()
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--no-sandbox')
        # options.add_argument("--window-size=1024,768")
        # if headless:
        #     options.add_argument('--headless')
        #     self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        # else:
        #     self.driver = webdriver.Chrome(ChromeDriverManager().install())
        # self.driver.get(self.url)
    
    def get_images(self,
            container_xpath='//div[@class="row row-cols-1 row-cols-sm-1  row-cols-md-5 row-cols-xl-5  row-cols-xxl-5 "]',
            col_img_xpath='./div[@class="col p-0 gcol"]',
            ind_img_xpath='.//img[@class="item-image img-fluid"]') -> list:
        '''
        This method will return a list of urls to the images
        '''
        elem = self.driver.find_element(By.XPATH, container_xpath)
        columns = elem.find_elements(By.XPATH, col_img_xpath)
        self.src_list = []
        for column in columns:
            images = column.find_elements(By.XPATH, ind_img_xpath)
            for img in images:
                try:
                    self.src_list.append(img.get_attribute('src'))
                except:
                    print('No source found')
        return self.src_list
    
    def download_images(self, path='.') -> None:
        '''
        This method will download the images to the specified path
        '''
        if not os.path.exists(f'{path}/{self.animal}'):
            os.makedirs(f'{path}/{self.animal}')
        if self.src_list is None:
            print('No images found, plase run get_images() first')
            return None
        
        for i, scr in enumerate(tqdm(self.src_list)):
            urllib.request.urlretrieve(scr, f'{path}/{self.animal}/{self.animal}_{i}.webp')
            # self.client.upload_file(f'{path}/{self.animal}/{self.animal}_{i}.webp', 'march-bucket-test', f'{self.animal}/{self.animal}_{i}.webp')
    # def upload_images(self):
    #     '''
    #     This method will upload the images to S3
    #     '''
    #     folder = self.animal
        
    #     for i, scr in enumerate(tqdm(self.src_list)):
    #         self.client.upload_file(f'{self.animal}/{self.animal}_{i}.webp', 'animal-images', f'{self.animal}/{self.animal}_{i}.webp')
