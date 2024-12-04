import numpy
import pandas  
import matplotlib.pyplot as pyplot
import seaborn
import streamlit as st



#Corpo

st.markdown("""
            # Análise e Visualização de Dados
            """)

## Introdução: contém o objetivo/propósito da análise
st.markdown("""
            ### O objetivo deste trabalho é realizar uma análise no Dataset IMDB Movies, procurando padrões, correlações e retirando possiveis insights.
            ---
            """)

## Descrição dos Dados: descrição inicial dos dados
st.markdown("""
            #### O dataset contém registros sobre as notas registradas no site IMDB, nomes dos filmes e seus respectivos diretores, além de sua duração e receita ganha.
            ##### Link do dataset: https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows/data
            ---
            """)

#Carregando o dataset
arquivo = 'imdb_top_1000.csv'
dataframe = pandas.read_csv(arquivo)

#A coluna 'Gross' possui a vírgula como separador das casas de milhar.
#A coluna 'Runtime' precisa de uma conversão apropriada para os inteiros.
#Há algumas colunas que precisam ser transformadas em números, removendo caracteres que impeçam a conversão.
dataframe["Gross"] = dataframe["Gross"].str.replace(",", "").astype(float)
dataframe["Runtime"] = dataframe["Runtime"].str.replace(" min", "").astype(int)
dataframe["Released_Year"] = dataframe["Released_Year"].str.extract(r'(\d+[.\d]*)').astype('Int64')

# SIDEBAR - Filtro de colunas
with st.sidebar:
    st.title('Filtros')
    cols_selected = \
        st.multiselect('Filtre os campos que deseja entender melhor:',
                       options=list(dataframe.columns),
                       default=list(dataframe.columns))

df_selected = dataframe[cols_selected]


st.markdown("""
    ## Dataset

""")

with st.expander('Dados gerais do dataset'):
    st.subheader('Primeiros registros')
    st.write(df_selected.head())
    
    st.subheader('Tamanho do Dataset')
    st.write('Quantidade de linhas:', df_selected.shape[0])
    st.write('Quantidade de colunas:', df_selected.shape[1])
    
    if st.checkbox('Exibir dados das colunas'):
        st.markdown("""
            - Poster_Link - Link que o IMDB está usando
            - Series_Title = Nome do filme
            - Released_Year - Ano que o filme foi lançado
            - Certificate - Certificado ganho pelo filme
            - Runtime - Duração total do filme
            - Genre - Gênero do filme
            - IMDB_Rating - Nota do filme no site do IMDB
            - Overview - Sinopse
            - Meta_score - Pontuação ganha pelo filme
            - Director - Diretor
            - Star1,Star2,Star3,Star4 - Nome dos principais atores
            - No_of_votes - Número total de votos
            - Gross - Dinheiro recebido com o filme
            """)

    st.subheader('Dados Faltantes')
    st.write(df_selected.isna().sum()[df_selected.isna().sum() > 0])

    st.subheader('Estatísticas Descritivas')
    st.write(df_selected.describe())

    ##Gerando visualizações

st.markdown("""
    ## Gerando Visualizações e Análises

""")
st.subheader('Gráficos')
option = st.selectbox(
    "Selecione o gráfico desejado",
    ("Relação entre IMDB Rating e Receita Bruta", "Relação entre IMDB Rating e Duração dos Filmes", "Média de Votos por Ano", "Gênero x Quantidade de Filmes"),
    index=None,
    placeholder="",
)

if option == "Relação entre IMDB Rating e Receita Bruta":
    fig, ax = pyplot.subplots(figsize=(8, 6))
    seaborn.scatterplot(x=dataframe["IMDB_Rating"], y=dataframe["Gross"], hue = dataframe["IMDB_Rating"], palette="viridis", s=10, ax=ax)
    ax.set_title("Relação entre IMDB Rating e Receita Bruta")
    ax.set_xlabel("IMDB Rating")
    ax.set_ylabel("Receita Bruta (USD)")
    st.pyplot(fig)

    st.markdown("""
        ### Análise
        ##### A relação entre a receita bruta e a classificação no IMDb dos filmes revela que uma alta arrecadação não implica, necessariamente, em uma boa avaliação. Embora apenas dois filmes com nota acima de 8.50 tenham ultrapassado a marca de 400 milhões de dólares em receita, é possível observar que a grande maioria dos filmes não atingem uma receita superior a 200 milhões.
        
""")


