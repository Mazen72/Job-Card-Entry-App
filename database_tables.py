import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_bootstrap_components as dbc




tables_menu=dcc.Dropdown(
        id='tables_dropdown',
        options=[
            dict(label='Customer Details', value='Customer Details'),
            dict(label='Pump Details', value='Pump Details'),
            dict(label='Technical Details', value='Technical Details'),
            dict(label='Testing Details 1', value='Testing Details 1'),
            dict(label='Testing Details 2', value='Testing Details 2'),
        ],
        value='Customer Details'
        , style=dict(color='black',fontWeight='bold')
    )

tables_menu_div= html.Div([tables_menu], style=dict( fontSize='2vh',border='0.5vh solid #00bfff'))

save_to_customer=dbc.Button("Save To Database", color="primary", size='lg', n_clicks=0,id="save_to_customer"
                            ,style=dict(fontSize='1.8vh')
                            )

save_to_pump=dbc.Button("Save To Database", color="primary", size='lg', n_clicks=0,id="save_to_pump"
                            ,style=dict(fontSize='1.8vh')
                            )

save_to_technical=dbc.Button("Save To Database", color="primary", size='lg', n_clicks=0,id="save_to_technical"
                            ,style=dict(fontSize='1.8vh')
                            )

save_to_testing=dbc.Button("Save To Database", color="primary", size='lg', n_clicks=0,id="save_to_testing"
                            ,style=dict(fontSize='1.8vh')
                            )
save_to_testing2=dbc.Button("Save To Database", color="primary", size='lg', n_clicks=0,id="save_to_testing2"
                            ,style=dict(fontSize='1.8vh')
                            )

save_msg1=html.Div([''],id='save_msg1',style=dict(fontSize='1.8vh',color='#1e90ff',fontWeight='bold') )
save_msg2=html.Div([''],id='save_msg2',style=dict(fontSize='1.8vh',color='#1e90ff',fontWeight='bold') )
save_msg3=html.Div([''],id='save_msg3',style=dict(fontSize='1.8vh',color='#1e90ff',fontWeight='bold') )
save_msg4=html.Div([''],id='save_msg4',style=dict(fontSize='1.8vh',color='#1e90ff',fontWeight='bold') )
save_msg5=html.Div([''],id='save_msg5',style=dict(fontSize='1.8vh',color='#1e90ff',fontWeight='bold') )


layout=html.Div([dbc.Row([dbc.Col([tables_menu_div]
                ,xl=dict(size=3, offset=0), lg=dict(size=3, offset=0),
                md=dict(size=3, offset=1), sm=dict(size=10, offset=1),
                xs=dict(size=10, offset=1))]), html.Br(),html.Div([],id='table_div'),
                html.Br(),html.Div([],id='button_div'),html.Br(),html.Div([],id='msg_div')

                   ])