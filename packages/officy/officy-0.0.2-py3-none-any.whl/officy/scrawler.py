class Scrawler:
    """基于 selenium 的爬虫，启动 chrome 浏览器，分为可见、无端两种模式"""

    def __init__(self, mode="light"):
        """
        1) 参数 mode，默认值为 light，任何其它取值均视为 dark。
        light 模式会打开 chrome 浏览器，并肉眼可见各种操作；
        dark 模式是无端模式，没有浏览器显示。
        2) chromedriver 的版本应与 chrome 一致；通常在此下载更新
        http://npm.taobao.org/mirrors/chromedriver/
        """

        if mode != "light":
            self.driver = self.start_driver_dark()
        else:
            self.driver = self.start_driver_light()

    def start_driver_dark(self):
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def start_driver_light(self):
        # "某些情况下，需要打开 chrome 浏览器使之全屏；否则某些处理可能失败"
        # 需要手动指定 chromedriver 的地址；
        # chromedriver = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver'
        # driver = webdriver.Chrome(chromedriver)
        # 如果设置好环境变量，就不需要指定了
        from selenium import webdriver

        driver = webdriver.Chrome()
        return driver

    def visit_url(self, driver, url):
        """示例代码：打开某个网页"""
        driver.get(url)

    def do_elements(self, driver):
        """示例代码：找到某个或某些元素，对元素作出某些操作"""
        # 多个元素是 find_elements_by_xpath
        ele = driver.find_element_by_xpath("//textarea[@maxlength='5000']")
        ele.clear()  # 清空
        ele.click()  # 点击
        ele.send_keys("随便写点啥")  # 发送值

        text = "随便写点啥"
        js = f"Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set.call(arguments[0], '{text}');arguments[0].dispatchEvent(new Event('input', {{ bubbles: true}}));"
        driver.execute_script(js, ele)  # 执行代码
