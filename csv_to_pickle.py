import pickle
import sys
import pandas as pd

file = sys.argv[1]

# open a file, where you ant to store the data
df = pd.read_csv(file)

end_file_name = file + ".pickle"


f = open(end_file_name, 'wb')
# dump information to that file
pickle.dump(df, f)

# close the file
f.close()
