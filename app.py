import pandas as pd
import plotly.express as px
import streamlit as st

#Configuração da Página
st.set_page_config(
    page_title="Dashboard de Salários da Área de Dados",
    page_icon="📊",
    layout="wide",
)

#Carregamento de Planilha
df = pd.read_csv("https://raw.githubusercontent.com/ThiagoAP18/dashboard-tratado-dados-imersao/refs/heads/main/df-imersao-final.csv")

#Barra Lateral
st.sidebar.header("🔍 Filtros")

#Filtros de Ano
anos_disponiveis = sorted(df['ano'].unique())
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

#Filtros de Senioridade
senioridades_disponiveis = sorted(df['senioridade'].unique())
senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)

#Filtros de Tipo de Contrato
contratos_disponiveis = sorted(df['contrato'].unique())
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

#Filtros de Tamanho de Empresa
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

#Filtragem do DataFrame -- Feita com base nas escolhas da barra lateral
df_filtrado = df[
    (df['ano'].isin(anos_selecionados)) &
    (df['senioridade'].isin(senioridades_selecionadas)) &
    (df['contrato'].isin(contratos_selecionados)) &
    (df['tamanho_empresa'].isin(tamanhos_selecionados))
]

#Conteúdo Principal
st.title("🎲 Dashboard de Salários da Área de Dados")
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.")

#Métricas Principais

st.subheader('Métricas gerais (Salário anual em Dólar)')

if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = df_filtrado.shape[0]
    cargos_mais_frequente = df_filtrado["cargo"].mode()[0]
else:
    salario_medio = 0
    salario_medio = 0
    salario_maximo = 0
    total_registros = 0
    cargos_mais_frequente = ""

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${salario_medio:,.0f}")
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_registros:,}")
col4.metric("Cargo mais comum", cargos_mais_frequente)

st.markdown("...")

#Análise com Gráficos
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        
        grafico_cargos = px.bar(
            top_cargos,
            x = 'usd',
            y = 'cargo',
            orientation='h',
            title="Os 10 maiores cargos por salário médio anual",
            labels={'usd': 'Média Salarial Anual (USD)', 'cargo': ''},
            hover_data={'cargo': False}
        )

        grafico_cargos.update_layout(title_x=0.1, yaxis={'categoryorder': 'total ascending'})
        grafico_cargos.update_traces(hovertemplate = "<b>Média Salarial Anual (USD)</b>: %{x}<br><extra></extra>")
        
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.")

with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='usd',
            nbins=30,
            title="Distribuição de salários médios",
            labels={'usd': "Faixa Salarial Anual (USD)"},
            color_discrete_sequence=["#EB5338"]
        )

        grafico_hist.update_layout(title_x = 0.1, yaxis_title = "Registros")
        grafico_hist.update_traces(hovertemplate="<b>Registros</b>: %{y}<br>"+
                                   "<b>Faixa Salarial (USD)</b>: %{x}"+
                                   "<extra></extra>")

        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de salários")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']

        grafico_remoto = px.pie(
            remoto_contagem,
            names="tipo_trabalho",
            values='quantidade',
            title='Proporção dos tipos de trabalho',
            color_discrete_sequence=px.colors.qualitative.Set3,
            color='tipo_trabalho',
            hole=0.5
        )

        grafico_remoto.update_traces(textinfo='percent+label', 
                                     hovertemplate="<b>Tipo de Trabalho</b>: %{label}<br>"+
                                                    "<b>Registros</b>: %{percent}<br>"+
                                                    "<extra></extra>")
        grafico_remoto.update_layout(title_x=0.1)

        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de tipos de trabalho")
