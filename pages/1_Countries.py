
# >>> Import Packages
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image
from utils import general_functions as gf



# >>> Local Functions

COUNTRY_LIST = ["India", "Australia", "Brazil", "Canada", "Indonesia", "New Zeland", "Philippines", "Qatar",
                "Singapure", "South Africa", "Sri Lanka", "Turkey", "United Arab Emirates", "England", "United States of America"]

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

def graph_country_detailed( df, metric):
    df_aux = df[['country_name', metric, 'restaurant_id']].groupby( ['country_name', metric] ).count().reset_index()
    
    country_dict  = {'country_name': COUNTRY_LIST, 
                 'yes': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                 'no' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                }
    df_graph = pd.DataFrame( data=country_dict, index=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] )

    for i in range( 0, df_aux.shape[0] ): 
        if df_aux.loc[i, metric] == 0:
            df_graph.loc[ df_graph['country_name'] == df_aux.loc[i, 'country_name'], 'no'] = df_aux.loc[i, 'restaurant_id']
        else:
            df_graph.loc[ df_graph['country_name'] == df_aux.loc[i, 'country_name'], 'yes'] = df_aux.loc[i, 'restaurant_id']

    fig = go.Figure(data=[
        go.Bar(name='Yes', x=df_graph['country_name'], y=df_graph['yes'], text=df_graph['yes'], textposition='auto', marker_color='Blue'),
        go.Bar(name='No', x=df_graph['country_name'], y=df_graph['no'], text=df_graph['no'], textposition='auto', marker_color='Red')
    ])
    
    return fig

def get_better_restaurant_by_country( df ):
    list_country_name, list_restaurant_id, list_restaurant_name, list_aggregate_rating, list_votes = [], [], [], [], []
    df_aux = df[['country_name', 'restaurant_id', 'restaurant_name', 'aggregate_rating', 'votes']].reset_index()

    for country in COUNTRY_LIST:
        df2_aux = df_aux[ df_aux['country_name'] == country].sort_values( ['aggregate_rating', 'votes'], ascending=False ).reset_index()
        
        if df2_aux.shape[0] > 0:
            list_country_name.append( df2_aux.loc[0, 'country_name'] )
            list_restaurant_id.append( df2_aux.loc[0, 'restaurant_id'] )
            list_restaurant_name.append( df2_aux.loc[0, 'restaurant_name'] )
            list_aggregate_rating.append( df2_aux.loc[0, 'aggregate_rating'] )
            list_votes.append( df2_aux.loc[0, 'votes'] )

    dict = { 'country_name' : list_country_name,
             'restaurant_id' : list_restaurant_id,
             'restaurant_name' : list_restaurant_name,
             'aggregate_rating' : list_aggregate_rating,
             'votes' : list_votes }
    
    return pd.DataFrame( dict )


def get_graph_quantity_restaurant( df, type_of_graph ):
    if type_of_graph == 'Geral':
        df_aux = df[['country_name', 'restaurant_id']].groupby('country_name').count().sort_values( 'restaurant_id', ascending=False ).reset_index()
        fig = px.bar( df_aux, x='country_name', y='restaurant_id', text_auto=True, height=300, labels={ 'restaurant_id': 'Quantidade de Restaurantes', 'country_name':'Países' })
    
        return fig
    elif type_of_graph == 'Permite reserva':
        fig = graph_country_detailed( df, 'has_table_booking')
        fig = fig.update_layout(barmode='group', height=300, yaxis= dict( title='Quantidade de Restaurantes' ), xaxis= dict( title='Países' ) )

        return fig
        
    elif type_of_graph == 'Faz entrega':
        fig = graph_country_detailed( df, 'is_delivering_now')
        fig = fig.update_layout(barmode='group', height=300, yaxis= dict( title='Quantidade de Restaurantes' ), xaxis= dict( title='Países' ) )

        return fig

    elif type_of_graph == 'Aceita Pedido On-line':
        fig = graph_country_detailed( df, 'has_online_delivery')
        fig = fig.update_layout(barmode='group', height=300, yaxis= dict( title='Quantidade de Restaurantes' ), xaxis= dict( title='Países' ) )

        return fig
    

def get_graph_rating_restaurant( df ):
    df_aux = df[['country_name', 'aggregate_rating']].groupby('country_name').mean().sort_values( 'aggregate_rating', ascending=False ).reset_index()
    df_aux['aggregate_rating'] = round( df_aux['aggregate_rating'] , 2)
    
    fig = px.bar( df_aux, y='country_name', x='aggregate_rating', text_auto=True, height=500, labels={ 'aggregate_rating': 'Média de notas (0-5)', 'country_name':'Países' })
    
    return fig

# >>> Main Function
def main():
    # Configurar o título e o layout da página
    st.set_page_config( page_title='Fome Zero - Visão Países', layout='wide' )
    
    # extraindo dados originais
    df_raw = gf.read_data( 'data/zomato.csv' )
    
    # limpando o dataset
    df = gf.clean_data( df_raw )
    
    # Montando a barra lateral do projeto
    gf.mount_sidebar()
    
    list_cuisines =  df['cuisines'].unique()
    list_top5_cuisines = df[['cuisines', 'restaurant_id']].groupby( 'cuisines' ).count().sort_values( 'restaurant_id', ascending=False).reset_index().loc[0:4, 'cuisines']
    
    all_cuisines = st.sidebar.checkbox('Todos os tipos de culinárias', value=True)
    
    cuisines_filter = st.sidebar.multiselect ( 'Selecione os tipos de culinárias que deseja filtrar:',
                                               list_cuisines,
                                               default=list_top5_cuisines,
                                               disabled=all_cuisines   
                                             )
    
    
    range_rating = st.sidebar.selectbox( 'Selecione a faixa das notas dos restaurantes:', ('A partir da nota', 'Até a nota') )
    rating_filter = st.sidebar.slider( '',
                                        value=0.0,
                                        min_value=0.0,
                                        max_value=5.0,
                                        step= 0.1)
    
    
    
    # Apply Filters
    
    # filtro por tipos de culinárias
    if not all_cuisines:
        df = df[ df['cuisines'].isin( cuisines_filter ) ]
    
    # filtro de nota de avaliação (rating)
    if range_rating == 'A partir da nota':
        df = df[ df['aggregate_rating'] >= rating_filter ]
    else:
        df = df[ df['aggregate_rating'] <= rating_filter ]
    
    # ******************** MAIN AREA ********************
    st.header( 'Visão Países' )
    
    with st.container():
        #st.subheader( 'Quantidade de Restaurantes por País' )
    
        type_of_graph = st.selectbox( 'Que quantidade de restaurantes você deseja visualizar ?',
                                      ('Geral', 'Permite reserva', 'Faz entrega', 'Aceita Pedido On-line') )
    
        fig = get_graph_quantity_restaurant( df, type_of_graph )
        st.plotly_chart( fig, use_container_width=True )
            
    with st.container():
        col1, col2 = st.columns( 2 )
    
        with col1:
            st.subheader( 'Média das Notas dos Restaurantes por País' )
            fig = get_graph_rating_restaurant( df )
            st.plotly_chart( fig, use_container_width=True )
        with col2:
            st.subheader( 'Tabela de Melhor Restaurante por País' )
            st.dataframe( get_better_restaurant_by_country( df ) )

    return None


# >>> Call Main Function
if __name__ == "__main__":
    main()


