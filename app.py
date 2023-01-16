
#Final project DADS5001 (Live chat analytics)
#Witsarut Wongsim 6420422017
#Pimchayanan Kusontramas 6420422018

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import datetime
df=pd.read_csv("chats-csv.csv",on_bad_lines='skip' )
df['datetime']= pd.to_datetime(df['datetime'])
# Group the data by username
grouped_data = df.groupby('name')
grouped_data
# Calculate the summary score for each category by summing the corresponding columns
scores = grouped_data[['positive_value','negative_value','joy','surprise','sadness','pleasant','fear','anger','neutral']].sum()

# Create a new dataframe with the username and scores
scores_df = pd.DataFrame(scores).reset_index()
scores_df['sum']=scores_df[['positive_value','negative_value', 'joy', 'surprise', 'sadness', 'pleasant', 'fear','anger', 'neutral']].sum(axis=1)
scores_df.sort_values(by='sum', ascending=False, inplace=True)
top10user=scores_df.iloc[0:10,:]
data = top10user
data['name'].unique()
text = df[['message']]
text.head()
text['message'] = text['message'].str.replace(r'[^ก-๙]','').reset_index(drop=True)
text['message'].astype(str)
text_data = pd.DataFrame(text, columns=['message'])
text = text.query('message != ""')
dfs=df[['datetime','message','positive_value','negative_value','joy','surprise','sadness','pleasant','fear','anger','neutral']]
dfs['datetime'] = pd.to_datetime(dfs['datetime'], unit='s')
dfs=dfs.dropna()
dfs[['positive_value','negative_value','joy','surprise','sadness','pleasant','fear','anger','neutral']] =dfs[['positive_value','negative_value','joy','surprise','sadness','pleasant','fear','anger','neutral']].cumsum()
df_accum = dfs


# load data into a DataFrame
categories = ['positive_value','negative_value','joy','surprise','sadness','pleasant','fear','anger']#,'neutral'

# Create a figure with 10 subplots
radar = make_subplots(rows=2, cols=5,specs=[[{'type': 'polar'}]*5]*2, subplot_titles=data['name'].unique())

# Iterate through the dataframe to add traces to each subplot
for i, username in enumerate(data['name'].unique()):
    user_data = data[data['name'] == username]
    trace = go.Scatterpolar(
        r = user_data[categories].values.tolist()[0],
        theta = categories,
        fill = 'toself',
    )
    # Add the trace to the corresponding subplot
    radar.add_trace(trace, row=i // 5 + 1, col=i % 5 + 1)

# Update the layout of the figure
radar.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0,62])), font=dict(size=8) )

app = dash.Dash()
col = ['positive_value','negative_value', 'joy', 'surprise', 'sadness', 'pleasant', 'fear','anger', 'neutral']
# sum each column individually
df_grouped = df[col].sum()


# Create bar chart
chart = dcc.Graph(
        id='bar-chart',
        figure={
            'data': [
                go.Bar(
                    x=df_grouped.index,
                    y=df_grouped.values
                )
            ],
            'layout': go.Layout(
                title='Bar Chart Sentiment Analysis',
                xaxis={'title': 'Sentiment'},
                yaxis={'title': 'Sum'}
                
            )
        }
    )



