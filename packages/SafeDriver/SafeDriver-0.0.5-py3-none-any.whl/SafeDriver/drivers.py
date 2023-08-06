import requests
from bs4 import BeautifulSoup
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from functools import reduce
import zipfile
import os
import shutil


__driver_index = 'https://chromedriver.chromium.org/downloads'
# log_path = Path(__file__).resolve().parent/'debug_info.log'
global soup
pypath = ''
option = Options()


def __get_all_driver():
    """
    获取网页中的chromedriver文字
    :return: all_driver_list 所有版本的chromedriver，列表形式返回
    """
    global soup
    res = requests.get(__driver_index)
    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup.prettify())
    all_strong = soup.findAll('strong')
    # print(all_strong)
    all_driver_list = []
    for i in all_strong:
        if 'ChromeDriver' in i.text:
            all_driver_list.append(i.text)
    # print(all_driver_list)
    return all_driver_list

# 100.0.4896.60
def __choose_driver(driver):
    """
    搜索并返回查找到的对应版本driver
    :param driver: 填入当前浏览器的版本
    :return: 一个匹配出来的对应driver版本列表
    """
    driver_list = __get_all_driver()
    # print(driver_list)
    driver = str(driver)
    driver = driver.strip()
    can_choose_driver = []
    for i in driver_list:
        if driver in i:
            can_choose_driver.append(i)
    if can_choose_driver == []:
        driver = driver.split('.')
        driver = driver[0] + '.' + driver[1] + '.' + driver[2]
        # print('切割的driver', driver)
        for j in driver_list:
            if driver in j:
                can_choose_driver.append(j)
    return can_choose_driver

# @pysnooper.snoop(output='debug_info.log', prefix="choose_driver", watch='driver')
def __updata_driver(my_version, use_os):
    """
    从网页中下载driver文件并保存在当前目录下
    :param my_version: 当前浏览器的版本
    :param use_os: 当前使用的系统
    :return:
    """
    try:
        if use_os == 'linux':
            my_os = 'chromedriver_linux64.zip'
        elif use_os == 'win':
            my_os = 'chromedriver_win32.zip'
        elif use_os == 'mac':
            my_os = 'chromedriver_mac64.zip'
        else:
            raise ValueError('输入的系统名称不正确！仅支持 win、 linux、 mac')
        find_driver = __choose_driver(my_version)
        if len(find_driver) == 0:
            raise ValueError('未找到相关driver文件')
        else:
            find_driver = find_driver[0]
        version_driver = find_driver.split(' ')[1]
        # Logger.success(f'正在进行driver{version_driver}下载，请稍后……')
        print(f'\033[1;50;32m正在进行driver{version_driver}下载，请稍后……\033[0m')
        url = f"https://chromedriver.storage.googleapis.com/{version_driver}/{my_os}"
        res = requests.get(url)
        with open(f'driver-{version_driver}.zip', 'wb') as f:
            f.write(res.content)
        # Logger.success(f'成功下载chromedriver文件，版本<{version_driver}>')
        print(f'\033[1;50;32m成功下载chromedriver文件，版本<{version_driver}>\033[0m')
    except ValueError as v:
        print(f'\033[1;50;31m{v}\033[0m')

# def check_chrome_version():
#     """
#     检查当前drvier是否能正常运行的代码
#     :return: 浏览器版本号
#     """
#     options = Options()
#     options.add_argument('--headless')
#     try:
#         dr = webdriver.Chrome(options=options)
#         dr.quit()
#         print('\033[1;50;32m浏览器版本可正常运行\033[0m')
#         return 1
#     except Exception as e:
#         print('\033[1;50;31m浏览器运行异常，尝试获取当前浏览器版本\033[0m')
#         erro_info = str(e).split('\n')[1]
#         chrome_version = erro_info.split(' ')[4]
#         # num_list = re.findall(f'\d+', erro_info)
#         # re_version = reduce(lambda x, y: x + '.' + y, num_list)
#         print(f'\033[1;50;33m当前浏览器版本：<{chrome_version}>\033[0m')
#         return chrome_version

def __unzip_file(zip_file):
    """
    解压下载的driver压缩包
    :param zip_file: 需要解压的文件
    :param upzippath: 需要保存的路径
    :return:
    """
    print('\033[1;50;32m正在解压下载的压缩文件\033[0m')
    file = zipfile.ZipFile(zip_file)
    for name in file.namelist():
        file.extract(name)
    file.close()

def __get_pypath():
    """
    获取当前python路径的代码
    :return:
    """
    global pypath
    try:
        py_path = os.popen('where python')
        py_path_list = list(py_path)[0].split('\\')[:-1]
        pypath = reduce(lambda x, y: x + '\\' + y, py_path_list)
        print(f'\033[1;50;32m当前python路径：{pypath}\033[0m')
    except:
        print('\033[1;50;31m自动获取python路径出错，请手动设置pypath(python的根目录路径)\033[0m')

def __move_file(target_path):
    """
    移动文件的函数
    :param target_path:
    :return:
    """
    try:
        file_path = Path('chromedriver.exe')
        # print(file_path)
        target_path = Path(target_path + '/' + 'chromedriver.exe')
        # print(target_path)
        file_path.replace(target_path)
        print(f'\033[1;50;32m已移动chromedriver.exe文件到{target_path}\033[0m')
    except Exception as e:
        try:
            shutil.move('chromedriver.exe', target_path)
            print(f'\033[1;50;32m已移动chromedriver.exe文件到{target_path}\033[0m')
        except:
            print(f'\033[1;50;31m未能成功移动文件到{target_path}请手动移动或者更新\033[0m')
            print(f'\033[1;50;31m{e}\033[0m')


def driver():
    try:
        dr = webdriver.Chrome(options=option)
        print('\033[1;50;32mdriver已正常启动\033[0m')
        return dr
    except Exception as e:
        if str(e).find('ChromeDriver only supports') >= 1:
            try:
                print('\033[1;50;32m浏览器chromedriver文件运行异常，尝试获取并更新chromedriver文件\033[0m')
                erro_info = str(e).split('\n')[1]
                chrome_version = erro_info.split(' ')[4]
                print(f'\033[1;50;33m当前浏览器版本：<{chrome_version}>\033[0m')
                if chrome_version:
                    if pypath == '':
                        __get_pypath()
                        __updata_driver(chrome_version, 'win')
                        __unzip_file(f'driver-{chrome_version}.zip')
                        __move_file(pypath)
                        Path(f'driver-{chrome_version}.zip').unlink()
                else:
                    raise Exception('获取chrome版本失败，代码停止运行')
                return webdriver.Chrome(options=option)
            except Exception as e:
                print('\033[1;50;31m更新chromedriver出错~\033[0m')
                print(f'\033[1;50;31m{e}\033[0m')
        else:
            print(f'\033[1;50;31m{e}\033[0m')
            print('\033[1;50;31m启用driver报错，可能是options配置出现问题、driver文件不存在、方法调用错误\033[0m')
