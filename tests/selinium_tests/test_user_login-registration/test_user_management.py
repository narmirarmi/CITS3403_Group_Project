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


def run_app(app):
    app.run(debug=False, use_reloader=False)


class TestSocialMediaSite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize and configure the Flask app for testing
        cls.app = create_app(config_class=TestingConfig)
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

        # Start the Flask server in a background thread
        cls.server_thread = threading.Thread(target=run_app, args=(cls.app,))
        cls.server_thread.start()

    def setUp(self):
        # Setup method to initiate the WebDriver
        self.driver = webdriver.Chrome()

    def test_user_registration(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/login")

        # Click the 'Register' pill to switch to the registration form from the login form
        register_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "tab-register"))
        )
        register_tab.click()

        # Wait for registration form to be visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "pills-register"))
        )

        # Locate input fields by id
        name = driver.find_element(By.ID, "registerName")
        username = driver.find_element(By.ID, "registerUsername")
        email = driver.find_element(By.ID, "registerEmail")
        password = driver.find_element(By.ID, "registerPassword")
        confirm_password = driver.find_element(By.ID, "registerRepeatPassword")

        # Send keys for registration details
        name.send_keys("example name3")
        username.send_keys("example username3")
        email.send_keys("Imran3@example.com")
        password.send_keys("password123")
        confirm_password.send_keys("password123")
        confirm_password.send_keys(Keys.RETURN)

        # Wait for and handle the alert
        try:
            WebDriverWait(driver, 10).until(EC.alert_is_present(),
                                            "Timed out waiting for registration success alert to appear.")
            alert = driver.switch_to.alert
            alert_text = alert.text
            # Assert the alert text to confirm successful registration
            self.assertEqual("Registration successful!", alert_text)
            alert.accept()
            print("Registration success alert was confirmed and accepted.")
        except TimeoutException:
            print("No alert appeared within 10 seconds")

        def test_user_login(self):
            driver = self.driver
            driver.get("http://127.0.0.1:5000/login")

            # Locate input fields by id
            email = driver.find_element(By.ID, "loginName")
            password = driver.find_element(By.ID, "loginPassword")

            # Send keys for registration details
            email.send_keys("testuser")
            password.send_keys("password123")
            confirm_password.send_keys("password123")
            confirm_password.send_keys(Keys.RETURN)

            # Wait for the registration to complete and check for success message
            success_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "success_message"))
            )
            # Verify registration was successful
            self.assertIn("Registration successful", success_message.text)

    def tearDown(self):
        # Close the browser window
        self.driver.quit()

    @classmethod
    def tearDownClass(cls):
        # This part ensures that the application and server are properly shutdown
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()
        # Stopping the Flask server
        cls.server_thread.join()


if __name__ == "__main__":
    unittest.main()

    # TODO register same person test, login after registration test, database wiping, image uploading, commenting, liking / disliking an image