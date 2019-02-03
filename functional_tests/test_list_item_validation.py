from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

	def test_cannot_add_empty_list_items(self):
		# Albert goes to the home page and accidentally tries to submit
		# an empty list item. He hits Enter on the empty input box
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys(Keys.ENTER)

        # The browser intercepts the request, and does not load the
        # list page
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:invalid'
			))


		# He starts typing some text for the new item and the error disappears 
		self.get_item_input_box().send_keys('Buy milk')
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:valid'
		))

		# Perversely, he now decides to submit a second blank list item
		self.get_item_input_box().send_keys(Keys.ENTER)


		# Again, the browser will not comply
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:invalid'
		))

		# He corrects it by filling some text in
		self.get_item_input_box().send_keys('Make tea')
		self.wait_for(lambda: self.browser.find_element_by_css_selector(
			'#id_text:valid'
		))
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for_row_in_list_table('2: Make tea')


		# He tries again with some text for the item, which now works
		# self.fail('Finish the test!')
