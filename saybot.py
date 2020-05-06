import json
import pickle
import random

import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.models import load_model
from keras.optimizers import SGD

import nltk
from nltk.tokenize import word_tokenize as wtk
from nltk.stem import WordNetLemmatizer
import pickle

lemmatizer = WordNetLemmatizer()

#intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


def trains(js,brain):

    words=[]
    classes = []
    documents = []
    ignore_words = ['?', '!']
    data_file = open(js).read()
    intents = json.loads(data_file) 

    for intent in intents['intents']:
        for pattern in intent['patterns']:

            #tokenize each word
            w = nltk.word_tokenize(pattern)
            words.extend(w)
            #add documents in the corpus
            documents.append((w, intent['tag']))

            # add to our classes list
            if intent['tag'] not in classes:
                classes.append(intent['tag'])

    # lemmaztize and lower each word and remove duplicates
    words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
    words = sorted(list(set(words)))
    # sort classes
    classes = sorted(list(set(classes)))
    # documents = combination between patterns and intents
    print (len(documents), "documents")
    # classes = intents
    print (len(classes), "classes", classes)
    # words = all words, vocabulary
    print (len(words), "unique lemmatized words", words)


    pickle.dump(words,open('words.pkl','wb'))
    pickle.dump(classes,open('classes.pkl','wb'))

        # create our training data
    training = []
    # create an empty array for our output
    output_empty = [0] * len(classes)
    # training set, bag of words for each sentence
    for doc in documents:
        # initialize our bag of words
        bag = []
        # list of tokenized words for the pattern
        pattern_words = doc[0]
        # lemmatize each word - create base word, in attempt to represent related words
        pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
        # create our bag of words array with 1, if word match found in current pattern
        for w in words:
            bag.append(1) if w in pattern_words else bag.append(0)
    
        # output is a '0' for each tag and '1' for current tag (for each pattern)
        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
    
        training.append([bag, output_row])
    # shuffle our features and turn into np.array
    random.shuffle(training)
    training = np.array(training)
    # create train and test lists. X - patterns, Y - intents
    train_x = list(training[:,0])
    train_y = list(training[:,1])
    print("Training data created")


    # Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
    # equal to number of intents to predict output intent with softmax
    model = Sequential()
    model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation='softmax'))

    # Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    #fitting and saving the model 
    hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
    model.save(brain, hist)

    #model = load_model(brain)

    print("model created")

    
class Saybot():
    #train bot and build brain file used for later chat

    def clean_up_sentence(self,sentence):
        # tokenize the pattern - split words into array
        sentence_words = nltk.word_tokenize(sentence)
        # stem each word - create short form for word
        sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    def bow(self,sentence, words, show_details=True):
        # tokenize the pattern
        sentence_words = self.clean_up_sentence(sentence)
        # bag of words - matrix of N words, vocabulary matrix
        bag = [0]*len(words)  
        for s in sentence_words:
            for i,w in enumerate(words):
                if w == s: 
                    # assign 1 if current word is in the vocabulary position
                    bag[i] = 1
                    if show_details:
                        res = "found in bag: %s" % w
        return(np.array(bag))

    def predict_class(self,sentence, model):
        # filter out predictions below a threshold
        p = self.bow(sentence, words,show_details=False)
        res = model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
        return return_list

    # chat response 
    def getResponse(self,ints, intents_json):
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if(i['tag']== tag):
                result = random.choice(i['responses'])
                break
        return result

    #decide what to response    
    def response(self,msg,br,inte):
        user = msg
        lst = wtk(user)
        #name = self.botname(bot)
        model = load_model(br)
        intents = json.loads(open(inte).read())

        if user != "quit":
            if 'youtube' in lst:
                text = user.split()
                y = "youtube"
                vid = ' '.join([i for i in text if i not in y])
                f.open(vid)
                response = "result will show on your web bowser"
                return response
            elif 'wikipedia' in lst:
                text = user.split() 
                y = "wikipedia"
                word = ' '.join([i for i in text if i not in y])
                response = f.short(word)
                return response
            elif 'google' in lst:
                text = user.split()
                y = "google"
                qus = ' '.join([i for i in text if i not in y])
                f.browser_search(qus)
                response = "result will show on your web browser"
                return response
            else:
                ints = self.predict_class(msg, model)
                response = self.getResponse(ints, intents)
                return response
        else:
            quit()           

'''
    def trains(js,brain):
        words=[]
        classes = []
        documents = []
        ignore_words = ['?', '!']
        data_file = open(js).read()
        intents = json.loads(data_file) 

        for intent in intents['intents']:
            for pattern in intent['patterns']:

                #tokenize each word
                w = nltk.word_tokenize(pattern)
                words.extend(w)
                #add documents in the corpus
                documents.append((w, intent['tag']))

                # add to our classes list
                if intent['tag'] not in classes:
                    classes.append(intent['tag'])

        # lemmaztize and lower each word and remove duplicates
        words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
        words = sorted(list(set(words)))
        # sort classes
        classes = sorted(list(set(classes)))
        # documents = combination between patterns and intents
        print (len(documents), "documents")
        # classes = intents
        print (len(classes), "classes", classes)
        # words = all words, vocabulary
        print (len(words), "unique lemmatized words", words)


        pickle.dump(words,open('words.pkl','wb'))
        pickle.dump(classes,open('classes.pkl','wb'))

        # create our training data
        training = []
        # create an empty array for our output
        output_empty = [0] * len(classes)
        # training set, bag of words for each sentence
        for doc in documents:
            # initialize our bag of words
            bag = []
            # list of tokenized words for the pattern
            pattern_words = doc[0]
            # lemmatize each word - create base word, in attempt to represent related words
            pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
            # create our bag of words array with 1, if word match found in current pattern
            for w in words:
                bag.append(1) if w in pattern_words else bag.append(0)
    
            # output is a '0' for each tag and '1' for current tag (for each pattern)
            output_row = list(output_empty)
            output_row[classes.index(doc[1])] = 1
    
            training.append([bag, output_row])
        # shuffle our features and turn into np.array
        random.shuffle(training)
        training = np.array(training)
        # create train and test lists. X - patterns, Y - intents
        train_x = list(training[:,0])
        train_y = list(training[:,1])
        print("Training data created")


        # Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer contains number of neurons
        # equal to number of intents to predict output intent with softmax
        model = Sequential()
        model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))

        # Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        #fitting and saving the model 
        hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
        model.save(brain, hist)

        #model = load_model(brain)

        print("model created")

        self.brain = brain

        def model():
            model = load_model(brain)
            print(model)
            return model
'''


if __name__== "__main__":
    trains()