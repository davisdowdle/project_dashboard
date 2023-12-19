import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


st.title('Real GDP per Capita Covariates')
url = 'https://raw.githubusercontent.com/davisdowdle/semesterproject/main/gdp.csv'
gdp = pd.read_csv(url)


st.header('Unique Country Information')

select_country = st.selectbox('Select a country', gdp.sort_values('Entity')['Entity'])
country_row = gdp[gdp['Entity'] == select_country]

col1, col2, col3, col4 = st.columns(4)

col1.subheader('Status')
if country_row.loc[:, 'Entity'].values[0] == country_row.loc[:, 'Parent'].values[0]:
    col1.write(':red[Country]')
else:
    col1.write(f":red[Territory - {country_row.loc[:, 'Parent'].values[0]}]")

col2.subheader('UN Region')
col2.write(f":red[{country_row.loc[:, 'Region'].values[0]}]")

col3.subheader('Primary Currency')
col3.write(f":red[{country_row.loc[:, 'Currency'].values[0]}]")

col4.subheader('Real GDP per Capita')
col4.write(f":red[{country_row.loc[:, 'GDP'].values[0]}]")

st.divider()

col1, col2, col3, col4 = st.columns(4)

col1.subheader('Population')
col1.write(f":red[{country_row.loc[:, 'Population'].values[0]}]")

col2.subheader('Geographic Area (sq mi)')
col2.write(f":red[{country_row.loc[:, 'Area'].values[0]}]")

col3.subheader('Population Density')
col3.write(f":red[{country_row.loc[:, 'Density'].values[0]}]")

col4.subheader('Trade Ratio')
col4.write(f":red[{country_row.loc[:, 'Ratio'].values[0]}]")


st.text('')


st.header('Country Statistic Comparison')

stat = st.selectbox('Select a statistic', ['Real GDP per Capita', 'Population', 'Geographic Area (sq mi)', 'Population Density', 'Trade Ratio'])
countries = st.multiselect('Select countries to compare', gdp.sort_values('Entity')['Entity'], default = 'AFGHANISTAN')

if stat == 'Real GDP per Capita':
    col = 'GDP'
if stat == 'Population':
    col = 'Population'
if stat == 'Geographic Area (sq mi)':
    col = 'Area'
if stat == 'Population Density':
    col = 'Density'
if stat == 'Trade Ratio':
    col = 'Ratio'

df = gdp[gdp['Entity'].isin(countries)].sort_values(col, ascending = False)

fig = plt.figure(figsize=(10, 4))
ax = sns.barplot(df, x = 'Entity', y = col, palette = 'Paired')
for index, v in enumerate(df[col]):
    ax.text(index, v, str(v), ha='center')
plt.title(f"{stat} for Country Selection")
plt.xlabel('Country/Territory')
plt.ylabel(stat)
st.pyplot(fig)


st.text('')


st.header('Numeric Variable Spread')

st.subheader('Worldwide Histogram')

var = st.selectbox('Select an x variable', ['Real GDP per Capita', 'Population', 'Geographic Area (sq mi)', 'Population Density', 'Trade Ratio'])
if var != 'Real GDP per Capita':
    df = gdp[gdp['Entity'] != 'WORLD']
else:
    df = gdp


if var == 'Real GDP per Capita':
    xvar = 'GDP'
if var == 'Population':
    xvar = 'Population'
if var == 'Geographic Area (sq mi)':
    xvar = 'Area'
if var == 'Population Density':
    xvar = 'Density'
if var == 'Trade Ratio':
    xvar = 'Ratio'

fig = plt.figure(figsize=(10, 4))
sns.histplot(df, x = xvar)
plt.title(f"Worldwide {var} Spread")
plt.xlabel(var)
plt.ylabel('Number of Countries')
st.pyplot(fig)

st.subheader('Regional Boxplot')

if var == 'Real GDP per Capita':
    yvar = 'GDP'
