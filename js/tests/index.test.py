from selenium import webdriver

# Create a new instance of the chrome driver
driver = webdriver.chrome()

# Navigate to the file location
driver.get("file:///path/to/index.html")

# Verify the title of the page
assert "Oaxaca" in driver.title

# Verify the navigation links
home_link = driver.find_element_by_xpath('//a[@href="index.html"]')
menu_link = driver.find_element_by_xpath('//a[@href="menu.html"]')
about_link = driver.find_element_by_xpath('//a[@href="about.html"]')
contact_link = driver.find_element_by_xpath('//a[@href="contact.html"]')
login_link = driver.find_element_by_xpath('//a[@href="login.html"]')

# Close the browser
driver.quit()
