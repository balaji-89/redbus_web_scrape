from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from scrapping_src import get_route_link_map, extract_bus_info
from sql_src import connect_sql_server,add_route, add_bus_info


if __name__ == "__main__":

    #scrapping data
    driver = webdriver.Edge()
    driver.maximize_window()
    action = ActionChains(driver)
    route_link_map = get_route_link_map(driver, action)
    bus_info = extract_bus_info(driver, route_link_map)
    driver.quit()

    #saving to sql
    cursor = connect_sql_server('localhost', 'root', 'password')
    add_route(cursor,route_link_map)
    add_bus_info(cursor,bus_info)
