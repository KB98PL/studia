import unittest

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime
from datetime import timedelta


URL = 'http://127.0.0.1:8000'

class XPATH_LOCATORS:
    # Text fields
    FIRST_NAME = '//form[@id="formma"]//input[@id="inputEmail3"]'
    LAST_NAME  = '//form[@id="formma"]//input[@id="inputPassword3"]'
    BIRTH_DATE = '//form[@id="formma"]//input[@id="dataU"]'

    # Checkboxes
    PARENTS_AGREEMENT = '//form[@id="formma"]//input[@id="rodzice"]'
    DOCTORS_NOTE      = '//form[@id="formma"]//input[@id="lekarz"]'

    # Button
    SUBMIT_BUTTON = '//form[@id="formma"]//button[@class="btn btn-default"]'


class TestCases(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
    
    def tearDown(self):
        self.driver.quit()


    def wait_for_alert(self, timeout = 3):
        ''' Waits until alert pop up with given timeout '''
        WebDriverWait(self.driver, timeout).until(
            EC.alert_is_present(),
            'Waiting for alert timed out'
        )


    def test_case_1(self):
        ''' Submit empty form '''
        self.driver.get(URL)

        # Find and click the 'Wyslij' button
        button = self.driver.find_element_by_xpath(XPATH_LOCATORS.SUBMIT_BUTTON)
        button.click()

        # Read alert message
        self.wait_for_alert()
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()

        # Take screenshot
        self.driver.save_screenshot('screenshots/1.png')

        # Compare result with expected message
        expected_message = 'Imie musi byc wypelnione'
        self.assertEqual(alert_text, expected_message)


    def test_case_2(self):
        ''' Submit form without last name filled in '''
        self.driver.get(URL)

        # Fill the first name field
        first_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.FIRST_NAME)
        first_name.send_keys('Jan')

        # Now submit the form
        button = self.driver.find_element_by_xpath(XPATH_LOCATORS.SUBMIT_BUTTON)
        button.click()

        # Read alert message
        self.wait_for_alert()
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()

        # Take screenshot
        self.driver.save_screenshot('screenshots/2.png')

        # Compare result with expected message
        expected_message = 'Nazwisko musi byc wypelnione'
        self.assertEqual(alert_text, expected_message)

    
    def test_case_3(self):
        ''' Submit form without birth date filled in '''
        self.driver.get(URL)

        # Fill the first name field
        first_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.FIRST_NAME)
        first_name.send_keys('Jan')

        # Fill the last name field
        last_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.LAST_NAME)
        last_name.send_keys('Kowalski')

        # Now submit the form
        button = self.driver.find_element_by_xpath(XPATH_LOCATORS.SUBMIT_BUTTON)
        button.click()

        # Read alert message
        self.wait_for_alert()
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()

        # Take screenshot
        self.driver.save_screenshot('screenshots/3.png')

        # Compare result with expected message
        expected_message = 'Data urodzenia nie moze byc pusta'
        self.assertEqual(alert_text, expected_message)


    def test_case_4(self):
        ''' Submit form with invalid birth date but in correct form (as date) '''
        self.driver.get(URL)

        # Fill the first name field
        first_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.FIRST_NAME)
        first_name.send_keys('Jan')

        # Fill the last name field
        last_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.LAST_NAME)
        last_name.send_keys('Kowalski')

        # Fill the birth date field with year higher than current year
        birth_date = self.driver.find_element_by_xpath(XPATH_LOCATORS.BIRTH_DATE)
        birth_date.send_keys('01-01-2030')

        # Now submit the form
        button = self.driver.find_element_by_xpath(XPATH_LOCATORS.SUBMIT_BUTTON)
        button.click()

        # Skip first alert
        self.wait_for_alert()
        self.driver.switch_to.alert.accept()

        # Read second alert message
        self.wait_for_alert()
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()

        # Take screenshot
        self.driver.save_screenshot('screenshots/4.png')

        # Compare result with expected message
        expected_message = 'Blad danych'
        self.assertEqual(alert_text, expected_message)


    def test_case_5(self):
        ''' Submit form with birth date in invalid format '''
        self.driver.get(URL)

        # Fill the first name field
        first_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.FIRST_NAME)
        first_name.send_keys('Jan')

        # Fill the last name field
        last_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.LAST_NAME)
        last_name.send_keys('Kowalski')

        # Fill the birth date field with year higher than current year
        birth_date = self.driver.find_element_by_xpath(XPATH_LOCATORS.BIRTH_DATE)
        birth_date.send_keys('tekst')

        # Now submit the form
        button = self.driver.find_element_by_xpath(XPATH_LOCATORS.SUBMIT_BUTTON)
        button.click()

        # Skip first alert
        self.wait_for_alert()
        self.driver.switch_to.alert.accept()

        # Read second alert message
        self.wait_for_alert()
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()

        # Take screenshot
        self.driver.save_screenshot('screenshots/5.png')

        # Compare result with expected message
        expected_message = 'Blad danych'
        self.assertEqual(alert_text, expected_message)


    def test_case_6(self):
        ''' Submit form with spaces as a birth date '''
        self.driver.get(URL)

        # Fill the first name field
        first_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.FIRST_NAME)
        first_name.send_keys('Jan')

        # Fill the last name field
        last_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.LAST_NAME)
        last_name.send_keys('Kowalski')

        # Fill the birth date field with year higher than current year
        birth_date = self.driver.find_element_by_xpath(XPATH_LOCATORS.BIRTH_DATE)
        birth_date.send_keys('     ')

        # Check the checkbox
        doctors_note = self.driver.find_element_by_xpath(XPATH_LOCATORS.DOCTORS_NOTE)
        doctors_note.click()

        # Now submit the form
        button = self.driver.find_element_by_xpath(XPATH_LOCATORS.SUBMIT_BUTTON)
        button.click()

        # Skip first alert
        self.wait_for_alert()
        self.driver.switch_to.alert.accept()

        # Read second alert message
        self.wait_for_alert()
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()

        # Take screenshot
        self.driver.save_screenshot('screenshots/6.png')

        # Compare result with expected message
        expected_message = 'Blad danych'
        self.assertEqual(alert_text, expected_message)

    
    def test_case_7(self):
        ''' Submit form with data for person without classification '''
        self.driver.get(URL)

        # Fill the first name field
        first_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.FIRST_NAME)
        first_name.send_keys('Jan')

        # Fill the last name field
        last_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.LAST_NAME)
        last_name.send_keys('Kowalski')

        # Calculate date 1 year before
        now = datetime.today()
        date_of_birth = datetime(year = now.year - 1, month = now.month, day = now.day)

        # Fill the birth date field with year higher than current year
        birth_date = self.driver.find_element_by_xpath(XPATH_LOCATORS.BIRTH_DATE)
        birth_date.send_keys(date_of_birth.strftime('%d-%m-%Y'))

        # Check the checkboxes
        doctors_note = self.driver.find_element_by_xpath(XPATH_LOCATORS.DOCTORS_NOTE)
        parents_agreement = self.driver.find_element_by_xpath(XPATH_LOCATORS.PARENTS_AGREEMENT)
        doctors_note.click()
        parents_agreement.click()

        # Now submit the form
        button = self.driver.find_element_by_xpath(XPATH_LOCATORS.SUBMIT_BUTTON)
        button.click()

        # Skip first alert
        self.wait_for_alert()
        self.driver.switch_to.alert.accept()

        # Read second alert message
        self.wait_for_alert()
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()

        # Take screenshot
        self.driver.save_screenshot('screenshots/7.png')

        # Compare result with expected message
        expected_message = 'Brak kwalifikacji'
        self.assertEqual(alert_text, expected_message)
    

    def test_case_8(self):
        ''' Submit form with data for 'Mlodzik' classification: Lower bound '''
        self.driver.get(URL)

        # Fill the first name field
        first_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.FIRST_NAME)
        first_name.send_keys('Jan')

        # Fill the last name field
        last_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.LAST_NAME)
        last_name.send_keys('Kowalski')

        # Today 10th birthday
        now = datetime.today()
        date_of_birth = datetime(year = now.year - 10, month = now.month, day = now.day)

        # Fill the birth date field with year higher than current year
        birth_date = self.driver.find_element_by_xpath(XPATH_LOCATORS.BIRTH_DATE)
        birth_date.send_keys(date_of_birth.strftime('%d-%m-%Y'))

        # Check the checkboxes
        doctors_note = self.driver.find_element_by_xpath(XPATH_LOCATORS.DOCTORS_NOTE)
        parents_agreement = self.driver.find_element_by_xpath(XPATH_LOCATORS.PARENTS_AGREEMENT)
        doctors_note.click()
        parents_agreement.click()

        # Now submit the form
        button = self.driver.find_element_by_xpath(XPATH_LOCATORS.SUBMIT_BUTTON)
        button.click()

        # Skip first alert
        self.wait_for_alert()
        self.driver.switch_to.alert.accept()

        # Read second alert message
        self.wait_for_alert()
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()

        # Take screenshot
        self.driver.save_screenshot('screenshots/8.png')

        # Compare result with expected message
        expected_message = 'Mlodzik'
        self.assertEqual(alert_text, expected_message)

    
    def test_case_9(self):
        ''' Submit form with data for 'Mlodzik' classification: Upper bound '''
        self.driver.get(URL)

        # Fill the first name field
        first_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.FIRST_NAME)
        first_name.send_keys('Jan')

        # Fill the last name field
        last_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.LAST_NAME)
        last_name.send_keys('Kowalski')

        # Tomorrow 14th birthday
        now = datetime.today()
        date_of_birth = datetime(year = now.year - 14, month = now.month, day = now.day)
        date_of_birth += timedelta(1)

        # Fill the birth date field with year higher than current year
        birth_date = self.driver.find_element_by_xpath(XPATH_LOCATORS.BIRTH_DATE)
        birth_date.send_keys(date_of_birth.strftime('%d-%m-%Y'))

        # Check the checkboxes
        doctors_note = self.driver.find_element_by_xpath(XPATH_LOCATORS.DOCTORS_NOTE)
        parents_agreement = self.driver.find_element_by_xpath(XPATH_LOCATORS.PARENTS_AGREEMENT)
        doctors_note.click()
        parents_agreement.click()

        # Now submit the form
        button = self.driver.find_element_by_xpath(XPATH_LOCATORS.SUBMIT_BUTTON)
        button.click()

        # Skip first alert
        self.wait_for_alert()
        self.driver.switch_to.alert.accept()

        # Read second alert message
        self.wait_for_alert()
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()

        # Take screenshot
        self.driver.save_screenshot('screenshots/9.png')

        # Compare result with expected message
        expected_message = 'Mlodzik'
        self.assertEqual(alert_text, expected_message)


    def test_case_10(self):
        ''' Submit form with data for 'Junior' classification: Lower bound '''
        self.driver.get(URL)

        # Fill the first name field
        first_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.FIRST_NAME)
        first_name.send_keys('Jan')

        # Fill the last name field
        last_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.LAST_NAME)
        last_name.send_keys('Kowalski')

        # Today 14th birthday
        now = datetime.today()
        date_of_birth = datetime(year = now.year - 14, month = now.month, day = now.day)

        # Fill the birth date field with year higher than current year
        birth_date = self.driver.find_element_by_xpath(XPATH_LOCATORS.BIRTH_DATE)
        birth_date.send_keys(date_of_birth.strftime('%d-%m-%Y'))

        # Check the checkboxes
        doctors_note = self.driver.find_element_by_xpath(XPATH_LOCATORS.DOCTORS_NOTE)
        parents_agreement = self.driver.find_element_by_xpath(XPATH_LOCATORS.PARENTS_AGREEMENT)
        doctors_note.click()
        parents_agreement.click()

        # Now submit the form
        button = self.driver.find_element_by_xpath(XPATH_LOCATORS.SUBMIT_BUTTON)
        button.click()

        # Skip first alert
        self.wait_for_alert()
        self.driver.switch_to.alert.accept()

        # Read second alert message
        self.wait_for_alert()
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()

        # Take screenshot
        self.driver.save_screenshot('screenshots/10.png')

        # Compare result with expected message
        expected_message = 'Junior'
        self.assertEqual(alert_text, expected_message)


    def test_case_11(self):
        ''' Submit form with data for 'Junior' classification: Upper bound '''
        self.driver.get(URL)

        # Fill the first name field
        first_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.FIRST_NAME)
        first_name.send_keys('Jan')

        # Fill the last name field
        last_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.LAST_NAME)
        last_name.send_keys('Kowalski')

        # Tomorrow 18th birthday
        now = datetime.today()
        date_of_birth = datetime(year = now.year - 18, month = now.month, day = now.day)
        date_of_birth += timedelta(1)

        # Fill the birth date field with year higher than current year
        birth_date = self.driver.find_element_by_xpath(XPATH_LOCATORS.BIRTH_DATE)
        birth_date.send_keys(date_of_birth.strftime('%d-%m-%Y'))

        # Check the checkboxes
        doctors_note = self.driver.find_element_by_xpath(XPATH_LOCATORS.DOCTORS_NOTE)
        parents_agreement = self.driver.find_element_by_xpath(XPATH_LOCATORS.PARENTS_AGREEMENT)
        doctors_note.click()
        parents_agreement.click()

        # Now submit the form
        button = self.driver.find_element_by_xpath(XPATH_LOCATORS.SUBMIT_BUTTON)
        button.click()

        # Skip first alert
        self.wait_for_alert()
        self.driver.switch_to.alert.accept()

        # Read second alert message
        self.wait_for_alert()
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()

        # Take screenshot
        self.driver.save_screenshot('screenshots/11.png')

        # Compare result with expected message
        expected_message = 'Junior'
        self.assertEqual(alert_text, expected_message)


    def test_case_12(self):
        ''' Submit form with data for 'Dorosly' classification: Lower bound '''
        self.driver.get(URL)

        # Fill the first name field
        first_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.FIRST_NAME)
        first_name.send_keys('Jan')

        # Fill the last name field
        last_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.LAST_NAME)
        last_name.send_keys('Kowalski')

        # Today 18th birthday
        now = datetime.today()
        date_of_birth = datetime(year = now.year - 18, month = now.month, day = now.day)

        # Fill the birth date field with year higher than current year
        birth_date = self.driver.find_element_by_xpath(XPATH_LOCATORS.BIRTH_DATE)
        birth_date.send_keys(date_of_birth.strftime('%d-%m-%Y'))

        # Now submit the form
        button = self.driver.find_element_by_xpath(XPATH_LOCATORS.SUBMIT_BUTTON)
        button.click()

        # Skip first alert
        self.wait_for_alert()
        self.driver.switch_to.alert.accept()

        # Read second alert message
        self.wait_for_alert()
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()

        # Take screenshot
        self.driver.save_screenshot('screenshots/12.png')

        # Compare result with expected message
        expected_message = 'Dorosly'
        self.assertEqual(alert_text, expected_message)


    def test_case_13(self):
        ''' Submit form with data for 'Dorosly' classification: Upper bound '''
        self.driver.get(URL)

        # Fill the first name field
        first_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.FIRST_NAME)
        first_name.send_keys('Jan')

        # Fill the last name field
        last_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.LAST_NAME)
        last_name.send_keys('Kowalski')

        # Tomorrow 65th birthday
        now = datetime.today()
        date_of_birth = datetime(year = now.year - 65, month = now.month, day = now.day)
        date_of_birth += timedelta(1)

        # Fill the birth date field with year higher than current year
        birth_date = self.driver.find_element_by_xpath(XPATH_LOCATORS.BIRTH_DATE)
        birth_date.send_keys(date_of_birth.strftime('%d-%m-%Y'))

        # Now submit the form
        button = self.driver.find_element_by_xpath(XPATH_LOCATORS.SUBMIT_BUTTON)
        button.click()

        # Skip first alert
        self.wait_for_alert()
        self.driver.switch_to.alert.accept()

        # Read second alert message
        self.wait_for_alert()
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()

        # Take screenshot
        self.driver.save_screenshot('screenshots/13.png')

        # Compare result with expected message
        expected_message = 'Dorosly'
        self.assertEqual(alert_text, expected_message)


    def test_case_14(self):
        ''' Submit form with data for 'Senior' classification '''
        self.driver.get(URL)

        # Fill the first name field
        first_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.FIRST_NAME)
        first_name.send_keys('Jan')

        # Fill the last name field
        last_name = self.driver.find_element_by_xpath(XPATH_LOCATORS.LAST_NAME)
        last_name.send_keys('Kowalski')

        # Today 65th birthday
        now = datetime.today()
        date_of_birth = datetime(year = now.year - 65, month = now.month, day = now.day)

        # Fill the birth date field with year higher than current year
        birth_date = self.driver.find_element_by_xpath(XPATH_LOCATORS.BIRTH_DATE)
        birth_date.send_keys(date_of_birth.strftime('%d-%m-%Y'))

        # Now submit the form
        button = self.driver.find_element_by_xpath(XPATH_LOCATORS.SUBMIT_BUTTON)
        button.click()

        # Skip first alert
        self.wait_for_alert()
        self.driver.switch_to.alert.accept()

        # Read second alert message
        self.wait_for_alert()
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()

        # Take screenshot
        self.driver.save_screenshot('screenshots/14.png')

        # Compare result with expected message
        expected_message = 'Senior'
        self.assertEqual(alert_text, expected_message)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCases)
    unittest.TextTestRunner(verbosity = 2).run(suite)