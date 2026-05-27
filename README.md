# 🔥 PyroSat — Sistema de Alerta Precoce de Queimadas

**Disciplina:** SDTCC — Secure DevOps Tools & Cloud Computing  
**Global Solution — Indústria Espacial**  
**ODS Conectados:** 13 (Ação Climática) · 15 (Vida Terrestre) · 11 (Cidades Seguras)

---

## 🛰️ Sobre o projeto

O PyroSat é uma plataforma de alerta precoce de queimadas que utiliza dados orbitais (INPE/NASA FIRMS) para detectar focos de calor em tempo real, prever propagação de incêndios com base em dados de vento, umidade e vegetação, e acionar automaticamente a defesa civil.

**Problema:** O Brasil perde milhões de hectares por ano para queimadas. Os dados satelitais existem, mas não há sistema integrado que cruze focos de calor + previsão de vento + tipo de vegetação + histórico para prever propagação nas próximas horas.

**Solução:** Dashboard web com mapa de calor interativo hospedado no Azure, com pipeline CI/CD automatizado e monitoramento ativo.

---

## 🏗️ Arquitetura Azure

```
GitHub (código)
    │
    ├── GitHub Actions (CI/CD Pipeline)
    │       ├── Checkout + Build
    │       ├── Login Azure (via AZURE_CREDENTIALS secret)
    │       └── Deploy → Azure App Service
    │
Azure Subscription
    ├── Resource Group: rg-pyrosat
    ├── App Service Plan: asp-pyrosat (Linux, B1)
    ├── App Service: pyrosat-app (Python 3.11)
    ├── Key Vault: kv-pyrosat
    │       └── Secret: azure-credentials
    └── Application Insights: ai-pyrosat
            ├── Alert Rule: focos-criticos
            └── Log Stream (monitoramento ao vivo)
```

---

## 🔐 Segurança (DevSecOps)

| Prática | Implementação |
|---|---|
| Credenciais | Azure Service Principal no GitHub Secrets (`AZURE_CREDENTIALS`) |
| Key Vault | `kv-pyrosat` com secret `azure-credentials` vinculado |
| HTTPS | Habilitado por padrão no Azure App Service |
| IAM | Role Assignment: `Contributor` no Resource Group `rg-pyrosat` |
| Código | Nenhuma senha ou chave exposta no código-fonte |

---

## 📊 Monitoramento

- **Application Insights**: ativo, instrumentação automática
- **Alert Rule**: `alerta-focos-criticos` — condition: requests > 100/min, severity: 2
- **Log Stream**: evidência de uso durante testes via Azure Portal

---

## 🚀 Deploy

A cada `git push` na branch `main`, o GitHub Actions:
1. Faz checkout do código
2. Configura Python 3.11
3. Instala dependências
4. Login no Azure com `AZURE_CREDENTIALS` (secret)
5. Deploy automático no App Service
6. Confirmação de deploy com URL pública

---

## 🌐 Endpoints

| Rota | Descrição |
|---|---|
| `/` | Dashboard principal com mapa interativo |
| `/api/fires` | JSON com focos ativos (INPE/NASA simulado) |
| `/api/alerts` | JSON com alertas de propagação |
| `/api/stats` | Estatísticas globais |
| `/health` | Health check da aplicação |

---

## 🔧 Como rodar localmente

```bash
pip install -r requirements.txt
python app.py
# Acesse: http://localhost:8000
```
## RM's

André Soler - RM98827
Fabrizio Maia - RM551869
Rodrigo Paixão - RM968669
Victor Asfur - RM551684
Vitor Shimizu - RM550390
