import numpy
import pandas
import matplotlib.pyplot as pyplot
import seaborn
import streamlit

arquivo = 'imdb_top_1000.csv'
dataframe = pandas.read_csv(arquivo)

#A coluna 'Gross' possui a vírgula como separador das casas de milhar.
#A coluna 'Runtime' precisa de uma conversão apropriada para os inteiros.
#Há algumas colunas que precisam ser transformadas em números, removendo caracteres que impeçam a conversão.
dataframe["Gross"] = dataframe["Gross"].str.replace(",", "").astype(float)
dataframe["Runtime"] = dataframe["Runtime"].str.replace(" min", "").astype(int)
dataframe["Released_Year"] = dataframe["Released_Year"].str.extract(r'(\d+[.\d]*)').astype('Int64')

#Mostrar valores introdutórios
print('VALORES INICIAIS: \n ', dataframe.head(), '\n')
print('QUANTIDADE DE LINHAS, NOME E TIPO DAS COLUNAS, E VALORES NÃO-NULOS: \n ')
dataframe.info()
print('\n')
print('INFORMAÇÕES DESCRITIVAS DOS DADOS QUE SÃO NÚMEROS: \n ', dataframe.describe(), '\n')

matriz_correlacao = dataframe.corr(numeric_only=True)
print(matriz_correlacao)



streamlit.title("IMDB - Filmes no top 1000")

streamlit.subheader("Dataset de Filmes")
streamlit.write(dataframe)

# Gráfico: Relação entre IMDB Rating e Receita Bruta
streamlit.subheader("Relação entre IMDB Rating e Receita Bruta")

fig, ax = pyplot.subplots(figsize=(8, 6))
seaborn.scatterplot(x=dataframe["IMDB_Rating"], y=dataframe["Gross"], s=10, palette="viridis", ax=ax)
ax.set_title("Relação entre IMDB Rating e Receita Bruta")
ax.set_xlabel("IMDB Rating")
ax.set_ylabel("Receita Bruta (USD)")
streamlit.pyplot(fig)

# Gráfico: Tempo de Execução
streamlit.subheader("Tempo de Execução dos Filmes")

runtime_counts = dataframe["Runtime"].value_counts().reset_index()
runtime_counts.columns = ["Runtime", "Film Count"]
all_runtimes = pandas.DataFrame({"Runtime": range(0, runtime_counts["Runtime"].max() + 1)})
full_data = pandas.merge(all_runtimes, runtime_counts, on="Runtime", how="left").fillna(0)

fig2, ax2 = pyplot.subplots(figsize=(14, 6))
seaborn.barplot(x="Runtime", y="Film Count", data=full_data, palette="muted", ax=ax2)

ax2.set_xlim(0, full_data["Runtime"].max())

tick_interval = 10
xticks = numpy.arange(0, full_data["Runtime"].max() + 1, tick_interval)
ax2.set_xticks(xticks)

ax2.set_xlabel("Tempo de execução (Minutos)")
ax2.set_ylabel("Quantidade de filmes")

streamlit.pyplot(fig2)

# Gráfico: Média de Votos por Ano
streamlit.subheader("Número de Votos por Ano")
fig3, ax3 = pyplot.subplots(figsize=(10, 8))
seaborn.lineplot(x="Released_Year", y="No_of_Votes", data=dataframe, marker="o", color="orange", ax=ax3)
ax3.set_title("Número de Votos por Ano")
ax3.set_xlabel("Ano de Lançamento")
ax3.set_ylabel("Média de Votos")
streamlit.pyplot(fig3)