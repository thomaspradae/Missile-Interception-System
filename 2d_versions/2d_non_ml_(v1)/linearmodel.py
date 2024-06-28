import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

df = pd.read_csv("2d_versions/100k_iterations_v3.csv")
df_dependent = df[['Intercept_X', 'Intercept_Y']]
df_independent = df[['Target_X', 'Target_Y', 'Defense_X', 'Defense_Y', 'Attack_X', 'Attack_Y']]

# print(df.dtypes)
# print(df_dependent.dtypes)

model = LinearRegression().fit(df_independent, df_dependent)
print(model.coef_)
print(model.intercept_)
print(model.score(df_independent, df_dependent))
# Print the model error
# print(model.score(df_independent, df_dependent))

input = np.array([[1.44223862, 2.08929817, 2.1920255, 1.52822521, 2.59597292, -4.12118971]])
predictions = model.predict(input)
print(predictions)
# input_2d = input.reshape(1,-1)
# print(input_2d)
# print(input_2d)
# predictions = model.predict(input_2d)

 
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(df_independent, df_dependent, test_size=0.2, random_state=42)

# Train the model on the training data
model = LinearRegression().fit(X_train, y_train)

# Make predictions on the test data
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
print("Mean Squared Error:", mse)
print("Mean Absolute Error:", mae)
