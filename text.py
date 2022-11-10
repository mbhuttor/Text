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
        self.sentence_lengths = {}
        self.last_word = {}
            
     def __repr__(self):
            """Return a string representation of the TextModel."""
            s = 'text model name: ' + self.name + '\n'
            s += '  number of words: ' + str(len(self.words)) + '\n'
            s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
            s += '  number of stems: ' + str(len(self.stems)) + '\n'
            s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
            s += '  number of different last word with same punctuation and word: ' + str(len(self.last_word)) + '\n'
            return s
    
     def add_string(self, s):  
        """ adds a string of texts
        to the model by augmenting the feature dictionaries defined in the constructor."""
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
        count = 0
        for char in s.split():
            if char[-1] in '.!?':
                if char in self.last_word:
                    self.last_word[char] += 1
                    count = 0
                else:
                     self.last_word[char] = 1
                     count = 0
        
        
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
        
     def similarity_scores(self, other):
         """that computes and returns a list of log similarity 
         scores measuring the similarity of self and other –
         one score for each type of feature (words, word lengths,
         stems, sentence lengths, and your additional feature)."""
         word_score = compare_dictionaries(other.words, self.words)
         word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
         stems_score = compare_dictionaries(other.stems, self.stems)
         sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
         last_word_score = compare_dictionaries(other.last_word, self.last_word)
         final_list = [word_score,word_lengths_score,stems_score,sentence_lengths_score, last_word_score]
         return final_list
     def classify(self, source1, source2):
         """ that compares the called TextModel 
         object (self) to two other “source” TextModel 
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
             
             
        
def clean_text(txt):
    """takes a string of text txt as a parameter and returns a 
    list containing the words in txt after it has been “cleaned”."""
    txt = txt.replace('?', '')
    txt = txt.replace('!', '')
    txt = txt.replace("'", '') 
    txt = txt.replace('"', '')
    txt = txt.replace('-', '')
    txt = txt.replace('_', '')
    txt = txt.replace('—', '')
    txt = txt.replace('[', '')
    txt = txt.replace(']', '')
    txt = txt.replace('_', '')
    txt = txt.replace('/', '')
    txt = txt.replace('.', '')
    txt = txt.replace(',', '')
    txt = txt.replace(':', '')
    txt = txt.replace(';', '')
    txt = txt.replace('(', '')
    txt = txt.replace(')', '')
    txt = txt.lower()
    txt = txt.split()
    return txt

def stem(s):
    """hat accepts a string as a parameter. 
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
    score = 0
    total = 0
    for c in d1:
        total += d1[c]
    for c in d2:
        if c in d1:
            score += d2[c] * math.log(d1[c] / total)
        else:
            score += d2[c] * math.log(0.5/total)
            
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
    
    
