from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from scrapping_src.code import get_route_link_map, extract_bus_info
from sql_src.code import add_route, add_bus_info
import mysql.connector


if __name__ == "__main__":

    #scrapping data
    driver = webdriver.Edge()
    driver.maximize_window()
    action = ActionChains(driver)
    route_link_map = get_route_link_map(driver, action)
    bus_info = extract_bus_info(driver, route_link_map)
    driver.quit()

    #saving to sql
    con = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password'
            )
    cursor = con.cursor()
    add_route(cursor,route_link_map)
    add_bus_info(cursor,bus_info)
    con.commit()

    
    
    
