# Aplicação Sobre o Mercado de Criptomoedas

Repositório com informações sobre o mercado de criptomoedas. Este projeto coleta dados atualizados de criptomoedas da API CoinCap, armazena em um banco de dados PostgreSQL no GCP Cloud SQL e visualiza os dados no Power BI.

## Visão Geral

O projeto automatiza a coleta de dados de criptomoedas, armazenando-os de forma organizada e permitindo análise visual. De forma geral, três criptomoedas foram escolhidas para serem analisadas: **Bitcoin, Ethereum e Solana.**

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
    * Utilizei um filtro para pegar três criptomoedas em específico: Bitcoin, Ethereum e Solana.
* **Limitação de Acesso:**
    * A função `tratar_limite_requisicoes` implementa um mecanismo de espera exponencial para lidar com o limite de requisições da API, garantindo a coleta contínua de dados.

### Modelagem de Dados

* **Estrutura de Dados:**
    * Os dados coletados são armazenados em DataFrames Pandas, facilitando a manipulação e o processamento.
    * As funções `inserir_assets()`, `inserir_asset_por_id()`, `inserir_historico_asset()`, `inserir_exchanges()` e `inserir_markets()` indicam a criação de tabelas correspondentes no banco de dados.
    * As colunas dos Dataframes são mapeadas para colunas nas tabelas do banco de dados.
* **Tabelas no Banco de Dados:**
    * O código adiciona valores nas tabelas no banco de dados para representar as criptomoedas e seus atributos relevantes.
    * O codigo utiliza tratamento de erro para não inserir dados duplicados nas tabelas e para acrescentar, diariamente, os dados daquele dia.
 
     ![Captura de tela 2025-02-27 154656](https://github.com/user-attachments/assets/dc773838-192f-4c84-aa5b-5b50b2794883)
 

### Banco de Dados

* **Escolha e Configuração:**
    * O código utiliza o banco de dados relacional PostgreSQL, hospedado no GCP Cloud SQL.
    * A biblioteca `psycopg2` é usada para conectar ao banco de dados e executar consultas SQL.
    * A função `conectar_banco()` é responsavel por criar esta conexão.
      
  ![image](https://github.com/user-attachments/assets/8f18cbaa-a6fb-4fc3-91d0-2cf1bd4637b7)


### Armazenamento Eficiente

* **Mecanismo de Armazenamento:**
    * As funções `inserir_assets()`, `inserir_asset_por_id()`, `inserir_historico_asset()`, `inserir_exchanges()` e `inserir_markets()` são responsáveis por inserir e atualizar os dados no banco de dados.
    * O código utiliza tratamento de erros para garantir a consistência e a integridade das informações, evitando a inserção de dados duplicados.
    * O código itera sobre os dataframes Pandas, e insere linha por linha no banco de dados.

### Configuração Externa

* **Parâmetros Externos:**
    * Para melhorar a segurança e a flexibilidade, foi criado um arquivo `.env` para armazenar as credenciais de conexão com o banco de dados e outras variáveis de ambiente sensíveis. **Arquivo precisa ser criado na máquina local para funcionar**
    * Todas às informações referentes a este arquivo foram enviadas por e-mail.

### Boas Práticas

* **Código Limpo e Organizado:**
    * **Modularização:** O código é dividido em funções bem definidas, cada uma com uma responsabilidade específica, facilitando a leitura e a manutenção. Funções como `pegarAssets()`, `pegarAssetPorId()`, `inserir_assets()`, e `conectar_banco()` demonstram essa prática.
    * O tratamento de erros é implementado em várias partes do código, garantindo a robustez do programa.
    * O código utiliza bibliotecas populares e bem documentadas, como `requests`, `pandas` e `psycopg2`.

### Visualização de Dados

* O Power BI foi conectado ao banco de dados para criar o dashboard.
* O dashboard mostra informações como capitalização de mercado, volume de negociação e histórico de preços.

### Infraestrutura GCP

* Toda a infraestrutura está no GCP, usando Cloud SQL para o banco de dados e o Colab para a criação do notebook.

 ![image](https://github.com/user-attachments/assets/e755ec51-fa90-49b9-ae58-2ada475ded69)


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

A etapa final do projeto consistiu na criação de um dashboard no Power BI para informar, de forma visual, os dados coletados pela API. Informações como: volume de transação nas últimas 24 horas, **quantidade de criptomoedas coletadas e preço médio das criptomoedas** são exemplos de dados que podem ser observados no painel.

![Captura de tela 2025-02-27 155242](https://github.com/user-attachments/assets/e734aee0-481f-450f-8ce9-c82c76f32d05)

### Insights

Através da coleta e a visualização do painel, é possível observar que a moeda Bitcoin é a que mais tem movimentações diárias. Também é possivel notar que a exchange Binance é a mais utilizada, seguida da gdax e cripto, respectivamente.

### Para o Futuro

Implementar um sistema de alertas que notifica os usuários sobre mudanças significativas no mercado de criptomoedas (por exemplo, variações de preço, volume de negociação).
