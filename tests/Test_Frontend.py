import subprocess
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
import unittest
import time

from src import getConfig


class TestFrontend(unittest.TestCase):

    def setUp(self):
        self.server = subprocess.Popen(["../venv/bin/python", "../src/main.py"], stdout=subprocess.PIPE)
        time.sleep(1)  # Wait for the server to start
        self.driver = webdriver.Firefox()  # or webdriver.Chrome(), depending on your browser
        driver = self.driver
        driver.get(
            f'http://localhost:{getConfig.get_config("application_port")}/register')  # replace with the URL of your login page

        # Find the form elements
        firstname_input = driver.find_element(By.NAME, 'vname')
        lastname_input = driver.find_element(By.NAME, 'nname')
        submit_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')

        # Fill out the form
        firstname_input.send_keys('test')
        lastname_input.send_keys('user')

        # Submit the form
        submit_button.click()

    def test_login_form(self):
        driver = self.driver
        # Check the result
        user_id_element = driver.find_element(By.XPATH, "//h2[contains(text(), 'Home of test ID: ')]")
        user_id = user_id_element.text.split(' ')
        user_name = user_id[2]
        user_id = user_id[4]
        self.assertIsNotNone(user_id)
        self.assertEqual(user_id, '52')
        self.assertEqual(user_name, 'test')
        cookie = self.driver.get_cookie('UserID')
        self.assertIsNotNone(cookie)
        self.assertEqual(cookie['value'], '52')

    def test_meal_selector_page_minus(self):
        driver = self.driver
        driver.get(
            f'http://localhost:{getConfig.get_config("application_port")}/mealselector')  # replace with the URL of your meal selector page
        time.sleep(3)
        kid_vegetarian_counter = driver.find_element(By.XPATH,
                                                     '//div[@id="kid_vegetarian_ct"]//div[contains(@class, "amount")]')
        normal_counter = driver.find_element(By.XPATH,
                                             '//div[@id="normal_ct"]//div[contains(@class, "amount")]')
        vegetarian_counter = driver.find_element(By.XPATH,
                                                 '//div[@id="vegetarian_ct"]//div[contains(@class, "amount")]')
        kid_normal_counter = driver.find_element(By.XPATH,
                                                 '//div[@id="kid_normal_ct"]//div[contains(@class, "amount")]')
        kid_vegetarian_plus_button = driver.find_element(By.XPATH,
                                                         '//div[@id="kid_vegetarian_ct"]//button[contains(@class, "minus")]')
        normal_plus_button = driver.find_element(By.XPATH,
                                                 '//div[@id="normal_ct"]//button[contains(@class, "minus")]')
        vegetarian_plus_button = driver.find_element(By.XPATH,
                                                     '//div[@id="vegetarian_ct"]//button[contains(@class, "minus")]')
        kid_normal_plus_button = driver.find_element(By.XPATH,
                                                     '//div[@id="kid_normal_ct"]//button[contains(@class, "minus")]')
        # Find the form elements
        normal_rand = random.randrange(1, 4)
        kid_vegetarian_rand = random.randrange(1, 4)
        vegetarian_rand = random.randrange(1, 4)
        kid_normal_rand = random.randrange(1, 4)
        normal_counter = int(normal_counter.text) - normal_rand
        vegetarian_counter = int(vegetarian_counter.text) - vegetarian_rand
        kid_normal_counter = int(kid_normal_counter.text) - kid_normal_rand
        kid_vegetarian_counter = int(kid_vegetarian_counter.text) - kid_vegetarian_rand
        for i in range(normal_rand):
            normal_plus_button.click()
        for i in range(vegetarian_rand):
            vegetarian_plus_button.click()
        for i in range(kid_normal_rand):
            kid_normal_plus_button.click()
        for i in range(kid_vegetarian_rand):
            kid_vegetarian_plus_button.click()
        confirm_button = driver.find_element(By.ID, 'bestaetigen')
        self.assertIsNotNone(confirm_button)
        confirm_button.click()
        time.sleep(6)
        self.assertEqual(driver.current_url, f'http://localhost:{getConfig.get_config("application_port")}/home')
        driver.get(
            f'http://localhost:{getConfig.get_config("application_port")}/mealselector')  # replace with the URL of your meal selector page
        time.sleep(2)
        kid_vegetarian_counter_after_plus = driver.find_element(By.XPATH,
                                                                '//div[@id="kid_vegetarian_ct"]//div[contains(@class, "amount")]')
        normal_counter_after_plus = driver.find_element(By.XPATH,
                                                        '//div[@id="normal_ct"]//div[contains(@class, "amount")]')
        vegetarian_counter_after_plus = driver.find_element(By.XPATH,
                                                            '//div[@id="vegetarian_ct"]//div[contains(@class, "amount")]')
        kid_normal_counter_after_plus = driver.find_element(By.XPATH,
                                                            '//div[@id="kid_normal_ct"]//div[contains(@class, "amount")]')
        self.assertEqual(int(kid_vegetarian_counter_after_plus.text), int(kid_vegetarian_counter))
        self.assertEqual(int(normal_counter_after_plus.text), int(normal_counter))
        self.assertEqual(int(vegetarian_counter_after_plus.text), int(vegetarian_counter))
        self.assertEqual(int(kid_normal_counter_after_plus.text), int(kid_normal_counter))

    def test_meal_selector_page_plus(self):
        driver = self.driver
        driver.get(
            f'http://localhost:{getConfig.get_config("application_port")}/mealselector')  # replace with the URL of your meal selector page
        time.sleep(2)
        kid_vegetarian_counter = driver.find_element(By.XPATH,
                                                     '//div[@id="kid_vegetarian_ct"]//div[contains(@class, "amount")]')
        normal_counter = driver.find_element(By.XPATH,
                                             '//div[@id="normal_ct"]//div[contains(@class, "amount")]')
        vegetarian_counter = driver.find_element(By.XPATH,
                                                 '//div[@id="vegetarian_ct"]//div[contains(@class, "amount")]')
        kid_normal_counter = driver.find_element(By.XPATH,
                                                 '//div[@id="kid_normal_ct"]//div[contains(@class, "amount")]')
        kid_vegetarian_plus_button = driver.find_element(By.XPATH,
                                                         '//div[@id="kid_vegetarian_ct"]//button[contains(@class, "plus")]')
        normal_plus_button = driver.find_element(By.XPATH,
                                                 '//div[@id="normal_ct"]//button[contains(@class, "plus")]')
        vegetarian_plus_button = driver.find_element(By.XPATH,
                                                     '//div[@id="vegetarian_ct"]//button[contains(@class, "plus")]')
        kid_normal_plus_button = driver.find_element(By.XPATH,
                                                     '//div[@id="kid_normal_ct"]//button[contains(@class, "plus")]')
        # Find the form elements
        normal_rand = random.randrange(4, 10)
        kid_vegetarian_rand = random.randrange(4, 10)
        vegetarian_rand = random.randrange(4, 10)
        kid_normal_rand = random.randrange(4, 10)
        normal_counter = int(normal_counter.text) + normal_rand
        vegetarian_counter = int(vegetarian_counter.text) + vegetarian_rand
        kid_normal_counter = int(kid_normal_counter.text) + kid_normal_rand
        kid_vegetarian_counter = int(kid_vegetarian_counter.text) + kid_vegetarian_rand
        for i in range(normal_rand):
            normal_plus_button.click()
        for i in range(vegetarian_rand):
            vegetarian_plus_button.click()
        for i in range(kid_normal_rand):
            kid_normal_plus_button.click()
        for i in range(kid_vegetarian_rand):
            kid_vegetarian_plus_button.click()

        confirm_button = driver.find_element(By.ID, 'bestaetigen')

        self.assertIsNotNone(confirm_button)
        confirm_button.click()
        time.sleep(6)
        self.assertEqual(driver.current_url, f'http://localhost:{getConfig.get_config("application_port")}/home')
        driver.get(f'http://localhost:{getConfig.get_config("application_port")}/mealselector')
        time.sleep(2)
        kid_vegetarian_counter_after_plus = driver.find_element(By.XPATH,
                                                                '//div[@id="kid_vegetarian_ct"]//div[contains(@class, "amount")]')
        normal_counter_after_plus = driver.find_element(By.XPATH,
                                                        '//div[@id="normal_ct"]//div[contains(@class, "amount")]')
        vegetarian_counter_after_plus = driver.find_element(By.XPATH,
                                                            '//div[@id="vegetarian_ct"]//div[contains(@class, "amount")]')
        kid_normal_counter_after_plus = driver.find_element(By.XPATH,
                                                            '//div[@id="kid_normal_ct"]//div[contains(@class, "amount")]')
        self.assertEqual(int(kid_vegetarian_counter_after_plus.text), int(kid_vegetarian_counter))
        self.assertEqual(int(normal_counter_after_plus.text), int(normal_counter))
        self.assertEqual(int(vegetarian_counter_after_plus.text), int(vegetarian_counter))
        self.assertEqual(int(kid_normal_counter_after_plus.text), int(kid_normal_counter))

    def tearDown(self):
        self.driver.close()
        self.server.terminate()
        self.server.kill()
        self.driver.quit()


def suite():
    suite_var = unittest.TestSuite()
    suite_var.addTest(TestFrontend('test_login_form'))
    suite_var.addTest(TestFrontend('test_meal_selector_page_plus'))
    suite_var.addTest(TestFrontend('test_meal_selector_page_minus'))
    return suite_var


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
