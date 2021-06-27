#%%
from numpy.core.numeric import NaN
import requests
import pandas
from dataclasses import dataclass, field
import csv
import altair as alt
import seaborn as sns
import plotly.express as px
response = requests.get('https://restcountries.eu/rest/v2/all')


country_json = response.json()

countries = pandas.json_normalize(country_json)

countries.latlng = countries.latlng.apply(lambda y: [0,0] if y==[] else y)
# overwriting countries dataframe with specified data
countries = countries[['name', 'capital', 'region', 'subregion', 'latlng', 'area', 'borders', 'currencies', 'languages', 'population', 'nativeName']]

# converting borders to count of bordering countries
countries['border_count'] = countries.borders.str.len()


countries[['latitude','longitude']] =  countries.latlng.astype(str).str.split(',',expand = True)
countries['latitude'] = countries['latitude'].str.strip('[')
countries['longitude'] = countries['longitude'].str.strip(']')

countries['latitude'] = pandas.to_numeric(countries['latitude'])
countries['longitude'] = pandas.to_numeric(countries['longitude'])

countries['language_count'] = countries.languages.str.len()


region_grouping = countries.groupby('region')

region_grouping.describe() 

#%%

countries = countries.sort_values(by=['population'])
px.histogram(countries.tail(10), x='name', y = 'population',labels={
                     "name": "Name",
                     "population": "Population"
                 },
             title="Countries By Population",nbins=10).update_xaxes(categoryorder="total descending")

#%%
fig = px.scatter(countries, x="border_count", y="area",
                 size="population", color="region",
                 labels={
                     "border_count": "Border Count",
                     "area": "Area"
                 },title="Bor" ,
                 hover_name="name", log_x=False, size_max=60)
fig.show()
#%%
source = countries
alt.Chart(source).mark_circle(size=60).encode(
    x='border_count',
    y='language_count',
    tooltip=['border_count', 'language_count']
).properties(title='Borders vs Languages').interactive()

#%%  
import seaborn as sns
sns.set_style('darkgrid')
sns.boxplot(x='language_count', y='region', data=countries).set(title="Languages by Region", xlabel="Number of Languages", ylabel="Region")

#%%
fig = px.scatter(countries, x="border_count", y="language_count",
                 size="population", color="region",
                 hover_name="name", log_x=False, size_max=60,
                 title = "Number of Languages Based on Bordering Countries and Region",
                 labels={'border_count':'Number of Bordering Countries',
                        'language_count':'Number of Languages'})
fig.show()
# %%
