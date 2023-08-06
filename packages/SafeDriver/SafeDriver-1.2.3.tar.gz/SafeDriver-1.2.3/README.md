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
# 路径和系统配置
路径和系统保存在option中，配置需要导入option
```pycon
from SafeDriver.drivers import option
option.pypath = 'xxx' # python的根目录路径
option.os_ = 'xxx'  # 当前使用的操作系统
```

# 注意事项：
1、option.os_：参数不赋值，则视为自动查找当前操作系统
2、option.pypath：参数不赋值，则视为自动查到python路径(目前自动查找操作系统仅支持windows系统，linux和mac用户请手动配置option.pypath属性) 

# 目前仅支持chrome浏览器，暂未更新其他浏览器

# 使用问题快查
## 在mac和linux上，SafeDriver不好使
SafeDriver自动查找的路径是python的路径，这个查找，在linux和mac上面并不一定能正常进行，linux和mac的用户，最好是手动配置好option.os_和option.pypath
## 如果更好保持稳定性？
建议代码中，指定driver的保存路径，此时的option.pypath则需要是你保存driver的路径
## mac用户不能移动文件
这属于mac系统的限制，某些路径需要进行授权才能访问和显示，所以可以将driver文件放在可直接访问的目录，在代码中设置好driver路径，并将这个路径赋值给option.pypath