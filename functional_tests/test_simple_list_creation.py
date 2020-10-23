from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_for_one_user(self):
        # User searches out new to-do app via its homepage
        self.browser.get(self.live_server_url)

        # User notices page title and header mention to-do lists
        self.browser.quit()
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # User is invited to enter a to-do list item immediately
        inputbox = self.get_item_input_box()
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # User types "Buy guitar strings" into a text box
        inputbox.send_keys('Buy guitar strings')

        # When user hits enter, page updates, now page lists
        # "1: Buy guitar strings" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy guitar strings')

        # There is still a text box inviting her to add another item.
        # User enters "Re-string guitar"
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Re-string guitar')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again - both items are now on the list
        self.wait_for_row_in_list_table('1: Buy guitar strings')
        self.wait_for_row_in_list_table('2: Re-string guitar')

        # Site has generated unique URL for user -- there is text explaining this
        # self.fail('Finish the test!')

        # User visits that URL - their to-do list is still there

        # Satisfied, they go on about their day

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy guitar strings')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy guitar strings')

        # Edith noticed that their list has a unique URL
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        ## We use a new browser session to make sure that no info
        ## of Edith's is coming through from cookies, etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. Cannot see Edith's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy guitar strings', page_text)
        self.assertNotIn('Re-string guitar', page_text)

        # Francis starts a new list by entering a new item.
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Francis gets own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # Again, no sign of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy guitar strings', page_text)
        self.assertIn('Buy milk', page_text)

        # Both satisfied - days carry on.