from robobrowser import RoboBrowser
from tqdm import tqdm
import pandas
import sys
import os

dirname = os.path.abspath(os.path.dirname('__file__'))
dirname = dirname + '/../StackOverflowScraper/SOfiles'
stackoverflow = 'http://stackoverflow.com'
browser = RoboBrowser(parser='html.parser')
Name_Code = {} #key is name of webpage, value is Code
Code = []

def get_name(s):
    name = ""
    x = len(s)-1
    for i in reversed(s):
        if i is '/':
            break
        x -= 1
    for j in range(x+1, len(s)):
        name = name + s[j]
    return name

def get_buggy_code():
    global Code
    print("GETTING BUGGY CODE\n")
    for i in tqdm(range(1,2)):
        try:
            browser.open('https://stackoverflow.com/questions/tagged/java?sort=newest&page=' + str(i) + '&pagesize=15')
        except:
            print("Couldn't open https://stackoverflow.com/questions/tagged/java?sort=newest&page=" + str(i) + '&pagesize=15')
        questions_block = browser.find('div', id= 'questions')
        if questions_block is None:
            continue
        questions = questions_block.find_all('a', class_= 'question-hyperlink')
        if questions is None:
            continue
        for question in questions:
            question = question.get('href')
            if question is None:
                continue
            print(stackoverflow + question)
            try:
                browser.open(stackoverflow + question)
            except:
                print("Couldn't open " + (stackoverflow + question))
                continue
            Name = get_name(question)
            Name += '_Q'
            question_text = browser.find('div', class_= 'post-text')
            if question_text is None:
                continue
            code_blocks = question_text.find_all('pre')
            # if there's only one code block it is more likely to contain the bug as
            # opposed to a question with multiple blocks of code
            if len(code_blocks) is 1:
                for code_block in code_blocks:
                    code = code_block.find('code')
                    code = str(code)
                    code = code[6:]
                    code = code[:-7]
                    print(code)
                    Code.append(code)
                    Code.append("buggy")
                    Name_Code[Name] = tuple(Code)
                    Code = []
                print('\n')
            else:
                continue

def get_good_code():
    global Code
    print("GETTING GOOD CODE\n")
    for i in tqdm(range(1,2)):
        try:
            browser.open('https://stackoverflow.com/questions/tagged/java?sort=newest&page=' + str(i) + '&pagesize=15')
        except:
            print("Couldn't open https://stackoverflow.com/questions/tagged/java?sort=newest&page=" + str(i) + '&pagesize=15')
        questions_block = browser.find('div', id= 'questions')
        if questions_block is None:
            continue
        questions = questions_block.find_all('a', class_= 'question-hyperlink')
        if questions is None:
            continue
        for question in questions:
            question = question.get('href')
            if question is None:
                continue
            print(stackoverflow + question)
            try:
                browser.open(stackoverflow + question)
            except:
                print("Couldn't open " + (stackoverflow + question))
                continue
            Name = get_name(question)
            Name += '_A'
            answers_container = browser.find('div', id= 'answers')
            if answers_container is None:
                continue
            answers = answers_container.find_all('div', class_='answer')
            if answers is None:
                continue
            for answer in answers:
                # if there's only one code block it is more likely to good code as
                # opposed to an answer with multiple blocks of code
                answer = answer.find('div', class_='post-layout')
                answer = answer.find('div', class_='answercell post-layout--right')
                answer = answer.find('div', class_='post-text')
                code_blocks = answer.find_all('pre')
                if len(code_blocks) is 1:
                    for code_block in code_blocks:
                        code = code_block.find('code')
                        code = str(code)
                        code = code[6:]
                        code = code[:-7]
                        print(code)
                        Code.append(code)
                        Code.append("good")
                        Name_Code[Name] = tuple(Code)
                        Code = []
                    print('\n')
                else:
                    continue

def main():
    global Name_Code
    get_buggy_code()
    get_good_code()
    for key, value in Name_Code.items():
        with open(dirname + '/' + key, 'w') as f:
            f.write(key)
    return Name_Code

