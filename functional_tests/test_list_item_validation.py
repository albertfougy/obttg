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
		self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You can't have an element list item"
		)

		# He tries again with some text for the item, which now works
		self.fail('Finish the test!')