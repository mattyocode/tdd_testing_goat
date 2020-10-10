from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User searches out new to-do app via its homepage
        self.browser.get('http://localhost:8000')

        # User notices page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # User is invited to enter a to-do list item immediately
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # User types "Buy guitar strings" into a text box
        inputbox.send_keys('Buy guitar strings')

        # When user hits enter, page updates, now page lists
        # "1: Buy guitar strings" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy guitar strings')

        # There is still a text box inviting her to add another item.
        # User enters "Re-string guitar"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Re-string guitar')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again - both items are now on the list
        self.check_for_row_in_list_table('1: Buy guitar strings')
        self.check_for_row_in_list_table('2: Re-string guitar')

        # Site has generated unique URL for user -- there is text explaining this
        self.fail('Finish the test!')

        # User visits that URL - their to-do list is still there

        # Satisfied, they go on about their day

if __name__ == '__main__':
    unittest.main()