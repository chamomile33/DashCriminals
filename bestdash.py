
from dash import Dash, html, dcc,Input,Output
import dash
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
import numpy as np


colors = {
    'background': {'GreyTheme ':'#F5F5F5','BlueTheme':'#F0F8FF'},
    'text': {'GreyTheme ':'#324359','BlueTheme':'#004d00'},
    'header':{'GreyTheme ':'#191970','BlueTheme':'#004d00'}
}



df = pd.read_csv('crimedata.csv')
df = df.drop_duplicates()

column_name = {'Убийства':'murdPerPop','Насилие' : 'rapesPerPop','Нападение':'assaultPerPop'}
race = {'Europian':'racePctWhite','Asian':'racePctAsian','Afro-American':'racepctblack','Hispanic':'racePctHisp'}
div = {'Total divorced':'TotalPctDiv','Male divorced':'MalePctDivorce','Female divorced':'FemalePctDiv'}
div_people = {'Total divorced':'людей','Male divorced':'мужчин','Female divorced':'женщин'}
income = {'Capita income':'perCapInc','Household income':'medIncome', 'Family income':'medFamInc'}
income_name = {'Capita income':'душу населения','Household income':'домохозяйство', 'Family income':'семью'}
intervals = {'Убийства':[-1,5,15,35,max(df['murdPerPop'])],'Насилие' : [-1,25,40,120,max(df['rapesPerPop'])],'Нападение': [-1,70,200,600,max(df['assaultPerPop'])]}
column_name_group = {'Убийства':'murdPerPopGroup','Насилие' : 'rapesPerPopGroup','Нападение':'assaultPerPopGroup'}
for_traces = ['убийств','случаев насилия','нападений и хулиганств']
crimes = ['Убийства', 'Насилие', 'Нападение']


app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = dbc.Container([
        dbc.Row([
            dbc.Col(dcc.Dropdown(['Убийства', 'Насилие', 'Нападение'],
         'Убийства',id='demo-dropdown'),width = 2),
         dbc.Col(html.H1('Убийства',id = 'header'),width=8),
         dbc.Col(dcc.RadioItems(['GreyTheme ', 'BlueTheme'],'GreyTheme ', inputStyle={"margin-right": "20px"},
         style = {'font-size':14},id='theme'),width = 2)
         ]),
        dbc.Row(
            [
                dbc.Col(dcc.RadioItems(['Europian', 'Asian','Afro-American','Hispanic'], 'Afro-American',style = {'font-size':14},id = 'race'),width = 1),
                dbc.Col(dcc.Graph(id='violence1'),width = 5),
                dbc.Col(dcc.Graph(id='violence2'),width = 5)
            ]
        ),
        html.Hr(style={'color':'#191970'}),
        dbc.Row(
            [
                dbc.Col(dcc.Dropdown(['Total divorced', 'Male divorced', 'Female divorced'],
                'Total divorced',id='divorce'),style = {'font-size':15,'width':'50%'}),
                dbc.Col(dcc.Dropdown(['Capita income','Household income', 'Family income'],
                'Capita income',id='income'),style = {'font-size':15,'width':'50%'})

            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='violence4')),
                dbc.Col(dcc.Graph(id='violence3'))
            ]
        ),
        html.Hr(style={'color':'#191970'}),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='violence5')),
            ]
        )
]
)

@app.callback(
    Output('header', 'children'),
    Input('demo-dropdown', 'value'))
def update_header(value):
    return value

@app.callback(
    Output('header', 'style'),
    Input('theme', 'value'))
def update_header_style(theme):
    return {'textAlign': 'center', 'color': colors['header'][theme]}



@app.callback(
    Output('violence1', 'figure'),
    Input('demo-dropdown', 'value'),
    Input('race','value'),
    Input('theme','value'))
