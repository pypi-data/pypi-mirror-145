import pandas as pd
import pandera as pa

# Extração do arquivo

A = "c:\workspace\Python\\Projeto_ETL\\ocorrenciaCNIPA.csv"
df = pd.read_csv(A, sep=";",parse_dates=['ocorrencia_dia'],dayfirst=True, na_values=['**','****','*****','###!','####','NULL'])

# Validação do dados
schema = pa.DataFrameSchema( 
         columns = {"codigo_ocorrencia": pa.Column(pa.Int),
                    "codigo_ocorrencia2": pa.Column(pa.Int),
                    "ocorrencia_classificacao": pa.Column(pa.String),
                    "ocorrencia_cidade": pa.Column(pa.String),
                    "ocorrencia_uf": pa.Column(pa.String, pa.Check.str_length(2,2), nullable=True),
                    "ocorrencia_aerodromo": pa.Column(pa.String, nullable=True),
                    "ocorrencia_dia": pa.Column(pa.DateTime),
                    "ocorrencia_hora": pa.Column(pa.String,pa.Check.str_matches(
                        r'^([0-1]?[0-9]|[2][0-3]):([0-5][0-9])(:[0-5][0-9])?$'),nullable=True), #expressão regular para validar hora minuto e segundo
                    "total_recomendacoes": pa.Column(pa.Int)
         }) 
        
schema.validate(df)

# Limpeza dos dados

# df.replace(['**','****','*****','###!','####','NULL'],pd.NA,inplace=True) #já tratado na extração
# print(df.isna().sum())
# df['ocorrencia_hora_bkp'] = df.ocorrencia_hora #cria nova coluna
# df.drop(['ocorrencia_hora_bkp'], axis=1, inplace=True) #deleta a coluna
# print(df)
# df.drop_duplicates()#deleta linhas duplicadas
# df.dropna() #Deleta todos os NA do dataframe colocando alguns parametros deleta a linha onde tem o NA
# df.set_index('codigo_ocorrencia', inplace=True) #define determinada como indice
# print(df.loc[60894]) #imprime o indice determinado
# df.reset_index(drop=True, inplace=True) #reseta o indice da coluna
# print(df.head(10)) #primeiros 5
# print(df.loc[5,'ocorrencia_cidade']) #imprime dado da celula determinada(Linha e Coluna)

# print(df)
# print(df.dtypes)
# print(df.tail(5)) #ultimos 5 

# Transformação dos dados
df['ocorrencia_dia_hora'] = pd.to_datetime(df.ocorrencia_dia.astype(str) + ' ' + df.ocorrencia_hora) # cria nova coluna com a data e hora no tipo datetime
# print(df.head())

#Filtros a partir de string
# df.ocorrencia_cidade.str[0] == 'C' #primeiro caracter igual a C
# df.ocorrencia_cidade.str[-1] == 'A' #ultimo caracter igual a A
# df.ocorrencia_cidade.str[-2:] == 'MA' #termina com MA
#  df.ocorrencia_cidade.str.contains('MA') #dentro da string o que tiver MA


filtro = df.ocorrencia_classificacao.isin(['INCIDENTE GRAVE','INCIDENTE']) #isin alternativa para o conectivo ou
# filtro2 = df.ocorrencia_uf == 'SP'
# print(df.loc[filtro | filtro2]) #conectivo ou
# print(df.loc[filtro & filtro2]) #conectivo e

#GroupBy e soma

print(df.loc[filtro].groupby(['ocorrencia_uf']).size().sort_values(ascending=False))








