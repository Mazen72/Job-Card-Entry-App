# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input,Output,State
import database_tables
import pandas as pd
import dash_table
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from sqlalchemy.types import String
from fpdf import FPDF
from waitress import serve

server = Flask(__name__)
app = dash.Dash(
    __name__,server=server,
    meta_tags=[
        {
            'charset': 'utf-8',
        },
        {
            'name': 'viewport',
            'content': 'width=device-width, initial-scale=1, shrink-to-fit=no'
        }
    ] , external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server.config.update(
    SECRET_KEY=os.urandom(12),
    SQLALCHEMY_DATABASE_URI='sqlite:///job_card_data.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db = SQLAlchemy()

try:
    pd.read_sql_table('customer_details_table',con='sqlite:///job_card_data.db')
except:
    df1=pd.DataFrame(columns=['Job No','Abi Serial No','Customer Name','Customer Address','Customer Phone'])

    df1.to_sql('customer_details_table',con='sqlite:///job_card_data.db',index=False,if_exists='replace',dtype={"Job No": String(20)})

try:
    pd.read_sql_table('pump_details_table',con='sqlite:///job_card_data.db')
except:
    df2=pd.DataFrame(columns=['Job No','Customer Name','Abi Serial No','Pump Details','Size','Make','HP',
                                  'Pump Stages', 'Pump Type','Pump Phase', 'Impeller Model','Shaft Size', 'Shaft Height',
                                  'Coupling Type', 'NO of Middle DOL','Shaft Pressing', 'Casing Pressing','Play Height',
                                  'Hylam Type','Coupling To Hylam (mm)','Hylam To Impeller (mm)','Coupling To Impeller (mm)'])

    df2.to_sql('pump_details_table', con='sqlite:///job_card_data.db', index=False,if_exists='replace',dtype={"Job No": String(20)})


try:
    pd.read_sql_table('technical_details',con='sqlite:///job_card_data.db')
except:
    df3=pd.DataFrame(columns=['Job No','Pump Details','Size','Make','HP','Pump Stages',
                     'CL','Slots','Wire Size','Turns','Connection Type','Paper Size'])

    df3.to_sql('technical_details',con='sqlite:///job_card_data.db',index=False,if_exists='replace',dtype={"Job No": String(20)})

try:
    pd.read_sql_table('testting_details_table1',con='sqlite:///job_card_data.db')
except:
    df4=pd.DataFrame(columns=['Job No','Volt','O/Amps','Shut off Amps','RPM','Full Head(m)','Open Flow (lps)'])

    df4.to_sql('testting_details_table1',con='sqlite:///job_card_data.db',index=False,if_exists='replace',dtype={"Job No": String(20)})


try:
    pd.read_sql_table('testting_details_table2',con='sqlite:///job_card_data.db')
except:
    df4=pd.DataFrame(columns=['Job No','Volt','Amps','RPM','Head(m)','Flow(lps)'])

    df4.to_sql('testting_details_table2',con='sqlite:///job_card_data.db',index=False,if_exists='replace',dtype={"Job No": String(20)})



app.config.suppress_callback_exceptions = True

df_pmp=pd.read_sql_table('pump_details_table',con='sqlite:///job_card_data.db')
df_tech=pd.read_sql_table('technical_details',con='sqlite:///job_card_data.db')

header_text=html.Div('Job Card Entry App',style=dict(color='black',
                     fontWeight='bold',fontSize='3vh'))
db_header_text=  dbc.Col([ header_text] ,
        xs=dict(size=10,offset=2), sm=dict(size=10,offset=2),
        md=dict(size=6,offset=0), lg=dict(size=3,offset=5), xl=dict(size=3,offset=5))
navigation_header=dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Add/View Job Card", active='exact', href="/add_card",id='add_card',
                                style=dict(fontSize='1.8vh'))),
        dbc.NavItem(dbc.NavLink("View Database Tables", href="/view_database",active='exact',id='view_database',
                                style=dict(fontSize='1.8vh')))
    ],
    pills=True,
)
db_navigation_header=dbc.Col([navigation_header],
                             xs=dict(size=12, offset=0), sm=dict(size=12, offset=0),
                             md=dict(size=12, offset=0), lg=dict(size=12, offset=0), xl=dict(size=12, offset=0)
                             )

job_number_text=html.H1('Job Number: ',
                           style=dict(fontSize='3.5vh',fontWeight='bold',color='#1e90ff',textAlign='center'))

job_number_input=dbc.Input(
    placeholder='Enter Job Number',
    n_submit=0,
    type='text',
    id='job_number_input', size="lg",autocomplete='off'
)

customer_details=html.H1('Customer Details',
                           style=dict(fontSize='3.5vh',fontWeight='bold',color='#1e90ff',textAlign='center'))

