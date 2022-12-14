import random
import math

class TextModel:    

   
     def __init__ (self, model_name):
        """ that constructs a new 
        TextModel object by accepting a string model_name 
        as a parameter and initializing the following three attributes: name, 
        words, and words lengths"""
        self.name = model_name      
        self.words = {}
        self.word_lengths= {}
        self.stems= {}
        self.lengths = {}
        self.model = {}
        
     def __repr__(self):
            """Return a string representation of the TextModel."""
            s = 'text model name: ' + self.name + '\n'
            s += '  number of words: ' + str(len(self.words)) + '\n'
            s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
            s += '  number of stems: ' + str(len(self.stems)) + '\n'
            s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
            s += '  number of model lengths: ' + str(len(self.model)) + '\n'
            
            return s
    
     def add_string(self, s):  
        """ adds a string of texts
        to the model by augmenting the feature dictionaries defined in the constructor."""
        
        
        self.model = build_dictionary(s)
        
        
        #sentence length    
        number = 0
        for letter in s.split():
            number += 1
            if letter[-1]  in '.!?':
                if number in self.sentence_lengths:
                    self.sentence_lengths[number] += 1
                    number = 0
                else:
                    self.sentence_lengths[number] = 1
                    number = 0
        
        #clean
        word_list = clean_text(s)
        
        for w in word_list:
            if w in self.words:
                self.words[w] += 1
            else:
                self.words[w] = 1
            len(w)
            if len(w) in self.word_lengths:
                self.word_lengths[len(w)] += 1
            else:
                self.word_lengths[len(w)] =  1
            if w not in self.stems :
                self.stems[w] = 1
            else:
                self.stems[w] += 1
                
                
                
     def add_file(self, filename):
      """adds all of the text in the file identified by filename to the model"""
      f = open(filename, 'r', encoding='utf8', errors='ignore')   
      text = f.read()        
      f.close()
      self.add_string(text)
   
     def save_model(self):
        """saves the TextModel object self by writing its various 
        feature dictionaries to files."""
        f1 = open((self.name + '-' + 'words'), 'w')
        f1.write(str(self.words))
        f1.close()
        
        f2 = open((self.name + '-'+ 'word_lengths'), 'w')
        f2.write(str(self.word_lengths))
        f2.close()
        
        f3 = open((self.name + '_' + 'stems'), 'w')
        f3.write(str(self.stems))
        f3.close()
        
        f4 = open((self.name + '_' + 'sentence_lengths'), 'w')
        f4.write(str(self.sentence_lengths))
        f4.close()
        
        f5 = open((self.name + '_' + 'last_word'), 'w')
        f5.write(str(self.last_word))
        f5.close()
        
        f = open(self.name +'model', 'w')
        f.write(str(self.model))
        f.close()
   
     def read_model(self):
        """reads the stored dictionaries for the 
        called TextModel object from their files and assigns 
        them to the attributes of the called TextModel."""
        f1 = open((self.name + '-' + 'words'), 'r')
        d_str = f1.read()
        f1.close()
        self.words = dict(eval(d_str))
        
        f2 = open((self.name + '-' + 'word_lengths'), 'r')
        b_str= f2.read()
        f2.close()
        self.word_lengths = dict(eval(b_str))
        
        f3 = open((self.name + '_' + 'stems'), 'r')
        e_str = f3.read()
        f3.close()
        self.stems = eval(e_str)
        
        f4 = open((self.name + '_' + 'sentence_lengths'), 'r')
        f_str = f4.read()
        f4.close()
        self.sentence_lengths = eval(f_str)
        
        f5 = open((self.name + '_' + 'last_word'), 'r')
        k_str = f5.read()
        f5.close()
        self.last_word = eval(k_str)
        
        f = open(self.name +'model', 'r')    # Open for reading.
        d_str = f.read()           # Read in a string that represents a dict.
        f.close()
        self.model = dict(eval(d_str))  # Convert the string to a dictionary.
        
     def similarity_scores(self, other):
         """that computes and returns a list of log similarity 
         scores measuring the similarity of self and other ???
         one score for each type of feature (words, word lengths,
         stems, sentence lengths, and your additional feature)."""
         word_score = compare_dictionaries(other.words, self.words)
         word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
         stems_score = compare_dictionaries(other.stems, self.stems)
         sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
         
         
         s1 = create_text(other.model, len(other.words))
         s2 = create_text(self.model, len(self.words))
         test1 = TextModel('first Model')
         test2 = TextModel('second  Model')
         test1.add_string(s1)
         test2.add_string(s2)
         
         model1 = compare_dictionaries(test2.words, test1.words)
         model2 = compare_dictionaries(test2.word_lengths, test1.word_lengths)
         model3 = compare_dictionaries(test2.stems, test1.stems)
         model4 = compare_dictionaries(test2.sentence_lengths, test1.sentence_lengths)
         
         score = (model1 + model2 + model3 + model4) / 4
        
         final_list = [word_score,word_lengths_score,stems_score,sentence_lengths_score, score]
         return final_list
     
     def classify(self, source1, source2):
         """ that compares the called TextModel 
         object (self) to two other ???source??? TextModel 
         objects (source1 and source2) and determines which of these 
         other TextModels is the more likely source of the called TextModel."""
         scores1 = self.similarity_scores(source1)
         scores2 = self.similarity_scores(source2)
         print('scores for', source1.name, ':', scores1)
         print('scores for', source2.name, ':', scores2)
         post1 = 0
         post2 = 0
         for i in range (5):
             if scores1[i] > scores2[i]:
                 post1 += 1
             elif scores1[i] < scores2[i]:
                 post2 +=  1            
         if post1 > post2 :
             print(self.name, "is more likely to have come from", source1.name)
         elif post1 == post2:
             print(self.name,'is equally likely to come from', source1.name, 'and', source2.name)
         else:
             print(self.name, 'is more likely to have come from', source2.name)
             
