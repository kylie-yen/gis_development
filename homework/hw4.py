import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Edge()
driver.get("https://sh.lianjia.com/ershoufang/rs吴泾/")
time.sleep(3)

# 获取6页的房屋信息
total_page = 6
# 创建一个空的DataFrame用于存储数据
data = pd.DataFrame(columns=['位置', '房屋信息', '价格信息'])
# 遍历所有页面
for page in range(1, total_page + 1):
    print(f"正在处理第 {page} 页...")
    if page != 1:
        if page==2:
            css="#content > div.leftContent > div.contentBottom.clear > div.page-box.fr > div > a:nth-child(2)"
        else:
            css="#content > div.leftContent > div.contentBottom.clear > div.page-box.fr > div > a:nth-child("+str(page+1)+")"
        next_page=driver.find_element(By.CSS_SELECTOR,value=css)
        # click()方法无法使用，会提示要点击的元素被遮盖了
        driver.execute_script('arguments[0].click()', next_page)
        time.sleep(3)  # 延迟等待页面加载

# 获取当前页面的房源信息
    houses = driver.find_elements(By.XPATH, "/html/body/div[4]/div[1]/ul/li")
    # time.sleep(2)
    for house in houses:
        location = house.find_element(By.CLASS_NAME, "positionInfo").text
        house_info = house.find_element(By.CLASS_NAME, "houseInfo").text
        price_info = house.find_element(By.CLASS_NAME, "priceInfo").text
        new_house = pd.DataFrame({'位置': [location], '房屋信息': [house_info], '价格信息': [price_info]})
        data = pd.concat([data, new_house])
        # time.sleep(3)


# 将数据保存到Excel文件
data.to_excel("闵行区吴泾镇二手房信息.xlsx", index=False)
print("数据已保存到 闵行区吴泾镇二手房信息.xlsx")
# 关闭浏览器
driver.close()
