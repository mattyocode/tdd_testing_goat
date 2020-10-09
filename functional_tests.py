from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User searches out new to-do app via its homepage
        self.browser.get('http://localhost:8000')

        # User notices page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # User is invited to enter a to-do list item immediately

        # User types "Buy guitar strings" into a text box

        # When user hits enter, page updates, now page lists
        # "1: Buy guitar strings" as an item in a to-do list

        # There is still a text box inviting her to add another item.
        # User enters "Re-string guitar"

        # The page updates again - both items are now on the list

        # Site has generated unique URL for user -- there is text explaining this

        # User visits that URL - their to-do list is still there

        # Satisfied, they go on about their day

if __name__ == '__main__':
    unittest.main()