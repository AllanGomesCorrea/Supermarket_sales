import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

file_name = 'quantidade_produtos.csv'
df = pd.read_csv(file_name)

file_name2 = 'total.csv'
df2 = pd.read_csv(file_name2)

# Inicializar o aplicativo Dash com Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Juntar as três primeiras colunas em uma única coluna
df['Filter'] = df.apply(lambda x: f"{x['Gender']} - {x['Customer type']} - {x['Product line']}", axis=1)
df2['Filter'] = df2.apply(lambda x: f"{x['Gender']} - {x['Customer type']} - {x['Product line']}", axis=1)

# Obter as categorias únicas para as colunas 'Gender', 'Customer type' e 'Product line'
gender_categories = df['Gender'].unique()
customer_type_categories = df['Customer type'].unique()
product_line_categories = df['Product line'].unique()

# Criar as options para os dropdowns
gender_options = [{'label': gender, 'value': gender} for gender in gender_categories]
customer_type_options = [{'label': customer_type, 'value': customer_type} for customer_type in customer_type_categories]
product_line_options = [{'label': product_line, 'value': product_line} for product_line in product_line_categories]


# Layout do aplicativo
app.layout = html.Div([
    html.H1('Dashboard Supermarket sales'),

    # Row para os dropdowns
    dbc.Row([
        # Dropdown para selecionar o gênero
        dbc.Col(
            dcc.Dropdown(
                id='gender-dropdown',
                options=gender_options,
                value=gender_categories[0],  # Valor padrão
                style={'width': '200px'}
            )
        ),
        # Dropdown para selecionar o tipo de cliente
        dbc.Col(
            dcc.Dropdown(
                id='customer-type-dropdown',
                options=customer_type_options,
                value=customer_type_categories[0],  # Valor padrão
                style={'width': '200px'}
            )
        ),
        # Dropdown para selecionar a linha de produto
        dbc.Col(
            dcc.Dropdown(
                id='product-line-dropdown',
                options=product_line_options,
                value=product_line_categories[0],  # Valor padrão
                style={'width': '200px'}
            )
        )
    ]),
    
    # Row para os gráficos
    dbc.Row([
        # Coluna para o primeiro par de gráficos
        dbc.Col([
            dcc.Graph(id='bar-chart1')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='bar-chart2')
        ], width=6)
    ]),
    dbc.Row([
        # Coluna para o segundo par de gráficos
        dbc.Col([
            dcc.Graph(id='bar-chart3'),
            html.Button('Atualizar Gráfico', id='update-button', n_clicks=0, style={'display': 'none'})
        ], width=6),
        dbc.Col([
            dcc.Graph(id='bar-chart4'),
            html.Button('Atualizar Gráfico', id='update-button', n_clicks=0, style={'display': 'none'})
        ], width=6)
    ])    
])


# Callback para atualizar o primeiro gráfico com base nas categorias selecionadas
@app.callback(
    Output('bar-chart1', 'figure'),
    [Input('gender-dropdown', 'value'),
     Input('customer-type-dropdown', 'value'),
     Input('product-line-dropdown', 'value')]
)
def update_bar_chart1(gender, customer_type, product_line):
    filtered_df = df[(df['Gender'] == gender) & (df['Customer type'] == customer_type) & (df['Product line'] == product_line)]
    fig = px.bar(filtered_df, x='Product line', y='Quantity', title=f'Total of items by product line ({product_line})', barmode='group')
    return fig

# Callback para atualizar o segundo gráfico com base na categoria selecionada
@app.callback(
    Output('bar-chart2', 'figure'),
    [Input('gender-dropdown', 'value'),
     Input('customer-type-dropdown', 'value'),
     Input('product-line-dropdown', 'value')]
)
def update_bar_chart2(gender, customer_type, product_line):
    filtered_df = df2[(df2['Gender'] == gender) & (df2['Customer type'] == customer_type) & (df2['Product line'] == product_line)]
    fig = px.bar(filtered_df, x='Product line', y='Total', title=f'Total ($) by product line ({product_line})', barmode='group')
    return fig

@app.callback(
    Output('bar-chart3', 'figure'),
    [Input('update-button', 'n_clicks')]
)
def update_bar_chart3(_):
    fig = px.bar(df, x='Filter', y='Quantity', title='Total of items', barmode='group')
    fig.update_layout(xaxis={'tickfont': {'size': 10}})  # Define o tamanho da fonte dos ticks
    return fig

@app.callback(
    Output('bar-chart4', 'figure'),
    [Input('update-button', 'n_clicks')]
)
def update_bar_chart4(_):
    fig = px.bar(df2, x='Filter', y='Total', title='Total of items', barmode='group')
    fig.update_layout(xaxis={'tickfont': {'size': 10}})  # Define o tamanho da fonte dos ticks
    return fig



# Executar o aplicativo Dash
if __name__ == '__main__':
    app.run_server(debug=True)