customer_name_text=html.H1('Customer Name',
                           style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

customer_name_input=dbc.Input( placeholder='Enter Customer Name', n_submit=0,
                         type='text', id='customer_name_input', size="lg",autocomplete='off'
)

customer_phone_text=html.H1('Customer Phone',
                           style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

customer_phone_input=dbc.Input( placeholder='Enter Customer Phone', n_submit=0,
                         type='text', id='customer_phone_input', size="lg",autocomplete='off'
)

customer_address_text=html.H1('Customer Address',
                           style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

customer_address_input=dbc.Input( placeholder='Enter Customer Phone', n_submit=0,
                         type='text', id='customer_address_input', size="lg",autocomplete='off'
)

pump_details=html.H1('Pump/Motor Details',
                           style=dict(fontSize='3.5vh',fontWeight='bold',color='#1e90ff',textAlign='center'))

abi_serial_text=html.H1('Abi Serial No.', style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

abi_serial_input=dbc.Input( placeholder='Enter Serial No.', n_submit=0,
                         type='text', id='abi_serial_input', size="lg",autocomplete='off'
)


pump_size_text=html.H1('Size', style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

pump_size_suggestions= list(df_pmp['Size'])
pump_size_list=html.Datalist(
    id='pump_size_suggestions',
    children=[html.Option(value=word) for word in pump_size_suggestions])

pump_size_input=dbc.Input( placeholder='Enter Size', n_submit=0,list='pump_size_suggestions',
                         type='text', id='pump_size_input', size="lg",autocomplete='off'
)

pump_vendor_text=html.H1('Make', style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

pump_vendor_input=dbc.Input( placeholder='Enter Make ', n_submit=0,
                         type='text', id='pump_vendor_input', size="lg",autocomplete='off'
)

pump_hp_text=html.H1('HP', style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

pump_hp_input=dbc.Input( placeholder='Enter HP', n_submit=0,
                         type='text', id='pump_hp_input', size="lg",autocomplete='off'
)


pump_type_text=html.H1('Pump Type', style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

pump_type_suggestions= list(df_pmp['Pump Type'])
pump_type_list=html.Datalist(
    id='pump_type_suggestions',
    children=[html.Option(value=word) for word in pump_type_suggestions])

pump_type_input=dbc.Input( placeholder='Enter Pump Type', n_submit=0,list='pump_type_suggestions',
                         type='text', id='pump_type_input', size="lg",autocomplete='off'
)


pump_phase_text=html.H1('Pump Phase', style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

pump_phase_suggestions= ['Single','Three']
pump_phase_list=html.Datalist(
    id='pump_phase_suggestions',
    children=[html.Option(value=word) for word in pump_phase_suggestions])

pump_phase_input=dbc.Input( placeholder='Enter Pump Phase ', n_submit=0,list='pump_phase_suggestions',
                         type='text', id='pump_phase_input', size="lg",autocomplete='off'
)

pump_stages_text=html.H1('Pump Stages', style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

pump_stages_input=dbc.Input( placeholder='Enter Pump Stages', n_submit=0,
                         type='text', id='pump_stages_input', size="lg",autocomplete='off'
)

impeller_model_text=html.H1('Impeller Model', style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))


impeller_model_suggestions= list(df_pmp['Impeller Model'])
impeller_model_list=html.Datalist(
    id='impeller_model_suggestions',
    children=[html.Option(value=word) for word in impeller_model_suggestions])

impeller_model_input=dbc.Input( placeholder='Enter Impeller Model', n_submit=0,list='impeller_model_suggestions' ,
                         type='text', id='impeller_model_input', size="lg",autocomplete='off'
)

shaft_size_text=html.H1('Shaft Size', style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

shaft_size_input=dbc.Input( placeholder='Enter Shaft Size', n_submit=0,
                         type='text', id='shaft_size_input', size="lg",autocomplete='off'
)

shaft_height_text=html.H1('Shaft Height', style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

shaft_height_input=dbc.Input( placeholder='Enter Shaft Height ', n_submit=0,
                         type='text', id='shaft_height_input', size="lg",autocomplete='off'
)

coupling_type_text=html.H1('Coupling Type', style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

coupling_type_input=dbc.Input( placeholder='Enter Coupling Type', n_submit=0,
                         type='text', id='coupling_type_input', size="lg",autocomplete='off'
)


middle_dol_text=html.H1('Middle DOL NO.', style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

middle_dol_input=dbc.Input( placeholder='Enter Middle DOL NO.', n_submit=0,
                         type='text', id='middle_dol_input', size="lg",autocomplete='off'
)

shaft_pressing_text=html.H1('Shaft Pressing', style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

shaft_pressing_input=dbc.Input( placeholder='Enter Shaft Pressing', n_submit=0,
                         type='text', id='shaft_pressing_input', size="lg",autocomplete='off'
)

casing_pressing_text=html.H1('Casing Pressing', style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

casing_pressing_input=dbc.Input( placeholder='Enter Casing Pressing', n_submit=0,
                         type='text', id='casing_pressing_input', size="lg",autocomplete='off'
)


play_height_text=html.H1('Play Height', style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

play_height_input=dbc.Input( placeholder='Enter Play Height', n_submit=0,
                         type='text', id='play_height_input', size="lg",autocomplete='off'
)

hylam_type_text=html.H1('Hylam Type', style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

hylam_type_suggestions= list(df_pmp['Hylam Type'])
hylam_type_list=html.Datalist(
    id='hylam_type_suggestions',
    children=[html.Option(value=word) for word in hylam_type_suggestions])

hylam_type_input=dbc.Input( placeholder='Enter Hylam Type', n_submit=0,list= 'hylam_type_suggestions',
                         type='text', id='hylam_type_input', size="lg",autocomplete='off'
)

coupling_to_hylam_text=html.H1('Coupling To Hylam Height (mm)', style=dict(fontSize='2.5vh',fontWeight='bold',color='black',textAlign='center'))

coupling_to_hylam_input=dbc.Input( placeholder='Enter value in (mm)', n_submit=0,
                         type='text', id='coupling_to_hylam_input', size="lg",autocomplete='off'
)

hylam_to_impeller_text=html.H1('Hylam To Impeller Height (mm)', style=dict(fontSize='2.5vh',fontWeight='bold',color='black',textAlign='center'))

hylam_to_impeller_input=dbc.Input( placeholder='Enter Hylam To Impeller Height (mm)', n_submit=0,
                         type='text', id='hylam_to_impeller_input', size="lg",autocomplete='off'
)

coupling_to_impeller_text=html.H1('Coupling To Impeller (mm)', style=dict(fontSize='2.5vh',fontWeight='bold',color='black',textAlign='center'))

coupling_to_impeller_input=dbc.Input( placeholder='Enter Coupling To Impeller (mm)', n_submit=0,
                         type='text', id='coupling_to_impeller_input', size="lg",autocomplete='off'
)





technical_details=html.H1('Technical Details',
                           style=dict(fontSize='3.5vh',fontWeight='bold',color='#1e90ff',textAlign='center'))

cl_text=html.H1('CL', style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

cl_input=dbc.Input( placeholder='Enter CL ', n_submit=0,
                         type='text', id='cl_input', size="lg",autocomplete='off'
)

slots_text=html.H1('Slots',style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

slots_type_suggestions= list(df_tech['Slots'])
slot_type_list=html.Datalist(
    id='slot_type_suggestions',
    children=[html.Option(value=word) for word in slots_type_suggestions])

slots_input=dbc.Input( placeholder='Enter Slots number', n_submit=0,list='slot_type_suggestions' ,
                         type='text', id='slots_input', size="lg",autocomplete='off'
)

wire_size_text=html.H1('Wire Size',
                           style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

wire_size_input=dbc.Input( placeholder='Enter Wire Size', n_submit=0,
                         type='text', id='wire_size_input', size="lg",autocomplete='off'
)

turns_text=html.H1('Turns',style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

turns_input=dbc.Input( placeholder='Enter Turns Number', n_submit=0,
                         type='text', id='turns_input', size="lg",autocomplete='off'
)

connection_text=html.H1('Connection Type',style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

connection_type_suggestions= ['Star','Delta','Star/Delta']
connection_type_list=html.Datalist(
    id='connection_type_suggestions',
    children=[html.Option(value=word) for word in connection_type_suggestions])

connection_input=dbc.Input( placeholder='Enter Connection Type', n_submit=0,list= 'connection_type_suggestions',
                         type='text', id='connection_input', size="lg",autocomplete='off'
)

paper_size_text=html.H1('Paper Size',style=dict(fontSize='3vh',fontWeight='bold',color='black',textAlign='center'))

paper_size_input=dbc.Input( placeholder='Enter Paper Size', n_submit=0,
                         type='text', id='paper_size_input', size="lg",autocomplete='off'
)

testing_details=html.H1('Testing Details',
                           style=dict(fontSize='4vh',fontWeight='bold',color='#1e90ff',textAlign='center'))

testing_data = {'Volt':['','',''], 'O/Amps':['','',''],'Shut off Amps':['','',''],
                      'RPM':['','',''],'Full Head(m)':['','',''],'Open Flow (lps)':['','','']}

testing_df=pd.DataFrame(testing_data)

testing_table=html.Div([dash_table.DataTable(
            columns = [
                {
                    'name': str(x),
                    'id': str(x),
                    'deletable': False,
                } for x in testing_df.columns
             ],id='testing_table',
          data=testing_df.to_dict('records'),    page_size=50
    ,style_cell=dict(textAlign= 'center', border= '2px solid black'
    ,backgroundColor= 'white',color='black',fontSize='2vh',fontWeight='bold'),
    style_header=dict(backgroundColor= '#00bfff',
        fontWeight= 'bold', border= '1px solid black',fontSize='2vh'),
            editable=True,
            row_deletable=True,

            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_action='none',  # render all of the data at once. No paging.
            style_table={'height': '100%', 'overflowY': 'auto','overflowX':'auto'}

)
            ]
    ,id='testing_table_df')

add_testing_case=dbc.Button("Add Testing Case", color="primary", size='lg', n_clicks=0,id="add_testing_case"
                            ,style=dict(fontSize='1.8vh')
                            )

testing_data2 = {'Volt':['','',''], 'Amps':['','',''],'RPM':['','',''],'Head(m)':['','',''],'Flow(lps)':['','','']}
testing_df2=pd.DataFrame(testing_data2)

testing_table2=html.Div([dash_table.DataTable(
            columns = [
                {
                    'name': str(x),
                    'id': str(x),
                    'deletable': False
                } for x in testing_df2.columns
             ],id='testing_table2',
          data=testing_df2.to_dict('records'),    page_size=50
    ,style_cell=dict(textAlign= 'center', border= '2px solid black'
    ,backgroundColor= 'white',color='black',fontSize='2vh',fontWeight='bold'),
    style_header=dict(backgroundColor= '#00bfff',
        fontWeight= 'bold', border= '1px solid black',fontSize='2vh'),
            editable=True,
            row_deletable=True,

            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_action='none',  # render all of the data at once. No paging.
            style_table={'height': '100%', 'overflowY': 'auto','overflowX':'auto'}

)
            ]
    ,id='testing_table_df2')



submit_job_card=dbc.Button("Submit Job Card", color="primary", size='lg', n_clicks=0,id="submit_job_card"
                            ,style=dict(fontSize='1.8vh')
                            )

submit_card_msg=html.Div([''],id='confirm_msg',style=dict(fontSize='1.8vh',color='#1e90ff',fontWeight='bold') )


view_card_msg=html.Div([''],id='view_card_msg',style=dict(fontSize='1.8vh',color='#1e90ff',fontWeight='bold') )

add_testing_case2=dbc.Button("Add Testing Case", color="primary", size='lg', n_clicks=0,id="add_testing_case2"
                            ,style=dict(fontSize='1.8vh')
                            )
view_job_card=dbc.Button("View Card", color="primary", size='lg', n_clicks=0,id="view_job_card"
                            ,style=dict(fontSize='1.8vh')
                            )

clear_job_card1=dbc.Button("Clear Data", color="primary", size='lg', n_clicks=0,id="clear_data1"
                            ,style=dict(fontSize='1.8vh')
                            )

clear_job_card2=dbc.Button("Clear Data", color="primary", size='lg', n_clicks=0,id="clear_data2"
                            ,style=dict(fontSize='1.8vh')
                            )

pdf_input=dbc.Input( placeholder='Enter Job No', n_submit=0,
                         type='text', id='pdf_input', size="lg",autocomplete='off'
)

download_pdf=dbc.Button("Download To PDF", color="primary", size='lg', n_clicks=0,id="download_pdf"
                            ,style=dict(fontSize='1.8vh')
                            )

pdf_msg=html.Div([''],id='pdf_msg',style=dict(fontSize='1.8vh',color='#1e90ff',fontWeight='bold') )

add_card_layout= html.Div([
                   dbc.Row([dbc.Col([ job_number_text,job_number_input]
                    ,xl=dict(size=2,offset=2),lg=dict(size=2,offset=1),
                    md=dict(size=3,offset=1),sm=dict(size=10,offset=1),xs=dict(size=10,offset=1) ),

                            dbc.Col([view_card_msg]
                    ,xl=dict(size=3,offset=0),lg=dict(size=3,offset=0),
                    md=dict(size=3,offset=0),sm=dict(size=10,offset=1),xs=dict(size=10,offset=1) ),

                            dbc.Col([pdf_input,html.Br(), download_pdf,pdf_msg]
                    ,xl=dict(size=2, offset=1), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1))

                            ]),html.Br(),

                    dbc.Row([dbc.Col([view_job_card]
                     ,xl=dict(size=1, offset=2), lg=dict(size=1, offset=2),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1)),

                    dbc.Col([clear_job_card1]
                     ,xl=dict(size=3, offset=0), lg=dict(size=3, offset=0),
                      md=dict(size=3, offset=0), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1))
                             ]), html.Br(),

                   dbc.Row([dbc.Col([customer_details]
                    ,xl=dict(size=4, offset=4), lg=dict(size=4, offset=4),
                    md=dict(size=3, offset=1), sm=dict(size=10, offset=1),
                    xs=dict(size=10, offset=1))]),  html.Br(),

                   dbc.Row( [ dbc.Col([ customer_name_text,customer_name_input]
                    ,xl=dict(size=2,offset=2),lg=dict(size=2,offset=1),
                    md=dict(size=3,offset=1),sm=dict(size=10,offset=1),xs=dict(size=10,offset=1) ),

                    dbc.Col([customer_phone_text, customer_phone_input]
                     ,xl=dict(size=2, offset=1), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1)),

                    dbc.Col([customer_address_text, customer_address_input]
                    ,xl=dict(size=2, offset=1), lg=dict(size=2, offset=1),
                    md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1))

                              ]), html.Br(),

                   dbc.Row([dbc.Col([pump_details]
                     , xl=dict(size=4, offset=4), lg=dict(size=4, offset=4),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1),
                     xs=dict(size=10, offset=1))]), html.Br(),

                   dbc.Row([dbc.Col([abi_serial_text, abi_serial_input]
                     , xl=dict(size=2, offset=2), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1)),

                   dbc.Col([pump_size_text, pump_size_input,pump_size_list]
                     , xl=dict(size=2, offset=1), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1)),

                   dbc.Col([pump_vendor_text, pump_vendor_input]
                     , xl=dict(size=2, offset=1), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1))

                 ]), html.Br(),

                   dbc.Row([dbc.Col([pump_hp_text, pump_hp_input]
                     , xl=dict(size=2, offset=2), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1)),

                   dbc.Col([pump_stages_text, pump_stages_input]
                     , xl=dict(size=2, offset=1), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1)),

                   dbc.Col([pump_type_text, pump_type_input,pump_type_list]
                     , xl=dict(size=2, offset=1), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1))

                  ]), html.Br(),

                   dbc.Row([dbc.Col([pump_phase_text, pump_phase_input,pump_phase_list]
                     , xl=dict(size=2, offset=2), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1)),

                   dbc.Col([impeller_model_text, impeller_model_input,impeller_model_list]
                     , xl=dict(size=2, offset=1), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1)),

                   dbc.Col([shaft_size_text, shaft_size_input]
                     , xl=dict(size=2, offset=1), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1))

                  ]), html.Br(),

                   dbc.Row([dbc.Col([shaft_height_text, shaft_height_input]
                     , xl=dict(size=2, offset=2), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1)),

                   dbc.Col([coupling_type_text, coupling_type_input]
                     , xl=dict(size=2, offset=1), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1)),

                   dbc.Col([middle_dol_text, middle_dol_input]
                     , xl=dict(size=2, offset=1), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1))

                  ]), html.Br(),

                   dbc.Row([dbc.Col([shaft_pressing_text, shaft_pressing_input]
                     , xl=dict(size=2, offset=2), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1)),

                   dbc.Col([casing_pressing_text, casing_pressing_input]
                     , xl=dict(size=2, offset=1), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1)),

                   dbc.Col([play_height_text, play_height_input]
                     , xl=dict(size=2, offset=1), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1))

                  ]), html.Br(),

                  dbc.Row([dbc.Col([coupling_to_impeller_text, coupling_to_impeller_input]
                     , xl=dict(size=2, offset=2), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1)),

                  dbc.Col([coupling_to_hylam_text, coupling_to_hylam_input]
                     , xl=dict(size=2, offset=1), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1)),

                  dbc.Col([hylam_to_impeller_text, hylam_to_impeller_input]
                     , xl=dict(size=2, offset=1), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1))

                  ]), html.Br(),

                  dbc.Row([dbc.Col([hylam_type_text, hylam_type_input,hylam_type_list]
                     , xl=dict(size=2, offset=2), lg=dict(size=2, offset=1),
                     md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1))]),html.Br(),

                   dbc.Row([dbc.Col([technical_details]
                                    , xl=dict(size=4, offset=4), lg=dict(size=4, offset=4),
                                    md=dict(size=3, offset=1), sm=dict(size=10, offset=1),
                                    xs=dict(size=10, offset=1))]), html.Br(),

                   dbc.Row([dbc.Col([cl_text, cl_input]
                                    , xl=dict(size=2, offset=2), lg=dict(size=2, offset=1),
                                    md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1)),

                            dbc.Col([slots_text, slots_input,slot_type_list]
                                    , xl=dict(size=2, offset=1), lg=dict(size=2, offset=1),
                                    md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1)),

                            dbc.Col([wire_size_text, wire_size_input]
                                    , xl=dict(size=2, offset=1), lg=dict(size=2, offset=1),
                                    md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1))

                            ]),html.Br(),
                   dbc.Row([dbc.Col([turns_text, turns_input]
                                    , xl=dict(size=2, offset=2), lg=dict(size=2, offset=1),
                                    md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1)),

                            dbc.Col([connection_text, connection_input,connection_type_list]
                                    , xl=dict(size=2, offset=1), lg=dict(size=2, offset=1),
                                    md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1)),

                            dbc.Col([paper_size_text, paper_size_input]
                                    , xl=dict(size=2, offset=1), lg=dict(size=2, offset=1),
                                    md=dict(size=3, offset=1), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1))
                            ]),html.Br(),

                  dbc.Row([dbc.Col([testing_details,html.Br(),testing_table]
                                    ,xl=dict(size=8, offset=2), lg=dict(size=8, offset=2),
                                     md=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                                     xs=dict(size=10, offset=1))]), html.Br(),

                  dbc.Row([dbc.Col([add_testing_case]
                                   ,xl=dict(size=3, offset=2), lg=dict(size=3, offset=2),
                                    md=dict(size=5, offset=1), sm=dict(size=8, offset=2),
                                    xs=dict(size=8, offset=2))]), html.Br(),

                  dbc.Row([dbc.Col([html.Br(), testing_table2]
                                  ,xl=dict(size=8, offset=2), lg=dict(size=8, offset=2),
                                   md=dict(size=10, offset=1), sm=dict(size=10, offset=1),
                                   xs=dict(size=10, offset=1))]), html.Br(),

                  dbc.Row([dbc.Col([add_testing_case2]
                                  ,xl=dict(size=3, offset=2), lg=dict(size=3, offset=2),
                                   md=dict(size=5, offset=1), sm=dict(size=8, offset=2),
                                   xs=dict(size=8, offset=2))]), html.Br(),

                  dbc.Row([dbc.Col([submit_job_card]
                                   ,xl=dict(size=2, offset=2), lg=dict(size=2, offset=2),
                                   md=dict(size=5, offset=1), sm=dict(size=8, offset=2),
                                   xs=dict(size=8, offset=2)),
                           dbc.Col([clear_job_card2]
                                   ,xl=dict(size=2, offset=0), lg=dict(size=3, offset=0),
                                   md=dict(size=3, offset=0), sm=dict(size=10, offset=1), xs=dict(size=10, offset=1)),
                           dbc.Col([submit_card_msg]
                                   ,xl=dict(size=3, offset=0), lg=dict(size=3, offset=0),
                                   md=dict(size=5, offset=1), sm=dict(size=8, offset=2),
                                   xs=dict(size=8, offset=2))

                           ]), html.Br(),

                #  dbc.Row([]), html.Br(),


    ])
