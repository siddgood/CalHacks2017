# /usr/bin/env python
# Download the twilio-python library from twilio.com/docs/libraries/python
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from helpers import *

app = Flask(__name__)
callers = {}

@app.route("/", methods=['GET', 'POST'])
def sms():
    """Respond and greet the caller by name."""
    # Try adding your own number to this list!
    from_number = request.values.get('From', None)

    if from_number in callers and callers[from_number]['name_set'] == 0:
        callers[from_number]['name'] = request.values.get('Body', None)
        message = "\nEnter your age, height, weight, and gender separated by spaces."
        resp = MessagingResponse()
        resp.message(message)
        callers[from_number]['name_set'] = 1
        return str(resp)

    if from_number in callers and callers[from_number]['setup'] == 0:
        age, height, weight, gender = request.values.get('Body', None).split(" ")
        callers[from_number]['stats']['age'] = float(age)
        callers[from_number]['stats']['height'] = float(height)
        callers[from_number]['stats']['weight'] = float(weight)
        callers[from_number]['stats']['gender'] = gender

        if gender == "Male" or gender == "male":
            callers[from_number]['stats']['bmr'] = (66 + (6.23 * float(weight)) + (12.7 * float(height)) - (6.76 * float(age)))
        else:
            callers[from_number]['stats']['bmr'] = (655 + (4.35 * float(weight)) + (4.7 * float(height)) - (4.7 * float(age)))

        message = "\nUSAGE:\nTo find out how many calories a food is, enter <food>?.\nTo log a meal, enter <food>"
        resp = MessagingResponse()
        resp.message(message)
        callers[from_number]['setup'] = 1
        return str(resp)

    if from_number in callers:
        body = request.values.get('Body', None)

        if "left" in body or "can I" in body or "can i" in body or "how many more" in body:
            message = "You have " + str(callers[from_number]['stats']['bmr']) + " left."
            resp = MessagingResponse()
            resp.message(message)
            return str(resp)

        if "how many calories have I eaten" in body or "how many" in body or "have I" in body or "have i" in body or "so far" in body:
            if callers[from_number]['stats']['gender'] == "Male" or callers[from_number]['stats']['gender'] == "male":
                bmr = (66 + (6.23 * float(callers[from_number]['stats']['weight'])) + (12.7 * float(callers[from_number]['stats']['height'])) - (6.76 * float(callers[from_number]['stats']['age'])))
            else:
                bmr = (655 + (4.35 * float(callers[from_number]['stats']['weight'])) + (4.7 * float(callers[from_number]['stats']['height'])) - (4.7 * float(callers[from_number]['stats']['age'])))

            message = "You have eaten " + str(bmr - callers[from_number]['stats']['bmr']) + " calories today."
            resp = MessagingResponse()
            resp.message(message)
            return str(resp)

        food = get_calories(body.strip("?"))
        if body[-1:] == "?":
            message = "\n" + food["name"].replace("+", " ") + ":\nTotal Calories: " + str(food['total']) + "\nFat (g): " + str(food['fat'])+ "\nCarbs (g): " + str(food['carbs'])+ "\nProtein (g): " + str(food['protein'])
        else:
            callers[from_number]['stats']['bmr'] -= food['total']
            message = "\n" + food["name"].replace("+", " ") + ":\nTotal Calories: " + str(food['total']) + "\nCals Left (g): " + str(callers[from_number]['stats']['bmr'])
    else:
        message = ("\nHi! I'm FoodBot! What's your name?")
        callers.update({
            from_number: {
                'name': "",
                'stats': {
                    'age': 0.0,
                    'height': 0.0,
                    'weight': 0.0,
                    'gender': "",
                    "bmr": 0.0
                    },
                'name_set': 0,
                'setup': 0
            }
        })
        print(callers)

    resp = MessagingResponse()
    resp.message(message)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
