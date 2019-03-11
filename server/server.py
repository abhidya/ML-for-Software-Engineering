#!/usr/bin/env python
import javalang
from flask import Flask, render_template, request, jsonify

try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle

async_mode = None

app = Flask(__name__)
x = None

with open('model.pkl', 'rb') as input:
    x = pickle.load(input)



@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/compute_bugs', methods=['POST'])
def upload_entry():
    data = request.data.decode("utf-8")
    message = []
    code ={}
    try:
        tree = javalang.parse.parse(data)
        j = 0
        for codeblock in tree.children:
            if codeblock != None and codeblock != []:
                j = j +1
                print(codeblock)
                result = x.predict_text_main(data)
                if result == "c":
                    bug = "Semantic Bug"
                elif result == "p":
                    bug = "Perfective Refactor Possible"
                elif result == "a":
                    bug = "Adaptive Refactor Possible"
                else:
                    bug = result
                try:
                    line =   bug + "CodeBlock at Line " + str(codeblock._position.line) + " Column " + str(codeblock._position.column) + " \n"
                    if bug == "Correct":
                        line = bug + " CodeBlock OK at Line " + str(codeblock._position.line) + " Column " + str(codeblock._position.column) + " \n"

                    #   line =  "Bug in CodeBlock at Line UNKNOWN  Column UNKOWN \n"
                    message.append(line)
                except (AttributeError):
                    line = bug + " bug in CodeBlock " + str(j)
                    if bug == "Correct":
                        line = "CodeBlock " + str(j) + " OK"
                    message.append(line)

                    pass

    except (javalang.parser.JavaSyntaxError, KeyError, javalang.tokenizer.LexerError) as e:

        try:
            message.append(str(e.__class__.__name__) + " "+ str(e.description) + " " + str(e.at
                                                                                ))
        except (TypeError, AttributeError):
            try:
                message.append(str(e.__class__.__name__))
            except (TypeError):
                pass
            pass
    message = list(set(message))
    code['msg'] = message
    return jsonify(code), 200


if __name__ == '__main__':
    app.run(debug=True)
