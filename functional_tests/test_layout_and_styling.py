from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys


class LayoutAndStyling(FunctionalTest):
		# Satisfied, they both go back to sleep
	def test_layout_and_styling(self):
			# Albert goes to the homepage
			self.browser.get(self.live_server_url)
			self.browser.set_window_size(1024, 768)

			# She notices the input box is nicely centered
			inputbox = self.browser.find_element_by_id('id_new_item')
			self.assertAlmostEqual(
				inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10
			)