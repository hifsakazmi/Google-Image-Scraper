# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 13:01:02 2020

@author: OHyic
"""
#import selenium drivers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

#from selenium.common.exceptions import StaleElementReferenceException, TimeoutException

#import helper libraries
import time
import urllib.request
from urllib.parse import urlparse
import os
import requests
import io
from PIL import Image
import re

#custom patch libraries
import patch

class GoogleImageScraper():
    def __init__(self, webdriver_path, image_path, search_key="", number_of_images=1, headless=True, min_resolution=(0, 0), max_resolution=(1920, 1080), max_missed=10):
        #check parameter types
        image_path = os.path.join(image_path, search_key)
        if (type(number_of_images)!=int):
            print("[Error] Number of images must be integer value.")
            return
        if not os.path.exists(image_path):
            print("[INFO] Image path not found. Creating a new folder.")
            os.makedirs(image_path)
            
        #check if chromedriver is installed
        if (not os.path.isfile(webdriver_path)):
            is_patched = patch.download_lastest_chromedriver()
            if (not is_patched):
                exit("[ERR] Please update the chromedriver.exe in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")

        for i in range(1):
            try:
                #try going to www.google.com
                options = Options()
                if(headless):
                    options.add_argument('--headless')
                service = Service(webdriver_path)                    
                driver = webdriver.Chrome(service=service, options=options)
                driver.set_window_size(1400,1050)
                driver.get("https://www.google.com")
                try:
                    
                    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "W0wltc"))).click()
                except Exception as e:
                    continue
            except Exception as e:
                #update chromedriver
                print(e)
                pattern = r'(\d+\.\d+\.\d+\.\d+)'
                version = list(set(re.findall(pattern, str(e))))[0]
                is_patched = patch.download_lastest_chromedriver(version)
                if (not is_patched):
                    exit("[ERR] Please update the chromedriver.exe in the webdriver folder according to your chrome version:https://chromedriver.chromium.org/downloads")

        self.driver = driver
        self.search_key = search_key
        self.number_of_images = number_of_images
        self.webdriver_path = webdriver_path
        self.image_path = image_path
        self.url = "https://www.google.com/search?q=%s&source=lnms&tbm=isch&sa=X&ved=2ahUKEwie44_AnqLpAhUhBWMBHUFGD90Q_AUoAXoECBUQAw&biw=1920&bih=947"%(search_key)
        self.headless=headless
        self.min_resolution = min_resolution
        self.max_resolution = max_resolution
        self.max_missed = max_missed

    def find_image_urls(self):
        """
            This function search and return a list of image urls based on the search key.
            Example:
                google_image_scraper = GoogleImageScraper("webdriver_path","image_path","search_key",number_of_photos)
                image_urls = google_image_scraper.find_image_urls()

        """
        print("[INFO] Gathering image links")
        self.driver.get(self.url)
        print(f"{self.url}")
        image_urls=[]
        count = 0
        missed_count = 0
        indx_1 = 0
        indx_2 = 0
        search_string = '//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img'
        print(f"{search_string}")
        time.sleep(3)
        while self.number_of_images > count and missed_count < self.max_missed:
            print(f"here 1")
            if indx_2 > 0:
                try:
                    imgurl = self.driver.find_element(By.XPATH, search_string%(indx_1,indx_2+1))
                    print(f"imgURL 1: {imgurl}")
                    imgurl.click()
                    indx_2 = indx_2 + 1
                    missed_count = 0
                except Exception as e:
                    print(f"Ex 1: {e}")
                    try:
                        imgurl = self.driver.find_element(By.XPATH, search_string%(indx_1+1,1))
                        print(f"imgURL 2: {imgurl}")
                        imgurl.click()
                        indx_2 = 1
                        indx_1 = indx_1 + 1
                    except Exception as e:
                        print(f"Ex 2: {e}")
                        indx_2 = indx_2 + 1
                        missed_count = missed_count + 1
            else:
                print(f"here 2")
                try:
                    imgurl = self.driver.find_element(By.XPATH, search_string%(indx_1+1))
                    print(f"imgURL 3: {imgurl}")
                    imgurl.click()
                    missed_count = 0
                    indx_1 = indx_1 + 1    
                except Exception as e:
                    try:
                        print(f"Ex 3: {e}")
                        imgurl = self.driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[%s]/div[%s]/a[1]/div[1]/img'%(indx_1,indx_2+1))
                        print(f"imgURL in exception: {imgurl}")
                        imgurl.click()
                        missed_count = 0
                        indx_2 = indx_2 + 1
                        search_string = '//*[@id="islrg"]/div[1]/div[%s]/div[%s]/a[1]/div[1]/img'
                    except Exception as e:
                        print(f"Ex 4: {e}")
                        indx_1 = indx_1 + 1
                        missed_count = missed_count + 1
                    
            try:
                #select image from the popup
                time.sleep(1)
                class_names = ["n3VNCb","iPVvYb","r48jcc","pT0Scc"]
                images = [self.driver.find_elements(By.CLASS_NAME, class_name) for class_name in class_names if len(self.driver.find_elements(By.CLASS_NAME, class_name)) != 0 ][0]
                print("d2")
                for image in images:
                    #only download images that starts with http
                    src_link = image.get_attribute("src")
                    if(("http" in src_link) and (not "encrypted" in src_link)):
                        print(
                            f"[INFO] {self.search_key} \t #{count} \t {src_link}")
                        image_urls.append(src_link)
                        count +=1
                        break
            except Exception as e:
                print(e)
                print("[INFO] Unable to get link")

            try:
                #scroll page to load next image
                if(count%3==0):
                    self.driver.execute_script("window.scrollTo(0, "+str(indx_1*60)+");")
                element = self.driver.find_element(By.CLASS_NAME,"mye4qd")
                element.click()
                print("[INFO] Loading next page")
                time.sleep(3)
            except Exception:
                time.sleep(1)



        self.driver.quit()
        print("[INFO] Google search ended")
        return image_urls
        
    def find_image_urls_upadated(self):
        print("[INFO] Gathering image links 2")
        self.driver.get(self.url)
        print(self.url)
        # Wait for the search results to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "img.YQ4gaf"))
        )
        image_urls = set()

        # Get the first 10 thumbnails
        thumbnails = self.driver.find_elements(By.CSS_SELECTOR, "img.YQ4gaf")[:self.number_of_images]
        for index in range(len(thumbnails)):
            try:
                # Re-fetch the list of thumbnails dynamically
                thumbnails = self.driver.find_elements(By.CSS_SELECTOR, "img.YQ4gaf")
                if index >= len(thumbnails):
                    print("Not enough thumbnails found.")
                    break
                
                # Select the current thumbnail
                thumbnail = thumbnails[index]
                
                
                # Click on the thumbnail to open the larger image
                #thumbnail.click()
                # Scroll to the thumbnail to ensure it's in view
                self.driver.execute_script("arguments[0].scrollIntoView(true);", thumbnail)
                time.sleep(1)  # Pause briefly to allow scrolling to complete
                
                try:
                    thumbnail.click()
                except ElementClickInterceptedException:
                    print(f"Click intercepted for thumbnail at index {index}. Retrying with JS...")
                    self.driver.execute_script("arguments[0].click();", thumbnail)

                # Wait for the large image to load
                large_image = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "img.sFlh5c.FyHeAf.iPVvYb"))
                )
                image_url = large_image.get_attribute("src")
                print(f"Image {index + 1}: {image_url}")

                #images = self.driver.find_elements(By.CSS_SELECTOR, 'img.sFlh5c.FyHeAf.iPVvYb')
                #for image in images:
                
                #    if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                #        src_link = image.get_attribute('src')
                #        image_urls.append(src_link)
                #        print(f"Found {len(index)}")
                
                # Get the URL of the larger image
                src_link = large_image.get_attribute("src")
                image_urls.add(src_link)
            except Exception as e:
                print(f"Failed to get image {index + 1}: {e}")

        # Optional: Pause between downloads to avoid triggering Google's rate limits
        #time.sleep(2)

        return list(image_urls)

    def save_images(self,image_urls, keep_filenames):
        print(keep_filenames)
        #save images into file directory
        """
            This function takes in an array of image urls and save it into the given image path/directory.
            Example:
                google_image_scraper = GoogleImageScraper("webdriver_path","image_path","search_key",number_of_photos)
                image_urls=["https://example_1.jpg","https://example_2.jpg"]
                google_image_scraper.save_images(image_urls)

        """
        print("[INFO] Saving image, please wait...")
        for indx,image_url in enumerate(image_urls):
            try:
                print("[INFO] Image url:%s"%(image_url))
                search_string = ''.join(e for e in self.search_key if e.isalnum())
                image = requests.get(image_url,timeout=5)
                if image.status_code == 200:
                    with Image.open(io.BytesIO(image.content)) as image_from_web:
                        try:
                            if (keep_filenames):
                                #extact filename without extension from URL
                                o = urlparse(image_url)
                                image_url = o.scheme + "://" + o.netloc + o.path
                                name = os.path.splitext(os.path.basename(image_url))[0]
                                #join filename and extension
                                filename = "%s.%s"%(name,image_from_web.format.lower())
                            else:
                                filename = "%s%s.%s"%(search_string,str(indx),image_from_web.format.lower())

                            image_path = os.path.join(self.image_path, filename)
                            print(
                                f"[INFO] {self.search_key} \t {indx} \t Image saved at: {image_path}")
                            image_from_web.save(image_path)
                        except OSError:
                            rgb_im = image_from_web.convert('RGB')
                            rgb_im.save(image_path)
                        image_resolution = image_from_web.size
                        if image_resolution != None:
                            if image_resolution[0]<self.min_resolution[0] or image_resolution[1]<self.min_resolution[1] or image_resolution[0]>self.max_resolution[0] or image_resolution[1]>self.max_resolution[1]:
                                image_from_web.close()
                                os.remove(image_path)

                        image_from_web.close()
            except Exception as e:
                print("[ERROR] Download failed: ",e)
                pass
        print("--------------------------------------------------")
        print("[INFO] Downloads completed. Please note that some photos were not downloaded as they were not in the correct format (e.g. jpg, jpeg, png)")
