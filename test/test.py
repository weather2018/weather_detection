import numpy as np
import pandas as pd

frame = pd.DataFrame(np.arange(9).reshape((3,3)), index=['a','b','c'], columns=['Ohio', 'Texas', 'Califormia'])
print(frame)

print(np.arange(9).reshape((3,3)))