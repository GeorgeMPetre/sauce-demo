from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select



class ProductPage:
    def __init__(self, driver):
        self.driver = driver

    def is_product_list_displayed(self):
        return len(self.driver.find_elements(By.CLASS_NAME, "inventory_item")) > 0

    def add_first_item_to_cart(self):
        self.driver.find_elements(By.CLASS_NAME, "btn_inventory")[0].click()

    def go_to_cart(self):
        self.driver.find_element(By.CSS_SELECTOR, ".shopping_cart_link").click()

    def get_all_product_images(self):
        return self.driver.find_elements(By.CLASS_NAME, "inventory_item_img")




    def sort_by_name_z_a(self):
        dropdown = self.driver.find_element(By.CLASS_NAME, "product_sort_container")
        select = Select(dropdown)
        select.select_by_value("za")
        print("Successfully attempted Z to A sort.")


    def sort_by_price_low_high(self):
        dropdown = self.driver.find_element(By.CLASS_NAME, "product_sort_container")
        select = Select(dropdown)
        select.select_by_value("lohi")
        print("Successfully attempted Low to High price sort.")

    def is_sorting_alert_displayed(self):
        self.driver.find_element(By.CLASS_NAME, "alert-info")

    def get_inventory_items_order(self):
        try:
            product_elements = self.driver.find_elements(By.CLASS_NAME, 'inventory_item_name')
            product_names = [product.text for product in product_elements]
            return product_names
        except Exception as e:
            print(f"Error while retrieving product names: {str(e)}")
            return []



    def sort_by_price_high_low(self):
            dropdown = self.driver.find_element(By.CLASS_NAME, "product_sort_container")
            select = Select(dropdown)
            select.select_by_value("hilo")
            print("Successfully attempted High to Low price sort.")



