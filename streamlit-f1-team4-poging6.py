#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import streamlit as st 


# In[2]:

seasons = [2021]

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


# #### Visualizing data

# In[ ]:


# Plotting the data
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

# Making the layout
fig1.update_layout({'updatemenus': [
        {'active': 0, 'buttons': dropdown_buttons}
        ]})
fig1.update_xaxes(type='category', title={'text': 'Race'})
fig1.update_yaxes(title={'text': 'Gecumuleerd aantal punten'})
fig1.update_layout(legend_title_text='Coureur')
fig1.show()


# In[ ]:


# Plotting the data
fig2 = px.line(df_2021, x="round", y="totalPointsConstructor", color='Constructor.name', 
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

# Making the layout
fig2.update_layout({'updatemenus': [
        {'active': 0, 'buttons': dropdown_buttons}
        ]})

fig2.update_xaxes(type='category', title={'text': 'Race'})
fig2.update_yaxes(title={'text': 'Gecumuleerd aantal punten'})
fig2.update_layout(legend_title_text='Constructeur')
fig2.show()


# In[ ]:


fig3 = px.bar(df_2021, x='Driver.familyName', y='points', color='Constructor.name', 
             animation_frame='round', animation_group='points', range_x=[-0.5, 9.5], range_y=[0,30],
             labels={"Driver.familyName":"Coureur", 'points':'Punten', 'Constructor.name':'Constructeur team'}, 
             title='Punten per coureur per ronde')

fig3.update_xaxes(tickangle=45)
fig3['layout'].pop('updatemenus')
sliders = [dict(
    active=0,
    currentvalue={"prefix": "Round ", 'suffix':':'},
    pad={"t": 5})]

fig3.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'}, sliders=sliders)
fig3['layout']['sliders'][0]['pad']=dict(r= 10, t= 100,)
fig3.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="right",
    x=1.2))
fig3.show()


# In[ ]:


fig4 = px.bar(df_2021, x='Constructor.name', y='points', color='Driver.familyName', 
             animation_frame='round', animation_group='points', range_x=[-0.5, 9.5], range_y=[0,45],
             labels={"Driver.familyName":"Coureur", 'points':'Punten', 'Constructor.name':'Constructeur team'}, 
             title='Punten per constructeur per race')

fig4['layout'].pop('updatemenus')
sliders = [dict(
    active=0,
    currentvalue={"prefix": "Round ", 'suffix':':'},
    pad={"t": 5})]


fig4.update_xaxes(tickangle=45)
fig4.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'}, sliders=sliders)
fig4['layout']['sliders'][0]['pad']=dict(r= 10, t= 100,)
fig4.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="right",
    x=1.2))
fig4.show()

# Calc. podium places
fig5 = go.Figure()

counter = 0

for position, group in df_2021.groupby(by='position'):

    if counter < 3:

        fig5.add_trace(go.Bar(
            x=group['Driver.familyName'].value_counts().keys().tolist(),
            y=group['Driver.familyName'].value_counts().tolist(),
        name=position))
    
        counter+=1

sliders = [
    {'steps':[
    {'method': 'update', 'label': '1e plek', 'args': [{'visible': [True, False, False]}]},
    {'method': 'update', 'label': '2e plek', 'args': [{'visible': [False, True, False]}]},
    {'method': 'update', 'label': '3e plek', 'args': [{'visible': [False, False, True]}]}]}]

fig5.update_layout(
    title="Verdeling podiumplaatsen per coureur in seizoen 2021",
    # xaxis_title="Coureur",
    yaxis_title="Aantal podiumplaatsen",
    legend_title="Podiumplaats")

fig5.show()

# Calc. podium places
fig6 = go.Figure()

counter = 0