with col_graf4:
    if not df_filtrado.empty:
        paises_media_salarial = df_filtrado.groupby('residencia')['usd'].mean().sort_values(ascending=False).reset_index()

        paises_nomes = {
            'US': 'Estados Unidos',
            'AU': 'Austrália',
            'CA': 'Canadá',
            'JP': 'Japão',
            'GB': 'Reino Unido',
            'MX': 'México',
            'NL': 'Países Baixos',
            'ES': 'Espanha',
            'FR': 'França',
            'MT': 'Malta',
            'IT': 'Itália',
            'LT': 'Lituânia',
            'PH': 'Filipinas',
            'NZ': 'Nova Zelândia',
            'DE': 'Alemanha',
            'LV': 'Letônia',
            'IE': 'Irlanda',
            'MK': 'Macedônia do Norte',
            'AT': 'Áustria',
            'PL': 'Polônia',
            'SK': 'Eslováquia',
            'BR': 'Brasil',
            'SI': 'Eslovênia',
            'FI': 'Finlândia',
            'HK': 'Hong Kong',
            'LS': 'Lesoto',
            'IN': 'Índia',
            'JM': 'Jamaica',
            'CH': 'Suíça',
            'BE': 'Bélgica',
            'ID': 'Indonésia',
            'PE': 'Peru',
            'SG': 'Singapura',
            'PT': 'Portugal',
            'HU': 'Hungria',
            'RO': 'Romênia',
            'AR': 'Argentina',
            'ZA': 'África do Sul',
            'PA': 'Panamá',
            'EE': 'Estônia',
            'LU': 'Luxemburgo',
            'DZ': 'Argélia',
            'EG': 'Egito',
            'CL': 'Chile',
            'GR': 'Grécia',
            'KE': 'Quênia',
            'CD': 'República Democrática do Congo',
            'SE': 'Suécia',
            'KR': 'Coreia do Sul',
            'TW': 'Taiwan',
            'NO': 'Noruega',
            'CZ': 'República Tcheca',
            'TR': 'Turquia',
            'NG': 'Nigéria',
            'CY': 'Chipre',
            'CO': 'Colômbia',
            'DK': 'Dinamarca',
            'AE': 'Emirados Árabicos Unidos',
            'BG': 'Bulgária',
            'JO': 'Jordânia',
            'RS': 'Sérvia',
            'UA': 'Ucrânia',
            'PR': 'Porto Rico',
            'SV': 'El Salvador',
            'EC': 'Equador',
            'DO': 'República Dominicana',
            'MY': 'Malásia',
            'XK': 'Kosovo',
            'CR': 'Costa Rica',
            'ZM': 'Zâmbia',
            'AM': 'Armênia',
            'RW': 'Ruanda',
            'IL': 'Israel',
            'LB': 'Líbano',
            'HR': 'Croácia',
            'PK': 'Paquistão',
            'HN': 'Honduras',
            'VE': 'Venezuela',
            'BM': 'Bermudas',
            'VN': 'Vietnã',
            'GE': 'Geórgia',
            'SA': 'Arábia Saudita',
            'OM': 'Omã',
            'BA': 'Bósnia e Herzegovina',
            'UG': 'Uganda',
            'MU': 'Maurício',
            'TH': 'Tailândia',
            'QA': 'Catar',
            'RU': 'Rússia',
            'TN': 'Tunísia',
            'GH': 'Gana',
            'AD': 'Andorra',
            'MD': 'Moldávia',
            'UZ': 'Uzbequistão',
            'CF': 'República Centro-Africana',
            'KW': 'Kuwait',
            'IR': 'Irã',
            'AS': 'Samoa Americana',
            'CN': 'China',
            'BO': 'Bolívia',
            'IQ': 'Iraque',
            'JE': 'Jersey'
        }

        paises_media_salarial['pais_nome_completo'] = paises_media_salarial['residencia'].map(paises_nomes)
        paises_media_salarial['pais_nome_completo'] = paises_media_salarial['pais_nome_completo'].fillna(paises_media_salarial['residencia'])

        grafico_paises = px.bar(paises_media_salarial,
                                x='residencia',
                                y='usd',
                                title='Media salarial anual por pais',
                                color_discrete_sequence=px.colors.qualitative.Pastel1,
                                labels={'residencia': "País (Sigla)", 'usd': "Média Salarial Anual (USD)"},
                                hover_data='pais_nome_completo')
        
        grafico_paises.update_layout(title_x = 0.1)
        grafico_paises.update_traces(hovertemplate = "<b>País</b>: %{customdata[0]}<br>"+
                                                    "<b>Média Salarial Anual</b>: %{y}"+
                                                    "<extra></extra>")
        
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Não existem dados suficientes para apresentação do gráfico de países")

col_graf5 = st.columns(1)