if var == 'Population':
    yvar = 'Population'
if var == 'Geographic Area (sq mi)':
    yvar = 'Area'
if var == 'Population Density':
    yvar = 'Density'
if var == 'Trade Ratio':
    yvar = 'Ratio'

fig = plt.figure(figsize=(10, 10))
sns.boxplot(df, x = 'Region', y = yvar, palette = 'tab10')
plt.title(f"{var} Spread by Region")
plt.xlabel('United Nations Region')
plt.ylabel(var)
st.pyplot(fig)


st.text('')


st.header('Dynamic Scatterplot')

x = st.selectbox('Select an x variable', ['Real GDP per Capita', 'Population', 'Geographic Area (sq mi)', 'Population Density', 'Trade Ratio'], index = 4)
y = st.selectbox('Select a y variable', ['Real GDP per Capita', 'Population', 'Geographic Area (sq mi)', 'Population Density', 'Trade Ratio'], index = 0)
lm = st.checkbox('Overlay linear model')

if x == 'Real GDP per Capita':
    xvar = 'GDP'
if x == 'Population':
    xvar = 'Population'
if x == 'Geographic Area (sq mi)':
    xvar = 'Area'
if x == 'Population Density':
    xvar = 'Density'
if x == 'Trade Ratio':
    xvar = 'Ratio'

if y == 'Real GDP per Capita':
    yvar = 'GDP'
if y == 'Population':
    yvar = 'Population'
if y == 'Geographic Area (sq mi)':
    yvar = 'Area'
if y == 'Population Density':
    yvar = 'Density'
if y == 'Trade Ratio':
    yvar = 'Ratio'

if lm:
    fig = sns.lmplot(data = gdp, x = xvar, y = yvar, ci = None)
else:
    fig = plt.figure(figsize=(10, 4))
    sns.scatterplot(gdp, x = xvar, y = yvar)
plt.title(f"{x} vs {y}")
plt.xlabel(x)
plt.ylabel(y)
st.pyplot(fig)


st.text('')


st.header('Currency Queries')

st.subheader('Data Query')

curr = st.selectbox('Select a currency to query the data', gdp.sort_values('Currency')['Currency'].unique())
df = gdp[gdp['Currency'] == curr].sort_values('Entity')

st.write('Countries with above primary currency:')

st.dataframe(df)

st.subheader('Currency Comparison')

curr1 = st.selectbox('Select a currency', gdp.sort_values('Currency')['Currency'].unique(), index = 0)
count1 = gdp[gdp['Currency'] == curr1].shape[0]
gdp1 = gdp[gdp['Currency'] == curr1]['GDP'].mean()
ratio1 = gdp[gdp['Currency'] == curr1]['Ratio'].mean()

curr2 = st.selectbox('Select another currency', gdp.sort_values('Currency')['Currency'].unique(), index = 1)
count2 = gdp[gdp['Currency'] == curr2].shape[0]
gdp2 = gdp[gdp['Currency'] == curr2]['GDP'].mean()
ratio2 = gdp[gdp['Currency'] == curr2]['Ratio'].mean()

comp = {'Currency': [curr1, curr2],
        'Count': [count1, count2],
        'Average GDP': [gdp1, gdp2],
        'Average Ratio': [ratio1, ratio2]}

fig, axes = plt.subplots(1, 3, figsize=(12, 6))

sns.barplot(x = 'Currency', y = 'Count', data = comp, ax = axes[0], palette = 'Set2')
axes[0].set_title('Number of Countries')

sns.barplot(x = 'Currency', y='Average GDP', data = comp, ax = axes[1], palette = 'Set2')
axes[1].set_title('Average GDP')

sns.barplot(x = 'Currency', y='Average Ratio', data = comp, ax = axes[2], palette = 'Set2')
axes[2].set_title('Average Trade Ratio')

st.pyplot(fig)
