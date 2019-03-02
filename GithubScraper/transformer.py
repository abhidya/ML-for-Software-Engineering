import os
import re
from glob import glob
from tqdm import tqdm
import javalang
import pandas as pd


def get_source_code(commitId, project):
    import random
    import requests
    from robobrowser import RoboBrowser

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
    url = "https://github.com/" + project.replace("-", "/") + "/commit/" + commitId

    browser.open(url + "?diff=unified")
    results = browser.find_all("a")
    for item in results:
        if ".java" in str(item):
            second_url = "https://raw.githubusercontent.com/" + project.replace("-",
                                                                                "/") + "/" + commitId + "/" + item.string
            browser.open(second_url)
            return browser.find().text


def removeComments(string):
    string = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "",
                    string)  # remove all occurance streamed comments (/*COMMENT */) from string
    string = re.sub(re.compile("//.*?\n"), "",
                    string)  # remove all occurance singleline comments (//COMMENT\n ) from string
    return string


temp_subfiles = []

pattern = "*.java"

for dir, _, _ in os.walk("/home/manny/PycharmProjects/GithubScraper/java_code_files"):
    temp_subfiles.extend(glob(os.path.join(dir, pattern)))

# print(temp_subfiles)

if (False):
    for file in tqdm(temp_subfiles):
        with open(file, 'r') as myfile:
            data = myfile.read()  # .replace('\n', '')
            # data = removeComments(data)
            tree = javalang.parse.parse(data)
            # for codeblock in tree.children:
            #     print(codeblock)
            #     print("===============")
            #     for proto in codeblock:
            #         print(proto)
            #
            #         print("*************")
            #
            # tokens = list(javalang.tokenizer.tokenize(data))
            # for token in tokens:
            #     # print(token.value)
            #     # print(token.position)
            #     print(type(token))
import os
import re
from glob import glob
from tqdm import tqdm
import javalang
import pandas as pd


def get_source_code(commitId, project):
    import random
    import requests
    from robobrowser import RoboBrowser

    HEADERS_LIST = [
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13',
        'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
        'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
        'Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre'
    ]

    link = []
    codes = []

    while (len(codes) < 1):
        session = requests.Session()
        browser = RoboBrowser(session=session, user_agent=random.choice(HEADERS_LIST), parser="lxml")
        url = "https://github.com/" + project.replace("-", "/") + "/commit/" + commitId

        browser.open(url + "?diff=unified")

        results = browser.find_all("a")
        for item in results:
            if ".java" in str(item):
                try:
                    #             print(item.string)
                    second_url = "https://raw.githubusercontent.com/" + project.replace("-",
                                                                                        "/") + "/" + commitId + "/" + item.string
                    browser.open(second_url)
                    codes.append(browser.find().text)
                except:
                    pass

    return codes



def removeComments(string):
    string = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "",
                    string)  # remove all occurance streamed comments (/*COMMENT */) from string
    string = re.sub(re.compile("//.*?\n"), "",
                    string)  # remove all occurance singleline comments (//COMMENT\n ) from string
    return string


code = {"JavaSyntaxError": [], "code_col": [], "code_line": [], "code": [], "astcode": [], 'database_source': []}


temp_subfiles = []

pattern = "*.java"

for dir, _, _ in os.walk("/home/manny/PycharmProjects/GithubScraper/java_code_files"):
    temp_subfiles.extend(glob(os.path.join(dir, pattern)))

# print(temp_subfiles)

if (True):
    for file in tqdm(temp_subfiles):
        with open(file, 'r') as myfile:
            data = myfile.read()  # .replace('\n', '')
            # data = removeComments(data)
            try:
                tree = javalang.parse.parse(data)
                for codeblock in tree.children:
                    try:
                        code['code'].append(codeblock._position._source)
                    except AttributeError:
                        code['code'].append(None)
                    try:
                        code['code_line'].append(codeblock._position.line)
                    except AttributeError:
                        code['code_line'].append(None)
                    try:
                        code['code_col'].append(codeblock._position.column)
                    except AttributeError:
                        code['code_col'].append(None)

                    code['astcode'].append(codeblock)
                    code['database_source'].append("githubrepos")
                    code['JavaSyntaxError'].append(False)

            except (javalang.parser.JavaSyntaxError, KeyError):
                code['code'].append(source_code)
                code['astcode'].append(None)
                code['code_line'].append(None)
                code['code_col'].append(None)
                code['JavaSyntaxError'].append(True)
                code['database_source'].append("Promise")
                pass


def dict_append(code, key, value):
    if value == None:
        code[key].append("nan")
    else:
        code[key].append("value")
        return
