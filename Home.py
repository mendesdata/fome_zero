# >>> Import Libraries
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import branca
import math
from utils import general_functions as gf

# >>> Local Functions
def get_html_to_map( df, index ):
    restaurant_name = df.loc[index, 'restaurant_name']
    price =    'Price: ' + str( format( math.floor( df.loc[index, 'average_cost_for_two'] ), ',.2f' ) )  + '(' + df.loc[index, 'currency'] + ') for two' 
    cuisines = 'Type: ' + df.loc[index, 'cuisines']
    rating =   'Aggregate_rating: ' + str( round( df.loc[index, 'aggregate_rating'], 2 ) ) + '/5.0 ' 

    html =        '<b> ' +  restaurant_name + '</b><br><br>'
    html = html + '<h> ' + price  + '</h><br>' 
    html = html + '<h> ' + cuisines + '</h><br>' 
    html = html + '<h> ' + rating  + '</h><br>'     

    return html

def get_map_restaurants_by_country( df ):
    # Desenhar o mapa
    map = folium.Map( zoom_start=11 )
    marker_cluster = MarkerCluster().add_to( map )    

    for index, location_info in df.iterrows():
        iframe = branca.element.IFrame( html=get_html_to_map( df, index ), width=300, height=120)
        popup = folium.Popup(iframe, max_width=300)

        folium.Marker( [location_info['latitude'],
                      location_info['longitude']],
                      popup=popup).add_to( marker_cluster )


    return map

# >>> Main Function
def main():
    # Configurar título da página
    st.set_page_config( page_title='Fome Zero - Main Page', layout='wide' )  
    
    # Coletar dados originais
    df_raw = gf.load_data( 'data/zomato.csv' )
    
    # Limpar dataset
    df = gf.clean_data( df_raw )
    
    # Montar a barra lateral do projeto
    gf.mount_sidebar()
    
    # Aplicar o filtro por País
    df = gf.filter_country_sidebar( df )

    st.markdown( '# Fome Zero!')
    st.markdown( '## O Melhor lugar para encontrar seu mais novo restaurante favorito!' )
    st.markdown( '### Temos as seguintes marcas dentro da nossa plataforma:' )

    with st.container():
        col1, col2, col3, col4, col5 = st.columns ( 5 )
    
        with col1:
            col1.metric( 'Restaurantes cadastrados', df['restaurant_id'].nunique() )        
    
        with col2:
            col2.metric( 'Países cadastrados', df['country_code'].nunique()  ) 
    
        with col3:
            col3.metric( 'Cidades cadastradas', df['city'].nunique()  ) 
    
        with col4:
            col4.metric( 'Avaliações Feitas na Plataforma',  str( format( math.floor( df['votes'].sum() ), ',.0f' ) ).replace(",", ".")  ) 
    
        with col5:
            col5.metric( 'Tipos de Culinárias Oferecidos', df['cuisines'].nunique()  ) 
    
    with st.container():
        st.subheader( 'Mapa dos restaurantes' )
        map = get_map_restaurants_by_country( df )
        folium_static( map, width=1024, height=600 )

    return None

# >>> Call Main Function
if __name__ == "__main__":
    main()
    

