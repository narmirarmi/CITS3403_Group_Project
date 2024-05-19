import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import TestingConfig
from database.models import db
from core_app import create_app
import threading
import time

def run_app(app):
    app.run(debug=False, use_reloader=False)


class TestSocialMediaSite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize and configure the Flask app for testing with an in-memory database
        cls.app = create_app()  # Assuming create_app allows configuration overrides
        cls.app.config.update({
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'TESTING': True,
            'UPLOAD_FOLDER': '/upload_folder',  # Adjust as necessary
        })
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        with cls.app.app_context():
            db.create_all()

        # Start the Flask server in a background thread
        cls.server_thread = threading.Thread(target=run_app, args=(cls.app,))
        cls.server_thread.start()
        time.sleep(5)

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
        cls.server_thread.join()

    def setUp(self):
        # Setup method to initiate the WebDriver
        self.driver = webdriver.Chrome()


    def test_user_registration_and_login(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/login")

        # Navigate to the registration form
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "tab-register"))
        ).click()

        # Enter registration details
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "registerName"))
        ).send_keys("example name")
        driver.find_element(By.ID, "registerUsername").send_keys("exampleusername")
        driver.find_element(By.ID, "registerEmail").send_keys("email@example.com")
        driver.find_element(By.ID, "registerPassword").send_keys("password123")
        driver.find_element(By.ID, "registerRepeatPassword").send_keys("password123")
        driver.find_element(By.ID, "registerRepeatPassword").send_keys(Keys.RETURN)

        # Wait for and assert registration success message or redirect
        alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()

        # Navigate to the login form may not be needed as we refresh*
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "tab-login"))
        ).click()

        # Log in with the newly registered user
        driver.get("http://127.0.0.1:5000/login")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "loginName"))
        ).send_keys("email@example.com")
        driver.find_element(By.ID, "loginPassword").send_keys("password123")
        login_submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn.btn-primary.btn-block.mb-4"))
        )
        login_submit_button.click()

        # Verify login by checking if "Add New Listing" button is clickable
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-bs-target='#addListingModal']"))
        )
        self.assertTrue(driver.find_element(By.CSS_SELECTOR, "[data-bs-target='#addListingModal']").is_displayed())

    def tearDown(self):
        # Close the browser window
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()

    # TODO register same person test, login after registration test, database wiping, image uploading, commenting, liking / disliking an image