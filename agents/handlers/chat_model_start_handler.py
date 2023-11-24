from langchain.callbacks.base import BaseCallbackHandler
from pyboxen import boxen

# boxen return a string that we need to print, so lets make a func to print all str
def boxen_print(*args, **kwargs):
    print(boxen(*args, **kwargs))


# test the print
boxen_print("Text here", title="human", color="red")

class ChatModelStartHandler(BaseCallbackHandler):
    def on_chat_model_start(self, serialized, messages, **kwargs): # kwargs for key-words-args
        print(messages)
