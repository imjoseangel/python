import speech_recognition as sr
import pandas

from os import system

colnames = ['order', 'command']
data = pandas.read_csv('commands.csv', names=colnames, header=0)

orders = data.order.tolist()

cmddict = dict(zip(data.order, data.command))

recognizer = sr.Recognizer()

sr.Microphone.list_microphone_names()
mic = sr.Microphone(device_index=0)

system('say What do you want?')

with mic as source:
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

speechout = recognizer.recognize_google(audio).capitalize()

# speechout = recognizer.recognize_google(audio, language='es-ES').capitalize()

if speechout in orders:
    eval(cmddict.get(speechout))
else:
    print("I don't recognize the command")
    print("You said %s" % speechout)