with col_graf4:
    if not df_filtrado.empty:
        df_filtrado['residencia_iso3'] = df_filtrado['residencia'].apply(iso2_to_iso3)

        nomes_paises = {
            'USA': 'Estados Unidos',
            'AUS': 'Austrália',
            'CAN': 'Canadá',
            'JPN': 'Japão',
            'GBR': 'Reino Unido',
            'MEX': 'México',
            'NLD': 'Países Baixos',
            'ESP': 'Espanha',
            'FRA': 'França',
            'MLT': 'Malta',
            'ITA': 'Itália',
            'LTU': 'Lituânia',
            'PHL': 'Filipinas',
            'NZL': 'Nova Zelândia',
            'DEU': 'Alemanha',
            'LVA': 'Letônia',
            'IRL': 'Irlanda',
            'MKD': 'Macedônia do Norte',
            'AUT': 'Áustria',
            'POL': 'Polônia',
            'SVK': 'Eslováquia',
            'BRA': 'Brasil',
            'SVN': 'Eslovênia',
            'FIN': 'Finlândia',
            'HKG': 'Hong Kong',
            'LSO': 'Lesoto',
            'IND': 'Índia',
            'JAM': 'Jamaica',
            'CHE': 'Suíça',
            'BEL': 'Bélgica',
            'IDN': 'Indonésia',
            'PER': 'Peru',
            'SGP': 'Singapura',
            'PRT': 'Portugal',
            'HUN': 'Hungria',
            'ROU': 'Romênia',
            'ARG': 'Argentina',
            'ZAF': 'África do Sul',
            'PAN': 'Panamá',
            'EST': 'Estônia',
            'LUX': 'Luxemburgo',
            'DZA': 'Argélia',
            'EGY': 'Egito',
            'CHL': 'Chile',
            'GRC': 'Grécia',
            'KEN': 'Quênia',
            'COD': 'República Democrática do Congo',
            'SWE': 'Suécia',
            'KOR': 'Coreia do Sul',
            'TWN': 'Taiwan',
            'NOR': 'Noruega',
            'CZE': 'República Tcheca',
            'TUR': 'Turquia',
            'NGA': 'Nigéria',
            'CYP': 'Chipre',
            'COL': 'Colômbia',
            'DNK': 'Dinamarca',
            'ARE': 'Emirados Árabes Unidos',
            'BGR': 'Bulgária',
            'JOR': 'Jordânia',
            'SRB': 'Sérvia',
            'UKR': 'Ucrânia',
            'PRI': 'Porto Rico',
            'SLV': 'El Salvador',
            'ECU': 'Equador',
            'DOM': 'República Dominicana',
            'MYS': 'Malásia',
            'XKX': 'Kosovo',
            'CRI': 'Costa Rica',
            'ZMB': 'Zâmbia',
            'ARM': 'Armênia',
            'RWA': 'Ruanda',
            'ISR': 'Israel',
            'LBN': 'Líbano',
            'HRV': 'Croácia',
            'PAK': 'Paquistão',
            'HND': 'Honduras',
            'VEN': 'Venezuela',
            'BMU': 'Bermudas',
            'VNM': 'Vietnã',
            'GEO': 'Geórgia',
            'SAU': 'Arábia Saudita',
            'OMN': 'Omã',
            'BIH': 'Bósnia e Herzegovina',
            'UGA': 'Uganda',
            'MUS': 'Maurício',
            'THA': 'Tailândia',
            'QAT': 'Catar',
            'RUS': 'Rússia',
            'TUN': 'Tunísia',
            'GHA': 'Gana',
            'AND': 'Andorra',
            'MDA': 'Moldávia',
            'UZB': 'Uzbequistão',
            'CAF': 'República Centro-Africana',
            'KWT': 'Kuwait',
            'IRN': 'Irã',
            'ASM': 'Samoa Americana',
            'CHN': 'China',
            'BOL': 'Bolívia',
            'IRQ': 'Iraque',
            'JEY': 'Jersey'
        }

        salario_medio_cd_paises = df_filtrado[df_filtrado['cargo'] == 'Cientista de Dados'].groupby('residencia_iso3')['usd'].mean().reset_index()
        salario_medio_cd_paises['residencia_nome'] = salario_medio_cd_paises['residencia_iso3'].map(nomes_paises)
        salario_medio_cd_paises['residencia_nome'] = salario_medio_cd_paises['residencia_nome'].fillna(salario_medio_cd_paises['residencia_iso3'])

        grafico_paises_mapa = px.choropleth(salario_medio_cd_paises,
                                            locations='residencia_iso3',
                                            color='usd',
                                            color_continuous_scale='rdylgn',
                                            title='Mapa de Salário Médio Anual (USD) de Cientistas de Dados',
                                            labels={'residencia_iso3': 'País (Sigla)', 'usd': 'Salário Médio Anual (USD)'},
                                            hover_data=['residencia_nome', 'usd'])
        
        grafico_paises_mapa.update_layout(title_x = 0.1)
        grafico_paises_mapa.update_traces(hovertemplate = '<b>País</b>: %{customdata[0]}<br>'+
                                                        '<b>Salário Médio Anual (USD)</b>: %{customdata[1]:,.2f}<br>'+
                                                        "<extra></extra>")
        
        st.plotly_chart(grafico_paises_mapa, use_container_width=True)
    else:
        st.warning("Não existem dados suficientes para apresentação do gráfico de países")

#Dados Detalhados
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)