app.layout=html.Div([dbc.Row([ db_header_text] ,style=dict(backgroundColor='#00bfff'),id='header' ),
                     dbc.Row([  html.Br(),db_navigation_header]),html.Br(),
                     html.Div(id='page-content'),
                     dcc.Location(id='url', refresh=True,pathname='/add_card') ,
                     html.Div([''],id='hidden_div1',style=dict(display='none'))
    ]
)


@app.callback(Output('pdf_msg', 'children'),
             [Input('download_pdf', 'n_clicks'),Input('clear_data1', 'n_clicks'),Input('clear_data2', 'n_clicks')],
              State('pdf_input','value')

,prevent_initial_call=True
)
def download_pdf(download_pdf,c1,c2,pdf_input):
    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == 'clear_data1' or button_id == 'clear_data2':
            return ''


    customer_df = pd.read_sql_table('customer_details_table', con='sqlite:///job_card_data.db')
    pump_df = pd.read_sql_table('pump_details_table', con='sqlite:///job_card_data.db')
    testing_df = pd.read_sql_table('testting_details_table1', con='sqlite:///job_card_data.db')
    technical_df = pd.read_sql_table('technical_details', con='sqlite:///job_card_data.db')
    testing_df2 = pd.read_sql_table('testting_details_table2', con='sqlite:///job_card_data.db')

    if pdf_input == None:
        return 'please enter job number'

    elif pdf_input not in customer_df['Job No'].values:
        return 'job number you entered doesnt exist'

    elif pdf_input in customer_df['Job No'].values:


        # Create instance of FPDF class
        # Letter size paper, use inches as unit of measure
        pdf = FPDF(format='letter', unit='in')

        # Add new page. Without this you cannot create the document.
        pdf.add_page()

        # Remember to always put one of these at least once.
        pdf.set_font('Times', '', 10.0)

        # Effective page width, or just epw
        epw = pdf.w - 1 * pdf.l_margin

        # Set column width to 1/4 of effective page width to distribute content
        # evenly across table and page
        col_width = epw / 5
        filtered_customer_df=customer_df[customer_df['Job No']==str(pdf_input)]
        filtered_pump_df = pump_df[pump_df['Job No'] == str(pdf_input)]
        filtered_technical_df = technical_df[technical_df['Job No'] == str(pdf_input)]
        filtered_testing_df = testing_df[testing_df['Job No'] == str(pdf_input)]
        filtered_testing2_df = testing_df2[testing_df2['Job No'] == str(pdf_input)]

        data = [list(filtered_customer_df.columns),
                filtered_customer_df.values.tolist()[0],

                ]

        pdf.set_font('Times', 'B', 12.0)
        pdf.cell(epw, 0.0, 'Customer Details', align='C')
        pdf.set_font('Times', '', 10.0)
        pdf.ln(0.5)
        th = pdf.font_size
        for row in data:
            for datum in row:
                # Enter data in colums
                pdf.cell(col_width, 2 * th, str(datum), border=1)

            pdf.ln(2 * th)

        pdf.ln(4 * th)

        data = [list(filtered_pump_df.iloc[:,2:7].columns),
                filtered_pump_df.iloc[:,2:7].values.tolist()[0],
                list(filtered_pump_df.iloc[:, 7:12].columns),
                filtered_pump_df.iloc[:, 7:12].values.tolist()[0],
                list(filtered_pump_df.iloc[:, 12:17].columns),
                filtered_pump_df.iloc[:, 12:17].values.tolist()[0],
                list(filtered_pump_df.iloc[:, 17:22].columns),
                filtered_pump_df.iloc[:, 17:22].values.tolist()[0]
                ]

        pdf.set_font('Times', 'B', 14.0)
        pdf.cell(epw, 0.0, 'Pump Details', align='C')
        pdf.set_font('Times', '', 10.0)
        pdf.ln(0.5)

        for row in data:
            for datum in row:
                # Enter data in colums
                pdf.cell(col_width, 2 * th, str(datum), border=1)

            pdf.ln(2 * th)

        pdf.ln(4 * th)

        data = [list(filtered_technical_df.iloc[:,2:7].columns),
                filtered_technical_df.iloc[:,2:7].values.tolist()[0],
                list(filtered_technical_df.iloc[:, 7:12].columns),
                filtered_technical_df.iloc[:, 7:12].values.tolist()[0],

                ]

        pdf.set_font('Times', 'B', 14.0)
        pdf.cell(epw, 0.0, 'Technical Details', align='C')
        pdf.set_font('Times', '', 10.0)
        pdf.ln(0.5)

        for row in data:
            for datum in row:
                # Enter data in colums
                pdf.cell(col_width, 2 * th, str(datum), border=1)

            pdf.ln(2 * th)



        pdf.ln(4 * th)

        data = [list(filtered_testing_df.iloc[:,1:7].columns),
                filtered_testing_df.iloc[:,1:7].values.tolist()[0],

                ]

        pdf.set_font('Times', 'B', 14.0)
        pdf.cell(epw, 0.0, 'Testing Details 1', align='C')
        pdf.set_font('Times', '', 10.0)
        pdf.ln(0.5)

        for row in data:
            for datum in row:
                # Enter data in colums
                pdf.cell(epw / 6, 2 * th, str(datum), border=1)

            pdf.ln(2 * th)

        pdf.ln(4 * th)

        data = [list(filtered_testing2_df.iloc[:,1:6].columns),
                filtered_testing2_df.iloc[:,1:6].values.tolist()[0],
                ]

        pdf.set_font('Times', 'B', 14.0)
        pdf.cell(epw, 0.0, 'Testing Details 2', align='C')
        pdf.set_font('Times', '', 10.0)
        pdf.ln(0.5)

        for row in data:
            for datum in row:
                # Enter data in colums
                pdf.cell(col_width, 2 * th, str(datum), border=1)

            pdf.ln(2 * th)

        pdf.output('Job {}.pdf'.format(pdf_input), 'F')
        return 'Downloaded'



