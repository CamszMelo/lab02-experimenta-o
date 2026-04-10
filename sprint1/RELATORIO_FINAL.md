# Relatório Final: Um Estudo das Características de Qualidade de Sistemas Java

## 1. Introdução e Hipóteses

Este estudo visa analisar a qualidade interna de repositórios Java populares no GitHub, utilizando métricas de produto (CK) e correlacionando-as com métricas de processo (popularidade, maturidade, atividade e tamanho).

### Hipóteses Informais:
*   **RQ 01 (Popularidade):** Espera-se que repositórios mais populares tenham melhor qualidade (menor acoplamento e maior coesão), devido ao maior escrutínio da comunidade.
*   **RQ 02 (Maturidade):** Repositórios mais antigos podem apresentar maior complexidade e acoplamento devido ao acúmulo de código legado.
*   **RQ 03 (Atividade):** Uma alta taxa de releases pode indicar um projeto bem mantido, possivelmente com métricas de qualidade estáveis.
*   **RQ 04 (Tamanho):** Projetos maiores tendem a ter maior acoplamento (CBO) e maior profundidade de herança (DIT) naturalmente devido à sua escala.

## 2. Metodologia

A coleta de dados foi realizada em duas etapas:
1.  **Métricas de Processo:** Coletadas via API GraphQL do GitHub para os repositórios Java mais populares.
2.  **Métricas de Qualidade:** Utilizou-se a ferramenta **CK** para extrair métricas de classe (CBO, DIT, LCOM) após o clone superficial (`--depth=1`) de cada repositório.

Para este relatório, analisamos uma amostra de 10 repositórios altamente populares para validar o pipeline e extrair tendências iniciais.

## 3. Resultados e Análise Estatística

Os dados foram sumarizados utilizando a média, mediana e desvio padrão. Abaixo, apresentamos as correlações de Spearman (p-valor < 0.05 indica significância estatística).

### Tabela de Correlações (Spearman)

| Relação (X vs Y) | Coeficiente (r) | P-valor | Observação |
| :--- | :--- | :--- | :--- |
| **Tamanho (LOC) vs CBO** | 0.97 | < 0.001 | Correlação Positiva Forte |
| **Tamanho (LOC) vs DIT** | 0.91 | 0.001 | Correlação Positiva Forte |
| **Atividade (Releases) vs CBO** | 0.71 | 0.047 | Correlação Positiva Moderada |
| **Popularidade (Stars) vs CBO** | -0.31 | 0.452 | Sem significância |
| **Maturidade (Idade) vs DIT** | 0.50 | 0.199 | Sem significância |

## 4. Discussão

*   **RQ 01 (Popularidade):** Não encontramos uma correlação estatisticamente significativa entre estrelas e qualidade na nossa amostra. Isso sugere que a popularidade externa não garante necessariamente uma estrutura interna superior.
*   **RQ 02 (Maturidade):** A idade do projeto mostrou uma tendência positiva com a profundidade de herança, mas sem significância estatística na amostra reduzida.
*   **RQ 03 (Atividade):** O número de releases correlacionou-se positivamente com o acoplamento. Projetos com muitas entregas tendem a crescer em interdependência.
*   **RQ 04 (Tamanho):** Esta foi a correlação mais forte. Quanto maior o código (LOC), maiores são o acoplamento (CBO) e a complexidade da hierarquia (DIT). Isso valida a hipótese de que o crescimento do sistema traz desafios inerentes de design.

## 5. Conclusão

O estudo demonstra que o tamanho do sistema é o principal preditor de métricas de acoplamento e herança em sistemas Java. Embora a popularidade seja um indicador de relevância, ela não substitui a necessidade de monitoramento contínuo da qualidade interna, especialmente à medida que o projeto cresce em linhas de código e número de lançamentos.

---
*Relatório gerado automaticamente como parte do Laboratório de Experimentação de Software.*
