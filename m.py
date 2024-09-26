from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import json
from tqdm import tqdm

# 设置 WebDriver
options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
driver = webdriver.Edge(options=options)

driver.set_page_load_timeout(10)
def load_page_with_retry(url, retry_limit=1):
    for attempt in range(retry_limit + 1):
        try:
            # 尝试加载目标网页
            # print(f"正在加载页面，尝试次数: {attempt + 1}")
            driver.get(url)
            return True  # 页面加载成功
        except TimeoutException:
            print(f"页面加载超时，第 {attempt + 1} 次尝试失败。")
            if attempt < retry_limit:
                print("刷新页面再试...")
                driver.refresh()  # 刷新页面重试
            else:
                print("已达到最大重试次数，跳过该页面。")
                return False  # 达到最大重试次数，返回失败   

#負けヒロインが多すぎる！
urls='https://bangumi.tv/subject/464376/comments?page='
for i in tqdm(range(1,113)):
    url=urls+str(i)
    # 打开目标网页

    load_page_with_retry(url, retry_limit=3)
    time.sleep(2)   # 等待页面加载
    

    # 获取所有评论块
    comments = driver.find_elements(By.CSS_SELECTOR, '.text_container.text_main_even')

    # 遍历每个评论块
    for comment in comments:
        star_class=str(-1)
        try:
            
            # 提取星级
            star_element = comment.find_elements(By.CSS_SELECTOR, '.starlight')
            for star_element in star_element:
                star_class = star_element.get_attribute('class')
            
            # 提取星级中的数字
            star_number = int(star_class.replace('starlight stars', ''))
            
            # 提取评论内容
            comment_text = comment.find_element(By.CSS_SELECTOR, 'p.comment').text
            
            # 根据星级分类保存评论
            if star_number == 6:
                with open('M1.txt', 'a', encoding='utf-8') as file:
                    file.write(comment_text + '\n\n')
            elif star_number > 6:
                with open('M2.txt', 'a', encoding='utf-8') as file:
                    file.write(comment_text + '\n\n')
            elif star_number <6 and star_number >0:
                with open('M0.txt', 'a', encoding='utf-8') as file:
                    file.write(comment_text + '\n\n')
            else :
                with open('M_no.txt', 'a', encoding='utf-8') as file:
                    file.write(comment_text + '\n\n')
                
                    
        except Exception as e:
            print(f"Error processing comment: {e}")

    # 关闭浏览器
driver.quit()


