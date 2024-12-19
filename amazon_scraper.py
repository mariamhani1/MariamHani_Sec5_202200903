from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# Set up the WebDriver
driver = webdriver.Chrome()
driver.maximize_window()
wait = WebDriverWait(driver, 20)

try:
    # Load Amazon homepage
    driver.get("https://www.amazon.eg")
    time.sleep(5)
    print("Amazon homepage loaded")

    # Wait for search box
    search_box = wait.until(
        EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    )
    search_box.clear()
    search_box.send_keys("Macbook")
    search_box.submit()
    print("Searched for: Macbook")

    # Wait for search results with multiple selector attempts
    print("Waiting for search results...")
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".s-main-slot"))
    )
    time.sleep(3)

    selectors = [
        ".s-result-item:not(.AdHolder) .a-link-normal.a-text-normal",
        ".s-result-item:not(.AdHolder) h2 a",
        ".s-main-slot .s-result-item:not(.AdHolder) .a-link-normal",
        "[data-component-type='s-search-result'] h2 a"
    ]

    first_product = None
    for selector in selectors:
        try:
            print(f"Trying selector: {selector}")
            first_product = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
            )
            if first_product:
                break
        except:
            continue

    if not first_product:
        raise Exception("No product found with any selector")

    # Scroll and click product
    print("Product found, scrolling...")
    driver.execute_script(
        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
        first_product
    )
    time.sleep(2)
    first_product.click()

    # Extract product details
    print("Extracting details...")
    details = {
        'title': wait.until(
            EC.presence_of_element_located((By.ID, "productTitle"))
        ).text.strip()
    }

    # Get price
    try:
        price_element = wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center.aok-relative"
            ))
        )
        print("Product Price:", price_element.text)
    except NoSuchElementException:
        print("Product Price: Not available")

    # Get rating
    try:
        rating_element = wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                "#acrPopover .a-icon-alt, #averageCustomerReviews .a-icon-alt"
            ))
        )
        print("Product Rating:", rating_element.text)
    except NoSuchElementException:
        print("Product Rating: Not available")

    # Take screenshot
    print("Taking screenshot...")
    driver.save_screenshot("amazon_product_page_screenshot.png")
    print("Screenshot saved as 'amazon_product_page_screenshot.png'")

except TimeoutException:
    print("Timeout occurred while waiting for elements to load")
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    time.sleep(5)
    driver.quit()