# Gerenciador de Campanhas do Facebook Ads

Este projeto é uma aplicação baseada em Streamlit para gerenciar campanhas do Facebook Ads. Ele permite visualizar contas de anúncios, listar campanhas ativas, ajustar orçamentos e pausar ou ativar campanhas diretamente pela interface.

## 📌 Funcionalidades

✅ Listar todas as contas de anúncios associadas ao token do aplicativo.
✅ Exibir campanhas ativas para uma conta de anúncio selecionada.
✅ Ajustar orçamento de campanhas e conjuntos de anúncios (CBO e ABO).
✅ Pausar ou ativar campanhas diretamente pela interface.
✅ Interface amigável utilizando **Streamlit**.

## 🚀 Como Executar

### 1️⃣ Instalar Dependências

Antes de executar o projeto, instale as dependências necessárias:

```bash
pip install requests streamlit
```

### 2️⃣ Configurar Tokens de Acesso

Os tokens de acesso aos aplicativos do Facebook devem ser definidos no dicionário `TOKENS` dentro do código:

```python
TOKENS = {
    "App 1": "YOU-TOKEN-APP",
}
```

Substitua `YOU-TOKEN-APP` pelo seu token de acesso válido.

### 3️⃣ Executar o Aplicativo

Agora, basta rodar o aplicativo usando Streamlit:

```bash
streamlit run nome_do_arquivo.py
```

Substitua `nome_do_arquivo.py` pelo nome real do arquivo onde o código está salvo.

## ⚙️ Como Funciona

### 🔹 Obtenção de Contas de Anúncio
A função `obter_contas_de_anuncio(access_token)` busca todas as contas associadas ao token fornecido.

### 🔹 Listagem de Campanhas Ativas
A função `obter_campaigns_ativas(ad_account_id, access_token)` retorna todas as campanhas ativas de uma conta de anúncio.

### 🔹 Ajuste de Orçamento
A função `alterar_orcamento(ad_account_id, access_token, campaign_id, percentual, aumentar=True)` permite aumentar ou diminuir o orçamento da campanha.

### 🔹 Pausar ou Ativar Campanha
A função `pausar_ou_ativar_campanha(access_token, campaign_id, status)` permite alterar o status de uma campanha para `PAUSED` ou `ACTIVE`.

## 🛠 Possíveis Melhorias

- Suporte para múltiplos aplicativos com diferentes tokens.
- Implementação de autenticação OAuth para maior segurança.
- Histórico de alterações para acompanhamento das mudanças nos orçamentos.
- Adicionar suporte para relatórios de desempenho das campanhas.

## 📜 Licença

Este projeto é open-source e pode ser modificado conforme necessário.

---

**Desenvolvido com ❤️ para facilitar o gerenciamento de campanhas no Facebook Ads!**
