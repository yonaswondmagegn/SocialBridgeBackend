# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import responses
# from rest_framework import status
# import base64
# from django.core.files.base import ContentFile
# from selenium.webdriver.chrome.options import Options

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# import pickle


# class PostToFacebookMarkatePlace(APIView):
#     def post(self,request):
#         image_data = request.FILES.get('image')
#         print(image_data)
#         PATH = 'C:/chromedriver.exe'
#         services = Service(PATH)
        
#         chrome_otp = Options()

#         prefs = {
#             "profile.default_content_setting_values.notifications": 2 
#         }
#         chrome_otp.add_experimental_option("prefs", prefs)

#         driver = webdriver.Chrome(service=services,options=chrome_otp)

#         cookies = pickle.load(open("facebook_cookies.pkl", "rb"))
#         for cookie in cookies:
#             driver.add_cookie(cookie)
        
#         driver.get('https://www.facebook.com/marketplace/create/item')

#         try:
#             file_input = driver.find_element(By.XPATH, "//input[@type='file']")
#             file_input.send_keys(image_data)
#             print(file_input)
#         except:
#             print('hellow world')

import time
import re
import os
import base64
import pyperclip
import pickle
from django.core.files.base import ContentFile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class PostToFacebookMarketplace(APIView):
    def post(self, request):
        try:
            image_file = request.FILES.get('image')
            print(image_file)
            if not image_file:
                return Response({"error": "No image file found"}, status=status.HTTP_400_BAD_REQUEST)
            
            temp_image_path = f"temp_{image_file.name}"
            with open(temp_image_path, 'wb') as f:
                f.write(image_file.read())
        
            title = request.data.get('title')
            if not title:
                return Response({"error": "title is Requred"}, status=status.HTTP_400_BAD_REQUEST)
            price = request.data.get('price')
            category = request.data.get('category')
            print(category)
            if not price:
                price = 0
            print(price)
            print(int(price))
            description  = request.data.get("discription")
            if not description:
                return Response({"error": "description is Requred"}, status=status.HTTP_400_BAD_REQUEST)


            PATH = 'C:/chromedriver.exe'
            service = Service(PATH)
            
            chrome_otp = Options()
            chrome_otp.add_argument("--headless=new")
            # chrome_otp.add_argument("--no-sandbox")
            chrome_otp.add_argument("--headless")
            chrome_otp.add_argument("--window-size=1920,1080")
            chrome_otp.add_argument("--disable-gpu")
            # chrome_otp.add_argument("--disable-dev-shm-usage")
       

            prefs = {
                "profile.default_content_setting_values.notifications": 2
            }
            chrome_otp.add_experimental_option("prefs", prefs)

            driver = webdriver.Chrome(service=service, options=chrome_otp)
            driver.get('https://www.facebook.com')

        
            try:
                cookies = pickle.load(open(r"C:\Users\yonas\Desktop\project\SaaSProjects\bridge\FacebookMarkatePlace\facebook_cookies.pkl", "rb"))
                for cookie in cookies:
                    driver.add_cookie(cookie)
            except:
                return Response({'error':'cookie error'},status=status.HTTP_400_BAD_REQUEST)

            driver.get('https://www.facebook.com/marketplace/create/item')
            def remove_emojis(text):
                        emoji_pattern = re.compile(
                            "["
                            "\U0001F600-\U0001F64F"  
                            "\U0001F300-\U0001F5FF"  
                            "\U0001F680-\U0001F6FF"  
                            "\U0001F700-\U0001F77F"  
                            "\U0001F780-\U0001F7FF"  
                            "\U0001F800-\U0001F8FF"  
                            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
                            "\U0001FA00-\U0001FAFF"  # Chess Symbols
                            "\U00002702-\U000027B0"  # Dingbats
                            "]+", flags=re.UNICODE)
                        
                        return emoji_pattern.sub(r'', text)
            try:
                try:
                    WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
                    )
                    print('found it ..coutninue')
                except:
                    print('not found sorry')
                print('continue one')

                file_input = driver.find_element(By.XPATH, "//input[@type='file']")
                file_input.send_keys(os.path.abspath(temp_image_path))  
                print(f"File input success: {file_input}")
                try:
                    image_xpath = "//img[contains(@class, 'x1lcm9me') and contains(@class, 'x1yr5g0i') and contains(@class, 'xrt01vj') and @alt='']"
                    WebDriverWait(driver, 60).until(
                        EC.visibility_of_element_located((By.XPATH, image_xpath))
                    )
                    print(' two found it ..coutninue')
                except:
                    print(' two not found sorry')
                print('continue two ')
                try:
                    driver.save_screenshot('inpuscreenshott.png')
                except:
                    print('saving screen shoot error')
                first_input = driver.find_elements(By.TAG_NAME, "input") 
                first_input[5].click()
                pyperclip.copy(title)
                # try:
                #     first_input[5].send_keys(Keys.CONTROL,'v')
                # except:
                #     print('coping error')
                #      # Remove emojis
                removed_text = remove_emojis(title)
                first_input[5].send_keys(removed_text)

                first_input[6].send_keys(price)
                category_button = driver.find_element(By.CSS_SELECTOR, 'label[aria-label="Category"]')
                category_button.click()
                element = driver.find_element(By.XPATH, f"//span[text()='{category}']/ancestor::div[@role='button']")
                element.click()
                condtion_button = driver.find_element(By.CSS_SELECTOR, 'label[aria-label="Condition"]')
                condtion_button.click()
                n_bt = driver.find_element(By.XPATH,"//span[text()='New']")
                n_bt.click()
                d_input = driver.find_elements(By.TAG_NAME,'textarea')
                disc_emoj = remove_emojis(description)
                d_input[0].send_keys(disc_emoj)
                try:
                    n_button = WebDriverWait(driver, 100).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and @aria-label='Next']"))
                    )
                    n_button.click()
                except:
                    print('nbutton Error')
                if not n_button:
                    print('n button not found')
                try:
                    publish_button = WebDriverWait(driver, 100).until(
                        EC.element_to_be_clickable((By.XPATH, "//span[text()='Publish']"))
                    )
                except:
                    return Response({'error':"can't get publish button "},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                if publish_button:
                    class_name = "span x1lliihq x6ikm8r x10wlt62 x1n2onr6"
                    array_list = class_name.split(" ")
                    class_join = '.'.join(array_list)
                    WebDriverWait(driver, 100).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, class_join))
                    )
                    d_ele = driver.find_elements(By.CSS_SELECTOR, class_join)
                    for c_e in d_ele[:20]:
                        c_e.click()
                    publish_button.click()
                else:
                    
                    return Response({'error':"can't get publish button "},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                return Response({"error": "File upload failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({"message": "Image uploaded successfully"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            # Clean up the temporary image file
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)