for position, group in df_2021.groupby(by='position'):

    if counter < 3:

        fig6.add_trace(go.Pie(labels=group['Driver.familyName'].value_counts().keys().tolist(), 
                             values=group['Driver.familyName'].value_counts().tolist(), 
                             scalegroup='one',title='# of podium finishes per driver'))

        counter+=1

sliders = [
    {'steps':[
    {'method': 'update', 'label': '1e plek', 'args': [{'visible': [True, False, False]}]},
    {'method': 'update', 'label': '2e plek', 'args': [{'visible': [False, True, False]}]},
    {'method': 'update', 'label': '3e plek', 'args': [{'visible': [False, False, True]}]}]}]

fig6.data[1].visible = False
fig6.data[2].visible = False

fig6.update_traces(textposition='inside',textinfo='value',marker=dict(line=dict(color='#000000', width=2)))
fig6.update_layout(
    title="Verdeling podiumplaatsen per coureur in seizoen 2021",
    # xaxis_title="Coureur",
    yaxis_title="Aantal podiumplaatsen",
    legend_title="Driver",
    sliders=sliders)

fig6.show()

# Calc. avg speed of fastest lap per track in bar plot

fig9 = go.Figure()

names = []
means = []

for name, group in df_2021.groupby(['Circuit.circuitName']):

    names.append(name)
    means.append(group['FastestLap.AverageSpeed.speed'].mean())

fig9.add_trace(go.Bar(x=means, y=names, orientation='h'))

fig9.update_xaxes(title={'text': 'Seconden'})
fig9.update_yaxes(title={'text': 'Circuit'})
fig9.update_layout(title="Gemiddelde tijd van de snelste ronde per circuit in seizoen 2021")

fig9.show()

# Calc. pole positions per driver

fig7 = go.Figure()

driversPoles = []
polePositions = []

driversWins = []
winPositions = []

for driver, group in df_2021.groupby('Driver.familyName'):
    
    rowNumPoles = group[group['grid'] == 1].shape[0]

    rowNumWins = group[group['position'] == 1].shape[0]

    if(rowNumPoles != 0):
        driversPoles.append(driver)
        polePositions.append(rowNumPoles)



    if(rowNumWins != 0):
        driversWins.append(driver)
        winPositions.append(rowNumWins)
    
    
    
    # winPositions.append(rowNumWins)


fig7.add_trace(go.Bar(x=driversPoles, y=polePositions, name="Pole"))
fig7.add_trace(go.Bar(x=driversWins, y=winPositions, name="Win"))

# Create the buttons
dropdown_buttons = [
{'label': "ALL", 'method': "update", 'args': [{"visible": [True, True]}, {"title": "ALL"}]},
{'label': "Pole", 'method': "update", 'args': [{"visible": [True, False]}, {"title": "Pole"}]},
{'label': "Win", 'method': "update", 'args': [{"visible": [False, True]}, {"title": "Win"}]}
]

fig7.update_layout(
    title="Verdeling pole posities en races gewonnen per coureur in seizoen 2021",
    xaxis_title="Coureur",
    yaxis_title="Aantal poles/wins",
    legend_title="Type",
    updatemenus = [{'active': 0, 'buttons': dropdown_buttons}]
    )

fig7.show()

#Finished, +1 Lap, +2 Laps, +3 Laps
df_2021['Finished_Int'] = np.where((df_2021['status']=='Finished')| 
                                     (df_2021['status'] == '+1 Lap')|
                                     (df_2021['status'] == '+2 Laps')|
                                     (df_2021['status'] == '+3 Laps'),1,0)

df_2021['TotalPoints'] = df_2021.groupby(by=['Driver.familyName'])['points'].transform('sum')

df_2021['TotalFinishes'] = df_2021.groupby(by=['Driver.familyName'])['Finished_Int'].transform('sum')

fig8 = px.scatter(df_2021, x="TotalPoints", y="TotalFinishes", color="Driver.familyName",
                 range_y=[15, 23], title='Verdeling aantal punten per gefinishte races', 
                 labels={'TotalFinishes':'# Finishes', 'TotalPoints':'Aantal punten', 'Driver.familyName':'Coureur'})

