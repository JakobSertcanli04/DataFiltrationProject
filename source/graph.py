import pandas as pd
import re
import ast
import plotly.express as px

# Read the file
with open('2015-2025.csv.txt', 'r') as f:
    raw = f.read()

# Extract dictionary-like strings
dict_strings = re.findall(r'\{.*?\}', raw, re.DOTALL)

# Safely parse them into actual Python dictionaries
data = []
for d in dict_strings:
    try:
        # Clean up any malformed keys (like trailing newlines or \r\n)
        cleaned = re.sub(r'\s+', ' ', d)
        parsed = ast.literal_eval(cleaned)
        data.append(parsed)
    except Exception as e:
        print("Skipping entry due to error:", e)

# Convert to DataFrame
df = pd.DataFrame(data)

# Replace NaNs with 0 for consistent numeric handling
df.fillna(0, inplace=True)

# Drop all-zero columns (excluding 'Year' which we'll add)
df = df.loc[:, (df != 0).any(axis=0)]

# Add Year column (2015 to 2015 + number of entries)
df['Year'] = list(range(2015, 2015 + len(df)))

# Group by year (in case of duplicate years — not likely, but safe)
df_yearly = df.groupby('Year').sum(numeric_only=True).reset_index()

# Reshape for plotting
df_melted = df_yearly.melt(id_vars='Year', var_name='Category', value_name='Count')

# Plot using Plotly
fig = px.line(df_melted,
              x='Year',
              y='Count',
              color='Category',
              markers=True,
              title='Environmental Impact Trends by Category (2015–2025)')

fig.update_traces(mode='lines+markers', hovertemplate='<b>%{x}</b><br>%{fullData.name}: %{y}<extra></extra>')
fig.update_layout(xaxis=dict(dtick=1), yaxis_title='Count', xaxis_title='Year')

fig.show()