@app.callback(Output('job_number_input', 'value'),
             [Input('clear_data1', 'n_clicks'),Input('clear_data2', 'n_clicks'),Input('url', 'pathname')]
)
def generate_job_no(c1,c2,pathname):
    customer_df = pd.read_sql_table('customer_details_table', con='sqlite:///job_card_data.db')

    if customer_df.shape[0]==0:
        return '1'

    else:
        last_job = customer_df['Job No'].values[-1]
        return '{}'.format(int(last_job)+1)

@app.callback([Output('view_card_msg', 'children'),Output('customer_name_input', 'value'),Output('customer_address_input', 'value')
              ,Output('customer_phone_input', 'value'),
               Output('abi_serial_input', 'value'),Output('pump_size_input', 'value'),Output('pump_vendor_input', 'value'),
               Output('pump_hp_input', 'value'),Output('pump_stages_input', 'value'),Output('pump_type_input', 'value'),
               Output('pump_phase_input', 'value'),Output('impeller_model_input', 'value'),Output('shaft_size_input', 'value'),
               Output('shaft_height_input', 'value'),Output('coupling_type_input', 'value'),Output('middle_dol_input', 'value'),
               Output('shaft_pressing_input', 'value'),Output('casing_pressing_input', 'value'),Output('play_height_input', 'value'),
               Output('hylam_type_input', 'value'),Output('coupling_to_impeller_input', 'value'),Output('coupling_to_hylam_input', 'value'),
               Output('hylam_to_impeller_input', 'value'),Output('cl_input', 'value'),Output('slots_input', 'value'),
               Output('wire_size_input', 'value'),Output('turns_input', 'value'),Output('connection_input', 'value'),
               Output('paper_size_input', 'value')

                ],Input('view_job_card', 'n_clicks'),Input('clear_data1', 'n_clicks'),Input('clear_data2', 'n_clicks'),

              State('job_number_input', 'value'),

prevent_initial_call=True)