fig8.update_layout()
fig8.show()

# #### Setting up the dashboard

# In[ ]:


st.set_page_config(layout="wide")
st.title('F1 2021 Season Overview')


# In[ ]:

st.subheader('Inladen van de API')
st.markdown('Voor het maken van een dashboard is er gebruikt gemaakt van de Formule 1 API, die verkregen is via http://ergast.com/mrd/. Deze dataset bevat de gegevens van alle Formule 1 races van 1950 tot nu. Door de hoeveelheid van data is er gekozen om voor dit dashboard alleen gebruik te maken van het seizoen 2021. Met behulp van onderstaande code worden eerst alle races van het 2021 seizoen opgehaald, waarna per opgehaalde race hierbij ook de bijbehorende resultaten worden verzameld:')

import_api= '''seasons = [2021]

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
                print('Successfully fetched data from source: ' + url + '.')'''

st.code(import_api, language='python')
st.markdown('Door de print functies in bovenstaande code kan je precies zien of het importeren is gelukt, en zo niet zal er een foutmelding worden gegeven. Echter is de data die nu is verkregen nog niet bruikbaar. Dit komt omdat de json data nog nested is. Dit wordt opgelost door de volgende code:') 

fixing_nested = '''df_seasons_races = pd.json_normalize(seasons_races, 
    record_path=['Results'], 
    meta=['season', 'round', 'raceName', 'date', 'time', ['Circuit', 'circuitName'], 
          ['Circuit', 'Location', 'locality'], ['Circuit', 'Location', 'country']])'''
st.code(fixing_nested, language='python')
st.markdown('Omdat er dus in eerste instantie het idee was om meer dan alleen het 2021 seizoen te gebruiken, is er met de volgende code alle data uit het 2021 seizoen gesubset voor specifieke doeleinden:')

subset_2021 = '''df_2021 = df_seasons_races[df_seasons_races['season'] == 2021]'''
st.code(subset_2021, language='python')

st.markdown('Naast de bestaande data zijn er voor de visualisaties extra kolommen met data aangemaakt. Deze extra kolommen maken het mekkelijker om bepaalde inzichten in totale punten en finishes per coureur en team te weergeven.')

kolommen_code = '''df_seasons_races['totalPointsDriver'] = df_seasons_races.groupby(by=['season','Driver.driverId'])['points'].transform('cumsum')
df_seasons_races['totalPointsConstructor'] = df_seasons_races.groupby(by=['season','Constructor.constructorId'])['points'].transform('cumsum')
df_2021['Finished_Int'] = np.where((df_2021['status']=='Finished')| 
                                     (df_2021['status'] == '+1 Lap')|
                                     (df_2021['status'] == '+2 Laps')|
                                     (df_2021['status'] == '+3 Laps'),1,0)

df_2021['TotalPoints'] = df_2021.groupby(by=['Driver.familyName'])['points'].transform('sum')

df_2021['TotalFinishes'] = df_2021.groupby(by=['Driver.familyName'])['Finished_Int'].transform('sum')'''

st.code(kolommen_code, language='python')


st.markdown('Nu de dataset volledig en correct is geimporteerd, kan deze worden bekeken. In onderstaande tabel zijn de eerste 10 rijen van de dataset zichtbaar gemaakt.')
st.dataframe(df_2021.head(10))

st.subheader('Behaalde punten in seizoen 2021')
st.markdown("Om eerst een overzicht te creëren van de uitkomst van het 2021 seizoen is er voor gekozen om twee line charts op te stellen. Hiermee is de puntenverdeling per coureur en per team overzichtelijk gevisualiseerd. In de dropdown menu's kan er specifieker gekeken worden naar een enkele coureur of team.")


# In[ ]:

st.markdown('**Code uitleg**')
st.markdown('Om de visualisatie te realiseren is er gebruik gemaakt van plotly express. Door de  juiste dataframe, x-as, y-as en nog een aantal variabelen in te vullen (zoals in de code hier onder), kan er met de px.line functie een juiste grafiek worden geplot. Zoals te zien is de code voor het maken van de labels erg lang. Er is gekeken naar een betere oplossing hier voor, maar die is helaas niet gevonden. De onderstaande code is op een aantal benodigde aanpassingen voor beide lijngrafieken gebruikt')

linechart_code = '''# Plotting the data
fig2 = px.line(df_2021, x="round", y="totalPointsConstructor", color='Constructor.name', 
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

# Making the layout
fig2.update_layout({'updatemenus': [
        {'active': 0, 'buttons': dropdown_buttons}
        ]})

fig2.update_xaxes(type='category', title={'text': 'Race'})
fig2.update_yaxes(title={'text': 'Gecumuleerd aantal punten'})
fig2.update_layout(legend_title_text='Constructeur')
fig2.show()'''

st.code(linechart_code, language='python')

plot1, plot2 = st.columns([5, 5])
plot1.plotly_chart(fig1)
plot2.plotly_chart(fig2)


# In[ ]:

st.markdown('Om meer in te zoomen op het algemene overzicht wat de lijngrafieken hebben gegeven, zijn er twee staafgrafieken gerealiseerd. Aan de hand van een slider onderaan de grafieken kan er makkelijk per race worden gekeken naar het aantal behaalde punten per coureur en team. In de rechter van de twee onderstaande grafieken is gebruik gemaakt van een stacked overzicht om de verschillen in behaalde punten tussen de teamgenoten te visualiseren.')
st.markdown('**Code uitleg**')
st.markdown('Voor het maken van de staafgrafieken is weer gebruik gemaakt van plotly express. Echter is er nu inplaats van de px.line functie gebruik gemaakt van de px.bar functie. Het verder invullen van de benodigde data gaat volgens de zelfde weg. Om een slider toe te voegen zijn de elementen animation_frame en animation_group nodig. Met de animation_frame wordt bepaald welke data voor de slider wordt gebruikt. Met de animation_group wordt vastgesteld welke data hetzelfde blijft.')

barplot_code = '''fig4 = px.bar(df_2021, x='Constructor.name', y='points', color='Driver.familyName', 
             animation_frame='round', animation_group='points', range_x=[-0.5, 9.5], range_y=[0,45],
             labels={"Driver.familyName":"Coureur", 'points':'Punten', 'Constructor.name':'Constructeur team'}, 
             title='Punten per constructeur per race')

fig4['layout'].pop('updatemenus')
sliders = [dict(
    active=0,
    currentvalue={"prefix": "Round ", 'suffix':':'},
    pad={"t": 5})]


fig4.update_xaxes(tickangle=45)
fig4.update_layout(barmode='stack', xaxis={'categoryorder':'total descending'}, sliders=sliders)
fig4['layout']['sliders'][0]['pad']=dict(r= 10, t= 100,)
fig4.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="right",
    x=1.2))
fig4.show()'''            

st.code(barplot_code, language='python')

plot3, plot4 = st.columns([5, 5])
plot3.plotly_chart(fig3)
plot4.plotly_chart(fig4)

st.subheader('Raceposities in seizoen 2021')

st.markdown('Onderstaande staafgrafiek en cirkeldiagram vormen gezamenlijk een inzicht in de behaalde podiumfinishes van de coureurs. Zo is in de staafgrafiek in een oogopslag te zien hoeveel eerste, tweede en derde plaatsen elke coureur heeft behaald. De cirkeldiagram rechts ernaast laat verder de verhouding tussen de coureurs per podiumpositie zien.')

st.markdown('**Code uitleg**')

