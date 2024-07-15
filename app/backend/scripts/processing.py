import pandas as pd
import plotly.express as px
import statsmodels as sm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import os
from io import StringIO

print(os.getcwd())

df = pd.read_csv("app/backend/scripts/testing.csv")
start_date = '2021-09-12'
end_date = '2022-02-20'
df = df[(df['ordine_data'] >= start_date) & (df['ordine_data'] <= end_date)]


# Define the date range for the x-axis
fig = px.line(df, x='ordine_data', y=df.columns)
fig.update_xaxes(range=[start_date, end_date])



df_trimmed = df.drop(columns=['ordine_data'])
df_trimmed.corr()


fig1 = px.scatter(df, x=['google_performance_max_spent'], y='revenue')
fig2 = px.scatter(df, x=['Sconti'], y='revenue')

from statsmodels.regression.linear_model import OLS
inputs = ['Sconti', 'google_search_spent']
X = df[inputs]
y = df['revenue']
X = sm.tools.add_constant(X)
result = OLS(y, X).fit()
# print(result.summary())


X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle = True, test_size = 0.2)

model = LinearRegression()
model.fit(X_train, y_train)
'''
print("Training Score:", model.score(X_train, y_train))
print("Testing Score:", model.score(X_test, y_test))

'''
df['predictions'] = model.predict(X)

fig = px.line(df, x='ordine_data', y = ['revenue', 'predictions'])

fig = fig.to_html(full_html=False)











def process(fileData):
    df = pd.read_csv(StringIO(fileData.decode('utf-8')))
    return df.to_html()