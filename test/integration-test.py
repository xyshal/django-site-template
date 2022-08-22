import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service

class IntegrationTest(unittest.TestCase):
    def setUp(self):
        service_obj = Service(log_path='/data/webdriver.log')
        self.driver = webdriver.Firefox(service=service_obj)

    def tearDown(self):
        self.driver.quit()

    def test_example(self):
        self.driver.get("http://localhost")
        assert "Test Site" in self.driver.title, self.driver.title
        assert "The database has 0 records" in self.driver.find_element(By.ID, "nRecords").text

if __name__ == '__main__':
    unittest.main()
