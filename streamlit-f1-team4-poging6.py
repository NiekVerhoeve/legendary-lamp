#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st 


# In[2]:


st.set_page_config(layout="wide")
st.title('F1 2021 Season Overview')

col1, col2 = st.columns([3, 1])
col1.write(fig1)
col1.write(fig2)
# In[3]:


seasons = [2021, 2020, 2019, 2018, 2017]

seasons_races = []

for season in seasons:
    
    url = 'https://ergast.com/api/f1/' + str(season) + '.json'
    
    response = requests.get(url)

    if response.status_code != 200:

        print('Error fetching data from source: ' + url)

    else:

        data = response.json()

        for race in data['MRData']['RaceTable']['Races']:
            
            url = 'http://ergast.com/api/f1/' + str(season) + '/' + race['round'] + '/results.json'
            
            response = requests.get(url)

            if response.status_code != 200:

                print('Error fetching data from source: ' + url)

            else:

                data = response.json()

                seasons_races.append(data['MRData']['RaceTable']['Races'][0])

                print('Successfully fetched data from source: ' + url + '.')


# In[4]:


df_seasons_races = pd.json_normalize(seasons_races, 
    record_path=['Results'], 
    meta=['season', 'round', 'raceName', 'date', 'time', ['Circuit', 'circuitName'], ['Circuit', 'Location', 'locality'], ['Circuit', 'Location', 'country']]
)


# In[5]:


df_seasons_races[['season', 'round', 'grid', 'position']] = df_seasons_races[['season', 'round', 'grid', 'position']].astype(int)
df_seasons_races[['points', 'FastestLap.AverageSpeed.speed']] = df_seasons_races[['points', 'FastestLap.AverageSpeed.speed']].astype(float)


# In[6]:


df_seasons_races['totalPointsDriver'] = df_seasons_races.groupby(by=['season','Driver.driverId'])['points'].transform('cumsum')
df_seasons_races['totalPointsConstructor'] = df_seasons_races.groupby(by=['season','Constructor.constructorId'])['points'].transform('cumsum')


# In[7]:


df_2021 = df_seasons_races[df_seasons_races['season'] == 2021]


# In[8]:


fig1 = px.line(df_2021, x="round", y="totalPointsDriver", color='Driver.familyName', 
              title="Gecumuleerd aantal punten per coureur per race in seizoen 2021", range_y=[0,450])

