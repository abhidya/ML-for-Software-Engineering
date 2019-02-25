SOscraper.py scrapes StackOverflow's main page for all Java related questions. It gathers the code from the questions/answers and labels them as either 'buggy' or 'good.'
We make the assumption that the code in the questions with only one block of code is likely buggy and the code in the answers with only one block of code is likely good code.