def build_dictionary(text):
    """takes string, which is the name of the file, and splits it into key-value pairs. 
    """
    #creates an array
    words = text.split()
    
    #creates a dictionary
    result = {}
    currentWord = '*'
    
    for nextWord in words:
        if currentWord not in result:
            result[currentWord] = [nextWord]
        else:
            result[currentWord] += [nextWord]
        lastletter = nextWord[len(nextWord)-1]
        if lastletter in '!?.':
            currentWord = '*'
        else:
            currentWord = nextWord
    return result

def create_text(words_dict, number_words):
    """creates text length of num_words
    takes in the dictionary containing the words
    Iand return the desired length of the ouput
    """
    answer = ''
    currentWord = '*'
    for x in range(number_words):
        wordPrint = random.choice(words_dict[currentWord])
        answer += wordPrint + ' '
        lastletter = wordPrint[len(wordPrint)-1]
        if lastletter in '!?.':
            currentWord = '*'
        else:
            currentWord = wordPrint
    
    return answer

def clean_text(txt):
   """Takes a string and cleans it by making it all lowercase with no punctuation
   """
   txt = txt.lower()
   words = txt.split()
   cleaned = ''
   for x in words:
       for y in x:
           if y in 'abcdefghijklmnopqrstuvwxyz123456789':
               cleaned += y
       cleaned += ' '
   #gets rid of extra space the line above put in on the last iteration
   cleaned = cleaned[:-1]
   txt = cleaned.split()
   return txt


def stem(s):
    """that accepts a string as a parameter. 
    The function should then return the stem of s."""
    word_stem = s
    if word_stem[-2:] == 'ed':
        if len(word_stem) < 5:
            word_stem = word_stem
        else:
            word_stem = word_stem[:-2]
    elif word_stem[-1] == 's':
        word_stem = word_stem[:-1]
    elif word_stem[-1:]  == 'y':
        word_stem= word_stem[:-1] + 'i'
    elif word_stem[-4:] == 'able':
        if len(word_stem) > 7:
            word_stem = word_stem[:-4]
        else:
            word_stem = word_stem
    elif word_stem[-1]  == 'e':
        word_stem = word_stem[:-1]
    elif word_stem[-3:] == 'ing':
        if len(s) < 6:
            word_stem = word_stem
        elif word_stem[-4] == word_stem[-5]:
            word_stem = word_stem[:-4]
        else:
            word_stem = word_stem[:-3]
    elif word_stem[-3:] == 'ies':
        word_stem = word_stem[:-2]
    else:
        word_stem = word_stem
    return word_stem

def compare_dictionaries(d1,d2):
    """It should take two feature 
    dictionaries d1 and d2 as inputs, 
    and it should compute and return their log similarity score"""
    if d1 == {}:
        return -50
    score = 0
    total = sum(d1.values())
    temp_score = 0
    for c in d2:
        if c in d1:
            temp_score = d1[c] / total
            temp_score = d2[c] * math.log(temp_score)
            score += temp_score
            temp_score = 0
        else:
            temp_score = d2[c] * math.log(0.5/total)
            score += temp_score
            temp_score = 0
    return score 

def test():
    """ find the similairity score between different source and mystery.Outputs the source and 
    mystery are more related"""
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)
    
def run_tests():
    """ create text models and calculate their simliarity score  """
    source1 = TextModel('Friends')
    source1.add_file('friends.txt')

    source2 = TextModel('How I Met Your Mother')
    source2.add_file('how I met your mother.txt')

    new1 = TextModel('Big Bang Theory')
    new1.add_file('Big Bang Theory.txt')
    new1.classify(source1, source2) 
    
    new2 = TextModel('Friends 2')
    new2.add_file('friends2.txt')
    new2.classify(source1, source2) 
    
    new3 = TextModel('How I met your Mother 2 ')
    new3.add_file('How I met your mother 2.txt')
    new3.classify(source1, source2) 
    
    new4 = TextModel('New girl')
    new4.add_file('New girl.txt')
    new4.classify(source1, source2) 
    

    
