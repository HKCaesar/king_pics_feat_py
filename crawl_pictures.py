# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 20:19:58 2018
@author: lxcnju
����seleniumģ���½��ȡ������ҫ�����ϵ�Ӣ��ͼƬ��װ��ͼƬ
"""


from selenium import webdriver          # ģ���½
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup           # ҳ�����
import re
import time
import os
import requests

chromePath =  r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'         # �ȸ����������λ��

wd = webdriver.Chrome(executable_path = chromePath)     # ���������
wait = WebDriverWait(wd, 2)                             # �趨�ȴ�ʱ��Ϊ100��

if not os.path.exists("pics"):
    os.mkdir("pics")
if not os.path.exists("pics/small_pics"):
    os.mkdir("pics/small_pics")
if not os.path.exists("pics/equipments_pics"):
    os.mkdir("pics/equipments_pics")

# ����ͼƬ
def download_img(img_url, fpath):
    resp = requests.get(img_url)
    fw = open(fpath, 'wb')
    fw.write(resp.content)
    fw.close()
    print("Save {} to {}...".format(img_url, fpath))
    time.sleep(1)

# ��ȡӢ��ͷ��    
def crawl_herolist():
    global wd, wait
    # Ӣ��ҳ
    hero_page_url = "http://pvp.qq.com/web201605/herolist.shtml"
    wd.get(hero_page_url)
    time.sleep(5)
    
    # ��ȡÿ��Ӣ�۵�ְλ��ͼƬurl
    hero_infos = {}
    all_places = ["̹��", "սʿ", "�̿�", "��ʦ", "����", "����"]   # ����ְλ
    for i in range(2, 8):
        # �����ť
        type_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.wrapper > div > div > div.herolist-box > div.clearfix.herolist-types > ul:nth-child(3) > li:nth-child({})'.format(i)))
        )
        type_btn.click()
        # Դ��
        html = wd.page_source
        # ������ְλ�µ�����Ӣ��
        soup = BeautifulSoup(html, 'lxml')
        blocks = soup.select("body > div.wrapper > div > div > div.herolist-box > div.herolist-content > ul > li")
        for block in blocks:
            img_url = block.select("a > img")[0]["src"]
            hero_name = block.select("a")[0].text.strip()
            print(img_url, hero_name)
            try:
                hero_infos[hero_name]
            except KeyError:
                hero_infos[hero_name] = {"places" : [], "url" : ""}
            hero_infos[hero_name]["places"].append(all_places[i - 2])
            hero_infos[hero_name]["url"] = img_url
    # ��������ͼƬ
    for hero_name, hero_info in hero_infos.items():
        fname = os.path.join("pics", "small_pics", hero_name + "_" + "_".join(hero_info["places"]) + ".jpg")
        download_img(hero_info["url"], fname)
    print("Done!")

# ��ȡ����װ��  
def crawl_equipments():
    global wd, wait
    # װ��ҳ
    time.sleep(2)
    item_page_url = "http://pvp.qq.com/web201605/item.shtml"
    wd.get(item_page_url)
    time.sleep(3)
    
    # ��ȡÿ��װ�������ú�ͼƬurl
    items_infos = {}
    all_types = ["����", "����", "����", "�ƶ�", "��Ұ", "����"]   # ����װ������
    for i in range(2, 8):
        # �����ť
        type_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.wrapper > div > div > div.herolist-box > div.clearfix.herolist-types.item-types > ul > li:nth-child({})'.format(i)))
        )
        
        type_btn.click()
        # Դ��
        html = wd.page_source
        # ����������������װ��
        soup = BeautifulSoup(html, 'lxml')
        blocks = soup.select("#Jlist-details > li")
        for block in blocks:
            img_url = block.select("a > img")[0]["src"]
            item_name = block.select("a")[0].text.strip()
            if "?" in item_name:
                item_name = "".join(item_name.split("?"))
            if not img_url.startswith("http"):
                img_url = "http:" + img_url
            print(img_url, item_name)
            try:
                items_infos[item_name]
            except KeyError:
                items_infos[item_name] = {"types" : [], "url" : ""}
            items_infos[item_name]["types"].append(all_types[i - 2])
            items_infos[item_name]["url"] = img_url
    # ��������ͼƬ
    for item_name, item_info in items_infos.items():
        fname = os.path.join("pics", "equipments_pics", item_name + "_" + "_".join(item_info["types"]) + ".jpg")
        download_img(item_info["url"], fname)
    print("Done!")

crawl_herolist()
crawl_equipments()