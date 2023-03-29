from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
import pytest
from pathlib import Path
from datetime import date


class Test_Demo_Class:

    def setup_method(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://www.saucedemo.com/")
        self.folderPath = str(date.today())
        Path(self.folderPath).mkdir(exist_ok=True)

    def teardown_method(self):
        self.driver.quit()

    def test_sadece_tik(self):
        self.waitForElementVisible((By.ID, 'login-button'))
        loginBtn = self.driver.find_element(By.ID, 'login-button')
        loginBtn.click()

        errorMessage = self.driver.find_element(By.XPATH, '//*[@id="login_button_container"]/div/form/div[3]/h3')
        self.driver.save_screenshot(f"{self.folderPath}/test_sadece_tik.png")

        assert errorMessage.text == "Epic sadface: Username is required"

    @pytest.mark.parametrize("username", ["denemea"])
    def test_sadece_kul_ad(self, username):
        self.waitForElementVisible((By.ID, 'user-name'))
        usernameInput = self.driver.find_element(By.ID, 'user-name')
        usernameInput.send_keys(username)
        self.waitForElementVisible((By.ID, 'login-button'))
        loginBtn = self.driver.find_element(By.ID, 'login-button')
        loginBtn.click()
        errorMessage = self.driver.find_element(By.XPATH, '//*[@id="login_button_container"]/div/form/div[3]/h3')
        self.driver.save_screenshot(f"{self.folderPath}/-{username}-test_sadece_ad.png")
        assert errorMessage.text == "Epic sadface: Password is required"

    @pytest.mark.parametrize("password", ["64851"])    
    def test_sadece_sifre(self,password):
        self.waitForElementVisible((By.ID, "password"))
        usernameInput = self.driver.find_element(By.ID, "password")
        usernameInput.send_keys(password)
        self.waitForElementVisible((By.ID, "login-button"))
        loginBtn = self.driver.find_element(By.ID, "login-button")
        loginBtn.click()
        errorMessage = self.driver.find_element(By.XPATH, '//*[@id="login_button_container"]/div/form/div[3]/h3')
        self.driver.save_screenshot(f"{self.folderPath}/-{password}-test_sadece_ad.png")
        assert errorMessage.text == "Epic sadface: Username is required"

    @pytest.mark.parametrize("username,password",[("1","1"),("kullaniciadim","sifrem")])
    def test_invalid_login(self,username,password):
        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_all_elements_located((By.ID,"user-name")))
        usernameInput = self.driver.find_element(By.ID,"user-name")
        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_all_elements_located((By.ID,"password")))
        passwordInput = self.driver.find_element(By.ID,"password")

        usernameInput.send_keys(username)
        passwordInput.send_keys(password)
        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_all_elements_located((By.ID,"login-button")))

        loginButton = self.driver.find_element(By.ID,"login-button")
        loginButton.click()
        WebDriverWait(self.driver,5).until(expected_conditions.visibility_of_all_elements_located((By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")))

        errorMassage = self.driver.find_element(By.XPATH,"//*[@id='login_button_container']/div/form/div[3]/h3")
        self.driver.save_screenshot(f"{self.folderPath}/test-invalid-login.png")

        assert errorMassage.text == "Epic sadface: Username and password do not match any user in this service"

    def test_error_icon(self):
        self.waitForElementVisible((By.ID, "login-button"))
        loginBtn = self.driver.find_element(By.ID, "login-button")
        loginBtn.click()

        errorBtn = self.driver.find_element(By.CLASS_NAME, "error-button")
        self.driver.save_screenshot(f"{self.folderPath}/test-error_icon.png")
        errorIcon = len(self.driver.find_elements(By.CLASS_NAME, "error_icon"))
        errorBtn.click()

        assert errorIcon > 0


    @pytest.mark.parametrize("username, password", [("standard_user", "secret_sauce")])
    def test_success_login(self,username,password):
     
     self.waitForElementVisible((By.ID,"user-name"))
     usernameInput = self.driver.find_element(By.ID, "user-name")

     self.waitForElementVisible((By.ID,"password"),10)
     passwordInput = self.driver.find_element(By.ID,"password")

     usernameInput.send_keys(username)
     passwordInput.send_keys(password)

     loginBtn = self.driver.find_element(By.ID,"login-button")
     loginBtn.click()

     self.waitForElementVisible((By.CLASS_NAME, "inventory_list"))
     products = self.driver.find_elements(By.CLASS_NAME, 'inventory_item')
     self.driver.save_screenshot(f"{self.folderPath}/test-success-login.png")
     assert len(products) == 6

    @pytest.mark.parametrize("username, password", [("standard_user", "123456789"), ("standard_user", "987654321"), ("standard_user", "456789123")])
    def test_yanlis_sifre_login(self, username, password):
        self.waitForElementVisible((By.ID, 'user-name'))
        usernameInput = self.driver.find_element(By.ID, 'user-name')
        passwordInput = self.driver.find_element(By.ID, 'password')
        loginBtn = self.driver.find_element(By.ID, 'login-button')

        actions = ActionChains(self.driver)
        actions.send_keys_to_element(usernameInput, username)
        actions.send_keys_to_element(passwordInput, password)
        actions.send_keys_to_element(loginBtn, Keys.ENTER)
        actions.perform()

        errorMessage = self.driver.find_element(By.XPATH, '//*[@id="login_button_container"]/div/form/div[3]/h3')
        self.driver.save_screenshot(f"{self.folderPath}/test_yanlis_sifre_login-{username}-{password}-login.png")
        assert errorMessage.text == 'Epic sadface: Username and password do not match any user in this service'
    
    @pytest.mark.parametrize("username, password", [("standard_user", "secret_sauce")])       
    def test_About(self,username,password):
        Test_Demo_Class.test_menu_yardım(self,username,password)
     
        self.waitForElementVisible((By.ID, 'about_sidebar_link'))
        about= self.driver.find_element(By.ID, 'about_sidebar_link')
        about.click()
        self.driver.save_screenshot(f"{self.folderPath}/test_About.png")

    @pytest.mark.parametrize("username, password", [("standard_user", "secret_sauce")])  
    def test_LogOut(self,username,password):
        Test_Demo_Class.test_menu_yardım(self,username,password)
     
        self.waitForElementVisible((By.ID, 'logout_sidebar_link'))
        about= self.driver.find_element(By.ID, 'logout_sidebar_link')
        self.driver.save_screenshot(f"{self.folderPath}/test_LogOut.png")    
        about.click()
        
    @pytest.mark.parametrize("username, password", [("standard_user", "secret_sauce")])
    def test_menu_yardım(self,username,password):
        self.waitForElementVisible((By.ID, 'user-name'))
        usernameInput = self.driver.find_element(By.ID, 'user-name')
        passwordInput = self.driver.find_element(By.ID, 'password')
        loginBtn = self.driver.find_element(By.ID, 'login-button')
        
        actions = ActionChains(self.driver)
        actions.send_keys_to_element(usernameInput, username)
        actions.send_keys_to_element(passwordInput, password)
        actions.send_keys_to_element(loginBtn, Keys.ENTER)
        actions.perform()

        self.waitForElementVisible((By.XPATH, "/html/body/div/div/div/div[1]/div[1]/div[1]/div/div[1]/div/button"))
        git = self.driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[1]/div[1]/div/div[1]/div/button')
        git.click()
    
    def waitForElementVisible(self, locator, timeout=5):
        WebDriverWait(self.driver, timeout).until(expected_conditions.visibility_of_element_located(locator))