from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip

class ItemValidationTest(FunctionalTest):

	def test_cannot_add_empty_list_items(self):
		# Albert goes to the home page and accidentally tries to submit
		# an empty list item. He hits Enter on the empty input box
		self.browser.get(self.live_server_url)
		self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

		# The home page refreshes, and there is an error message saying
		# that list items cannot be blank
		# Pass to a new helper method called "wait_for"
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You can't have an empty list item"
		))

		# He tries again with some text for the item, which now works
		self.browser.find_element_by_id('id_new_item').send_keys('Buy milk')
		self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		# Perversely, he now decides to submit a second blank list item
		self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

		# He receives a similar warning on the list page
		self.wait_for(lambda: self.assertEqual(
			self.browser.find_element_by_css_selector('has-error').text,
			"You can't have an empty list item"
		))

		# He corrects it by filling some text in
		self.browser.find_element_by_id('id_new_item').send_keys('Make tea')
		self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for_row_in_list_table('2: Make tea')


		# He tries again with some text for the item, which now works
		# self.fail('Finish the test!')