def update_violent1(value,race_choice,theme):
    ind1 = crimes.index(value)
    fig = px.scatter(df,x=column_name[value], y='PctKidsBornNeverMar',color = race[race_choice],
    labels = {race[race_choice]: f'{race_choice} percent'},color_continuous_scale='thermal')
    fig.update_traces(hovertemplate=f"Количество убийств {for_traces[ind1]} на 100K: "+"%{x}, Процент внебрачных детей: %{y}<extra></extra>")
    fig.update_layout(title=dict(text = f"Зависимость между количеством {for_traces[ind1]} на 100K и <br> внебрачных детей </br>",font=dict(family="Arial",size=17)),
                    xaxis_title=f"Количество {for_traces[ind1]}",
                    yaxis_title="Процент внебрачных детей")
    fig.update_layout(margin=dict(l=0, r=100, t=50, b=50))
    fig.update_layout(
        plot_bgcolor=colors['background'][theme],
        paper_bgcolor=colors['background'][theme],
        font_color=colors['text'][theme],
        height = 500
    )
    return fig

@app.callback(
    Output('violence2', 'figure'),
    Input('demo-dropdown', 'value'),
    Input('theme','value'))
def update_violent2(value,theme):
    ind1 = crimes.index(value)
    df_temp = df.dropna(subset = ['PctFam2Par',column_name[value]])
    cut = pd.cut(df_temp['PctFam2Par'].round(),[22,40,65,80,95])
    cut = cut.apply(lambda x: f'{x.left}%-{x.right}%').sort_values()
    fig1 = px.box(x = cut,y = df_temp[column_name[value]],color = cut,color_discrete_sequence=['green','purple','red','blue'])
    fig1.update_traces(hovertemplate="Процент полных семей: %{x}, " + f"Количество{for_traces[ind1]} на 100K:" + "%{y}<extra></extra>")
    fig1.update_layout(title=dict(text = f"Зависимость между количеством {for_traces[ind1]} на 100K и <br> процентом полных семей </br>",font=dict(family="Arial",size=17)),
                    yaxis_title=f"Количество {for_traces[ind1]}",
                    xaxis_title="Процент полных семей")
    fig1.update_layout(margin=dict(l=0, r=0, t=50, b=50),legend = dict(title=''),legend_orientation = 'h',boxgap = 0)
    fig1.update_layout(
        plot_bgcolor=colors['background'][theme],
        paper_bgcolor=colors['background'][theme],
        font_color=colors['text'][theme],
        height = 500
    )
    return fig1

@app.callback(
    Output('violence3', 'figure'),
    Input('demo-dropdown', 'value'),
    Input('theme','value'),
    Input('income','value'))
def update_violent3(value,theme,income_type):
    ind1 = crimes.index(value)
    df_temp = df.dropna(subset = [income[income_type],'racePctWhite',column_name[value]])
    df_temp[income[income_type]] = pd.qcut(df[income[income_type]],q = 7).apply(lambda x: f'{round(x.left/1000,2)}-{round(x.right/1000,2)}K')
    df_temp['racePctWhite'] = pd.cut(df['racePctWhite'],[2,20,50,70,85,90,95,100]).apply(lambda x: f'{round(x.left)}-{round(x.right)}')
    pivot = df_temp.pivot_table(columns = 'racePctWhite',index = income[income_type],values = column_name[value],aggfunc = (lambda x: round(x.mean(),2)))
    fig2 = px.imshow(pivot,labels = dict(color=f'Среднее количество {for_traces[ind1]} на 100K'),text_auto=True)
    fig2.update_traces(hovertemplate="Процент европиоидной расы: %{x}"+f"<br> Доход на {income_name[income_type]}:" +  "%{y}</br>Среднее количество" + f" {for_traces[ind1]} на 100K:" + " %{z} <extra></extra>")
    fig2.update_layout(title=dict(text = f"Зависимость количества {for_traces[ind1]} на 100K от уровня дохода <br> и процента европиоидной расы</br>",font=dict(family="Arial",size=17)),
                    xaxis_title="Процент европиоидной расы",
                    yaxis_title=f"Доход на {income_name[income_type]}",coloraxis=dict(showscale=False))
    fig2.update_layout(margin=dict(l=0, r=0, t=70, b=0))
    fig2.update_layout(
        plot_bgcolor=colors['background'][theme],
        paper_bgcolor=colors['background'][theme],
        font_color=colors['text'][theme],
        height = 500
    )
    return fig2


