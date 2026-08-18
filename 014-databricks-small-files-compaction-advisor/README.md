# Advisor de compactação de pequenos arquivos

> Azure 014 · intermediário · Azure Databricks e Delta Lake

Agrupa um inventário por partição, mede a proporção de arquivos menores que 8 MB e recomenda `OPTIMIZE` apenas quando o problema é relevante.

![Arquitetura](docs/arquitetura.svg)

```bash
python3 -m src.advisor
python3 -m unittest discover -s tests -v
```

## Ferramentas, bibliotecas e recursos utilizados

| Item | Função |
|---|---|
| Python / CSV | Análise local do inventário |
| Azure Databricks | Plataforma de processamento representada |
| Delta Lake `OPTIMIZE` | Compactação idempotente por bin-packing |
| Partições e Parquet | Unidade de análise e arquivos colunares |

## Conceitos de Engenharia de Dados aplicados

Small-file problem, bin-packing, layout físico, pruning e equilíbrio entre custo de manutenção e desempenho de leitura.

## Pré-requisitos e possíveis custos

Python 3.10+ e custo local zero. `OPTIMIZE` usa compute Databricks e pode gerar custo; o projeto somente recomenda, sem executar SQL.

## O que foi validado

Dois testes cobrem partição fragmentada e arquivos saudáveis. A amostra recomenda compactar somente a partição com dez arquivos pequenos.

## Tecnologias relacionadas ainda não utilizadas

Sem Spark, Delta API, Unity Catalog, predictive optimization, auto compaction, liquid clustering, Z-Ordering, VACUUM ou cluster.

## Referências oficiais

- [Otimizar layout dos arquivos](https://learn.microsoft.com/en-us/azure/databricks/delta/optimize)
- [Controlar tamanho dos arquivos](https://learn.microsoft.com/en-us/azure/databricks/tables/tune-file-size)

Rascunho local; nada foi publicado.

## O que foi feito neste projeto

Foi construída uma versão local, segura e pequena do problema descrito no início do README. Os dados de exemplo permitem acompanhar entrada, regra aplicada e saída sem depender de uma conta Azure. A integração cloud citada representa a evolução arquitetural; ela não é executada automaticamente.

## Passo a passo detalhado

### 1. Prepare o ambiente

Conclua primeiro o [Projeto 00 — Configuração do ambiente](../000-configuracao-ambiente/README.md). Ele explica VS Code, Python, `.venv`, Git e a CLI opcional desta cloud. Depois, no terminal do VS Code, entre nesta pasta:

```bash
cd "caminho/para/azure-data-engineering-projects"
cd "014-databricks-small-files-compaction-advisor"
```

Confirme que `pwd` termina em `014-databricks-small-files-compaction-advisor`. Os caminhos relativos usados pelo código dependem disso.

### 2. Reconheça os arquivos antes de executar

- Abra `README.md` para entender problema, ferramentas e custos.
- Abra `data/` para conhecer os dados fictícios de entrada e, quando existir, a saída esperada.
- Abra `src/` e localize a função principal antes de modificá-la.
- Abra `tests/` e relacione cada cenário ao comportamento esperado.
- Abra `docs/arquitetura.svg` no Preview do VS Code para acompanhar o fluxo.

### 3. Execute a implementação original

Use os comandos documentados neste projeto. O primeiro roteiro executável é:

```bash
python3 -m src.advisor
python3 -m unittest discover -s tests -v
```

Leia toda a saída. Exit code `0` significa execução normal; quando o README declara achados intencionais, outro código pode representar uma validação que bloqueou corretamente um caso inseguro.

### 4. Valide de forma independente

```bash
python3 -m unittest discover -s tests -v
```

Não considere apenas `OK`: leia o nome de cada teste e confirme qual regra ele prova. Depois, inspecione `data/output/` ou os destinos indicados anteriormente neste README.

### 5. Faça uma alteração controlada

Altere um único valor nos dados de exemplo e preveja o resultado. Execute novamente, compare a saída e desfaça sua alteração manual caso ela seja apenas um experimento. Não use dados pessoais, credenciais ou recursos reais.

### 6. Registre evidência de aprendizagem

Anote o comando usado, a entrada alterada, o resultado observado, o teste que protege a regra e uma frase explicando como o serviço Azure participaria em produção. Capturas de tela isoladas não substituem essa evidência técnica.

## Solução de problemas

| Sintoma | Causa provável | Como resolver |
|---|---|---|
| `No module named src` | Terminal aberto na pasta errada | Execute `pwd` e entre na raiz deste projeto |
| Arquivo em `data/` não encontrado | Comando executado de outra pasta | Repita o `cd` mostrado no passo 1 |
| Versão ou sintaxe incompatível | Python anterior a 3.10 | Volte ao projeto 00 e selecione o interpretador correto no VS Code |
| Comando retorna código não zero | Pode haver achado didático intencional | Leia a saída e “O que foi validado” antes de tratar como defeito |
| Saída antiga ou inesperada | Resultado de execução anterior | Confira parâmetros; resultados locais não devem ser publicados |
| CLI cloud pede login ou permissão | A etapa local foi ultrapassada | Interrompa; autenticação só é opcional quando este README a explica |

## Checklist de conclusão

- [ ] Concluí o projeto 00 e abri esta pasta no VS Code.
- [ ] Consigo explicar o problema e a função de cada ferramenta listada.
- [ ] Li dados, código, testes e diagrama antes de executar.
- [ ] Executei o exemplo local e interpretei a saída.
- [ ] Executei os testes e sei qual regra cada um protege.
- [ ] Fiz uma alteração controlada usando somente dados fictícios.
- [ ] Registrei evidência e uma conclusão técnica.
- [ ] Não criei recursos pagos, não fiz deploy, não publiquei e não executei `git push`.
