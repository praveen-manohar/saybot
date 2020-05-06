#Saybot is an NLTK and TFLearn bot machine. You can train it with 'intents.json' file

######To run the code:
    **Open your Terminal, and**
      >  run.py
    
You can change your file names, you can decide what you want. bot_brain -> master_brain, something likethat. it make you feel its your code. You're not restricted with what i have created. Its just an template. You can make it more functionable

**To Change the filenames,**
   > Open run.py file there you can see the files.

**To run on Terminal**
``` python
import os
import saybot as sb

tob = sb.Saybot()

def sam():
   user = input()
   print(tob.response(user,'bot_brain.h5','intents.json'))
   sam()
def start():
   if os.path.exists("bot_brain.h5"):
      sam()
   else:
      print(sb.trains('intents.json','bot_brain.h5'))
      start()
if __name__ = "__main__":
   start()
  ```
