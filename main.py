import time
from selenium import webdriver
from twocaptcha import TwoCaptcha


BASE_URL="https://www.google.com/recaptcha/api2/demo"
# BASE_URL="https://recaptcha-demo.appspot.com/recaptcha-v2-checkbox.php"

class FormFill(webdriver.Chrome):
    def __init__(self, driver_path="./chromedriver.exe", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super(FormFill, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self,exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()
        
    def open_form_link(self):
        self.get(BASE_URL)

    def solve(self, api):
        solver = TwoCaptcha(api)
        print(self.current_url)
        result = solver.recaptcha(
            sitekey='6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-',
            url=BASE_URL
        )
        while True:
            print("Waiting for result...")
            if len(result['code']) < 30 or False:
                time.sleep(3)
                # continue
            else:
                break
        
        
        print(result)

        self.execute_script("document.getElementById('g-recaptcha-response').style.display = 'block';")
        textarea = self.find_element_by_id('g-recaptcha-response')
        # textarea.clear()
        textarea.send_keys(result['code'])
        self.execute_script("document.getElementById('g-recaptcha-response').style.display = 'none';")

        submit_btn = self.find_element_by_id('recaptcha-demo-submit')
        submit_btn.click()            



if __name__ == '__main__':
    api_key = 'YOUR API KEY' #purchase api key from https://2captcha.com
    test = FormFill()
    test.open_form_link()
    test.solve(api_key)


