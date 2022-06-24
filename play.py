import keyboard
import pickle

# Getting back the objects:
with open('tanglewood_way.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
    keyboard_events = pickle.load(f)

print(keyboard_events)
keyboard.play(keyboard_events)