def view_job_card(n_clicks,c1,c2,job_number_input):
    customer_df=pd.read_sql_table('customer_details_table',con='sqlite:///job_card_data.db')
    pump_df=pd.read_sql_table('pump_details_table',con='sqlite:///job_card_data.db')
    technical_df =pd.read_sql_table('technical_details',con='sqlite:///job_card_data.db')
    ctx = dash.callback_context
    if ctx.triggered:
      button_id = ctx.triggered[0]['prop_id'].split('.')[0]
      if button_id == 'view_job_card':

        if job_number_input==None:
            return ('please enter job number',dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,
               dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,
               dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,
               dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,
               dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,
               dash.no_update,dash.no_update,dash.no_update)

        elif job_number_input in customer_df['Job No'].values:
            return ('',customer_df[customer_df['Job No']==job_number_input]['Customer Name'].values[0],
                customer_df[customer_df['Job No']==job_number_input]['Customer Address'].values[0],
                customer_df[customer_df['Job No']==job_number_input]['Customer Phone'].values[0],
                pump_df[customer_df['Job No'] == job_number_input]['Abi Serial No'].values[0],
                pump_df[customer_df['Job No'] == job_number_input]['Size'].values[0],
                pump_df[customer_df['Job No'] == job_number_input]['Make'].values[0],
                pump_df[customer_df['Job No'] == job_number_input]['HP'].values[0],
                pump_df[customer_df['Job No'] == job_number_input]['Pump Stages'].values[0],
                pump_df[customer_df['Job No'] == job_number_input]['Pump Type'].values[0],
                pump_df[customer_df['Job No'] == job_number_input]['Pump Phase'].values[0],
                pump_df[customer_df['Job No'] == job_number_input]['Impeller Model'].values[0],
                pump_df[customer_df['Job No'] == job_number_input]['Shaft Size'].values[0],
                pump_df[customer_df['Job No'] == job_number_input]['Shaft Height'].values[0],
                pump_df[customer_df['Job No'] == job_number_input]['Coupling Type'].values[0],
                pump_df[customer_df['Job No'] == job_number_input]['NO of Middle DOL'].values[0],
                pump_df[customer_df['Job No'] == job_number_input]['Shaft Pressing'].values[0],
                pump_df[customer_df['Job No'] == job_number_input]['Casing Pressing'].values[0],
                pump_df[customer_df['Job No'] == job_number_input]['Play Height'].values[0],
                pump_df[customer_df['Job No'] == job_number_input]['Hylam Type'].values[0],
                pump_df[customer_df['Job No'] == job_number_input]['Coupling To Hylam (mm)'].values[0],
                pump_df[customer_df['Job No'] == job_number_input]['Hylam To Impeller (mm)'].values[0],
                pump_df[customer_df['Job No'] == job_number_input]['Coupling To Impeller (mm)'].values[0],
                technical_df[customer_df['Job No'] == job_number_input]['CL'].values[0],
                technical_df[customer_df['Job No'] == job_number_input]['Slots'].values[0],
                technical_df[customer_df['Job No'] == job_number_input]['Wire Size'].values[0],
                technical_df[customer_df['Job No'] == job_number_input]['Turns'].values[0],
                technical_df[customer_df['Job No'] == job_number_input]['Connection Type'].values[0],
                technical_df[customer_df['Job No'] == job_number_input]['Paper Size'].values[0]
                )

        elif job_number_input not in customer_df['Job No'].values:
            return ('job number you entered doesnt exist',dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,
               dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,
               dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,
               dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,
               dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,
               dash.no_update,dash.no_update,dash.no_update)
      else:
          return ('', '', '', '', '','','', '', '', '', '','', '', '', '', '',
                  '', '', '', '', '','', '', '', '', '','', '', '')


