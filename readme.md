# Racer Management System

## Descrição
O Racer Management System é uma aplicação desenvolvida com Flask, que permite gerenciar dados de corredores de Fórmula E. A aplicação simula dados de corredores, fornece informações sobre times e permite interação com uma interface gráfica utilizando Dear PyGui.

## Funcionalidades
- Simulação de dados de corredores com pontuação.
- API RESTful para acessar informações sobre corredores, equipes e pontuações.
- Interface gráfica para fácil interação e visualização dos dados.

## Tecnologias Utilizadas
- **Flask**: Framework web para Python.
- **Dear PyGui**: Biblioteca para criação de interfaces gráficas.
- **instagrapi**: Biblioteca para interação com Instagram (login).
- **Random**: Módulo para gerar dados aleatórios.

## Estrutura do Projeto
```
Racer Management System
│
├── app.py                # Arquivo principal que contém a lógica da aplicação
└── requirements.txt      # Dependências do projeto
```

## Como Rodar o Projeto

### Pré-requisitos
- Python 3.x
- Azure CLI (opcional, se for fazer o deploy na Azure)
- Apache Maven (opcional, se for fazer o deploy na Azure)

### Instalação
1. Clone o repositório:
   ```bash
   git clone https://github.com/SeuUsuario/RacerManagementSystem.git
   cd RacerManagementSystem
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Executando Localmente
1. Execute o arquivo principal:
   ```bash
   python app.py
   ```

2. Acesse a interface gráfica que será aberta na tela.

### Usando a API
A API está disponível nos seguintes endpoints:

- **GET /racer?name=<nome>**: Retorna informações sobre um corredor específico.
- **GET /racers**: Retorna uma lista de todos os corredores.
- **GET /team?team=<nome do time>**: Retorna corredores de uma equipe específica.
- **GET /teams**: Retorna todos os corredores organizados por equipe.
- **GET /top**: Retorna o corredor com a maior pontuação.
- **GET /points?field=<campo>&var=<valor>**: Retorna a soma de pontos de um corredor ou equipe específica.
- **POST /connect**: Conecta a uma conta do Instagram.

## Colaboradores do Projeto
<div style="display: flex; justify-content: space-between; align-items: center;">
<a href="https://github.com/AnaTorresLoureiro" target="_blank" style="text-align: center; margin-right: 10px;">
<img loading="lazy" src="https://avatars.githubusercontent.com/AnaTorresLoureiro" width=120>
<p style="font-size:min(2vh, 36px); margin-top: 10px;">Ana Laura Torres Loureiro - RM 554375</p>
</a>
<a href="https://github.com/MuriloCngp" target="_blank" style="text-align: center; margin-right: 10px;">
<img loading="lazy" src="https://avatars.githubusercontent.com/MuriloCngp" width=120>
<p style="font-size:min(2vh, 36px); margin-top: 10px;">Murilo Cordeiro Ferreira - RM 556727</p>
</a>
<a href="https://github.com/MateusLem" target="_blank" style="text-align: center; margin-right: 10px;">
<img loading="lazy" src="https://avatars.githubusercontent.com/MateusLem" width=120>
<p style="font-size:min(2vh, 36px); margin-top: 10px;">Mateus da Costa Leme - RM 557803</p>
</a>
<a href="https://github.com/Geronimo-augusto" target="_blank" style="text-align: center; margin-right: 10px;">
<img loading="lazy" src="https://avatars.githubusercontent.com/Geronimo-augusto" width=120>
<p style="font-size:min(2vh, 36px); margin-top: 10px;">	Geronimo Augusto Nascimento Santos - RM 557170</p>
</a>
<a href="https://github.com/Vitorr-AF" target="_blank" style="text-align: center; margin-right: 10px;">
<img loading="lazy" src="https://avatars.githubusercontent.com/Vitorr-AF" width=120>
<p style="font-size:min(2vh, 36px); margin-top: 10px;">Vitor Augusto França de Oliveira - RM 555469</p>
</a>
</div>
