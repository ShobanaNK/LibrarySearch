import pandas as pd
import os
from utils import generate_data, update_ChromaCollection

def process():
  data_to_store = pd.DataFrame()
  for fld in os.listdir('books'):
      data_to_store = data_to_store._append(generate_data('books/{}'.format(fld)), ignore_index=True)
  print( 'Processed {} of records to store.\n'.format(len(data_to_store)))
  update_ChromaCollection(data=data_to_store)
  print ("Processing Complete.")

if __name__ == "__main__":
    process()