if option == "Relação entre IMDB Rating e Duração dos Filmes":
    dataframe['Runtime'] = dataframe['Runtime'].astype(str)

    dataframe['Runtime'] = dataframe['Runtime'].str.replace(' min', '', regex=False).astype(float)

    fig3, ax3 = pyplot.subplots(figsize=(10, 6))
    seaborn.scatterplot(data=dataframe, x='Runtime', y='IMDB_Rating', alpha=0.7, color='blue', marker='x')
    pyplot.title('Relação entre Duração dos Filmes (minutos) e Notas IMDb', fontsize=14)
    pyplot.xlabel('Duração (minutos)', fontsize=12)
    pyplot.ylabel('Nota IMDb', fontsize=12)
    pyplot.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig3)

    st.markdown("""
        ### Análise
        ##### Em termos de tempo de execução, há uma concentração significativa de filmes com duração entre 100 e 130 minutos. O filme mais curto possui cerca de 72 minutos, enquanto o mais longo tem 240 minutos. Interessantemente, a maior parte dos filmes nessa faixa de tempo (100 a 130 minutos) apresenta notas abaixo de 8.50. Por outro lado, as melhores avaliações estão concentradas em filmes com duração entre 125 e 200 minutos, sendo que os filmes mais longos tendem a ter as maiores notas, já que possuem mais tempo para desenvolver melhor a história e os personagens. 

""")

if option == "Média de Votos por Ano":
    fig4, ax4 = pyplot.subplots(figsize=(10, 8))
    seaborn.lineplot(x="Released_Year", y="No_of_Votes", data=dataframe, marker="o", color="orange", ax=ax4)
    ax4.set_title("Número de Votos por Ano")
    ax4.set_xlabel("Ano de Lançamento")
    ax4.set_ylabel("Média de Votos")
    pyplot.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig4)

    st.markdown("""
        ### Análise
        ##### Analisando as variações de votos ao longo das décadas, nota-se que entre os anos 30 e 60 houve grandes flutuações nas classificações, com maior estabilidade a partir da década de 70, que perdurou até os anos 90. Embora a partir de 2000 tenha ocorrido uma certa estabilidade nas notas, elas continuaram a ser diversificadas entre diversos filmes. A partir de 2010, as classificações começaram a se concentrar em um tipo mais específico de filme. Franquias como StarWars e StarTrek nas décadas de 70 podem ser considerados fatores importantes para o crescimento, assim como os filmes Marvel na década de 2010.

""")

if option == "Gênero x Quantidade de Filmes":
    genre_counts = dataframe['Genre'].str.split(', ').explode().value_counts()
    fig5, ax5 = pyplot.subplots(figsize=(12, 6))
    genre_counts.plot(kind='bar', color='skyblue', edgecolor='black')
    pyplot.title('Quantidade de Filmes por Gênero', fontsize=16)
    pyplot.xlabel('Gênero', fontsize=14)
    pyplot.ylabel('Quantidade de Filmes', fontsize=14)
    pyplot.xticks(rotation=45, ha='right', fontsize=12)
    pyplot.tight_layout()
    st.pyplot(fig5)

    st.markdown("""
        ### Análise
        ##### O gênero 'drama' se destaca como o mais presente no ranking, sendo o mais recorrente entre os filmes com as melhores avaliações. Por ser bem amplo, o drama consegue explorar profundamente temas humanos e emocionais, o que faz com que o desenvolvimento dos personagens e da trama gere bastante impacto no público. Além disso, o drama abrange diversos subgêneros, como o drama psicológico, o que explica sua constante presença entre os filmes mais bem classificados.                                                                                                                                                      
""")