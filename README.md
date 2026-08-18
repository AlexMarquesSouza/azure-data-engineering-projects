# Radar de Engenharia de Dados · Azure

Projetos incrementais e práticos sobre engenharia de dados no Microsoft Azure.

| # | Projeto | Conceitos | Nível | Status |
|---:|---|---|---|---|
| 000 | [Configuração do ambiente](000-configuracao-ambiente/README.md) | VS Code, Python, Git, Azure CLI opcional | Fundamentos | Rascunho para revisão |
| 001 | [Pipeline Medalhão de Vendas](001-medallion-vendas/README.md) | Blob/ADLS, qualidade, bronze/silver/gold | Iniciante | Rascunho para revisão |
| 002 | [Carga incremental com watermark](002-carga-incremental-watermark/README.md) | Data Factory, delta, estado | Iniciante | Rascunho para revisão |
| 003 | [Dimensão histórica SCD Tipo 2](003-dimensao-scd2-clientes/README.md) | Fabric, Data Warehouse, histórico | Iniciante/intermediário | Rascunho para revisão |
| 004 | [Telemetria com janelas fixas](004-janelas-stream-analytics/README.md) | Event Hubs, Stream Analytics, tumbling window | Intermediário | Rascunho para revisão |
| 005 | [Observabilidade de pipelines](005-observabilidade-pipelines/README.md) | Data Factory, Azure Monitor, SLA | Intermediário | Rascunho para revisão |
| 006 | [Lifecycle para ADLS](006-lifecycle-adls/README.md) | Blob Storage, tiers, FinOps | Intermediário | Rascunho para revisão |
| 007 | [Roteador de arquivos com Event Grid](007-event-grid-file-router/README.md) | Event Grid, Blob events, idempotência | Intermediário | Rascunho para revisão |
| 008 | [Advisor de partition key Cosmos DB](008-cosmos-partition-key-advisor/README.md) | Cosmos DB, RU, cardinalidade | Intermediário | Rascunho para revisão |
| 009 | [Upsert idempotente Delta Lake](009-delta-merge-upsert/README.md) | Databricks, Delta, MERGE | Intermediário | Rascunho para revisão |
| 010 | [Otimizador de leitura Synapse](010-synapse-scan-optimizer/README.md) | Synapse Serverless, Parquet, I/O | Intermediário | Rascunho para revisão |
| 011 | [Validador de linhagem do Purview](011-purview-lineage-validator/README.md) | Purview, linhagem, análise de impacto | Intermediário | Rascunho para revisão |
| 012 | [Planejador de reprocessamento ADF](012-adf-tumbling-window-reprocess-planner/README.md) | ADF, tumbling windows, ordenação topológica | Intermediário | Rascunho para revisão |
| 013 | [Linter de Key Vault no ADF](013-adf-key-vault-reference-linter/README.md) | ADF, Key Vault, secret management | Intermediário | Rascunho para revisão |
| 014 | [Advisor de compactação Delta](014-databricks-small-files-compaction-advisor/README.md) | Databricks, Delta, pequenos arquivos | Intermediário | Rascunho para revisão |

## Regra editorial

Nenhum projeto deste radar deve ser publicado, enviado a um repositório remoto ou implantado no Azure sem revisão e autorização manual.

Cada projeto também deve explicar explicitamente:

- as ferramentas, bibliotecas e recursos de cloud utilizados;
- a função de cada ferramenta dentro da solução;
- os conceitos de engenharia de dados demonstrados;
- os pré-requisitos, custos ou recursos externos opcionais;
- o que foi executado e validado localmente;
- tecnologias relacionadas que ainda não fazem parte daquela versão.


## Manutenção deste repositório

Este diretório é autônomo: contém documentação, dependências do site, testes estruturais e scripts próprios. Após clonar:

```bash
cd "caminho/para/azure-data-engineering-projects"
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-docs.txt
python3 scripts/validate_projects.py
bash scripts/build_site.sh
```

O build gera somente documentação local. Publicação, criação de repositório remoto e `git push` continuam manuais.
