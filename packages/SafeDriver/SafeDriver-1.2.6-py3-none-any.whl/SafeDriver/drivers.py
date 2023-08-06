"""
SafeDriver稳定性driver程序：
Author：测码范晔
LICENSE_Type：MIT
SafeDriver出生本身意义在于维持chromedriver程序的稳定性，自动化进行driver的检查和更新driver文件，提高web自动化代码稳定性
作用：
使用程序的driver()，可自动判断driver的正确性，正常情况将直接返回selenium的webdriver.Chrome()，出现异常情况，程序将自动下载并替换原来的webdriver
并重新返回正确的webdriver，保证代码可运行状态
资源来源：
https://chromedriver.chromium.org/downloads
可修改配置：
option: 浏览器的配置项，使用方式同webdriver.ChromeOptions，仅是其实例
    option还包含两个可配置项os_,pypath
    option.os_=xxx 标识xxx为当前使用的系统，可填写参数“win”，“linux”，“mac”，"mac_m1"当不填入视为自动获取
    option.pypath=xxx 标识xxx为当前python根目录，必须是一个系统绝对路径，链接python根目录
导入使用：
使用driver：
frome SafeDriver.drivers import driver
driver = driver()
driver.get("https://xxxxx")
...
使用全局配置
from SafeDriver.drivers import option
from SafeDriver.drivers import driver
option.os_ = 'win'
option.pypath = 'C://Python/python38'
option.add_argument('--headless')
driver = driver()
driver.get('https://xxxx')
"""
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from functools import reduce
import zipfile
import os
import shutil
import platform
import re
import glob


__driver_index = 'https://chromedriver.chromium.org/downloads'
__filepath = Path(__file__).resolve().parent
__fspath = os.fspath(__filepath) + '/'


class __Option(Options):
    os_ = ''
    pypath = ''

option = __Option()

def __get_all_driver():
    """
    获取网页中的chromedriver文字
    :return: all_driver_list 所有版本的chromedriver，列表形式返回
    """
    # global __soup
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
        elif use_os == 'mac_m1':
            my_os = 'chromedriver_mac64_m1.zip'
        else:
            raise ValueError('输入的系统名称不正确！仅支持 win、 linux、 mac, mac_m1')
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
        with open(f'{__fspath}driver-{version_driver}.zip', 'wb') as f:
            f.write(res.content)
        # Logger.success(f'成功下载chromedriver文件，版本<{version_driver}>')
        print(f'\033[1;50;32m成功下载chromedriver文件，版本<{version_driver}>\033[0m')
        return version_driver
    except ValueError as v:
        print(f'\033[1;50;31m{v}\033[0m')

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

def __get_pypath(os_):
    """
    获取当前python路径的代码
    :return:
    """
    # global pypath
    global option
    try:
        if os_ == 'win':
            split_ = '\\'
            cmd = 'where python'
        else:
            split_ = '/'
            cmd = 'which python'
        path_ = list(os.popen(f'{cmd}'))[0]
        # py_path_list = list(py_path)[0].split('\\')[:-1]
        path_ = re.sub('\n\t\r\000', '', path_).strip()
        if path_.endswith('exe'):
            path_ = path_.split(f'{split_}')[:-1]
            path_ = reduce(lambda x, y: x + f'{split_}' + y, path_)
            option.pypath = path_
        else:
            option.pypath = path_
        print(f'\033[1;50;32m当前python路径：{option.pypath}\033[0m')
    except:
        print('\033[1;50;31m自动获取python路径出错，请手动设置pypath(python的根目录路径)\033[0m')

def __move_file(target_path):
    """
    移动文件的函数
    :param target_path:
    :return:
    """
    try:
        file_path = Path(__fspath + 'chromedriver.exe')
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

def __get_system():
    """
    识别当前系统代码
    :return:
    """
    # global os_
    global option
    plat = platform.system().lower()
    if 'win' in plat:
        option.os_ = 'win'
    elif 'linux' in plat:
        option.os_ = 'linux'
    else:
        option.os_ = 'mac'

def __deleta_files():
    """
    删除当前目录所有遗留文件
    :return:
    """
    exes = glob.glob(__fspath + '*.exe')
    zips = glob.glob(__fspath + "*.zip")
    files = exes + zips
    for exe in files:
        Path(exe).unlink(missing_ok=True)



def driver(*args, **kwargs):
    try:
        dr = webdriver.Chrome(*args, **kwargs, options=option)
        print('='*36)
        print(f'\033[1;50;32m{"*"*10} driver已正常启动 {"*"*10}\033[0m')
        print('='*36)
        return dr
    except Exception as e:
        if str(e).find('ChromeDriver only supports') >= 1:
            try:
                print('=' * 97)
                print(f'\033[1;50;31m{"*-"*10} 浏览器chromedriver文件运行异常，尝试获取并更新chromedriver文件 {"-*"*10}\033[0m')
                print('=' * 97)
                erro_info = str(e).split('\n')[1]
                chrome_version = erro_info.split(' ')[4]
                print(f'\033[1;50;33m当前浏览器版本：<{chrome_version}>\033[0m')
                if chrome_version:
                    # if pypath == '':
                    if option.os_ == '':
                        __get_system()
                    else:
                        if option.os_ not in ('win', 'linux', 'mac', 'mac_m1'):
                            raise Exception('输入的系统名称有误，参数为win、linux、mac')
                        else:
                            print(f'\033[1;50;32m当前为手动配置系统<{option.os_}>\033[0m')
                    if option.pypath == '':
                        __get_pypath(option.os_)
                    else:
                        if os.path.isdir(option.pypath):
                            print(f'\033[1;50;32m当前为手动配置的python路径：{option.pypath}\033[0m')
                        else:
                            raise Exception('当前路径不是指向的一个文件夹，或者路径不存在')
                    version = __updata_driver(chrome_version, option.os_)
                    if version:
                        __unzip_file(f'{__fspath}driver-{version}.zip')
                        __move_file(option.pypath)
                        Path(f'{__fspath}driver-{chrome_version}.zip').unlink(missing_ok=True)
                        Path(f'{__fspath}chromedriver.exe').unlink(missing_ok=True)
                    else:
                        raise Exception("未获取到driver版本名称")
                else:
                    raise Exception('获取chrome版本失败，代码停止运行')
                return webdriver.Chrome(*args, **kwargs, options=option)
            except Exception as e:
                print('\033[1;50;31m更新chromedriver出错~\033[0m')
                print(f'\033[1;50;31m{e}\033[0m')
            finally:
                __deleta_files()
        else:
            print(f'\033[1;50;31m{e}\033[0m')
            print('\033[1;50;31m启用driver报错，可能是options配置出现问题、driver文件不存在、方法调用错误\033[0m')
