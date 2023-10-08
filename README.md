# Projeto de Insights

O Objetivo de um projeto de Insights é recomendar soluções para a empresa ou negócio através de ***Insights*** gerados por uma Análise de Dados. Por tanto, dentro do *roadmap* de resolução de problemas em Data Science, cobriremos os seguintes passos:
* Recebimento da Questão de Negócio
* Definição de Escopo e entendimento do Problema de Negócio
* Coleta de Dados
* Limpeza dos Dados
* Exploração dos dados
* Elaboração de dashboards dinâmicos 

Cumprindo esses primeiros 5 passos e obtendo ***insights***, conseguiremos sugerir soluções sem termos que implementar algoritmos de ***Machine Learning*** mais complexos, dando assim agilidade na entrega de resultados para a empresa.

Todo o contexto de negócio deste projeto é fictício e foi criado pela [Comunidade DS](https://www.comunidadedatascience.com/).

# 1. Problema de Negócio - A Empresa *Fome Zero*
## Contexto do Problema

A empresa **Fome Zero** é uma marketplace de restaurantes. Ou seja, seu core business é facilitar o encontro e negociações de clientes e restaurantes. Os restaurantes fazem o cadastro dentro da plataforma da Fome Zero, que disponibiliza informações como endereço, tipo de culinária servida, se possui reservas, se faz entregas e também uma nota de avaliação dos serviços e produtos do restaurante, dentre outras informações.

Um novo CEO foi recém contratado e precisa entender melhor o negócio para conseguir tomar as melhores decisões estratégicas e alavancar ainda mais a Fome Zero, e para isso, ele precisa que seja feita uma análise nos dados da empresa e que sejam gerados dashboards, a partir dessas análises, para responder um conjunto de perguntas de negócio. A relação de perguntas está apresentada na seção **2.4 Perguntas de Negócio** deste documento.

Dessa forma, são objetivos deste projeto:

1. Criar um aplicativo Web que ofereça ao novo CEO da **Fome Zero** diferentes informações a respeito dos restaurantes cadastrados. Essas informações serão agrupadas em 4 dashborads, cada um representando um visão de dados diferente. Abaixo, a descrição do que será apresentado em cada uma desses dashboards:
    * Principal
        * Número total de restaurantes, países, cidades, avaliações e tipos de culinárias. Esses dados poderão ser filtrados por país.
        * Mapa com a localização geográfica e identificação dos restaurantes de acordo com os países selecionados
    * Países:
        * Gráficos indicando a quantidade de restaurantes por país a partir de critérios selecionáveis: total geral, número de restaurantes que fazem entrega, número de restaurantes que aceitam pedidos on-line, número de restaurantes que fazem reserva de mesas.
        * Gráficos com as notas médias de avaliação dos restaurantes de cada país de acordo com os tipos de culinárias selecionadas. Haverá a possibilidades de filtrar os restaurantes por faixa de nota, o que possibilita medir a performance do país dentro de uma determinada faixa de avaliação.
        * Tabela indicando qual o melhor restaurante por país, a partir dos tipos de culinárias selecionadas e a faixa de nota dos restaurantes. Os critérios de ranqueamento dos restaurantes estão apresentados na seção  **"2.3 Premissas"** deste documento.
    * Cidades:
        * Gráfico de cidades com o maior número de restaurantes cadastrados a partir dos seguintes filtros: por país, por tipo de culinária, por faixa de nota de avaliação dos restaurantes. Tambem será possível selecionar a quantidade de cidades que serão apresentadas no gráfico, respeitando o limite de 20 cidades.
        * Gráfico de cidades com o maior número de tipos de culinárias cadastrados a partir dos seguintes filtros: por país, por tipo de culinária, por faixa de nota de avaliação dos restaurantes. Tambem será possível selecionar a quantidade de cidades que serão apresentadas no gráfico, respeitando o limite de 20 cidades.
    * Tipos de Culinárias:
        * Quadro indicando qual o restaurante melhor ranqueado para cada tipo de culinária selecionada (maximo de 5 por consulta). Serão apresentados as seguintes informações dos restaurantes: nome, nota de avaliação, país e cidade. Os critérios de ranqueamento dos restaurantes estão apresentados na seção  **"2.3 Premissas"** deste documento.
        * Gráficos dos melhores e piores tipos de culinárias a partir das notas de avaliação dos restaurantes realizadas pelos clientes. O número máximo de tipos de culinárias por gráfico será de 20. Além da possibilidade de filtragem dos dados por país.
2. Responder perguntas de negócio organizadas por 4 temas: País, Cidades, Restaurantes e Tipos de Culinárias. A relação das perguntas estão na seção "3.2 Perguntas de Negócio". As respostas das perguntas constam nos dashboards apresentados no item anterior.

# 2. Premissas de Negócio
## 2.1. Os dados

A base de dados utilizada na construção desse projeto pode ser encontrada dentro da plataforma [Kaggle](https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset).
O conjunto de dados deste projeto está no arquivo **zomato.csv**

As colunas da base de dados são:

| Nome da Coluna | Descrição da Coluna                                                                                                                                                                                                                                                                                                                                                |
| :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| restaurant_id             | ID único de cada restaurante cadastrado na base de dados                                                                                                                                                                                                                                                                                                                           |
| restaurant_name           | Nome do restaurante                                                                                                                                                                                                                                                      |
| country_code          | Código do país do restaurante. Cada código representa um país, conforme tabela a seguir: 1: "India", 14: "Australia", 30: "Brazil", 37: "Canada", 94: "Indonesia", 148: "New Zeland", 162: "Philippines", 166: "Qatar", 184: "Singapure", 189: "South Africa", 191: "Sri Lanka", 208: "Turkey", 214: "United Arab Emirates", 215: "England", 216: "United States of America",                                                                                                                                                                                                                                                                                                                                       |
| city       | Nome da cidade do restaurante                                                                                                                                                                                                                                                                                                                                                  |
| address       | Endereço do restaurante  |
| locality    | Nome resumido da região onde o restaurante está localizado                                                                                                                                                                                                                                                                                                           |
| locality_verbose       | Nome completo da região onde o restaurante está localizado                                                                                                                                                                                                                                                                                                           |
| longitude         | Coordenada longitude do restaurante                                                                                                                                                                                                                                                                                                                                        |
| latitude     | Coordenada latitude do restaurante                                                                                                                                                                                                                         |
| cuisines           | Tipos de culináras oferecidos pelo restaurante                                                                                                                                                                                                                                                                             |
| average_cost_for_two      | Preço médio de um prato para duas pessoas                                                                                                                                                                                                                                                                             |
| currency          | Nome e símbolo da moeda do país do restaurantedesign do imóvel. 1 é a pior nota e 13 é a melhor nota                                                                                                                                                                                                                                                           |
| has_table_booking     | Indica se o restaurante faz entrega. (0) NÃO, (1) SIM                                                                                                                                                                                                                                                                              |
| has_online_delivery  | Indica se o restaurante aceita pedido on-line. (0) NÃO, (1) SIM                                                                                                                                                                                                                                                                    |
| is_delivering_now       | Indica se o restaurante está fazendo entregas. (0) NÃO, (1)  SIM                                                                                                                                                                                                                                                                                                                                 |
| switch_to_order_menu  | Não utilizado no projeto. Desconsiderar                                                                                                                                                                                                                                                                                                                                    |
| price_range        | Faixa de preço que o restaurante pratica. Os valores possíveis são: (1) Cheap, (2) Normal (3) Expensive (4) Gourmet                                                                                                                                                                                                                                                                                                                                            |
| aggregate_rating            | Nota média do restaurante a partir das avaliações dos clientes                                                                                                                                                                                                                                                                                                                                        |
| rating_color           | Não utilizado no projeto. Desconsiderar                                                                                                                                                                                                                                                                                                                                       |
| rating_text  | Não utilizado no projeto. Desconsiderar                                                                                                                                                                                                                                                                       |
| votes     | Quantidade de avaliações de clientes que o restaurante recebeu                                                                                                                                                                                                                                                                             |

## 2.2. Estratégia de Resolução
01. **Entender o problema de Negócio:** O objetivo desta etapa é compreender corretamente o que é pedido, ajustar as expectativas e demonstrar exemplos de como serão os resultados.
02. **Descrição dos Dados:** O objetivo é utilizar ferramentas estatísticas de localização e dispersão para possuir um entendimento melhor dos dados.
03. **Filtragem dos Dados:** O objetivo desta etapa é remover as linhas que possam conter dados incorretos ou dados que possam prejudicar a análise de alguma forma.
04. **Análise Exploratória dos Dados:** O objetivo desta etapa é realizar uma exploração dos dados validando hipóteses de negócio, para melhor entender o comportamento das variáveis na base de dados.
05. **Responder as perguntas de Negócio:**  O objetivo desta etapa é utilizar todo o conhecimento adquirido nas etapas anteriores e criar estratégias para responder as perguntas realizadas.

## 2.3. Ferramentas e Métodos Utilizados
- Python 3.11.5
- Jupyter Notebook
- CRISP-DS
- Git e GitHub
- Framework Streamlit para aplicação web e hospedagem
- Biblioteca Pandas para análise de dados
- Biblioteca Plotly para gráficos 
- Biblioteca Folium para mapas

## 2.3. Premissas
* ID de restaurantes duplicados serão removidos da base de dados.
* Linhas que possuírem colunas com valor indefinido **(NaN)** serão removidas da base de dados
* Será considerado apenas um tipo de culinária(**coluna cuisines**) por restaurante, sendo o primeiro tipo de culinária da lista
* Os restaurantes serão ranqueados conforme a seguinte ordem: maior nota média de avaliação dos clientes, maior número de avaliações recebidas, maior tempo de cadastro na plataforma.

## 2.4 Perguntas de Negócio
### Visão Geral
    1. Quantos restaurantes únicos estão registrados?
    2. Quantos países únicos estão registrados?
    3. Quantas cidades únicas estão registradas?
    4. Qual o total de avaliações feitas?
    5. Qual o total de tipos de culinária registrados?

### Visão Países
    1. Qual o nome do país que possui mais cidades registradas?
    2. Qual o nome do país que possui mais restaurantes registrados?
    3. Qual o nome do país que possui mais restaurantes com o nível de preço igual a 4
    registrados?
    4. Qual o nome do país que possui a maior quantidade de tipos de culinária
    distintos?
    5. Qual o nome do país que possui a maior quantidade de avaliações feitas?
    6. Qual o nome do país que possui a maior quantidade de restaurantes que fazem
    entrega?
    7. Qual o nome do país que possui a maior quantidade de restaurantes que aceitam
    reservas?
    8. Qual o nome do país que possui, na média, a maior quantidade de avaliações
    registrada?
    9. Qual o nome do país que possui, na média, a maior nota média registrada?
    10. Qual o nome do país que possui, na média, a menor nota média registrada?
    11. Qual a média de preço de um prato para dois por país?

### Visão Cidades
    1. Qual o nome da cidade que possui mais restaurantes registrados?
    2. Qual o nome da cidade que possui mais restaurantes com nota média acima de
    4?
    3. Qual o nome da cidade que possui mais restaurantes com nota média abaixo de
    2.5?
    4. Qual o nome da cidade que possui o maior valor médio de um prato para dois?
    5. Qual o nome da cidade que possui a maior quantidade de tipos de culinária
    distintas?
    6. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
    reservas?
    7. Qual o nome da cidade que possui a maior quantidade de restaurantes que fazem
    entregas?
    8. Qual o nome da cidade que possui a maior quantidade de restaurantes que
    aceitam pedidos

### Visão Restaurantes
    1. Qual o nome do restaurante que possui a maior quantidade de avaliações?
    2. Qual o nome do restaurante com a maior nota média?
    3. Qual o nome do restaurante que possui o maior valor de uma prato para duas
    pessoas?
    4. Qual o nome do restaurante de tipo de culinária brasileira que possui a menor
    média de avaliação?
    5. Qual o nome do restaurante de tipo de culinária brasileira, e que é do Brasil, que
    possui a maior média de avaliação?
    6. Os restaurantes que aceitam pedido online são também, na média, os
    restaurantes que mais possuem avaliações registradas?
    7. Os restaurantes que fazem reservas são também, na média, os restaurantes que
    possuem o maior valor médio de um prato para duas pessoas?
    8. Os restaurantes do tipo de culinária japonesa dos Estados Unidos da América
    possuem um valor médio de prato para duas pessoas maior que as churrascarias
    americanas (BBQ)?

### Visão Tipos de Culinárias
    1. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
    restaurante com a maior média de avaliação?
    2. Dos restaurantes que possuem o tipo de culinária italiana, qual o nome do
    restaurante com a menor média de avaliação?
    3. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
    restaurante com a maior média de avaliação?
    4. Dos restaurantes que possuem o tipo de culinária americana, qual o nome do
    restaurante com a menor média de avaliação?
    5. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
    restaurante com a maior média de avaliação?
    6. Dos restaurantes que possuem o tipo de culinária árabe, qual o nome do
    restaurante com a menor média de avaliação?
    7. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
    restaurante com a maior média de avaliação?
    8. Dos restaurantes que possuem o tipo de culinária japonesa, qual o nome do
    restaurante com a menor média de avaliação?
    9. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
    restaurante com a maior média de avaliação?
    10. Dos restaurantes que possuem o tipo de culinária caseira, qual o nome do
    restaurante com a menor média de avaliação?
    11. Qual o tipo de culinária que possui o maior valor médio de um prato para duas
    pessoas?
    12. Qual o tipo de culinária que possui a maior nota média?
    13. Qual o tipo de culinária que possui mais restaurantes que aceitam pedidos
    online e fazem entregas?




# 3. Resultado de Negócio
## 3.1. Oportunidades Identificadas
Apesar de estar presente em 15 países, a plataforma **Fome Zero** possui um alto grau de concentração no número de restaurantes em apenas dois países: India e Estados Unidos. Ambos representam praticamente 2/3 do total de restaurantes cadastrados. Há oportunidades de crescimento em países cuja população ultrapassa 200 milhões de habitantes, como Brasil e Indonésia.

Os clientes avaliam mais frequentemente os restaurantes que aceitam pedidos on-line. E no entanto, os restaurantes que não oferecem essa modalidade são maioria na plataforma. Convencer os restaurantes a adotar essa modalidade pode aumentar consideravelmente o engajamento de seus clientes, e por consequência, o da plataforma.

## 3.2. Exibição das Análises
Foi criado uma aplicação web utilizando o framework web Streamlit para facilitar o consumo das análises.

Link para acesso à aplicação: [Análises](https://fomezero-datamendes.streamlit.app/)

# 4. Lições Aprendidas
Foi constatado que poderíamos verificar e selecionar oportunidades de negócio para o CEO da empresa Fome Zero somente utilizando técnicas de manipulação de dados e ferramentas estatísticas, podendo entregar resultados sem a necessidade de utilizar técnicas e ferramentas mais complexas. Desta forma, oferecendo uma ótima relação custo/retorno.


# 5. Próximos Passos
* Realizar mais análises a fim de melhorar o entendimento dos dados da base de dados.
* Criar e validar hipóteses de negócio, relacionando as características dos restaurantes. Exemplo: Os restaurantes que aceitam pedidos on-line possuem uma avaliação melhor em relação aos demais ? 
* Considerar as faixas de preço dos restaurantes como critérios de filtro na elaboração dos gráficos, tabelas e quadros.
* Incluir uma página chamada "Restaurantes", onde o CEO  poderia montar a partir de vários critérios de filtro uma lista dos melhores e/ou piores restaurantes cadastrados na base. 
