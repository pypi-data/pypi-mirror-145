# @Time    : 2022/2/22 10:37
# @Author  : kang.yang@qizhidao.com
# @File    : decorate.py
import allure
import pytest


def feature(text):
    return allure.feature(text)


def story(text):
    return allure.story(text)


# 兼容历史版本
def module(text):
    return allure.story(text)


def title(text):
    return allure.title(text)


def data(*args, **kwargs):
    return pytest.mark.parametrize(*args, **kwargs)


# 有空把文件装饰器补上
def file_data():
    pass
