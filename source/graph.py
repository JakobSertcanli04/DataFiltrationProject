import pandas as pd
import re
import ast
import plotly.express as px

# This Python code snippet is reading data from a file named 'categorySortedByDateV.txt', parsing the
# content to extract dictionary strings, converting those strings into dictionaries using
# `ast.literal_eval`, creating a pandas DataFrame from the dictionaries, performing data manipulation
# to filter out columns with all zeros, adding a 'Year' column based on the data, grouping the data by
# year and summing the values, melting the DataFrame to have a long format suitable for plotting, and
# finally creating a line plot using Plotly Express to visualize the yearly trends of the data by
# category. The plot includes multiple lines for each category, with markers on data points, and a
# hover template to display detailed information when hovering over the data points.


with open('categorySortedByDateV.txt', 'r') as f:
    raw = f.read()

dict_strings = re.findall(r'\{[^{}]*\}', raw)
data = [ast.literal_eval(d) for d in dict_strings]

df = pd.DataFrame(data)

df = df.loc[:, (df != 0).any(axis=0)]

years = [2015 + i for i in range((len(df) + 11) // 12)]
df['Year'] = [years[i // 12] for i in range(len(df))]

df_yearly = df.groupby('Year').sum(numeric_only=True).reset_index()

df_melted = df_yearly.melt(id_vars='Year', var_name='Category', value_name='Count')

fig = px.line(df_melted,
              x='Year',
              y='Count',
              color='Category',
              markers=True,
              title='Yearly Trends')

fig.update_traces(mode='lines+markers', hovertemplate='<b>%{x}</b><br>%{fullData.name}: %{y}<extra></extra>')
fig.update_layout(xaxis=dict(dtick=1))  
fig.show()
