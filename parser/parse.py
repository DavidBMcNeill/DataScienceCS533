
# coding: utf-8

# In[ ]:


#Parsing API 
# Author: James Souder
#------------

import re
import pickle
import settings


# In[ ]:


REGEX = re.compile(settings.FEATURE_REGEX)


# In[ ]:


def split_data_dictionary():
    housing_file = open(settings.HOUSING_TXT, 'w')
    person_file = open(settings.PERSON_TXT, 'w')
    split_flag = False
    
    with open(settings.DATA_DICT, 'r') as data_dict: 
            for text in data_dict:
                if text == settings.TXT_SPLIT_VAL: # found beginning of person record
                    split_flag = True
                    
                if(split_flag):
                    if(text == settings.STOP_VAL):
                        break
                    person_file.append()
                else:
                    housing_file.append()
 


# In[ ]:


def create_decoding_dict(input_txt, pickle_name):
    decoder = {} # dict with feature key and tuple value to hold desc and subdecoder
    empty = '\n' # Stop symbol for subcodes
    
    with open(input_file) as iFile:
        for text in iFile:
            match = REGEX.match(text) # Finds next match
            if match: 
                # Get string portion of match object without whitespace and numbers
                key = re.match('[A-Z]*\d*', match.group(0)).group(0)
                desc = iFile.readline().strip() # Feature description
                subdecoder = {}
                sub = iFile.readline() #Begin reading subcodes
                while sub != empty:
                    codes = [x.strip() for x in sub.split(".")]
                    subdecoder[codes[0]] = codes[1]
                    sub = iFile.readline()
                decoder[key] = tuple(desc, subdecoder) # key maps to tuple containing desc and subdecoder

    with open(pickle_name, 'wb') as oPickle:
        pickle.dump(decoder, oPickle)

