import requests
import streamlit as st

BASE_URL = "https://graph.facebook.com/v22.0/"

# Criando sessão otimizada para requisições
session = requests.Session()
session.headers.update({"Content-Type": "application/json"})

# Dicionário com os tokens dos aplicativos
TOKENS = {
    "App 1": "YOUR-TOKEN-APP",
}

def obter_contas_de_anuncio(access_token):
    """ Obtém todas as contas de anúncio associadas ao token """
    url = f"{BASE_URL}me/adaccounts?fields=id,name,account_status&access_token={access_token}"
    response = session.get(url)
    if response.status_code == 200:
        return response.json().get("data", [])
    return []

def obter_campaigns_ativas(ad_account_id, access_token):
    """ Obtém todas as campanhas ativas da conta de anúncio """
    url = f"{BASE_URL}{ad_account_id}/campaigns?fields=id,name,daily_budget,status&limit=100&access_token={access_token}"
    response = session.get(url)
    if response.status_code == 200:
        campaigns = response.json().get("data", [])
        return [c for c in campaigns if c["status"] == "ACTIVE"]
    return []

def obter_todas_campaigns(ad_account_id, access_token):
    """ Obtém todas as campanhas da conta de anúncio, independentemente do status """
    url = f"{BASE_URL}{ad_account_id}/campaigns?fields=id,name,daily_budget,status&limit=100&access_token={access_token}"
    response = session.get(url)
    if response.status_code == 200:
        return response.json().get("data", [])  # Retorna todas as campanhas sem filtrar
    return []

def obter_ad_sets_da_campanha(campaign_id, access_token):
    """ Obtém todos os conjuntos de anúncios da campanha """
    url = f"{BASE_URL}{campaign_id}/adsets?fields=id,name,daily_budget&limit=100&access_token={access_token}"
    response = session.get(url)
    if response.status_code == 200:
        return response.json().get("data", [])
    return []

def alterar_orcamento(ad_account_id, access_token, campaign_id, percentual, aumentar=True):
    """ Altera o orçamento de uma campanha ou de seus conjuntos de anúncios """
    campaign = next((c for c in obter_campaigns_ativas(ad_account_id, access_token) if c["id"] == campaign_id), None)
    if not campaign:
        return [{"error": "Campanha não encontrada"}]  # Sempre retorna lista, evitando erro

    resultados = []

    if "daily_budget" in campaign:  # Orçamento a nível de campanha (CBO)
        orcamento_atual = float(campaign["daily_budget"]) / 100
        fator = 1 + (percentual / 100) if aumentar else 1 - (percentual / 100)
        novo_orcamento = max(100, int(orcamento_atual * fator * 100))

        url = f"{BASE_URL}{campaign_id}?access_token={access_token}"
        payload = {"daily_budget": novo_orcamento}
        response = session.post(url, json=payload)

        if response.status_code == 200:
            return [{
                "campanha": campaign["name"],
                "orcamento_anterior": f"R$ {orcamento_atual:.2f}",
                "orcamento_atualizado": f"R$ {novo_orcamento / 100:.2f}",
                "status": "Sucesso"
            }]
        return [{"campanha": campaign["name"], "error": response.json()}]

    # Se não tem daily_budget, significa que o orçamento está nos Ad Sets (ABO)
    ad_sets = obter_ad_sets_da_campanha(campaign_id, access_token)
    if not ad_sets:
        return [{"error": "Nenhum conjunto de anúncios encontrado para essa campanha"}]

    for ad_set in ad_sets:
        ad_set_id = ad_set["id"]
        orcamento_atual = float(ad_set.get("daily_budget", 0)) / 100
        fator = 1 + (percentual / 100) if aumentar else 1 - (percentual / 100)
        novo_orcamento = max(100, int(orcamento_atual * fator * 100))

        url = f"{BASE_URL}{ad_set_id}?access_token={access_token}"
        payload = {"daily_budget": novo_orcamento}
        response = session.post(url, json=payload)

        if response.status_code == 200:
            resultados.append({
                "ad_set": ad_set["name"],
                "orcamento_anterior": f"R$ {orcamento_atual:.2f}",
                "orcamento_atualizado": f"R$ {novo_orcamento / 100:.2f}",
                "status": "Sucesso"
            })
        else:
            resultados.append({"ad_set": ad_set["name"], "error": response.json()})

    return resultados  # Sempre retorna lista, independente do tipo de orçamento

