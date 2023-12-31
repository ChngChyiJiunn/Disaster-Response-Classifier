import sys
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    '''
    Load the raw data


    Args:
        messages_filepath: disaster_messages.csv filepath
        categories_filepath: disaster_categories.csv filepath

    Returns:
        df: A merged dataframe based on 'id' column (inner join)

    '''
    
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)

    df = messages.merge(categories,on ='id')
    return df


def clean_data(df):
    '''
    Perform data cleaning on teh merged dataframe returned from function load_data()

    Args:
        df:A merged uncleaned dataframe

    Returns:
        df:A cleaned datafrrame
    
    '''
    categories = df['categories'].str.split(";",expand=True)

    # select the first row of the categories dataframe
    row = categories.iloc[0,:]

    # use this row to extract a list of new column names for categories.
    # up to the second to last character of each string with slicing
    category_colnames = row.apply(lambda x : x[:-2] )
    categories.columns = category_colnames

    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].astype('str').str[-1]
        
        # convert column from string to numeric
        categories[column] = categories[column].astype('int')
    
    df.drop(columns = ['categories'],axis = 1,inplace = True)
    df = pd.concat([df,categories],axis = 1)
    df.drop_duplicates(inplace=True)

    return df


def save_data(df, database_filename):
    '''
    Save the cleaned data into database

    Args:
        df:A merged uncleaned dataframe
        database_filename: Location to store your Database

    Returns:
        None
    
    '''

    engine = create_engine('sqlite:///' + database_filename)
    df.to_sql('Disaster_Response_Table', engine, index=False)


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'Disaster_Response.db')


if __name__ == '__main__':
    main()