from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from web_scrape_src.web_scrap_code import get_route_link_map, extract_bus_info

if __name__ == "__main__":
    driver = webdriver.Edge()
    driver.maximize_window()
    action = ActionChains(driver)
    route_link_map = get_route_link_map(driver, action)
    bus_info = extract_bus_info(driver, route_link_map)
    driver.quit()