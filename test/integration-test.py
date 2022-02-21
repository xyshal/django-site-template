import unittest
from selenium import webdriver

class IntegrationTest(unittest.TestCase):
    def setUp(self):
        # TODO: servce_log_path deprecated, please pass in a Service object
        self.driver = webdriver.Firefox(service_log_path='/data/webdriver.log')

    def tearDown(self):
        self.driver.quit()

    def test_example(self):
        self.driver.get("http://localhost")
        assert "Test Site" in self.driver.title, self.driver.title
        # TODO: find_element_by_* deprecated, use find_element() instead
        assert "The database has 0 records" in self.driver.find_element_by_id("nRecords").text

if __name__ == '__main__':
    unittest.main()
