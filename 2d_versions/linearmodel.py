import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

df = pd.read_csv("50k_iterations_v2.csv")
df_dependent = df[['Intercept_X', 'Intercept_Y']]
df_independent = df[['Target_X', 'Target_Y', 'Defense_X', 'Defense_Y', 'Attack_X', 'Attack_Y']]

print(df.dtypes)
print(df_dependent.dtypes)

model = LinearRegression().fit(df_independent, df_dependent)
print(model.coef_)
print(model.intercept_)
print(model.score(df_independent, df_dependent))

input = np.array([[1.44223862, 2.08929817, 2.1920255, 1.52822521, 2.59597292, -4.12118971]])
predictions = model.predict(input)
print(predictions)
# input_2d = input.reshape(1,-1)
# print(input_2d)
# print(input_2d)
# predictions = model.predict(input_2d)

 