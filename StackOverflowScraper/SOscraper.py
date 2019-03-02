from robobrowser import RoboBrowser
from tqdm import tqdm

stackoverflow = 'http://stackoverflow.com'

browser = RoboBrowser(parser='html.parser')

Code = {}

def get_buggy_code():
    for i in tqdm(range(1,3)):
        try:
            browser.open('https://stackoverflow.com/questions/tagged/java?sort=newest&page=' + str(i) + '&pagesize=15')
        except:
            print("Couldn't open https://stackoverflow.com/questions/tagged/java?sort=newest&page=" + str(i) + '&pagesize=15')
        questions_block = browser.find('div', id= 'questions')
        questions = questions_block.find_all('a', class_= 'question-hyperlink')
        for question in questions:
            question = question.get('href')
            print(stackoverflow + question)
            try:
                browser.open(stackoverflow + question)
            except:
                print("Couldn't open " + (stackoverflow + question))
            question_text = browser.find('div', class_= 'post-text')
            code_blocks = question_text.find_all('pre')
            # if there's only one code block it is more likely to contain the bug as
            # opposed to a question with multiple blocks of code
            if len(code_blocks) is 1:
                for code_block in code_blocks:
                    code = code_block.find('code')
                    code = str(code)
                    code = code[6:]
                    code = code[:-7]
                    #print(code)
                    Code[code] = "buggy"
                #print('\n')
            else:
                continue

def get_good_code():
    for i in tqdm(range(1,3)):
        try:
            browser.open('https://stackoverflow.com/questions/tagged/java?sort=newest&page=' + str(i) + '&pagesize=15')
        except:
            print("Couldn't open https://stackoverflow.com/questions/tagged/java?sort=newest&page=" + str(i) + '&pagesize=15')
        questions_block = browser.find('div', id= 'questions')
        questions = questions_block.find_all('a', class_= 'question-hyperlink')
        for question in questions:
            question = question.get('href')
            print(stackoverflow + question)
            try:
                browser.open(stackoverflow + question)
            except:
                print("Couldn't open " + (stackoverflow + question))
            answers_container = browser.find('div', id= 'answers')
            answers = answers_container.find_all('div', class_='answer')
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
                        Code[code] = "good"
                    print('\n')
                else:
                    continue

# I need help with this part. I haven't checked out the MongoDB yet.

'''
if __name__ == '__main__':
    from pymongo import MongoClient
    mongo = MongoClient()
    #db = mongo.blackbox
    #coll = db.StackOverflow

    print("GETTING BUGGY CODE\n")
    get_buggy_code()
    print("GETTING GOOD CODE\n")
    get_good_code()

    #db.StackOverflow.insert_one()
'''
