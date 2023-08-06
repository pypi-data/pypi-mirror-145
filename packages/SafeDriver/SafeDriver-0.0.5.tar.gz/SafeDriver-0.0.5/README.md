# 介绍
浏览器的更新和driver文件的版本异常，经常是影响代码稳定性的一个原因，而每次driver文件的更新也是比较繁杂的工作，此次的safe-driver意在帮助维护driver的稳定性

# 作用
safe-driver导入后，可替换selenium的webdriver，使用方式和方法同selenium的webdriver
当启动浏览器driver文件出错时，程序将自动下载并更新浏览器驱动，并重新返回driver，提高代码的稳定性

# 导入
```pycon
from SafeDriver.drivers import driver
from SafeDriver.drivers import option
```
# 使用
此操作同selenium的webdriver.Chrome()
```pycon
driver = driver()
driver.get("https://www.baidu.com")
```

# 放入options参数
首先确定导入option配置参数
使用同selenium的ChromeOptions，可直接添加，添加后，无需再次写入到driver中
```pycon
from SafeDriver.drivers import option
option.add_argument('--headless')
```

# 目前仅支持windows的chrome浏览器，暂未更新其他系统和浏览器