app.layout = html.Div([
    html.Div(
        [
            
                dcc.Graph(
        id='acc_line_chart',
        figure={
            'data': [
                go.Scatter(x=df_accum.datetime, y=df_accum['positive_value'], mode='lines', name='positive_value'),
                go.Scatter(x=df_accum.datetime, y=df_accum['negative_value'], mode='lines', name='negative_value'),
                go.Scatter(x=df_accum.datetime, y=df_accum['joy'], mode='lines', name='joy'),
                go.Scatter(x=df_accum.datetime, y=df_accum['surprise'], mode='lines', name='surprise'),
                go.Scatter(x=df_accum.datetime, y=df_accum['sadness'], mode='lines', name='sadness'),
                go.Scatter(x=df_accum.datetime, y=df_accum['pleasant'], mode='lines', name='pleasant'),
                go.Scatter(x=df_accum.datetime, y=df_accum['fear'], mode='lines', name='fear'),
                go.Scatter(x=df_accum.datetime, y=df_accum['anger'], mode='lines', name='anger'),
                go.Scatter(x=df_accum.datetime, y=df_accum['neutral'], mode='lines', name='neutral'),

            ],
            'layout': go.Layout(
                xaxis={'title': 'Date and Time'},
                yaxis={'title': 'Sentiment'},
                margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                title = 'Accumulate Sentiment overtime Chart by category'
            )
        }
    ),   
    dcc.Graph(
        id='sentiment-chart',
        figure={
            'data': [
                go.Scatter(x=df['datetime'], y=df['positive_value'], mode='lines', name='positive_value'),
                go.Scatter(x=df['datetime'], y=df['negative_value'], mode='lines', name='negative_value'),
                go.Scatter(x=df['datetime'], y=df['joy'], mode='lines', name='joy'),
                go.Scatter(x=df['datetime'], y=df['surprise'], mode='lines', name='surprise'),
                go.Scatter(x=df['datetime'], y=df['sadness'], mode='lines', name='sadness'),
                go.Scatter(x=df['datetime'], y=df['pleasant'], mode='lines', name='pleasant'),
                go.Scatter(x=df['datetime'], y=df['fear'], mode='lines', name='fear'),
                go.Scatter(x=df['datetime'], y=df['anger'], mode='lines', name='anger'),
                go.Scatter(x=df['datetime'], y=df['neutral'], mode='lines', name='neutral'),
            ] ,
            'layout': go.Layout(
                
                xaxis={'title': 'Date and Time'},
                yaxis={'title': 'Sentiment'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                title='Sentiment overtime'
            )
        }
    ),
     dcc.Checklist(
        id='sentiment-categories',
        options=[
            {'label': 'positive_value', 'value': 'positive_value'},
            {'label': 'negative_value', 'value': 'negative_value'},
            {'label': 'joy', 'value': 'joy'},
            {'label': 'surprise', 'value': 'surprise'},
            {'label': 'sadness', 'value': 'sadness'},
            {'label': 'pleasant', 'value': 'pleasant'},
            {'label': 'fear', 'value': 'fear'},
            {'label': 'anger', 'value': 'anger'},
            {'label': 'neutral', 'value': 'neutral'}
        ],
        value=['positive_value'])
        
    ] , style = {'padding':10 , 'flex':1}) ,
    
    html.Div([
    dcc.Dropdown(
        id='column-selector',
        options=['positive_value', 'negative_value', 'joy', 'surprise', 'sadness', 'pleasant', 'fear', 'anger', 'neutral'],
        value='positive_value'
    ),
    dcc.Graph(id='heatmap')
] ,style = {'padding':10 , 'flex':1})

    
    
    
    
    
        ,chart,
    
    
     html.Div([
    # Create a dropdown menu with all the available usernames
    dcc.Dropdown(
        id='username-dropdown',
        options=[{'label': username, 'value': username} for username in data['name'].unique()],
        value='evejangja'
    ),
    # Create a Graph component to display the radar chart
    dcc.Graph(id='polar-chart',figure={'layout': go.Layout(title='Radar Chart by User')}),
],style={'padding':10 , 'flex':1}),
    
    
    dcc.Graph(figure=radar)
])

@app.callback(
    Output('sentiment-chart', 'figure'),
    [Input('sentiment-categories', 'value')])
def update_chart(sentiment_categories):
    data = []
    for category in sentiment_categories:
        x_values = df['datetime']
        y_values = df[category]
        data.append(go.Scatter(x=x_values, y=y_values, mode='lines', name=category))

    return {
        'data': data,
        'layout': go.Layout(
            xaxis={'title': 'Date and Time'},
            yaxis={'title': 'Sentiment'},
            margin={'l': 40, 'b': 40, 't': 40, 'r': 40},
            legend={'x': 0, 'y': 1},
            hovermode='closest',
            title='Sentiment overtime'
        )
    }

@app.callback(
    dash.dependencies.Output('polar-chart', 'figure'),
    [dash.dependencies.Input('username-dropdown', 'value')])
def update_chart(username):
    user_data = data[data['name'] == username]
    trace = go.Scatterpolar(
        r = user_data[categories].values.tolist()[0],
        theta = categories,
        fill = 'toself',
    )

    return {
        'data': [trace],
        'layout': go.Layout(
            polar=dict(radialaxis=dict(visible=True,range=[0,62])),
            title=f'Radar chart by username:{ username }'
        ),
        
    }

@app.callback(
    Output(component_id='heatmap', component_property='figure'),
    [Input(component_id='column-selector', component_property='value')]
)
def update_heatmap(column):
    df_pivot = df.pivot_table(values=column, index='datetime', columns='name')
    return {
        'data': [
            go.Heatmap(
                x=df_pivot.columns,
                y=df_pivot.index,
                z=df_pivot.values,
                colorscale='Blues', #Viridis
            )
        ],
        'layout': go.Layout(
            xaxis={'title': 'Name','automargin': True},
            yaxis={'title': 'Date and Time','automargin': True},
            height= 600,
            margin={'l': 40, 't': 40, 'r': 40},
            hovermode='closest',
            title=f'Sentiment Heatmap by {column}'
        )
    }



if __name__ == '__main__':
    app.run_server()
