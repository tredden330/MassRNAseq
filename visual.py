import numpy as np
from PIL import Image
import pandas as pd

size = 5000
shape = np.zeros((size, size, 3), dtype=np.uint8)

df = pd.read_parquet('data/correlations.parquet') * 254


for x in range(size):
    for y in range(size):
        val = df.iat[x,y]
        if pd.isna(val):
            value = 0.0
        else:
            value = round(df.iat[x,y])
        if value >= 0:
            shape[x][y] = (0, value, 0)
        else:
            shape[x][y] = (abs(value), 0, 0)

arr_image = Image.fromarray(shape, 'RGB')
# arr_image.putpixel((50, 50), white)
arr_image.save('test.jpg')