"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request, response
import json

robot_memory = {"dog_name":""}

@route('/', method='GET')
def index():
    response.set_cookie("dog_name", "")
    return template("chatbot.html")

def dogLoverAnswer(msg):
    if msg.lower() == 'yes':
        return {"animation":"dog", "msg": "I lov your positive vibes!! Great for " + robot_memory["dog_name"]}
    if msg.lower() == 'no':
        return {"animation":"takeoff", "msg": "Don't be so negative!!!"}
    return None

def checkBreed(user_message):
    largeDogs = ["golden", "mutt","border","lab", "labrador", "shepard", "akita"]
    smallDogs = [ "poodle", "shitsu"]
    for word in user_message.split(" "):
        if word.lower() in largeDogs:
            return {"animation": "excited", "msg": "Omg! I love big dogs."}
        elif word.lower() == "pug":
            return {"animation": "giggling", "msg": "Pugs are so funny!"}
        elif word.lower() in smallDogs:
            return {"animation": "heartbroke", "msg": "I don't really like small dogs"}
    return None

def checkDogName(user_message):
    for word in user_message.split(" "):
        if word.lower() == robot_memory["dog_name"]:
             return {"animation": "inlove", "msg":"I would love to meet "+ robot_memory["dog_name"]}
    return None

@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    robot_memory["dog_name"] = request.get_cookie("dog_name")
    result = None
    if not robot_memory["dog_name"]:
        response.set_cookie("dog_name",user_message)
        robot_memory["dog_name"] = user_message
        result = {"animation": "excited", "msg": robot_memory["dog_name"]+ " is a great name!!! "}
    if not result:
        result = dogLoverAnswer(user_message)
    if not result:
        result = checkBreed(user_message)
    if not result:
        result = checkDogName(user_message)
    if not result:
        result = {"animation": "heartbroken", "msg": "Sorry! I don't understand. Please ask something else."}
    return json.dumps(result)




@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
