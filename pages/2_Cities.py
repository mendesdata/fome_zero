
# >>> Import Libraries
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from utils import general_functions as gf

# >>> Local Functions
def city_with_older_restaurant( df, city_list ):
    df = df[ df['city'].isin( city_list) ][ ['city', 'restaurant_id'] ].sort_values( 'restaurant_id').reset_index()
    return df.loc[0, 'city']

def get_restaurant_cuisines(df, cuisine, func):
    df_aux = df[ df['cuisines'] == cuisine] 
    
    if func == 'max':    
        df_aux = df_aux[ df_aux['aggregate_rating'] == df_aux['aggregate_rating'].max() ][['restaurant_id', 'restaurant_name', 'aggregate_rating']].sort_values('restaurant_id').reset_index()
    else:
        df_aux = df_aux[ df_aux['aggregate_rating'] == df_aux['aggregate_rating'].min() ][['restaurant_id', 'restaurant_name', 'aggregate_rating']].sort_values('restaurant_id').reset_index()

    return df_aux.loc[0, 'restaurant_name'], df_aux.loc[0, 'restaurant_id'], df_aux.loc[0, 'aggregate_rating'] 


def get_graph_top_cities_qtt_restaurants( df, qtt ):
    df_aux = df[ ['country_name', 'city', 'restaurant_id'] ].groupby( ['country_name', 'city'] ).count().sort_values( 'restaurant_id', ascending=False).reset_index()
    df_aux = df_aux.loc[0:qtt-1, :]
    

    fig = px.bar( df_aux, x='city', y='restaurant_id', color='country_name', text_auto=True, height=500, labels={ 'city':'Cidades', 'restaurant_id':'Quantidade de restaurantes', 'country_name':'Países' } )    
    return fig

def get_graph_top_cities_qtt_cuisines( df, qtt ):
    df_aux = df[ ['country_name', 'city', 'cuisines'] ].groupby( ['country_name', 'city', 'cuisines'] ).count().sort_values( ['country_name', 'city', 'cuisines'] ).reset_index()
    df_aux = df_aux[['country_name', 'city', 'cuisines'] ].groupby( ['country_name', 'city'] ).count().sort_values( 'cuisines', ascending=False ).reset_index()
    df_aux = df_aux.loc[0:qtt-1, :]

    fig = px.bar( df_aux, x='city', y='cuisines', color='country_name', text_auto=True, height=500, labels={ 'city':'Cidades', 'cuisines':'Quantidade de tipos de culinária', 'country_name':'Países' })    
    return fig

# >>> Main Function
def main():
    # Configurar o título e o layout da página 
    st.set_page_config( page_title='Fome Zero - Visão Cidades', layout='wide' )
    
    # extraindo dados originais
    df_raw = gf.load_data( 'data/zomato.csv' )
    
    # limpando o dataset
    df = gf.clean_data( df_raw )
    
    # Montando a barra lateral do projeto
    gf.mount_sidebar()
    
    # Aplicar o filtro por País
    df = gf.filter_country_sidebar( df )
    
    
    range_rating = st.sidebar.selectbox( 'Selecione a faixa das notas dos restaurantes:', ('A partir da nota', 'Até a nota') )
    rating_filter = st.sidebar.slider( '',
                                        value=0.0,
                                        min_value=0.0,
                                        max_value=5.0,
                                        step= 0.1)
    
    count_cities_filter = st.sidebar.slider( 'Informe a quantidade de cidades que deseja visualizar:',
                                        value=10,
                                        min_value=1,
                                        max_value=20,
                                        step= 1)
    
    # Apply Filters
    
    
    # filtro de nota de avaliação (rating)
    if range_rating == 'A partir da nota':
        df = df[ df['aggregate_rating'] >= rating_filter ]
    else:
        df = df[ df['aggregate_rating'] <= rating_filter ]
    
    
    # ******************** MAIN AREA ********************
    st.header( 'Visão Cidades' )
    
    with st.container():
        st.subheader( 'Top ' + str(count_cities_filter) +' Cidades com mais restaurantes' )
        fig = get_graph_top_cities_qtt_restaurants( df, count_cities_filter )
        st.plotly_chart( fig, use_container_width=True )
            
    with st.container():
        st.subheader( 'Top ' + str(count_cities_filter) +'  Cidades com mais tipos de culinária' )
        fig = get_graph_top_cities_qtt_cuisines( df, count_cities_filter )
        st.plotly_chart( fig, use_container_width=True )

    return None

# >>> Call Main Function
if __name__ == "__main__":
    main()

        

