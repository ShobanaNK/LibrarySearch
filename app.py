from flask import Flask, redirect, url_for, render_template, request
from utils import query_collection

app = Flask(__name__)

conversation_bot = []
conversation_bot.append({'bot':"Enter your query or topic to search for books in library."})

# Routes to the default page
@app.route("/")
def default_func():
    return render_template("index_bookAssistant.html", name = conversation_bot)

# routes to the default page after end conversation
@app.route("/end_conv", methods = ['POST','GET'])
def end_conv():
    global conversation_bot
    conversation_bot = []
    return redirect(url_for('default_func'))

'''
Search functionality
'''
@app.route("/search", methods = ['POST'])
def assistant():
    global conversation_bot
    user_input = request.form["user_input_message"]
    
    conversation_bot.append({'user':user_input})
    result = query_collection(user_input)
    
    conversation_bot.append({'bot':"Here are some materials which matches your query. Happy Reading!"})
    conversation_bot.append({'bot':result})
    conversation_bot.append({'bot':"Please enter another search query."})
    return redirect(url_for('default_func'))

if __name__ == '__main__':
    app.run(debug=True, host= "0.0.0.0")