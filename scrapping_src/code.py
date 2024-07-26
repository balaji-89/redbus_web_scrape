import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def load_page(driver):
    """
    Loads the Redbus webpage and locates carousel elements.

    Parameters:
        driver (webdriver): The Selenium WebDriver instance.

    Returns:
        tuple: A tuple containing lists of carousel logos, the next arrow element, and carousel names.
    """

    driver.get('https://www.redbus.in/')
    time.sleep(2)

    element = driver.find_element(By.CSS_SELECTOR, "div.loaderHeading")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    next_arrow = driver.find_element(By.XPATH, '//*[@id="Carousel"]/span/span/i')
    coursal_logos = driver.find_elements(By.CSS_SELECTOR, 'img.rtcLogo')
    coursal_names = driver.find_elements(By.CSS_SELECTOR, 'div.rtcName')
    return coursal_logos, next_arrow,coursal_names


def get_route_link_map(driver, action):
        """
        Extracts route links from the carousel on the Redbus webpage.

        Parameters:
            driver (webdriver): The Selenium WebDriver instance.
            action (ActionChains): Selenium ActionChains instance for performing actions.

        Returns:
            dict: A dictionary mapping route names to their links.
        """
        coursal_logos,next_arrow,coursal_names= load_page(driver)
        next_turns = 0

        routes_link = {}

        for val in range(len(coursal_logos)):
            
            try:
                coursal_logos,next_arrow,coursal_names= load_page(driver)
                if next_turns!=0:
                    for _ in range(next_turns):
                        next_arrow.click()
                        time.sleep(2)
                    
                action.click(on_element = coursal_logos[val])
                action.perform()
                time.sleep(2)
                routes = driver.find_elements(By.CSS_SELECTOR, 'a.route')
                if len(routes) == 0:
                    raise Exception('custom error')
                
                wait = WebDriverWait(driver, 10)
                pagination_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.DC_117_paginationTable")))

                pagination_elements = pagination_container.find_elements(By.CSS_SELECTOR, "div")  

                for page in pagination_elements:
                    action.click(on_element  = page)
                    action.perform()
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.DC_117_paginationTable")))
                    routes = driver.find_elements(By.CSS_SELECTOR, 'a.route')
                    for route in routes:
                        routes_link[route.text] = route.get_attribute('href')


            except Exception as e: 
                try:
                    coursal_logos,next_arrow,coursal_names = load_page(driver)
                    for _ in range(next_turns+1):
                        next_arrow.click()
                        time.sleep(1)

                    action.click(on_element=coursal_logos[val])
                    action.perform()
                    time.sleep(2)
                    routes = driver.find_elements(By.CSS_SELECTOR, 'a.route')
                    if len(routes) != 0:
                        wait = WebDriverWait(driver, 10)
                        pagination_container = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.DC_117_paginationTable")))
                        pagination_elements = pagination_container.find_elements(By.CSS_SELECTOR, "div")
                        for page in pagination_elements:
                            action.click(on_element  = page)
                            action.perform()
                            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.DC_117_paginationTable")))
                            routes = driver.find_elements(By.CSS_SELECTOR, 'a.route')
                            for route in routes:
                                routes_link[route.text] = route.get_attribute('href')
                    next_turns +=1

                except Exception as e:
                    print(e)
                
        return routes_link

