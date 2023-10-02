import pandas as pd
import inflection
from PIL import Image
import streamlit as st

# capturando nome do país
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred",
}

# retorna o nome da país
def get_country_name(country_id):
    return COUNTRIES[country_id]

# retorna o nome da cor
def get_color_name(color_code):
    return COLORS[color_code]

# retorna a faixa de preço do restaurante
def get_price_range(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

# renomear e formatar as colunas do dataframe
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    
    return df

# limpar os dados do dataframe
def clean_data( df ):
    # renomear e formatar as colunas do dataset
    df = rename_columns( df )

    # removendo linhas duplicadas
    df = df.drop_duplicates().reset_index()

    # excluindo valores nulos das colunas
    df = df[ pd.isnull( df['cuisines'] ) == False ].reset_index()

    # restringindo somente um tipo de culinária por restaurante
    df['cuisines'] = df['cuisines'].apply( lambda x: x.split(',')[0] )

    # criando campo para capturar o nome do país
    df['country_name'] = df['country_code'].apply( lambda x: get_country_name( x ) )

    return df

# ler dados do arquivo csv
def read_data( file ):
    return pd.read_csv( file )
    
# Retorna a imagem do logo do projeto
def get_logo( file):
    return Image.open( file )

# Monta a barra lateral do projeto
def mount_sidebar():
    image = get_logo( 'img/logo.png' )
    
    col1, col2 = st.sidebar.columns( [1, 4], gap='small' )
    col1.image( image, width=35 )
    col2.markdown( '# Fome Zero')

    st.sidebar.markdown( """___""")
    st.sidebar.markdown( '## Filtro' )

# Aplica o filtro por país
def filter_country_sidebar( df ):
    list_countries =  df['country_name'].unique()
    list_top5_countries = df[['country_name', 'restaurant_id']].groupby( 'country_name' ).count().sort_values( 'restaurant_id', ascending=False).reset_index().loc[0:4, 'country_name']

    all_countries = st.sidebar.checkbox('Todos os países', value=True)

    countries_filter = st.sidebar.multiselect ( 'Selecione os países que deseja filtrar:',
                                               list_countries,
                                               default=list_top5_countries,
                                               disabled=all_countries  
                                             )


    # Apply Filter
    if not all_countries:
        df = df[ df['country_name'].isin( countries_filter ) ]

    return df