@app.callback(
    [Output('confirm_msg', 'children'),Output('connection_type_suggestions', 'children'),Output('pump_type_suggestions', 'children'),
     Output('pump_size_suggestions', 'children'),Output('hylam_type_suggestions', 'children'),
     Output('impeller_model_suggestions', 'children'),Output('slot_type_suggestions', 'children')],

    [Input('submit_job_card', 'n_clicks')],

    [State('job_number_input', 'value'),State('customer_name_input', 'value'),State('customer_address_input', 'value'),State('customer_phone_input', 'value'),
    State('abi_serial_input', 'value'),State('pump_size_input', 'value'),State('pump_vendor_input', 'value'),
    State('pump_hp_input', 'value'),State('pump_stages_input', 'value'),State('pump_type_input', 'value'),
    State('pump_phase_input', 'value'),State('impeller_model_input', 'value'),State('shaft_size_input', 'value'),
    State('shaft_height_input', 'value'),State('coupling_type_input', 'value'),State('middle_dol_input', 'value'),
    State('shaft_pressing_input', 'value'),State('casing_pressing_input', 'value'),State('play_height_input', 'value'),
    State('hylam_type_input', 'value'),State('coupling_to_impeller_input', 'value'),State('coupling_to_hylam_input', 'value'),
    State('hylam_to_impeller_input', 'value'),State('cl_input', 'value'),State('slots_input', 'value'),
    State('wire_size_input', 'value'),State('turns_input', 'value'),State('connection_input', 'value'),
    State('paper_size_input', 'value'),State('testing_table', 'data'),State('testing_table2', 'data')

     ],
    prevent_initial_call=True)
