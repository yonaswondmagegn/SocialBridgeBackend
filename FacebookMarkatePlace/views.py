import re
import os
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
from tempfile import NamedTemporaryFile


class PostToFacebookMarketplace(APIView):
    def post(self, request):
        try:
            image_file = request.FILES.get('image')
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
            if not price:
                price = 0
            description = request.data.get("discription")
            if not description:
                return Response({"error": "description is Requred"}, status=status.HTTP_400_BAD_REQUEST)

            PATH = '/usr/local/bin/chromedriver'
            service = Service(PATH)
            chrome_otp = Options()

            chrome_otp = Options()
            chrome_otp.add_argument("--headless=new")
            chrome_otp.add_argument("--no-sandbox")
            chrome_otp.add_argument("--disable-dev-shm-usage")
            chrome_otp.add_argument("--window-size=1920,1080")
            # Prevent DevToolsActivePort issue
            chrome_otp.add_argument("--remote-debugging-port=9222")

            prefs = {
                "profile.default_content_setting_values.notifications": 2
            }
            chrome_otp.add_experimental_option("prefs", prefs)
            print('a')
            driver = webdriver.Chrome(service=service, options=chrome_otp)
            driver.get('https://www.facebook.com')

            print('a1')
            try:
                cookies = pickle.load(open(
                    r"/home/yonas/SocialBridgeBackend/FacebookMarkatePlace/facebook_cookies.pkl", "rb"))
                for cookie in cookies:
                    driver.add_cookie(cookie)
            except:
                return Response({'error': 'cookie error'}, status=status.HTTP_400_BAD_REQUEST)

            print('a3')
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
                    "\U0001F900-\U0001F9FF"
                    "\U0001FA00-\U0001FAFF"
                    "\U00002702-\U000027B0"
                    "]+", flags=re.UNICODE)

                return emoji_pattern.sub(r'', text)
            try:
                try:
                    WebDriverWait(driver, 30).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//input[@type='file']"))
                    )
                except:
                    print('not found sorry')
                    return Response({'error': 'cookie error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                file_input = driver.find_element(
                    By.XPATH, "//input[@type='file']")
                file_input.send_keys(os.path.abspath(temp_image_path))
                # try:
                #     image_xpath = "//img[contains(@class, 'x1lcm9me') and contains(@class, 'x1yr5g0i') and contains(@class, 'xrt01vj') and @alt='']"
                #     WebDriverWait(driver, 60).until(
                #         EC.visibility_of_element_located(
                #             (By.XPATH, image_xpath))
                #     )
                # except Exception as e:
                #     print(e)
                #     print(' two not found sorry')
                #     return Response({'error': 'cookie error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                first_input = driver.find_elements(By.TAG_NAME, "input")
                try:
                    first_input[5].click()
                except:
                    print('input not clicabnle')
                print('a4')
                removed_text = remove_emojis(title)
                print('a5')
                first_input[5].send_keys(removed_text)
                print('a6')

                first_input[6].send_keys(price)
                category_button = driver.find_element(
                    By.CSS_SELECTOR, 'label[aria-label="Category"]')
                category_button.click()
                element = driver.find_element(
                    By.XPATH, f"//span[text()='{category}']/ancestor::div[@role='button']")
                driver.save_screenshot('category_p.png')
                element.click()
                print('a7')

                condtion_button = driver.find_element(
                    By.CSS_SELECTOR, 'label[aria-label="Condition"]')
                condtion_button.click()
                n_bt = driver.find_element(By.XPATH, "//span[text()='New']")
                n_bt.click()
                d_input = driver.find_elements(By.TAG_NAME, 'textarea')
                print('a8')
                disc_emoj = remove_emojis(description)
                d_input[0].send_keys(disc_emoj)
                try:
                    n_button = WebDriverWait(driver, 100).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//div[@role='button' and @aria-label='Next']"))
                    )
                    n_button.click()
                except:
                    print('nbutton Error')
                print('a8')
                if not n_button:
                    print('n button not found')
                try:
                    publish_button = WebDriverWait(driver, 100).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//span[text()='Publish']"))
                    )
                except Exception as e:
                    print(e)
                    return Response({'error': "can't get publish button "}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                if publish_button:
                    class_join = "div.x9f619.x1ja2u2z.x78zum5.x1n2onr6.x1iyjqo2.xs83m0k.xeuugli.x1qughib.x6s0dn4.x1a02dak.x1q0g3np.xdl72j9 > div > div > div > div:nth-child(1) > span > span > span"
                    WebDriverWait(driver, 100).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, class_join))
                    )
                    d_ele = driver.find_elements(By.CSS_SELECTOR, class_join)
                    for c_e in d_ele[:20]:
                        c_e.click()
                    publish_button.click()
                else:

                    return Response({'error': "can't get publish button "}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                print(e)
                return Response({"error": "File upload failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"message": "Image uploaded successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        finally:
            if os.path.exists(temp_image_path):
                os.remove(temp_image_path)


class GetProduct(APIView):
    def post(self, request):
        try:
            url = request.data.get('url')
            if not url:
                return Response({'error': 'url is requred'}, status=status.HTTP_400_BAD_REQUEST)

            PATH = '/usr/local/bin/chromedriver'
            service = Service(PATH)
            chrome_otp = Options()

            chrome_otp = Options()
            # chrome_otp.add_argument("--headless=new")
            chrome_otp.add_argument("--no-sandbox")
            chrome_otp.add_argument("--disable-dev-shm-usage")
            chrome_otp.add_argument("--window-size=1920,1080")
            chrome_otp.add_argument("--remote-debugging-port=9222")

            prefs = {
                "profile.default_content_setting_values.notifications": 2
            }
            chrome_otp.add_experimental_option("prefs", prefs)
            print('a')
            driver = webdriver.Chrome(service=service, options=chrome_otp)
            driver.get('https://www.facebook.com')

            print('a1')
            try:
                cookies = pickle.load(open(
                    r"/home/yonas/SocialBridgeBackend/FacebookMarkatePlace/facebook_cookies.pkl", "rb"))
                for cookie in cookies:
                    driver.add_cookie(cookie)
            except:
                return Response({'error': 'cookie error'}, status=status.HTTP_400_BAD_REQUEST)

            driver.get(url)
            
            img_urls = []
            title_text = ""
            price = ""
            description = ""
        
            try:
                # Locate parent div with the specific style
                parent_div = driver.find_elements(By.CSS_SELECTOR,'.x6s0dn4.x78zum5.x1y1aw1k.xwib8y2.xu6gjpd.x11xpdln.x1r7x56h.xuxw1ft.xc9qbxq.x193iq5w[style="transform: translate3d(0px, 0px, 0px);"]')
                if len(parent_div) == 0:
                    # Locate images in the alternative span > div > img structure
                    img_cont = driver.find_elements(By.CSS_SELECTOR,
                                                    'span.x78zum5.x1vjfegm > div > img.xz74otr'
                                                    )
                    if img_cont:
                        img_urls.append(img_cont[0].get_attribute('src'))
                else:
                    imgs = parent_div[0].find_elements(By.TAG_NAME, 'img')
                    for img in imgs:
                        img_urls.append(img.get_attribute('src'))

            except Exception as e:
                return Response({'error': f"image not found {e}"}, status=status.HTTP_400_BAD_REQUEST)
         
            title_js_text = driver.execute_script(
                  "return document.querySelectorAll('span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x10flsy6.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.xw06pyt.xngnso2.x1qb5hxa.x1xlr1w8.xzsf02u')[1].innerText;"
             )
            title_text = title_js_text
            price_elements_js = driver.execute_script(
                    """
                    let price = Array.from(document.querySelectorAll('div.x1xmf6yo >div > .x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x676frb.x1lkfr7t.x1lbecb7.x1s688f.xzsf02u'))
                    if(price.length == 0){
                        price = Array.from(document.querySelectorAll('div.x1xmf6yo >div > .x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x676frb.x1lkfr7t.x1lbecb7.xk50ysn.xzsf02u'))
                    }

                    if(price.length > 0){
                        return price[0]?.textContent
                    }else{
                        return 0
                    }
                    """
                )

            print(price_elements_js)
            price = price_elements_js

            
            def click_seemore():
                try:
                    see_more_element  = driver.find_element(By.XPATH, '//div[@role="button" and .//span[text()="See more"]]')        
                    if see_more_element:
                        see_more_element.click()
                except Exception as e:
                    print('exception')

        
            click_seemore()
            description_elements_js = driver.execute_script(
                """
                let description = Array.from(document.querySelectorAll('div.xz9dl7a.x4uap5.xsag5q8.xkhd6sd.x126k92a >div > span.x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x3x7a5m.x6prxxf.xvq8zen.xo1l8bm.xzsf02u'))
                if (description.length !==0){
                    return description[0].textContent
                }else{
                    return ''
                }
                """
            )
            print(description_elements_js)

            # Return the text content of the first element if it exists
            if len(description_elements_js) > 0:
                print(description_elements_js[0])
                description = description_elements_js[0]
            else:
                print("No description elements found.")

            
            return Response({
                'images': img_urls,
                'title': title_text,
                'price': price,
                'description': description,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'error':'some error occured'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
      
