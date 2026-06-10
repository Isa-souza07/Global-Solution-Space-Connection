# Mission Control AI — Mineração Espacial

## Integrantes

* **Artur Souza Pereira** — RM 570880
* **Isabela Camargo Souza** — RM 569196
* **Gustavo Gamba Zancopé** — RM 569287

Link do repositório GitHub: https://github.com/Isa-souza07/Global-Solution-Space-Connection

Link do vídeo do youtube: https://youtu.be/-k_aVcKBQZA


## Descrição do Projeto

O **Mission Control AI — Mineração Espacial** é um sistema desenvolvido em Python para simular o monitoramento inteligente de uma missão espacial experimental, com foco em segurança operacional, eficiência energética e sustentabilidade.

O projeto representa uma base de mineração espacial chamada **Orion Mining Alpha**, onde diferentes módulos da operação precisam ser monitorados continuamente para evitar falhas críticas, desperdício de energia e riscos para a equipe.

A solução interpreta dados simulados da missão, classifica os sistemas monitorados, gera alertas automáticos e apresenta recomendações para apoiar a tomada de decisão da equipe de controle.

## Objetivo

O objetivo do sistema é analisar dados simulados de uma missão espacial experimental, aplicando conceitos de programação, lógica computacional, tomada de decisão e sustentabilidade.

O foco principal está no monitoramento de recursos essenciais da operação, principalmente o **sistema de energia da mina**, que representa o controle de baterias, painéis, reatores e equipamentos essenciais para o funcionamento da base.

## Relação com Energias Renováveis e Sustentáveis

Em uma missão espacial, o uso eficiente da energia é essencial para manter os sistemas vitais funcionando. Como os recursos são limitados, o sistema precisa identificar rapidamente situações de risco e priorizar os módulos mais importantes.

Este projeto se conecta ao tema de **Energias Renováveis e Sustentáveis** porque simula uma operação em que a energia deve ser monitorada, economizada e direcionada para sistemas críticos quando necessário.

Quando o sistema identifica energia em nível crítico, ele recomenda ações como ativar o modo de economia de energia e priorizar os sistemas vitais da colônia. Dessa forma, a solução busca representar uma operação mais segura, eficiente e sustentável.

## Funcionalidades

O sistema possui as seguintes funcionalidades:

* Monitoramento de dados simulados da missão;
* Análise de temperatura da base de mineração;
* Análise da comunicação com a estação orbital;
* Análise do sistema de energia da mina;
* Análise do suporte de oxigênio da colônia;
* Análise da estabilidade estrutural da escavação;
* Classificação dos sistemas em `NORMAL`, `ATENÇÃO` ou `CRÍTICO`;
* Pontuação de risco para cada ciclo da missão;
* Geração automática de recomendações;
* Relatório completo da missão;
* Consulta ao último ciclo registrado;
* Histórico de análises executadas;
* Planejamento de perfuração com perfil LIDAR;
* Menu interativo no terminal.

## Como o Sistema Funciona

O código começa definindo as áreas monitoradas da missão em uma lista chamada `areas_monitoradas`. Essas áreas representam os principais módulos da base de mineração espacial.

Em seguida, os dados simulados são armazenados na matriz `dados_missao`. Cada linha da matriz representa um ciclo de monitoramento, e cada coluna representa uma leitura da missão, como temperatura, comunicação, energia, oxigênio e estabilidade.

Cada valor é analisado por funções específicas de classificação. Por exemplo:

* `classificar_temperatura()` analisa a temperatura da base;
* `classificar_comunicacao()` analisa o nível de comunicação;
* `classificar_bateria()` analisa o sistema de energia da mina;
* `classificar_oxigenio()` analisa o suporte de oxigênio;
* `classificar_estabilidade()` analisa a estabilidade estrutural.

Cada função retorna um status: `NORMAL`, `ATENÇÃO` ou `CRÍTICO`.

Depois disso, o sistema converte cada status em uma pontuação de risco:

* `NORMAL` = 0 pontos;
* `ATENÇÃO` = 1 ponto;
* `CRÍTICO` = 2 pontos.

A soma dos pontos define o estado geral de cada ciclo da missão:

* 0 a 2 pontos: `MISSÃO ESTÁVEL`;
* 3 a 5 pontos: `MISSÃO EM ATENÇÃO`;
* 6 pontos ou mais: `MISSÃO CRÍTICA`.

Com base nessa análise, o sistema gera recomendações automáticas. Caso algum módulo esteja em estado crítico, a recomendação é direcionada para aquela área. Por exemplo, se o sistema de energia estiver crítico, o programa recomenda ativar economia de energia e priorizar sistemas vitais.

## Planejamento LIDAR

Além do monitoramento da missão, o projeto também possui uma simulação de planejamento de perfuração com LIDAR.

O perfil LIDAR armazena informações como:

* profundidade;
* tipo de material;
* concentração de minério;
* risco de gás.

A função `escolher_alvo_perfuracao()` analisa esses dados e escolhe o melhor ponto de perfuração com base em um critério simples: maior concentração de minério com risco de gás aceitável.

Essa funcionalidade reforça a proposta sustentável do projeto, pois a operação não busca apenas produtividade, mas também segurança, redução de riscos e uso mais eficiente dos recursos.

## Estruturas de Programação Utilizadas

O projeto utiliza diferentes conceitos de programação, como:

* Variáveis;
* Listas;
* Matrizes;
* Tuplas;
* Dicionários;
* Funções;
* Estruturas condicionais;
* Laços de repetição;
* Entrada de dados pelo usuário;
* Menu interativo;
* Organização modular do código.

## Tecnologias Utilizadas

* Python 3
* VS Code ou PyCharm
* Terminal/Prompt de Comando
* GitHub para versionamento e entrega do projeto

## Como Executar o Projeto

1. Baixe ou clone este repositório.
2. Abra o arquivo `mission_control.py` em uma IDE, como VS Code ou PyCharm.
3. Execute o arquivo Python.
4. Use o menu interativo exibido no terminal.
5. Escolha as opções desejadas para visualizar dados, executar análises ou acessar o planejamento LIDAR.

## Menu do Sistema

Ao executar o programa, o usuário pode escolher entre as seguintes opções:

1. Visualizar dados brutos da missão;
2. Executar análise completa;
3. Visualizar status do último ciclo;
4. Histórico de análises;
5. Planejamento de perfuração com LIDAR;
6. Encerrar sistema.

## Exemplo de Uso

Ao selecionar a opção de análise completa, o sistema percorre todos os ciclos da missão, classifica cada módulo monitorado, calcula a pontuação de risco e exibe uma recomendação para a equipe.

No relatório final, o programa mostra:

* quantidade de ciclos analisados;
* médias dos sistemas monitorados;
* ciclo mais crítico;
* maior pontuação de risco;
* risco médio da missão;
* quantidade de ciclos críticos;
* tendência da missão;
* área mais afetada;
* classificação final da missão.

## Conclusão

O **Mission Control AI — Mineração Espacial** demonstra como a programação pode ser aplicada ao monitoramento de sistemas energéticos e operacionais em uma missão espacial experimental.

A solução permite interpretar dados simulados, identificar riscos, gerar alertas e sugerir ações automáticas para a equipe de controle. Com isso, o projeto contribui para uma operação mais segura, eficiente e sustentável, principalmente no uso inteligente da energia e na preservação dos recursos críticos da missão.
