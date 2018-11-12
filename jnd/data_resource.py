import settings
import pandas as pd
import os
from datetime import datetime


def create_csv(dataset, col_list=None):
    def generate_file_name():
        return dataset + datetime.now().strftime('_%m_%d_%y_%H_%M_%S') + '.csv'

    if not os.path.exists(settings.USER_GENERATED_DIR):
        os.mkdir(settings.USER_GENERATED_DIR)
    file_loc = 'data/' + dataset + '.csv'

    if col_list == None:
        frame = pd.read_csv(file_loc)
    else:
        frame = pd.read_csv(file_loc, usecols=col_list)
    name = generate_file_name()
    loc = settings.USER_GENERATED_DIR+name
    frame.to_csv(loc)
    return loc,name

# def Articles():
#     articles = [
#         {
#             'id': 1,
#             'title':'Article One',
#             'body':'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
#             'author':'Brad Traversy',
#             'create_date':'04-25-2017'
#         },
#         {
#             'id': 2,
#             'title':'Article Two',
#             'body':'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
#             'author':'John Doe',
#             'create_date':'04-25-2017'
#         },
#         {
#             'id': 3,
#             'title':'Article Three',
#             'body':'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
#             'author':'Brad Traversy',
#             'create_date':'04-25-2017'
#         }
#     ]
# return articles