from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


def get_driver():
    """初始化無頭模式的 WebDriver"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 啟用無頭模式
    chrome_options.add_argument("--disable-gpu")  # 避免某些系統上的圖形問題
    chrome_options.add_argument("--disable-dev-shm-usage")  # 避免資源問題
    driver = webdriver.Chrome(options=chrome_options)
    return driver


## 爬蟲幣種資訊
def get_crypto_data(crypto):
    print(f"[INFO] Fetching data for cryptocurrency: {crypto}")
    url = f"https://tw.tradingview.com/markets/cryptocurrencies/prices-all/"
    driver = get_driver()  # 使用無頭模式的 WebDriver
    driver.get(url)
    time.sleep(3)

    data = {}
    try:
        print("[INFO] 獲取表格資料中...")
        rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

        for row in rows:
            cells = row.find_elements(By.CSS_SELECTOR, "td")
            if len(cells) > 0 and crypto.upper() in cells[0].text:
                name = cells[0].text
                price = cells[2].text
                change = cells[3].text
                volume = cells[4].text
                market_cap = cells[5].text
                print(
                    f"幣種: {crypto}, 價格: {price}, 漲跌: {change}, 成交量: {volume}, 市值: {market_cap}"
                )
                data = {
                    "name": crypto,
                    "price": price,
                    "change": change,
                    "volume": volume,
                    "market_cap": market_cap,
                }
                break
        print(f"[INFO] Successfully fetched data: {data}")
    except Exception as e:
        print(f"[ERROR] Error occurred while fetching data for {crypto}: {e}")
    finally:
        driver.quit()
    return data


## 爬蟲新聞
def get_news(crypto):
    print(f"[INFO] Fetching news for cryptocurrency: {crypto}")
    url = "https://www.binance.com/zh-TC/square/news/all"
    driver = get_driver()  # 使用無頭模式的 WebDriver
    driver.get(url)

    news_list = []
    try:
        print("[INFO] 定位分類按鈕...")
        categories_div = driver.find_element(
            By.CSS_SELECTOR, "div.flex.flex-wrap.gap-2"
        )
        category_buttons = categories_div.find_elements(By.TAG_NAME, "a")

        for button in category_buttons:
            if crypto in button.text:
                print(f"[INFO] 點擊分類按鈕: {button.text}")
                ActionChains(driver).move_to_element(button).click(button).perform()
                time.sleep(3)
                break

        print("[INFO] 提取新聞資料...")
        container = driver.find_element(By.CLASS_NAME, "css-mycpt4")
        news_items = container.find_elements(By.CLASS_NAME, "css-vurnku")
        print(f"找到 {len(news_items)} 篇新聞。")

        for index, item in enumerate(news_items):
            try:
                time_element = item.find_element(By.CLASS_NAME, "css-vyak18")
                time_info = time_element.text
                title_element = item.find_element(By.CLASS_NAME, "css-yxpvu")
                title = title_element.text
                link = title_element.find_element(By.XPATH, "..").get_attribute("href")
                news_list.append({"title": title, "link": link, "time": time_info})
            except Exception as e:
                pass

        print(f"[INFO] 爬取到 {len(news_list)} 則新聞")
    except Exception as e:
        pass
    finally:
        driver.quit()

    return news_list
