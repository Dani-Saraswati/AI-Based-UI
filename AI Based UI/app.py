import subprocess
import speech_recognition as sr
from flask import Flask, render_template, redirect, url_for, request
import json
import webbrowser
app = Flask(__name__)
r = sr.Recognizer()
def listen_for_commands():
    r = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        r.adjust_for_ambient_noise(source)

    print("Listening for commands...")

    while True:
        with mic as source:
            audio = r.listen(source)
        try:
            command = r.recognize_google(audio)
            print("Command:", command)
            if "mouse" in command.lower():
                ai_mouse()
            elif "keyboard" in command.lower():
                ai_keyboard()
            elif "character" in command.lower():
                ai_char_ui()
            elif "voice" in command.lower():
                voice_ui()
            else:
                print("Unknown command:", command)
        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Speech Recognition service:", e)

def get_hyperlinks(letter):
    try:
        with open("reference.json", "r") as f:
            data = json.load(f)
            if letter in data:
                return data[letter]
            else:
                return None
    except Exception as e:
        print("An error occurred while getting the hyperlink:", e)
        return None
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/ai_mouse')
def ai_mouse():
    subprocess.run(['python', 'vrmouse.py'])
    return "AI Mouse Script"

@app.route('/ai_keyboard')
def ai_keyboard():
    subprocess.run(['python', 'vrkeyboard.py'])
    return "AI Keyboard Script"

@app.route('/ai_char_ui')
def ai_char_ui():
    subprocess.run(['python', 'testing.py'])
    return "AI Character-Based UI Script"

@app.route('/modify')
def modify():
    return render_template('modify.html')


@app.route('/update_hyperlink', methods=['GET', 'POST'])
def update_hyperlink():
    if request.method == 'POST':
        letter = request.form['letter']
        hyperlink = request.form['hyperlink']
        try:
            with open("reference.json", "r") as f:
                data = json.load(f)
                if letter in data:
                    data[letter] = hyperlink
                    with open("reference.json", "w") as f:
                        json.dump(data, f)
                    return "Hyperlink updated successfully."
                else:
                    return "Letter not found."
        except Exception as e:
            return "An error occurred while updating the hyperlink: {}".format(e)
    else:
        return render_template('update_hyperlink.html')

@app.route('/get_hyperlink', methods=['GET', 'POST'])
def get_hyperlink():
    if request.method == 'POST':
        letter = request.form['letter']
        hyperlink = get_hyperlinks(letter)
        if hyperlink:
            return render_template('get_hyperlink.html', hyperlink=hyperlink)
        else:
            return render_template('get_hyperlink.html', error="Letter not found")
    else:
        return render_template('get_hyperlink.html')

@app.route('/voice_ui')
def voice_ui():
    subprocess.run(['python', 'voice recognition.py'])
    return "Voice-Based UI Script"
@app.route('/voice_control')
def voice_control():
    listen_for_commands()

if __name__ == '__main__':
    app.run(debug=True)