def add_job_card(submit_job_card, job_number_input, customer_name_input,customer_address_input,customer_phone_input,abi_serial_input,
                 pump_size_input,pump_vendor_input,pump_hp_input,pump_stages_input,pump_type_input,
                 pump_phase_input,impeller_model_input,shaft_size_input,shaft_height_input,coupling_type_input,
                 middle_dol_input,shaft_pressing_input,casing_pressing_input,play_height_input,hylam_type_input,coupling_to_impeller_input,
                 coupling_to_hylam_input,hylam_to_impeller_input,cl_input,slots_input,wire_size_input,
                 turns_input,connection_input,paper_size_input,testing_table_data,testing_table_data2):

    customer_df=pd.read_sql_table('customer_details_table',con='sqlite:///job_card_data.db')
    pump_df=pd.read_sql_table('pump_details_table',con='sqlite:///job_card_data.db')
    testing_df=pd.read_sql_table('testting_details_table1',con='sqlite:///job_card_data.db')
    technical_df =pd.read_sql_table('technical_details',con='sqlite:///job_card_data.db')
    testing_df2=pd.read_sql_table('testting_details_table2',con='sqlite:///job_card_data.db')



    if job_number_input==None:
        return ('please enter job number',dash.no_update,dash.no_update,dash.no_update,dash.no_update,
                dash.no_update,dash.no_update )
    elif job_number_input in customer_df['Job No'].values:

        return ('job number already exists in database',dash.no_update,dash.no_update,dash.no_update,dash.no_update,
                dash.no_update,dash.no_update )
    else:
        customer_new_df=pd.DataFrame(data=[[job_number_input,abi_serial_input, customer_name_input,customer_address_input,customer_phone_input]],
                                     columns=list(customer_df.columns))
        customer_df=customer_df.append(customer_new_df,ignore_index=True)
        customer_df.to_sql('customer_details_table',con='sqlite:///job_card_data.db',index=False,if_exists='replace')
        pump_model='{} {} {}/{}'.format(pump_size_input,pump_vendor_input,pump_hp_input,pump_stages_input)
        pump_new_df=pd.DataFrame(data=[[job_number_input, customer_name_input,abi_serial_input,pump_model,
                 pump_size_input,pump_vendor_input,pump_hp_input,pump_stages_input,pump_type_input,
                 pump_phase_input,impeller_model_input,shaft_size_input,shaft_height_input,coupling_type_input,
                 middle_dol_input,shaft_pressing_input,casing_pressing_input,play_height_input,hylam_type_input,coupling_to_impeller_input,
                 coupling_to_hylam_input,hylam_to_impeller_input]],
                                 columns=list(pump_df.columns))
        pump_df=pump_df.append(pump_new_df,ignore_index=True)
        pump_df.to_sql('pump_details_table',con='sqlite:///job_card_data.db',index=False,if_exists='replace')


        technical_new_df=pd.DataFrame(data=[[job_number_input,pump_model,pump_size_input,pump_vendor_input,pump_hp_input,
                                             pump_stages_input,cl_input,slots_input,wire_size_input,
                                             turns_input,connection_input,paper_size_input]],
                                      columns=list(technical_df.columns))
        technical_df=technical_df.append(technical_new_df,ignore_index=True)
        technical_df.to_sql('technical_details',con='sqlite:///job_card_data.db',index=False,if_exists='replace')


        for dic in testing_table_data:
            dic['Job No']='{}'.format(job_number_input)

        testing_new_df=pd.DataFrame(data=testing_table_data)
        testing_df=testing_df.append(testing_new_df,ignore_index=True)
        testing_df.to_sql('testting_details_table1',con='sqlite:///job_card_data.db',index=False,if_exists='replace')

        for dic in testing_table_data2:
            dic['Job No']='{}'.format(job_number_input)

        testing_new_df2=pd.DataFrame(data=testing_table_data2)
        testing_df2=testing_df2.append(testing_new_df2,ignore_index=True)
        testing_df2.to_sql('testting_details_table2',con='sqlite:///job_card_data.db',index=False,if_exists='replace')



        return (['job card added successfully'.format(job_number_input)],
                [html.Option(value=word) for word in list(technical_df['Connection Type'])],
                [html.Option(value=word) for word in list(pump_df['Pump Type'])],
                [html.Option(value=word) for word in list(pump_df['Size'])],
                [html.Option(value=word) for word in list(pump_df['Hylam Type'])],
                [html.Option(value=word) for word in list(pump_df['Impeller Model'])],
                [html.Option(value=word) for word in list(technical_df['Slots'])])




@app.callback(
    [Output('table_div', 'children'),Output('button_div', 'children'),Output('msg_div', 'children')],
    Input('tables_dropdown', 'value')
)
def update_output(table_name):
    if table_name == 'Customer Details':
        customer_details_df = pd.read_sql_table('customer_details_table',con='sqlite:///job_card_data.db')

        customer_details_table = html.Div([dash_table.DataTable(
            columns=[
                {
                    'name': str(x),
                    'id': str(x),
                    'deletable': False,
                } for x in customer_details_df.columns
            ], id='customer_details_table',
            data=customer_details_df.to_dict('records'), page_size=50
            , style_cell=dict(textAlign='center', border='2px solid black'
                              , backgroundColor='white', color='black', fontSize='1.8vh', fontWeight='bold'),
            style_header=dict(backgroundColor='#00bfff',
                              fontWeight='bold', border='1px solid black', fontSize='2vh'),
            editable=True,
            row_deletable=True,
            filter_action="native",
            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_action='none',  # render all of the data at once. No paging.
            style_table={'height': '100%', 'overflowY': 'auto', 'overflowX': 'auto'}

        )
        ]
            , id='customer_details_table_div')
        return (customer_details_table,database_tables.save_to_customer,database_tables.save_msg1)

    elif table_name == 'Pump Details':
        pump_details_df = pd.read_sql_table('pump_details_table',con='sqlite:///job_card_data.db')


        pump_details_table = html.Div([dash_table.DataTable(
            columns=[
                {
                    'name': str(x),
                    'id': str(x),
                    'deletable': False,
                } for x in pump_details_df.columns
            ], id='pump_details_table',
            data=pump_details_df.to_dict('records')
            , style_cell=dict(textAlign='center', border='2px solid black'
                              , backgroundColor='white', color='black', fontSize='1.8vh', fontWeight='bold'),
            style_header=dict(backgroundColor='#00bfff',
                              fontWeight='bold', border='1px solid black', fontSize='2vh'),
            editable=True,
            row_deletable=True,
            filter_action="native",
            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_action='none',  # render all of the data at once. No paging.
            style_table={'height': '100%', 'overflowY': 'auto', 'overflowX': 'auto'}

        )
        ]
            , id='pump_details_table_div')
        return (pump_details_table,database_tables.save_to_pump,database_tables.save_msg2)

    elif table_name == 'Testing Details 1':
        testing_details_df = pd.read_sql_table('testting_details_table1',con='sqlite:///job_card_data.db')


        testing_details_table = html.Div([dash_table.DataTable(
            columns=[
                {
                    'name': str(x),
                    'id': str(x),
                    'deletable': False,
                } for x in testing_details_df.columns
            ], id='testing_details_table',
            data=testing_details_df.to_dict('records'), page_size=50
            , style_cell=dict(textAlign='center', border='2px solid black'
                              , backgroundColor='white', color='black', fontSize='1.8vh', fontWeight='bold'),
            style_header=dict(backgroundColor='#00bfff',
                              fontWeight='bold', border='1px solid black', fontSize='1.8vh'),
            editable=True,
            row_deletable=True,
            filter_action="native",
            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_action='none',  # render all of the data at once. No paging.
            style_table={'height': '100%', 'overflowY': 'auto', 'overflowX': 'auto'}

        )
        ]
            , id='testing_details_table_div')

        return (testing_details_table,database_tables.save_to_testing,database_tables.save_msg3)

    elif table_name == 'Technical Details':
        technical_details_df = pd.read_sql_table('technical_details',con='sqlite:///job_card_data.db')

        technical_details_table = html.Div([dash_table.DataTable(
            columns=[
                {
                    'name': str(x),
                    'id': str(x),
                    'deletable': False,
                } for x in technical_details_df.columns
            ], id='technical_details_table',
            data=technical_details_df.to_dict('records'), page_size=50
            , style_cell=dict(textAlign='center', border='2px solid black'
                              , backgroundColor='white', color='black', fontSize='1.8vh', fontWeight='bold'),
            style_header=dict(backgroundColor='#00bfff',
                              fontWeight='bold', border='1px solid black', fontSize='2vh'),
            editable=True,
            row_deletable=True,
            filter_action="native",
            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_action='none',  # render all of the data at once. No paging.
            style_table={'height': '100%', 'overflowY': 'auto', 'overflowX': 'auto'}

        )
        ]
            , id='technical_details_table_div')
        return (technical_details_table, database_tables.save_to_technical, database_tables.save_msg4)

    elif table_name == 'Testing Details 2':
        testing_details_df2 = pd.read_sql_table('testting_details_table2', con='sqlite:///job_card_data.db')

        testing_details_table2 = html.Div([dash_table.DataTable(
            columns=[
                {
                    'name': str(x),
                    'id': str(x),
                    'deletable': False,
                } for x in testing_details_df2.columns
            ], id='testing_details_table2',
            data=testing_details_df2.to_dict('records'), page_size=50
            , style_cell=dict(textAlign='center', border='2px solid black'
                              , backgroundColor='white', color='black', fontSize='1.8vh', fontWeight='bold'),
            style_header=dict(backgroundColor='#00bfff',
                              fontWeight='bold', border='1px solid black', fontSize='1.8vh'),
            editable=True,
            row_deletable=True,
            filter_action="native",
            sort_action="native",  # give user capability to sort columns
            sort_mode="single",  # sort across 'multi' or 'single' columns
            page_action='none',  # render all of the data at once. No paging.
            style_table={'height': '100%', 'overflowY': 'auto', 'overflowX': 'auto'}

        )
        ]
            , id='testing_details_table_div2')

        return (testing_details_table2, database_tables.save_to_testing2, database_tables.save_msg5)


    #df3=pd.DataFrame(columns=['Job No','Pump Details','Size','Make','HP','Pump Stages',
      #               'CL','Slots','Wire Size','Turns','Connection Type','Paper Size'])

