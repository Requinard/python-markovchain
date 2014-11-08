"""
Markov chains

Chain works like this
{
    "key store" :
    {
        "completion" : 1
    },
}

or in technical notation

{string : {string, int }}

Int is the probability that a word will follow
"""
import pickle
import random
import datetime

class Brain():
    def __init__(self):
        self.keyValue = {}
        self.unusedItems = ['!', '?', '.', ',', "..."]
        self.random = random.seed(datetime.datetime.now())

    def learn(self, sentence):
        """
        Incorporates a complete sentence into the dictionary
        :param sentence: Sentence that you want added to the markov brain
        :return: Success
        """
        words = sentence.split(" ")

        i = 0

        while True:
            # See if the array has come to an end
            try:
                # Get the keywords
                word1 = words[i]
                word2 = words[i + 1]
                supplement_word = words[i + 2].lower()
            except Exception:
                print "No more words to find"
                break

            try:
                last_word = words[i + 3]
            except:
                print "Found last word"
                supplement_word += '.'

            # increment counter
            i += 1

            # Compile full key
            completed_key = (word1 + " " + word2).lower()

            print("Key created: {}".format(completed_key))
            print("Value created: {}".format(supplement_word))

            # Remove unnecassry punctuation
            for item in self.unusedItems:
                if item in completed_key:
                    print("Mark removed: {}".format(item))
                    completed_key.replace(item, "")
                if item in supplement_word:
                    supplement_word.replace(item, "")

            # Manage existing keywords
            if self.keyValue.has_key(completed_key):
                print("Dictionary contains key {}".format(completed_key))
                responses = self.keyValue[completed_key]

                if supplement_word in responses.keys():
                    print "Updating supplement word {0} from {1} to {2}".format(supplement_word,
                                                                                str(responses[supplement_word]),
                                                                                str(responses[supplement_word]+ 1))
                    responses[supplement_word] += 1
                else:
                    print "Adding supplement key {0} at value 1"
                    responses[completed_key] = 1
            # Manage non-existing keywords
            else:
                print "Adding key {0} to dictionary with supplement {1} at value 1".format(completed_key,
                                                                                           supplement_word)
                key = self.keyValue

                key[completed_key] = {supplement_word: 1}

        self.save()

        return True

    def save(self):
        """
        Saves the brain keyvalue stores to a brain.dump file
        :return:
        """
        pickle.dump(self.keyValue, open("brain.dump", "w+"))
        print "Successfully saved file"

    def load(self):
        """
        Loads the brain keyvalue strores from a brain.dump file
        :return: Success of operation
        """
        try:
            var = pickle.load(open("brain.dump", "r"))
            if var != None:
                print "Successfully loaded file"
                self.keyValue = var
                return True
            return False
        except Exception:
            return Fals

    def respond(self, sentence):
        """
        Tries to respond to a specific sentence
        :param sentence: Sentence you want a response to
        :return: Sentence that is a direct response to input sentence
        """
        words = sentence.split(" ")
        completed_seed = ""
        seed_one = ""
        seed_two = ""
        i = 0

        # try to generate words from actual sentence. Do this ten times, otherwise we'll pick a random seed
        while True:
            try:
                seed_one = words[i]
                seed_two = words[i+1]
                completed_seed = (seed_one + " " + seed_two).lower()

                if completed_seed in self.keyValue.keys():
                    break

                i += 1
            except Exception:
                completed_seed = self.keyValue.keys()[random.randint(0, len(self.keyValue.keys())-1)]
                seed_one = completed_seed.split(" ")[0]
                seed_two = completed_seed.split(" ")[1]
                break


        # Start constructing response
        loop_word_one = seed_one
        loop_word_two = seed_two
        full_response = completed_seed

        while True:
            possibilities_weighted = []
            possible_responses = {}
            loop_completed_seed = "{0} {1}".format(loop_word_one, loop_word_two)

            # If the possible response throws an exception, we have no words to follow that up with. We then end the sentence
            try:
                possible_responses = self.keyValue[loop_completed_seed]
            except:
                return (full_response + ".").capitalize()


            # Add all repsonses to a list equal to the amount of times it has appeared
            for response in possible_responses.keys():
                for i in range(0, possible_responses[response]):
                    possibilities_weighted.append(response)

            # Chose a random value from the dictionairy
            chosen_response = possibilities_weighted[random.randint(0, len(possibilities_weighted)-1)]

            # Append chosen part to the new full response
            full_response += " " + chosen_response

            # If we have a dot in our sentence, we have found an end. Return the sentence
            if "." in chosen_response:
                return full_response.capitalize()

            # If we're still here, we swap the words around to generate the next word
            loop_word_one = loop_word_two
            loop_word_two = chosen_response