piechart_podium_code = '''fig5 = go.Figure()

counter = 0

for position, group in df_2021.groupby(by='position'):

    if counter < 3:

        fig5.add_trace(go.Bar(
            x=group['Driver.familyName'].value_counts().keys().tolist(),
            y=group['Driver.familyName'].value_counts().tolist(),
        name=position))
    
        counter+=1

sliders = [
    {'steps':[
    {'method': 'update', 'label': '1e plek', 'args': [{'visible': [True, False, False]}]},
    {'method': 'update', 'label': '2e plek', 'args': [{'visible': [False, True, False]}]},
    {'method': 'update', 'label': '3e plek', 'args': [{'visible': [False, False, True]}]}]}]

fig5.update_layout(
    title="Verdeling podiumplaatsen per coureur in seizoen 2021",
    yaxis_title="Aantal podiumplaatsen",
    legend_title="Podiumplaats")

fig5.show()'''

st.markdown('Om de cirkeldiagram op te stellen is gebruik gemaakt van plotly graphic object. Door gebruik van een variabele met waarde 0 (counter), kan 3 keer door een if statement gelooped worden om de waarden van finish positie een, twee en drie te verzamelen. Deze waardes worden met traces geplot op de cirkeldiagram. Hierna wordt met een slider een onderscheiding gemaakt tussen de drie verschillende podiumposities. Voor step 1, 1e plek, wordt de data van trace 2 en 3 verborgen. Hierdoor is dus alleen de data van podiumfinish 1 te zien als de slider op 1e plek staat. Dit geldt ook voor 2e en 3e plek, alleen worden hier dan andere traces verborgen.')
st.code(piechart_podium_code,language='python')

# In[ ]:

plot5, plot6 = st.columns([5, 5])
plot5.plotly_chart(fig5)
plot6.plotly_chart(fig6)

# In[ ]:

st.subheader('Pole posities, wins en finishes')
st.markdown('In de volgende visualisaties is gekeken naar de verhouding tussen wins en pole positions, en het aantal finishes en punten. In de staafgrafiek is een mooie visualisatie die per coureur 2 staven laat zien. Een staaf die het aantal pole posities aangeeft binnen het seizoen, en een andere staaf die de wins weergeeft. Met deze staafgrafiek is gemakkelijk te zien of er een duidelijk verband ligt tussen het aantal pole posities en wins per coureur. In de scatterplot is een overzicht gemaakt van het aantal punten en finishes per coureur. Uiteraard zijn er meerdere oorzaken waardoor een coureur een race niet kan finishen en dus geen kans maakt op punten. Hierdoor is er in dit scatterplot te zien hoeveel races die coureurs hebben gefinished en hoeveel punten zij in deze races hebben behaald.')

st.markdown('**Code uitleg**')
st.markdown('Voor de scatterplot is gebruik gemaakt van plotly express. Door de eerder opgestelde integer kolom met het aantal gefinishte races per coureur te gebruiken, kon deze waarde tegen het aantal behaalde punten per coureur worden geplot. Dit geeft als resultaat een mooie scatterplot waar duidelijke conclusies uit konnen worden getrokken. Zo is te zien dat Hamilton 2 races meer gefinisht heeft, maar toch minder punten heeft behaald dan Verstappen. ')

st.code(scatterplot_code,language='python')

scatterplot_code = '''fig8 = px.scatter(df_2021, x="TotalPoints", y="TotalFinishes", color="Driver.familyName",
                 range_y=[15, 23], title='Verdeling aantal punten per gefinishte races', 
                 labels={'TotalFinishes':'# Finishes', 'TotalPoints':'Aantal punten', 'Driver.familyName':'Coureur'})
fig8.update_layout()
fig8.show()'''

plot7, plot8 = st.columns([5, 5])
plot7.plotly_chart(fig7)
plot8.plotly_chart(fig8)

plot9, text8 = st.columns([5, 5])
plot9.plotly_chart(fig9)