@app.callback(
    Output('save_msg1', 'children'),
    Input('save_to_customer', 'n_clicks'),
    State('customer_details_table', 'data'),
    prevent_initial_call=True)
def save_to_database1(clicks,data):
    if clicks>0:
        df = pd.DataFrame(data=data,columns=['Job No','Abi Serial No','Customer Name','Customer Address','Customer Phone'])
        df.to_sql('customer_details_table',con='sqlite:///job_card_data.db',index=False,if_exists='replace')
        return 'saved successfully to Database'
    else:
        return ['']

@app.callback(
    Output('save_msg2', 'children'),
    Input('save_to_pump', 'n_clicks'),
    State('pump_details_table', 'data'),
    prevent_initial_call=True)
def save_to_database2(clicks,data):
    if clicks>0:
        df = pd.DataFrame(data=data,columns=['Job No','Customer Name','Abi Serial No','Pump Details','Size','Make','HP',
                                  'Pump Stages', 'Pump Type','Pump Phase', 'Impeller Model','Shaft Size', 'Shaft Height',
                                  'Coupling Type', 'NO of Middle DOL','Shaft Pressing', 'Casing Pressing','Play Height',
                                  'Hylam Type','Coupling To Hylam (mm)','Hylam To Impeller (mm)','Coupling To Impeller (mm)'])
        df.to_sql('pump_details_table',con='sqlite:///job_card_data.db',index=False,if_exists='replace')

        return 'saved successfully to Database'
    else:
        return ['']

@app.callback(
    Output('save_msg4', 'children'),
    Input('save_to_technical', 'n_clicks'),
    State('technical_details_table', 'data'),
    prevent_initial_call=True)
def save_to_database3(clicks,data):
    if clicks>0:
        df = pd.DataFrame(data=data,columns=['Job No','Pump Details','Size','Make','HP','Pump Stages',
                                             'CL','Slots','Wire Size','Turns','Connection Type','Paper Size'])
        df.to_sql('technical_details',con='sqlite:///job_card_data.db',index=False,if_exists='replace')
        return 'saved successfully to Database'
    else:
        return ['']

@app.callback(
    Output('save_msg3', 'children'),
    Input('save_to_testing', 'n_clicks'),
    State('testing_details_table', 'data'),
    prevent_initial_call=True)
def save_to_database4(clicks,data):
    if clicks>0:
        df = pd.DataFrame(data=data,columns=['Job No','Volt','O/Amps','Shut off Amps','RPM','Full Head(m)','Open Flow (lps)'])
        df.to_sql('testting_details_table1',con='sqlite:///job_card_data.db',index=False,if_exists='replace')
        return 'saved successfully to Database'
    else:
        return ['']

@app.callback(
    Output('save_msg5', 'children'),
    Input('save_to_testing2', 'n_clicks'),
    State('testing_details_table2', 'data'),
    prevent_initial_call=True)
def save_to_database5(clicks,data):
    if clicks>0:
        df = pd.DataFrame(data=data,columns=['Job No','Volt','Amps','RPM','Head(m)','Flow(lps)'])
        df.to_sql('testting_details_table2',con='sqlite:///job_card_data.db',index=False,if_exists='replace')
        return 'saved successfully to Database'
    else:
        return ['']


@app.callback(
    Output('testing_table', 'data'),
    [Input('add_testing_case', 'n_clicks'),Input('view_job_card','n_clicks'),
     Input('clear_data1', 'n_clicks'),Input('clear_data2', 'n_clicks')],
    [State('testing_table', 'data'),
     State('testing_table', 'columns'),State('job_number_input', 'value')],
    prevent_initial_call=True)
def add_testing_case(n_clicks,n_clicks2,c1,c2 ,rows, columns,job_number_input):
    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id=='add_testing_case':
            rows.append({c['id']: '' for c in columns})
            return rows

        elif button_id=='view_job_card':
            df = pd.read_sql_table('testting_details_table1', con='sqlite:///job_card_data.db')
            df=df[df['Job No']==job_number_input]
            return df.to_dict('records')
        else:
            df= pd.DataFrame(columns=['Job No','Volt','O/Amps','Shut off Amps','RPM','Full Head(m)','Open Flow (lps)'])
            return df.to_dict('records')


@app.callback(
    Output('testing_table2', 'data'),
    [Input('add_testing_case2', 'n_clicks'),Input('view_job_card','n_clicks'),
     Input('clear_data1', 'n_clicks'),Input('clear_data2', 'n_clicks')],
    [State('testing_table2', 'data'),
     State('testing_table2', 'columns'),State('job_number_input', 'value')],
    prevent_initial_call=True)
def add_testing_case2(n_clicks,n_clicks2, c1,c2,rows, columns,job_number_input):
    ctx = dash.callback_context
    if ctx.triggered:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id=='add_testing_case2':
            rows.append({c['id']: '' for c in columns})
            return rows

        elif button_id=='view_job_card':
            df = pd.read_sql_table('testting_details_table2', con='sqlite:///job_card_data.db')
            df=df[df['Job No']==job_number_input]
            return df.to_dict('records')
        else:
            df = pd.DataFrame(columns=['Job No', 'Volt', 'Amps', 'RPM', 'Head(m)', 'Flow(lps)'])
            return df.to_dict('records')


@app.callback([Output('page-content', 'children')],
              [Input('url', 'pathname')])
def display_page(pathname):

    if pathname=='/add_card':
        return [add_card_layout]

    elif pathname=='/view_database':
        return [database_tables.layout]



if __name__ == '__main__':
    serve(app.run_server(port=8520,debug=True))