@app.callback(
    Output('violence4', 'figure'),
    Input('demo-dropdown', 'value'),
    Input('theme','value'),
    Input('divorce','value'))
def update_violent4(value,theme,divorce):
    ind1 = crimes.index(value)
    df_temp = df.dropna(subset = [div[divorce],column_name[value]])
    df_temp[column_name[value]] = pd.cut(df[column_name[value]],intervals[value]).apply(lambda x: f'{round(max(0,x.left))}-{round(x.right)}')
    fig3 = ff.create_distplot([df_temp[df_temp[column_name[value]] == un][div[divorce]] for un in df_temp[column_name[value]].unique()],
                            group_labels =  df_temp[column_name[value]].unique(),show_hist=False)
    fig3.update_traces(hovertemplate="Процент разведенных: %{x}<br> Значение функции распределения: %{y}</br> <extra></extra>")
    fig3.update_layout(title=dict(text = f"Распределение процента разведенных {div_people[divorce]} <br> в зависимости от количества {for_traces[ind1]} </br>",font=dict(family="Arial",size=17)))
    fig3.update_layout(margin=dict(l=0, r=0, t=70, b=0),legend = dict(title = f'Количество {for_traces[ind1]} на 100K'),legend_orientation = 'h')
    fig3.update_layout(
        plot_bgcolor=colors['background'][theme],
        paper_bgcolor=colors['background'][theme],
        font_color=colors['text'][theme],
        height = 500
    )
    return fig3

@app.callback(
    Output('violence5', 'figure'),
    Input('demo-dropdown', 'value'),
    Input('theme','value'))
def update_violent5(value,theme):
    ind1 = crimes.index(value)
    df_temp = df.dropna(subset = ['PolicAveOTWorked',column_name[value]])
    df_temp[column_name[value]] = pd.cut(df[column_name[value]],intervals[value]).apply(lambda x: f'{round(max(0,x.left))}-{round(x.right)}')
    df_temp['PolicAveOTWorked'] = pd.qcut(df['PolicAveOTWorked'],q=7).apply(lambda x: f'{round(x.left)}-{round(x.right)}')
    fig4 = make_subplots(rows=2, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}],[{'type':'domain'},{'type':'domain'}]])
    for i in range(4):
        un = df_temp[column_name[value]].unique()[i]
        div = df_temp[df_temp[column_name[value]] == un]['PolicAveOTWorked']
        fig4.add_trace(go.Pie(labels = div.unique(),values=div.value_counts(),name = un),(i%2+1)%2+1,(i>1)+1)
    fig4.update_layout(margin=dict(l=0, r=0, t=30, b=0),legend = dict(title = 'Количество часов'))
    fig4.update_traces(hole=.4, hoverinfo="label+percent+name")
    fig4.update_layout(title=dict(text = f"Распределение количества сверхурочных часов полиции в зависимости от количества {for_traces[ind1]}",x = 0.5,font=dict(family="Arial",size=17)),
    annotations=[dict(text= df_temp[column_name[value]].unique()[0], x=0.195, y=0.19, font_size=12, showarrow=False),
                    dict(text=df_temp[column_name[value]].unique()[1], x=0.2, y=0.81, font_size=12, showarrow=False),
                    dict(text=df_temp[column_name[value]].unique()[2], x=0.79, y=0.19, font_size=12, showarrow=False),
                dict(text=df_temp[column_name[value]].unique()[3], x=0.8, y=0.81, font_size=12, showarrow=False)])
    fig4.update_layout(
        plot_bgcolor=colors['background'][theme],
        paper_bgcolor=colors['background'][theme],
        font_color=colors['text'][theme],
        height = 500
    )
    return fig4

if __name__ == '__main__':
    app.run_server(debug=True) 