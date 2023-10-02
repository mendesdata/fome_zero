
# >>> Import Packages
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from utils import general_functions as gf


# >>> Local Functions
def get_graph_top_cuisines( df, worst_cuisines, qtt):
    df_aux = df[ ['cuisines', 'aggregate_rating'] ].groupby( 'cuisines' ).mean().sort_values( 'aggregate_rating', ascending=worst_cuisines).reset_index()
    df_aux['aggregate_rating'] = round( df_aux['aggregate_rating'], 2)
    df_aux = df_aux.loc[0:qtt-1, :]

    fig = px.bar( df_aux, x='cuisines', y='aggregate_rating',  text_auto=True, height=400, labels={ 'aggregate_rating': 'Média de Notas', 'cuisines':'Tipos de culinárias' })    
    return fig

def get_best_restaurants_by_cuisine( df, list_cuisines ):
    list_restaurants = [0, 0, 0, 0, 0]
    index=0
    
    for cuisine in list_cuisines:
        df_aux =  ( df[  df['cuisines'] == cuisine ]
                   [['restaurant_id', 'aggregate_rating', 'votes']]
                   .sort_values( ['aggregate_rating', 'votes'], ascending=False)
                   .reset_index() )
        
        if df_aux.shape[0] > 0:
            list_restaurants[index] = df_aux.loc[0, 'restaurant_id'] 

        index = index+1
                               
    return list_restaurants 
    
def get_restaurants_columns( df, restaurant_id ):
    df_aux = df[ df['restaurant_id'] == restaurant_id][['cuisines', 'restaurant_name', 'country_name', 'city', 'aggregate_rating']].reset_index()

    cuisines = df_aux.loc[0, 'cuisines']
    restaurant_name = df_aux.loc[0, 'restaurant_name']    
    country_name = df_aux.loc[0, 'country_name']
    city = df_aux.loc[0, 'city']
    aggregate_rating = df_aux.loc[0, 'aggregate_rating']

    label_ = cuisines + ': '+ restaurant_name
    value_ = str( aggregate_rating ) +'/5.0'
    help_ = f"""
            Países: {country_name}\n
            Cidade: {city}\n
            """
    
    return cuisines, restaurant_name, country_name, city, aggregate_rating, label_, value_, help_

# >>> Main Function
def main():
    # Configurar o título e o layout da página
    st.set_page_config( page_title='Fome Zero - Visão Tipos de Culinárias', layout='wide' )
    
    # extraindo dados originais
    df_raw = gf.read_data( 'data/zomato.csv' )
    
    # limpando o dataset
    df = gf.clean_data( df_raw )
    
    # Montando a barra lateral do projeto
    gf.mount_sidebar()
    
    # Aplicar o filtro por País
    df = gf.filter_country_sidebar( df )
    
    
    count_cuisines_filter = st.sidebar.slider( 'Informe a quantidade de culinárias que deseja visualizar:',
                                        value=10,
                                        min_value=1,
                                        max_value=20,
                                        step= 1)
    
    # ******************** MAIN AREA ********************
    st.header( 'Visão Tipos de Culinárias' )
    
    with st.container():
        st.subheader( 'Melhor restaurante por tipo de culinária:' )
        
        list_cuisines =  df['cuisines'].unique()
        list_top5_cuisines = df[['cuisines', 'restaurant_id']].groupby( 'cuisines' ).count().sort_values( 'restaurant_id', ascending=False).reset_index().loc[0:4, 'cuisines']
        cuisines_filter = st.multiselect ( 'Selecione os tipos de culinárias que deseja filtrar (Máximo: 5) :',
                                               list_cuisines,
                                               default=list_top5_cuisines,
                                               max_selections=5
                                             )
    
        list_restaurants = get_best_restaurants_by_cuisine( df, cuisines_filter )
    
        col1, col2, col3, col4, col5 = st.columns( 5 )
    
        with col1:
            if list_restaurants[0] != 0:
                cuisines, restaurant_name, country_name, city, aggregate_rating, label_, value_, help_ = get_restaurants_columns( df, list_restaurants[0] )
                st.metric( label=label_,  value=value_, help=help_)
                
        with col2:
            if list_restaurants[1] != 0:
                cuisines, restaurant_name, country_name, city, aggregate_rating, label_, value_, help_ = get_restaurants_columns( df, list_restaurants[1] )
                st.metric( label=label_,  value=value_, help=help_)
                
        with col3:
            if list_restaurants[2] != 0:
                cuisines, restaurant_name, country_name, city, aggregate_rating, label_, value_, help_ = get_restaurants_columns( df, list_restaurants[2] )
                st.metric( label=label_,  value=value_, help=help_)
                
        with col4:
            if list_restaurants[3] != 0:
                cuisines, restaurant_name, country_name, city, aggregate_rating, label_, value_, help_ = get_restaurants_columns( df, list_restaurants[3] )
                st.metric( label=label_,  value=value_, help=help_)
                
        with col5:
            if list_restaurants[4] != 0:
                cuisines, restaurant_name, country_name, city, aggregate_rating, label_, value_, help_ = get_restaurants_columns( df, list_restaurants[4] )
                st.metric( label=label_,  value=value_, help=help_)
    
        st.write( '')
        st.write( '')
        st.write( '')
     
            
    with st.container():
        col1, col2 = st.columns( 2 )
    
        with col1:
            st.subheader( 'TOP '+str( count_cuisines_filter )+' melhores Tipos de Culinárias' )
            fig = get_graph_top_cuisines( df, False, count_cuisines_filter)
            st.plotly_chart( fig, use_container_width=True )
        with col2:
            st.subheader( 'TOP '+str( count_cuisines_filter )+' piores Tipos de Culinárias' )
            fig = get_graph_top_cuisines( df, True, count_cuisines_filter)
            st.plotly_chart( fig, use_container_width=True )

    return None

        
# >>> Call Main Function
if __name__ == "__main__":
    main()

