import json  # or `import simplejson as json` if on Python < 2.6
import os
import random
import time
import shutil
import requests
from robobrowser import RoboBrowser
import os
from glob import glob

HEADERS_LIST = [
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13',
    'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre'
]

link = []

session = requests.Session()
browser = RoboBrowser(session=session, user_agent=random.choice(HEADERS_LIST), parser="lxml")
page = 6
url = "https://github.com/search?l=Java&o=desc&p=" + str(page) + "&q=java&s=stars&type=Repositories"
browser.open(url)
results = browser.find_all("a", class_="v-align-middle")
temp_dir = "/home/manny/PycharmProjects/GithubScraper/temp"
javacode_dir = '/home/manny/PycharmProjects/GithubScraper/java_code_files'

while len(link) < 100:
    browser.open(url)
    results = browser.find_all("a", {"class": "v-align-middle"})
    while len(results) == 0:
        time.sleep(5)
    url = "https://github.com/search?l=Java&o=desc&p=" + str(page) + "&q=java&s=stars&type=Repositories"
    for item in results:
        jsonobj = item.get('data-hydro-click')
        obj = json.loads(jsonobj)
        obj = obj['payload']['result']['url']
        print(obj)
        try:
            os.makedirs(javacode_dir + "/" + obj.rsplit('/', 1)[-1])
        except:
            pass
        clone = "git clone " + obj + ".git"

        os.chdir(temp_dir)  # Specifying the path where the cloned project needs to be copied
        os.system(clone)  # Cloning
        temp_subfiles = []

        pattern = "*.java"

        for dir, _, _ in os.walk(temp_dir):
            temp_subfiles.extend(glob(os.path.join(dir, pattern)))

        for file in temp_subfiles:
            filename, file_extension = os.path.splitext(file)
            if file_extension == ".java":
                # print(file)
                try:
                    shutil.move(file, javacode_dir + "/" + obj.rsplit('/', 1)[-1])
                except:
                    pass
        for the_file in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
        # print(e)
                pass

    link.append(obj)
    page = page + 1

# print(link)
