import streamlit as st
import random
import json
from openai import OpenAI

# Carrega a chave da API a partir do arquivo de segredos.
api_key = st.secrets["openai"]["api_key"]
client = OpenAI(api_key=api_key)

st.title("Tarô Místico")
st.write("Preencha as informações abaixo para a sua consulta de tarô:")

# Entradas do usuário
nome = st.text_input("Nome:")
idade = st.number_input("Idade:", min_value=1, max_value=120, step=1)
genero = st.selectbox("Gênero:", ["Masculino", "Feminino", "Outro"])
pergunta = st.text_area("Sua pergunta:")

if st.button("Consultar Tarô"):
    # Carrega as cartas do arquivo JSON
    try:
        with open("cards.json", "r", encoding="utf8") as f:
            cartas_data = json.load(f)
        cartas_tarot = cartas_data["cards"]
    except Exception as e:
        st.error("Erro ao carregar as cartas do tarô: " + str(e))
        st.stop()

    # Sorteia 3 cartas distintas
    cartas_sorteadas = random.sample(cartas_tarot, 3)
    carta_resposta, carta_negativa, carta_positiva = cartas_sorteadas

    st.markdown("### Cartas Sorteadas")
    st.write("**Carta de Resposta:**", carta_resposta)
    st.write("**Carta Negativa:**", carta_negativa)
    st.write("**Carta Positiva:**", carta_positiva)

    # Monta o prompt com os dados coletados
    prompt = f"""
Eu sou um oráculo de tarô. Um cliente chamado {nome}, com {idade} anos e que se identifica como {genero}, fez a seguinte pergunta: "{pergunta}".

O tarô revelou as seguintes cartas:
- Resposta: {carta_resposta}
- Negativa: {carta_negativa}
- Positiva: {carta_positiva}

Com base nessas informações, por favor, interprete a leitura do tarô e forneça uma resposta detalhada e personalizada para o cliente.
    """

    # Chama a API do ChatGPT usando o novo formato
    with st.spinner("Interpretando seu tarô..."):
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um oráculo de tarô que responde de forma detalhada e personalizada."
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        interpretacao = completion.choices[0].message.content.strip()

    st.markdown("### Interpretação do Tarô")
    st.write(interpretacao)
