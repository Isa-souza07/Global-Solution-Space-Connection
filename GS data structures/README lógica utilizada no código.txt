## Explicação da lógica utilizada
=============================

Link do vídeo de execução do código: https://youtu.be/I1qYDpH9Qh8

============================

O sistema Mission Control AI — Mineração Espacial foi desenvolvido em Python com o objetivo de simular o monitoramento operacional de uma missão espacial experimental voltada para uma base de mineração. A lógica do programa se baseia na leitura de dados simulados de diferentes áreas da missão, como temperatura da base, comunicação com a estação orbital, sistema de energia, suporte de oxigênio e estabilidade estrutural da escavação.

Os dados da missão são organizados em uma matriz, onde cada linha representa um ciclo de monitoramento e cada coluna representa um parâmetro analisado. Dessa forma, o programa consegue percorrer todos os ciclos utilizando laços de repetição e avaliar individualmente cada valor registrado.

Para cada área monitorada, foram criadas funções específicas de classificação. Essas funções analisam o valor recebido e retornam um status de acordo com limites definidos no código. Os status possíveis são `NORMAL`, `ATENÇÃO` e `CRÍTICO`. Por exemplo, valores muito baixos de energia podem indicar risco operacional, enquanto temperaturas muito elevadas podem representar superaquecimento dos módulos da base.

Após a classificação de cada parâmetro, o sistema atribui uma pontuação de risco para cada status. O status `NORMAL` recebe 0 pontos, `ATENÇÃO` recebe 1 ponto e `CRÍTICO` recebe 2 pontos. A soma desses pontos define a situação geral de cada ciclo da missão. Com base nessa pontuação, o ciclo pode ser classificado como `MISSÃO ESTÁVEL`, `MISSÃO EM ATENÇÃO` ou `MISSÃO CRÍTICA`.

Além da análise individual dos ciclos, o programa também calcula um resumo geral da missão. Esse resumo inclui a quantidade de ciclos analisados, o ciclo mais crítico, a maior pontuação de risco, o risco médio, a tendência da missão, a área mais afetada e as médias dos principais sistemas monitorados. Essas informações ajudam a transformar os dados brutos em uma visão mais clara da situação operacional.

O sistema também possui uma lógica de recomendação automática. Caso algum parâmetro esteja em estado crítico, o programa gera uma recomendação específica para aquela área, como reduzir operações não essenciais, restabelecer comunicação, economizar energia ou priorizar suporte à vida. Se não houver estado crítico, mas existirem áreas em atenção, a recomendação é manter o monitoramento e preparar um plano de contingência. Caso todos os sistemas estejam normais, a recomendação é manter a operação.

Outra parte do código simula um planejamento de perfuração com base em um perfil LIDAR. Esse perfil contém profundidade, tipo de material, concentração de minério e risco de gás. O sistema analisa esses dados e escolhe automaticamente o melhor ponto de perfuração, considerando a maior concentração de minério possível sem ultrapassar limites de segurança.

A versão adaptada do código também possui uma análise textual automatizada. Quando a biblioteca Ollama está disponível no computador, o sistema pode gerar uma explicação mais natural sobre a situação da missão. Caso a IA local não esteja instalada ou não esteja funcionando, o programa continua operando normalmente com uma resposta lógica padrão, garantindo que o funcionamento principal não dependa obrigatoriamente da inteligência artificial.

Por fim, o programa utiliza um menu interativo no terminal, permitindo ao usuário visualizar os dados brutos, executar a análise completa, consultar o último ciclo, inserir uma nova leitura manual, acessar o histórico de análises, executar o planejamento de perfuração e encerrar o sistema. Com isso, o projeto aplica estruturas condicionais, laços de repetição, listas, matrizes e funções para organizar a lógica de monitoramento da missão espacial.
