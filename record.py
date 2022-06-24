import keyboard
import pickle

events = keyboard.record(until = 'l')

# Saving the objects:
with open('tanglewood_way.txt', 'wb') as file:  # Python 3: open(..., 'wb')
    pickle.dump(events, file)
