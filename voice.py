import speech_recognition as sr
from cmu_graphics import *
words = open("bad-words.txt").read().splitlines()
bad_words_set = set(words)

PROFANITY_SET = {"fuck", "shit", "bad"} 

# Initialize the recognizer
r = sr.Recognizer()

def is_profane(text):
    """Check if the given text contains profanity."""
    return any(profane_word in text.lower() for profane_word in PROFANITY_SET)

def onAppStart(app):
    app.width = 800
    app.height = 800

    app.is_paused = False
    app.speaker = 1
    app.timepassed = 0
    app.text = ""
    app.spoken = ""
    
    app.prevMessages = [
        (0,'lucia'),
        (1,'chris'),
        (0,'andy'),
        (1,'jeongwon'),
        (1,'yunho'),
        (0,'seungwan'),
        (1,'ateHate'),
        (1,'ateHate'),
        (1,'ateHate'),
        (0,'ateHate'),
        (1,'ateHate'),
        (0,'ateHate'),
        (1,'ateHate'),
        (0,'ateHate')
    ]
    app.welcome = True
    app.currentMessage = ''

def redrawAll(app):
    for i in range(2):
        if i == 0:
            color = 'lightGreen'
        else:
            color = 'lightyellow'
        
        drawRect(app.width/2*i,0,app.width/2,app.height,fill = color)
        drawRect(app.width/2*i,0,app.width/2,app.height/12,fill = 'white')
        drawLabel(f'User {i}',app.width/2 * i + app.width/4, app.height/24, size = 40)
        drawRect(app.width/2*i, app.height* 11/12,app.width/2,app.height/12,fill = 'white')
        drawCircle(app.width/2 * i + app.width/24 +10,app.height/24, app.height/30, fill = 'lightpink')

        for j in range(len(app.prevMessages)):
            user, message = app.prevMessages[j]
            startY = 80
            if user != i:
                drawRect(app.width/2 * i + 10, startY + 40 * j, len(message)*15, 30,fill = 'purple')
                drawLabel(message, app.width/2 * i + 20 , startY + 40 * j + 15, size = 20, align = 'left',fill = 'white')
            else:
                drawRect(app.width/2 * i + app.width/2 - 10 - len(message)*15, startY + 40 * j, len(message)*15, 30,fill = 'blue')
                drawLabel(message, app.width/2 * i + app.width/2 - 20, startY + 40 * j + 15, size = 20, align = 'right', fill = 'white')

    drawLine(app.width/2,0,app.width/2,app.height,lineWidth = 1)
    drawLine(0,app.height/12,app.width,app.height/12,lineWidth = 1)
    drawLine(0,app.height*11/12,app.width,app.height*11/12,lineWidth = 1)

    if app.is_paused:
        drawRect(app.width / 2, app.height / 2, 600, 600, fill='red', align='center')
        drawLabel("profanity detected!", app.width / 2, app.height / 2)
        drawLabel("please press space to continue.", app.width / 2, app.height / 2)

def onMousePress(app, mouseX, mouseY):
    if not app.is_paused and mouseY > 733:
        if mouseX < 400:
            app.speaker = 1
        elif mouseX > 400:
            app.speaker = 2
        listen_and_recognize(app)

def onKeyPress(app, key):
    if key == 'space' and app.is_paused:
        app.timepassed = -50
        app.speaker = 1
        app.is_paused = False
        app.text = ""
        app.spoken = ""

def listen_and_recognize(app):
    with sr.Microphone() as source:
        print(f"{app.speaker}, please say something...")
        audio = r.listen(source)
        try:
            app.text = r.recognize_google(audio)
            app.prevMessages.append((app.speaker - 1, app.text))
            if len(app.prevMessages) > 16:
                app.prevMessages = app.prevMessages[1:]
            print(app.text)
            if is_profane(app.text):
                app.is_paused = True
                return
            app.spoken = (f"{app.speaker} said: {app.text}")
            app.speaker = 3 - app.speaker
            return
        except sr.UnknownValueError:
            print(f"Could not understand {app.speaker}'s audio")
            return 

def main():
    runApp()

main()
