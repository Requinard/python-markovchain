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


class MarkovBrain():
    def __init__(self):
        self.keyValue = {}
        self.unusedItems = ['!', '?', '.']

    def learn(self, sentence):
        """
        Incorporates a complete sentence into the dictionairy
        :param sentence:
        :return:
        """
        words = sentence.split(" ")

        i = 0

        while True:
            # See if the array has come to an end
            try:
                # Get the keywords
                word1 = words[i]
                word2 = words[i + 1]
                supplement_word = words[i + 2]
            except Exception:
                print "No more words to find"
                break

            try:
                last_word = words[i + 3]
            except:
                print "Found last word"
                supplement_word += '.'

            # increment counter
            i += 2

            # Compile full key
            completed_key = word1 + " " + word2

            print("Key created: {}".format(completed_key))
            print("Value created: {}".format(supplement_word))

            # Remove unnecassry punctuation
            for item in self.unusedItems:
                if item in completed_key:
                    print("Mark removed: {}".format(item))
                    completed_key.replace(item, "")

            # Manage existing keywords
            if self.keyValue.has_key(completed_key):
                print("Dictionary contains key {}".format(completed_key))
                responses = self.keyValue[completed_key]

                if supplement_word in responses.keys():
                    print "Updating supplement word {2} from {0} to {1}".format(responses[completed_key], responses[completed_key] + 1, responses[supplement_word])
                    responses[completed_key] += 1
                else:
                    print "Adding supplement key {0} at value 1"
                    responses[completed_key] = 1
            # Manage non-existing keywords
            else:
                print "Adding key {0} to dictionary with supplement {1} at value 1".format(completed_key, supplement_word)
                key = self.keyValue

                key[completed_key] = {supplement_word: 1}

        return True