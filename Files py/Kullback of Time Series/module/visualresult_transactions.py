import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import module.initial_process as initial

(axes_x, result) = initial.inicio()
print(axes_x)
app = dash.Dash()
app.layout = html.Div(children=[
    html.Div([
        dcc.Graph(
            id='data_value',
            figure={
'data': [
                go.Scatter(
                    x=list(range(0, len(result))),
                    y=result,
                    text=result,
                    mode='lines+markers',
                    name='real consume',
                    marker={
                        'size': 10,
                        'opacity': 0.5,
                        'color' : 'rgb(0, 0, 255)',
                        'line': {'width': 0.5, 'color': 'rgb(0, 0, 255)'}
                    })
            ],
            'layout': go.Layout(
                xaxis={
                    'title': 'Month',
                    'tickvals': ['as'],
                    'ticktext': axes_x
                },
                yaxis={
                    'title': '',
                    'type': 'linear'
                },
                margin={'l': 100, 'b': 100, 't': 50, 'r': 50},
                height=750,
                legend={'x': 0, 'y': 1},
                hovermode = 'closest'
            )
            })
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '0 0 0 0'})
])

if __name__ == '__main__':
    app.run_server(debug=True)