
# coding: utf-8

# In[1]:


# Parser settings
# Author: James Souder
#-------------------------

# Text files for decoding features
DATA_DICT = '../docs/data_dict_txt/PUMS_Data_Dictionary_2012-2016.txt'
HOUSING_TXT = '../docs/data_dict_txt/housing_record.txt'
PERSON_TXT = '../docs/data_dict_txt/person_record.txt'

START_VAL = 'HOUSING RECORD'
SPLIT_VAL = 'PERSON RECORD'
STOP_VAL = 'END NOTES'

# Names of pickle storage
HOUSING_PICKLE = '../data/housing.pickle'
PERSON_PICKLE = '../data/population.pickle'

#Regular Expressions
FEATURE_REGEX = '[A-Z]+[0-9]*[ ]+[0-9]+' # Locates features in txt file

USER_GENERATED_DIR = './user_generated/'

