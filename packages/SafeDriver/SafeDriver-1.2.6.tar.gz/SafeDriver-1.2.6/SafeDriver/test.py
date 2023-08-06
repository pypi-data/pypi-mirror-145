from drivers import driver, option


option.os_ = 'win'
dr = driver()
dr.get('https://www.baidu.com')
print(dr.title)
dr.quit()