def extract_bus_info(driver,route_link_map):
    """
    Extracts bus information for each route from the Redbus webpage.

    Parameters:
        driver (webdriver): The Selenium WebDriver instance.
        route_link_map (dict): A dictionary mapping route names to their links.

    Returns:
        tuple: A tuple containing updated route links, bus information, and filtered routes.
    """
    updated_route_link = []
    final_bus = {}
    filtered_routes = []

    for primary_key, (key, val) in enumerate(route_link_map.items()):
            try:
                driver.get(val)
                time.sleep(5)
                total_bus_cnt = int(driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div[1]/div[1]/span[1]/span').text.split(' ')[0])
                gov_buses_drop_down_button = driver.find_elements(By.CSS_SELECTOR, 'div.w-16.fl.m-top-22')
                gov_buses_drop_down_button = [int(idx.text.split(' ')[0]) for idx in gov_buses_drop_down_button]
                time.sleep(2)
                bus_infos = []
                show_bus_buttons = [ele for ele in driver.find_elements(By.CSS_SELECTOR, 'div.button') if ele.text == "VIEW BUSES"]
                
                for idx in range(len(gov_buses_drop_down_button)):
                    show_bus_button = show_bus_buttons[idx]
                    show_bus_button.click()
                    time.sleep(2)
                    available_buses = gov_buses_drop_down_button[idx]
                    time.sleep(1)
                    for ele_idx in range(available_buses):
                        element = driver.find_element(By.XPATH, f'//*[@id="result-section"]/div[{idx+1}]/div[3]/ul')
                        li_list = element.find_elements(By.CSS_SELECTOR,'li.row-sec.clearfix')
                        li_element = li_list[ele_idx]
                        if li_element.get_attribute('class') !=  'rtcinlineFilterContainer' and li_element.get_attribute('ID') != None:
                            try:
                                card_info = li_element.find_element(By.CSS_SELECTOR, 'div.clearfix.row-one')
                                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", li_element)
                                time.sleep(1)
                                bus_infos.append([card_info.text])
                            except Exception as e:
                                print(e)
                                
                    if idx < len(gov_buses_drop_down_button)-1:
                            next_show_bus_button = driver.find_element(By.XPATH, f'//*[@id="result-section"]/div[{idx+1}]/div[3]/ul')
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_show_bus_button)
                            time.sleep(1)

                for pri_bus_idx in range(total_bus_cnt - sum(gov_buses_drop_down_button)):
                    element = driver.find_element(By.XPATH, f'//*[@id="result-section"]/div[{len(gov_buses_drop_down_button)+1}]/ul')
                    li_list = element.find_elements(By.CSS_SELECTOR,'li.row-sec.clearfix')
                    li_element = li_list[pri_bus_idx]
                    if li_element.get_attribute('class') !=  'rtcinlineFilterContainer' and li_element.get_attribute('ID') != None:
                        try:
                            card_info = li_element.find_element(By.CSS_SELECTOR, 'div.clearfix.row-one')
                            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", li_element)
                            time.sleep(1)
                            bus_infos.append([card_info.text])
                        except Exception as e:
                            print(e)
                updated_route_link.append([key,val])
                final_bus[key] = bus_infos

            except Exception as e:
                filtered_routes.append([key,val,e])

    return updated_route_link,final_bus,filtered_routes

def format_scrapped_code(route_link_map, bus_info):
        """
        Formats the scraped route and bus information into structured data.

        Parameters:
            route_link_map (list): A list of routes and their links.
            bus_info (dict): A dictionary of bus information for each route.

        Returns:
            tuple: A tuple containing formatted route links and formatted bus information.
        """
        #initializing primary key for route-link
        formatted_route_link = [[idx]+item for idx, item in enumerate(route_link_map,start=1)]

        formatted_bus_info = []
        for route,items in bus_info.items():
            
            #finding foreign key number
            for (primary_key, route_name, _) in formatted_route_link:
                if route_name == route:
                    foreign_key = primary_key
                    break

            for id, item in enumerate(items,start=1):
                all_info = item[0].split('\n')
                bus_name = all_info[0]
                bus_type = all_info[1]
                departure_time = all_info[2]

                reaching_time = None
                duration = None
                price = None
                available_seats = None
                rating  = None

                duration_pattern = re.compile(r'^\d{2}h \d{2}m$')
                time_format = re.compile(r'^\d{2}:\d{2}$')
                rating_format = re.compile(r'^\d\.\d')
                
                for val in all_info[3:]:
                    if 'INR' in val:
                        price = float(val.strip().split(' ')[1])

                    elif ('Seat available' in val) or ('Seats available' in val):
                        available_seats = int(val.split(' ')[0])

                    elif duration_pattern.match(val.strip()):
                        duration = val
                    
                    elif time_format.match(val.strip()):
                        reaching_time = val

                    elif rating_format.match(val.strip()):
                        rating = val

                formatted_bus_info.append([id, foreign_key, bus_name, bus_type,duration,departure_time,reaching_time,price,available_seats,rating])

        return formatted_route_link,formatted_bus_info