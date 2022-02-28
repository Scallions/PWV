from asyncio import tasks
from pydoc import cli
import requests
from loguru import logger
import asyncio
import random
import httpx
import re
import sys
import os
sys.path.append(".")
# print(os.getcwd())
# print(sys.path)
# print(__name__)
# print(__file__)

from data.filter_sites import greenland_sites

urls = ["http://geodesy.unr.edu/gps_timeseries/trop/QAQ1/QAQ1.2022.trop.zip"]


global_sem = None # 全局并发限制器

def test():
    for url in urls:
        file_name = url.split("/")[-1]
        logger.info(f"Downloading: {file_name}")
        rep = requests.get(url)
        if rep.status_code != 200:
            logger.warning(f"Download failed: {file_name}")
        else:
            with open(f"dataset/{file_name}", "wb") as f:
                f.write(rep.content)

async def get_download_urls(site):
    """获取该站点需要下载的数据url列表，使用正则匹配下载页面的链接

    Args:
        site (str)): 站点名

    Returns:
        [str]: 需要下载的url列表
    """
    ftp_root = f"http://geodesy.unr.edu/gps_timeseries/trop/{site}/"
    async with global_sem:
        async with httpx.AsyncClient() as client:
            r = await client.get(ftp_root)
    cnt = r.text
    reg = re.findall(r">(\w{4}\.\d{4}\.trop\.zip)</a>", cnt)
    reg = [f"http://geodesy.unr.edu/gps_timeseries/trop/{site}/{r}" for r in reg]
    return reg

async def download_url(url):
    """下载url的数据，如果文件存在直接跳过

    Args:
        url (str): 需要下载的url
    """
    # logger.info(f"Download: {url}")
    file_name = url.split("/")[-1]
    if os.path.exists(f"dataset/{file_name}"):
        return
    async with httpx.AsyncClient() as client:
        try:
            rep = await client.get(url)
        except:
            logger.warning(f"Get error: {url}")
            return
    if rep.status_code != 200:
        logger.warning(f"Download failed: {file_name}")
    else:
        with open(f"dataset/{file_name}", "wb") as f:
            f.write(rep.content)

async def download_one_site(site):
    """下载一个站点的所有数据，使用并发限制一定程度防止被封

    Args:
        site (str): 站点名
    """
    url_list = await get_download_urls(site)
    async with global_sem:
        tasks = [download_url(url) for url in url_list]
        await asyncio.wait(tasks)


async def main():
    global global_sem
    global_sem = asyncio.Semaphore(20)
    grl_sites = greenland_sites()
    tasks = []
    for site in grl_sites.itertuples():
        tasks.append(download_one_site(site.Sta))
        # tasks.append(asyncio.create_task(down_one_site(site.Sta)))
        # break


    # await asyncio.gather(*tasks)
    # for task in tasks:
    #     await task
    await asyncio.wait(tasks)


asyncio.run(main())