def pausar_ou_ativar_campanha(access_token, campaign_id, status):
    """ Pausa ou ativa uma campanha """
    url = f"{BASE_URL}{campaign_id}?access_token={access_token}"
    payload = {"status": status}
    
    response = session.post(url, json=payload)
    return response.json()

# Interface no Streamlit
st.title("Gerenciador de Campanhas do Facebook Ads")

# Selecionar o aplicativo (e token correspondente)
app_escolhido = st.selectbox("Selecione o Aplicativo:", list(TOKENS.keys()))
access_token = TOKENS[app_escolhido]

# Obter e listar contas de anúncio
contas = obter_contas_de_anuncio(access_token)
if not contas:
    st.error("Nenhuma conta de anúncio encontrada.")
    st.stop()

contas_dict = {c["name"]: c["id"] for c in contas if c["account_status"] == 1}
conta_escolhida_nome = st.selectbox("Selecione a Conta de Anúncio:", list(contas_dict.keys()))
ad_account_id = contas_dict[conta_escolhida_nome]

# Obter e listar campanhas ativas
campanhas = obter_campaigns_ativas(ad_account_id, access_token)
if not campanhas:
    st.error("Nenhuma campanha ativa encontrada para essa conta.")
    st.stop()

campanhas_dict = {c["name"]: c["id"] for c in campanhas}
campanha_escolhida_nome = st.selectbox("Selecione a Campanha:", list(campanhas_dict.keys()))
campaign_id = campanhas_dict[campanha_escolhida_nome]

st.success(f"Campanha Selecionada: {campanha_escolhida_nome} (ID: {campaign_id})")

# Verificar se a campanha tem orçamento próprio
campanha_detalhes = next((c for c in campanhas if c["id"] == campaign_id), None)

if "daily_budget" in campanha_detalhes:
    orcamento_atual = float(campanha_detalhes["daily_budget"]) / 100
    st.subheader(f"Orçamento Atual da Campanha: R$ {orcamento_atual:.2f}")
else:
    ad_sets = obter_ad_sets_da_campanha(campaign_id, access_token)
    if ad_sets:
        st.subheader("Orçamentos Atuais dos Ad Sets")
        for ad_set in ad_sets:
            orcamento_atual = float(ad_set.get("daily_budget", 0)) / 100
            st.write(f"🔹 {ad_set['name']}: R$ {orcamento_atual:.2f}")

# Opções de gerenciamento
opcao = st.selectbox("Escolha uma ação:", [
    "Aumentar orçamento", "Diminuir orçamento", "Pausar campanha"
])

if opcao in ["Aumentar orçamento", "Diminuir orçamento"]:
    percentual = st.number_input("Digite o percentual de ajuste do orçamento:", min_value=1, max_value=500, step=1)
    if st.button("Aplicar alteração"):
        resultados = alterar_orcamento(ad_account_id, access_token, campaign_id, percentual, aumentar=(opcao == "Aumentar orçamento"))

        st.subheader("Resultados da Alteração")
        for resultado in resultados:  # Agora itera sobre a lista
            if "error" in resultado:
                st.error(f"Erro: {resultado.get('campanha', resultado.get('ad_set', 'Desconhecido'))} - {resultado['error']}")
            else:
                st.success(f"✅ {resultado.get('campanha', resultado.get('ad_set', 'Desconhecido'))}:")
                st.write(f"🔸 **Orçamento Anterior:** {resultado['orcamento_anterior']}")
                st.write(f"🔹 **Novo Orçamento:** {resultado['orcamento_atualizado']}A")


elif opcao == "Pausar campanha" and st.button("Pausar"):
    resultado = pausar_ou_ativar_campanha(access_token, campaign_id, "PAUSED")
    if "error" in resultado:
        st.error(f"Erro: {resultado['error']}")
    else:
        st.success("✅ Campanha pausada com sucesso!")

elif opcao == "Ativar campanha" and st.button("Ativar"):
    resultado = pausar_ou_ativar_campanha(access_token, campaign_id, "ACTIVE")
    if "error" in resultado:
        st.error(f"Erro: {resultado['error']}")
    else:
        st.success("✅ Campanha ativada com sucesso!")
