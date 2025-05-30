from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from services.driver import DriverSetup

class LinkedInLogin:
    def __init__(self):
        self.driver= DriverSetup.setup_driver()

    def login_with_credentials(self,  linkedin_email, linkedin_password):

        self.driver.get("https://www.linkedin.com/login")

        try:
            # Wait for email field and enter email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.send_keys(linkedin_email)

            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(linkedin_password)

            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()

            # Wait for successful login
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("linkedin.com/feed")
            )
            print("Successfully logged in with credentials.")
            return True

        except Exception as e:
            print(f"Login failed: {e}")
            return False