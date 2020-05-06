import os
import saybot as sb

tob = sb.Saybot()

def sam():
    user = input()
    print (tob.response(user, 'bot_brain.h5','intents.json'))
    sam()

def start():
    if os.path.exists("bot_brain.h5"):
        sam()
    else:
    	print(sb.trains('intents.json','bot_brain.h5'))
    	start()

if __name__ == "__main__":
    start()