# Create the buttons
dropdown_buttons = [
{'label': "ALL", 'method': "update", 'args': [{"visible": [True]}, {"title": "Gecumuleerd aantal punten per coureur per race in seizoen 2021"}]},
{'label': "Hamilton", 'method': "update", 'args': [{"visible": [True, False, False, False, False, False, False, False, False, False,
                                                                 False, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Hamilton per race in seizoen 2021"}]},
{'label': "Verstappen", 'method': "update", 'args': [{"visible": [False, True, False, False, False, False, False, False, False, False,
                                                               False, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Verstappen per race in seizoen 2021"}]},
{'label': "Bottas", 'method': "update", 'args': [{"visible": [False, False, True, False, False, False, False, False, False, False,
                                                             False, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Bottas per race in seizoen 2021"}]},
{'label': "Norris", 'method': "update", 'args': [{"visible": [False, False, False, True, False, False, False, False, False, False,
                                                            False, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Norris per race in seizoen 2021"}]},
{'label': "Pérez", 'method': "update", 'args': [{"visible": [False, False, False, False, True, False, False, False, False, False,
                                                            False, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Pérez per race in seizoen 2021"}]},
{'label': "Leclerc", 'method': "update", 'args': [{"visible": [False, False, False, False, False, True, False, False, False, False,
                                                             False, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Leclerc per race in seizoen 2021"}]},
{'label': "Ricciardo", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, True, False, False, False,
                                                              False, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Ricciardo per race in seizoen 2021"}]},
{'label': "Sainz", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, True, False, False,
                                                                False, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Sainz per race in seizoen 2021"}]},
{'label': "Tsunoda", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, True, False,
                                                            False, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Tsunoda per race in seizoen 2021"}]},
{'label': "Stroll", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, True,
                                                             False, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Stroll per race in seizoen 2021"}]},
{'label': "Räikkönen", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                            True, False, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Räikkönen per race in seizoen 2021"}]},
{'label': "Giovinazzi", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                             False, True, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Giovinazzi per race in seizoen 2021"}]},
{'label': "Ocon", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                             False, False, True, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Ocon per race in seizoen 2021"}]},
{'label': "Russel", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                              False, False, False, True, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Russel per race in seizoen 2021"}]},
{'label': "Vettel", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                             False, False, False, False, True, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Vettel per race in seizoen 2021"}]},
{'label': "Schumacher", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                                False, False, False, False, False, True, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Schumacher per race in seizoen 2021"}]},
{'label': "Gasly", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                             False, False, False, False, False, False, True, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Gasly per race in seizoen 2021"}]},
{'label': "Latifi", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                                 False, False, False, False, False, False, False, True, False, False, False]}, {"title": "Gecumuleerd aantal punten Latifi per race in seizoen 2021"}]},
{'label': "Alonso", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                              False, False, False, False, False, False, False, False, True, False, False]}, {"title": "Gecumuleerd aantal punten Alonso per race in seizoen 2021"}]},
{'label': "Mazepin", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                             False, False, False, False, False, False, False, False, False, True, False]}, {"title": "Gecumuleerd aantal punten Mazepin per race in seizoen 2021"}]},
{'label': "Kubica", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, False,
                                                             False, False, False, False, False, False, False, False, False, False, True]}, {"title": "Gecumuleerd aantal punten Kubica per race in seizoen 2021"}]},
]

fig1.update_layout({'updatemenus': [
        {'active': 0, 'buttons': dropdown_buttons}
        ]})
fig1.update_xaxes(type='category', title={'text': 'Race'})
fig1.update_yaxes(title={'text': 'Gecumuleerd aantal punten'})
fig1.update_layout(legend_title_text='Coureur')
fig1.show()
st.plotly_chart(fig1)


# In[9]:


fig2 = px.bar(df_2021, x='Driver.code', y='points', color='Circuit.circuitName', 
             animation_frame='round', animation_group='points', range_x=[-0.5, 9.5], range_y=[0,30],
             labels={"Driver.code":"Driver", 'points':'Points', 'Circuit.circuitName':'Circuit'}, 
             title='Point per driver per round')

#fig = px.bar(df_2021, x='Driver.code', y='points', color='Constructor.name', 
#            range_x=[-0.5, 9.5], range_y=[0,30],
#             labels={"Driver.code":"Driver", 'points':'Points', 'Circuit.circuitName':'Circuit'}, 
#             title='Point per driver per round')

fig2.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'})


# legenda verplaatsen zodat formaat chart niet wijzigd 
fig2.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="right",
    x=1))
fig2.show()
st.plotly_chart(fig2)


# In[10]:


fig3 = px.line(df_2021, x="round", y="totalPointsConstructor", color='Constructor.name', 
              title="Gecumuleerd aantal punten per constructeur per race in seizoen 2021", range_y=[0,650])

# Create the buttons
dropdown_buttons = [
{'label': "ALL", 'method': "update", 'args': [{"visible": [True, True, True]}, {"title": "Gecumuleerd aantal punten per constructeur per race in seizoen 2021"}]},
{'label': "Mercedes", 'method': "update", 'args': [{"visible": [True, False, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Mercedes per race in seizoen 2021"}]},
{'label': "Red Bull", 'method': "update", 'args': [{"visible": [False, True, False, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Red Bull per race in seizoen 2021"}]},
{'label': "McLaren", 'method': "update", 'args': [{"visible": [False, False, True, False, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten McLaren per race in seizoen 2021"}]},
{'label': "Ferrari", 'method': "update", 'args': [{"visible": [False, False, False, True, False, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Ferrari per race in seizoen 2021"}]},
{'label': "AlphaTauri", 'method': "update", 'args': [{"visible": [False, False, False, False, True, False, False, False, False, False]}, {"title": "Gecumuleerd aantal punten AlphaTauri per race in seizoen 2021"}]},
{'label': "Aston Martin", 'method': "update", 'args': [{"visible": [False, False, False, False, False, True, False, False, False, False]}, {"title": "Gecumuleerd aantal punten Aston Martin per race in seizoen 2021"}]},
{'label': "Alfa Romeo", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, True, False, False, False]}, {"title": "Gecumuleerd aantal punten Alfa Romeo per race in seizoen 2021"}]},
{'label': "Alpine F1 Team", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, True, False, False]}, {"title": "Gecumuleerd aantal punten Alpine F1 Team per race in seizoen 2021"}]},
{'label': "Williams", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, True, False]}, {"title": "Gecumuleerd aantal punten Williams per race in seizoen 2021"}]},
{'label': "Haas F1 Team", 'method': "update", 'args': [{"visible": [False, False, False, False, False, False, False, False, False, True]}, {"title": "Gecumuleerd aantal punten Haas F1 Team per race in seizoen 2021"}]},
]

# Update the figure to add dropdown menu
fig3.update_layout({'updatemenus': [
        {'active': 0, 'buttons': dropdown_buttons}
        ]})

fig3.update_xaxes(type='category', title={'text': 'Race'})
fig3.update_yaxes(title={'text': 'Gecumuleerd aantal punten'})
fig3.update_layout(legend_title_text='Constructeur')
fig3.show()
st.plotly_chart(fig3)


# In[11]:


# bar constructor points per race


# In[12]:


# Calc. pole positions per driver

fig4 = go.Figure()

drivers = []
polePositions = []
winPositions = []

for driver, group in df_2021.groupby('Driver.familyName'):
    
    rowNumPoles = group[group['grid'] == 1].shape[0]
    rowNumWins = group[group['position'] == 1].shape[0]
    
    drivers.append(driver)
    polePositions.append(rowNumPoles)
    winPositions.append(rowNumWins)


fig4.add_trace(go.Bar(x=drivers, y=polePositions, name="Pole"))
fig4.add_trace(go.Bar(x=drivers, y=winPositions, name="Win"))

# Create the buttons
dropdown_buttons = [
{'label': "ALL", 'method': "update", 'args': [{"visible": [True, True]}, {"title": "ALL"}]},
{'label': "Pole", 'method': "update", 'args': [{"visible": [True, False]}, {"title": "Pole"}]},
{'label': "Win", 'method': "update", 'args': [{"visible": [False, True]}, {"title": "Win"}]}
]
fig4.update_layout(

    title="Verdeling pole posities en races gewonnen per coureur in seizoen 2021",
    xaxis_title="Coureur",
    yaxis_title="Aantal",
    legend_title="Type",
  		updatemenus = [
        {'active': 0, 'buttons': dropdown_buttons}
        ]
        )

fig4.show()
st.plotly_chart(fig4)


# In[18]:


# Calc. pole positions per driver

fig5 = go.Figure()

drivers = []
polePositions = []

for driver, group in df_2021.groupby('Driver.familyName'):
    
    rowNum = group[group['grid'] == 1].shape[0]
    
    drivers.append(driver)
    polePositions.append(rowNum)

fig5.add_trace(go.Pie(labels=drivers, values=polePositions, scalegroup='one'))
fig5.update_traces(textposition='inside',textinfo='value',marker=dict(line=dict(width=2)))
fig5.update_layout(uniformtext_minsize=20, uniformtext_mode='hide',title="Verdeling pole positions per coureur in seizoen 2021", legend=dict(font=dict(size=12)),margin=dict(
        l=0,
        r=0,
        b=0,
        t=50,
        pad=0,
        
    ))

    
fig5.show()
st.plotly_chart(fig5)


# In[14]:


# Calc. podium places
fig6 = go.Figure()

counter = 0

for position, group in df_2021.groupby(by='position'):

    if counter < 3:

        fig6.add_trace(go.Bar(
            x=group['Driver.familyName'].value_counts().keys().tolist(),
            y=group['Driver.familyName'].value_counts().tolist(),
        name=position))
    
        counter+=1

sliders = [
    {'steps':[
    {'method': 'update', 'label': '1e plek', 'args': [{'visible': [True, False, False]}]},
    {'method': 'update', 'label': '2e plek', 'args': [{'visible': [False, True, False]}]},
    {'method': 'update', 'label': '3e plek', 'args': [{'visible': [False, False, True]}]}]}]

fig6.update_layout(
    title="Verdeling podiumplaatsen per coureur in seizoen 2021",
    # xaxis_title="Coureur",
    yaxis_title="Aantal podiumplaatsen",
    legend_title="Podiumplaats")

fig6.show()
st.plotly_chart(fig6)


# In[19]:


# Calc. podium places
fig7 = go.Figure()

counter = 0

for position, group in df_2021.groupby(by='position'):

    if counter < 3:

        fig7.add_trace(go.Pie(labels=group['Driver.familyName'].value_counts().keys().tolist(), 
                             values=group['Driver.familyName'].value_counts().tolist(), 
                             scalegroup='one',title='# of podium finishes per driver'))

        counter+=1

sliders = [
    {'steps':[
    {'method': 'update', 'label': '1e plek', 'args': [{'visible': [True, False, False]}]},
    {'method': 'update', 'label': '2e plek', 'args': [{'visible': [False, True, False]}]},
    {'method': 'update', 'label': '3e plek', 'args': [{'visible': [False, False, True]}]}]}]

fig7.data[1].visible = False
fig7.data[2].visible = False

fig7.update_traces(textposition='inside',textinfo='value',marker=dict(line=dict(color='#000000', width=2)))
fig7.update_layout(
    title="Verdeling podiumplaatsen per coureur in seizoen 2021",
    # xaxis_title="Coureur",
    yaxis_title="Aantal podiumplaatsen",
    legend_title="Driver",
    sliders=sliders)

fig7.show()
st.plotly_chart(fig7)


# In[16]:


fig8 = px.bar(df_2021, x='Constructor.name', y='points', color='Driver.code', 
             animation_frame='round', animation_group='points', range_x=[-0.5, 9.5], range_y=[0,45],
             labels={"Driver.code":"Driver", 'points':'Points', 'Constructor.name':'Constructor team'}, 
             title='Points constructor driver per round')

fig8['layout'].pop('updatemenus')
sliders = [dict(
    active=0,
    currentvalue={"prefix": "Round ", 'suffix':':'},
    pad={"t": 5})]


fig8.update_xaxes(tickangle=45)
fig8.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'}, sliders=sliders)
fig8['layout']['sliders'][0]['pad']=dict(r= 10, t= 100,)
fig8.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="right",
    x=1))
fig8.show()
st.plotly_chart(fig8)


# In[20]:


# Calc. avg speed of fastest lap per track in histogram

fig9 = go.Figure()

names = []
means = []

for name, group in df_2021.groupby(['Circuit.circuitName']):

    names.append(name)
    means.append(group['FastestLap.AverageSpeed.speed'].mean())

fig9.add_trace(go.Bar(x=means, y=names, orientation='h'))

fig9.show()
st.plotly_chart(fig9)


# In[ ]:




