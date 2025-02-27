# Aplicação Sobre o Mercado de Criptomoedas

Repositório com informações sobre o mercado de criptomoedas. Este projeto coleta dados atualizados de criptomoedas da API CoinCap, armazena em um banco de dados PostgreSQL no GCP Cloud SQL e visualiza os dados no Power BI.

## Visão Geral

O projeto automatiza a coleta de dados de criptomoedas, armazenando-os de forma organizada e permitindo análise visual.

## Detalhes Operacionais

### Conexão com a API

* **Implementação:**
    * O código utiliza a biblioteca `requests` do Python para realizar solicitações HTTP à API da CoinCap.
    * Funções como `pegarAssets()`, `pegarAssetPorId()`, `pegarHistoricoAsset()`, `pegarExchanges()` e `pegarMarkets()` são responsáveis por fazer as requisições aos diferentes endpoints da API.
    * O tratamento de erros, como o limite de requisições (código 429), é implementado na função `tratar_limite_requisicoes`, garantindo que a conexão seja resiliente.
* **Dados Estruturados:**
    * Os dados recebidos da API estão no formato JSON.
    * O código utiliza a biblioteca `json` para processar esses dados e convertê-los em dicionários Python.
    * Em seguida, esses dicionarios são convertidos em DataFrames Pandas, para melhor manipulação.

### Coleta de Dados

* **Informações Atualizadas:**
    * O código foi projetado para coletar dados atualizados sobre criptomoedas da API CoinCap.
    * A frequência de coleta pode ser ajustada conforme necessário.
* **Escopo da Coleta:**
    * O código coleta dados de todas as criptomoedas disponíveis na API, abrangendo informações como preço, capitalização de mercado e volume de negociação.
    * Também é possível coletar dados de criptomoedas específicas, se necessário.
* **Limitação de Acesso:**
    * A função `tratar_limite_requisicoes` implementa um mecanismo de espera exponencial para lidar com o limite de requisições da API, garantindo a coleta contínua de dados.

### Modelagem de Dados

* **Estrutura de Dados:**
    * Os dados coletados são armazenados em DataFrames Pandas, facilitando a manipulação e o processamento.
    * As funções `inserir_assets()`, `inserir_asset_por_id()`, `inserir_historico_asset()`, `inserir_exchanges()` e `inserir_markets()` indicam a criação de tabelas correspondentes no banco de dados.
    * As colunas dos Dataframes são mapeadas para colunas nas tabelas do banco de dados.
* **Tabelas no Banco de Dados:**
    * O código cria tabelas no banco de dados para representar as criptomoedas e seus atributos relevantes.
    * No mínimo duas tabelas são criadas: uma para informações gerais das criptomoedas e outra para o histórico de preços.
    * O codigo utiliza tratamento de erro para não inserir dados duplicados nas tabelas.

### Banco de Dados

* **Escolha e Configuração:**
    * O código utiliza o banco de dados relacional PostgreSQL, hospedado no GCP Cloud SQL.
    * A biblioteca `psycopg2` é usada para conectar ao banco de dados e executar consultas SQL.
    * A função `conectar_banco()` é responsavel por criar está conexão.

### Armazenamento Eficiente

* **Mecanismo de Armazenamento:**
    * As funções `inserir_assets()`, `inserir_asset_por_id()`, `inserir_historico_asset()`, `inserir_exchanges()` e `inserir_markets()` são responsáveis por inserir e atualizar os dados no banco de dados.
    * O código utiliza tratamento de erros para garantir a consistência e a integridade das informações, evitando a inserção de dados duplicados.
    * O código itera sobre os dataframes Pandas, e insere linha por linha no banco de dados.

### Configuração Externa

* **Parâmetros Externos:**
    * As credenciais de conexão com o banco de dados são definidas diretamente no código.
    * Para melhorar a segurança e a flexibilidade, é recomendável usar variáveis de ambiente ou arquivos de configuração externos.

### Boas Práticas

* **Código Limpo e Organizado:**
    * **Modularização:** O código é dividido em funções bem definidas, cada uma com uma responsabilidade específica, facilitando a leitura e a manutenção. Funções como `pegarAssets()`, `pegarAssetPorId()`, `inserir_assets()`, e `conectar_banco()` demonstram essa prática.
    * O tratamento de erros é implementado em várias partes do código, garantindo a robustez do programa.
    * O código utiliza bibliotecas populares e bem documentadas, como `requests`, `pandas` e `psycopg2`.

### Visualização de Dados

* Conectamos o Power BI ao banco de dados para criar dashboards e visualizações.
* Os dashboards mostram informações como capitalização de mercado, volume de negociação e histórico de preços.

### Infraestrutura GCP

* Toda a infraestrutura está no GCP, usando Cloud SQL para o banco de dados.
* O uso do GCP garante escalabilidade e confiabilidade.

## Instalação

1.  Clone este repositório para sua máquina local.
2.  Navegue até o diretório do projeto: `cd nome-do-repositorio`
3.  Crie um arquivo `.env` na raiz do projeto e adicione as credenciais de banco de dados (enviadas por e-mail).
   * Observação: Por motivos de segurança, enviei as credenciais por e-mail. Qualquer dúvida, pode me chamar: eudanieljunges@gmail.com
4.  Instale as dependências do projeto: `pip install -r requirements.txt`

**Observações:**

Certifique-se de que o Python esteja instalado em seu sistema e disponível no PATH. Você pode verificar a instalação abrindo o terminal e executando o comando python --version

## Execução

Para executar o script, utilize o seguinte comando:

```bash
python caseTecnicoCadastra.py
```

![Captura de tela 2025-02-27 151748](https://github.com/user-attachments/assets/5a105e9b-68c0-49ad-a570-bd875dffb6e1)

O código vai mostrar o status do load de cada tabela para o Postgres. Por estar rodando local, pode demorar entre 5-10 minutos para toda a execução ser finalizada.


### Power BI

