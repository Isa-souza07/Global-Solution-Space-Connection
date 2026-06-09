# Global-Solution-Space-Connection
# Mission Control AI 🚀

O Mission Control AI é um sistema construído em Python que monitora e avalia os parâmetros vitais de uma base de mineração espacial, como níveis de oxigênio, estabilidade estrutural e temperatura. A Inteligência Artificial (modelo local *Llama 3.2* via Ollama) está integrada à lógica do código para atuar como Diretora de Controle da missão, interpretando o status em tempo real para emitir alertas e recomendar planos de ação imediatos diante de cenários críticos.

## 👥 Integrantes

1. **Gustavo Gamba Zancopé** — RM: 569287
2. **Isabela Camargo Souza** — RM: 569196
3. **Artur Souza Pereira** — RM: 570880

---

## 🔗 Links Importantes

- **Repositório GitHub:** [Acessar Repositório](https://github.com/Isa-souza07/Global-Solution-Space-Connection)
- **Vídeo de Demonstração:** [Assistir no YouTube](https://youtu.be/xpTfYVj9-kw)

---

## 🛠️ Como executar no Google Colab

1. **Abra o notebook diretamente pelo link abaixo:**
   👉 [Acessar Notebook no Google Colab](https://colab.research.google.com/drive/1clt2L6IpnvyFw_7yAgV5P-IsibchOqS8?usp=sharing)

2. **Execute as células na seguinte ordem:**
   - Instalação e inicialização do `Ollama`.
   - Download do modelo `llama3.2:1b` e import da biblioteca `ollama`.
   - Definição das constantes, funções de classificação e análise de regras lógicas.
   - Execução das funções da IA (conclusão da missão, ciclo manual e LIDAR).
   - Execução do bloco de ciclo manual para testar leituras em tempo real.
   - Executar a célula da função `menu()` para acessar o painel interativo.

3. **Utilize o menu textual para interagir com o sistema:**
   - Visualizar os dados brutos simulados da missão.
   - Rodar a análise completa (geração do relatório lógico + avaliação da IA).
   - Visualizar o status do último ciclo executado.
   - Utilizar o módulo LIDAR com IA para determinar o alvo ideal de perfuração.

---

## 📸 Demonstração do Sistema

Abaixo, evidenciamos a integração do sistema Python com o modelo de linguagem Llama 3.2, atuando como Diretor de Controle da Missão.

![Código de Integração da IA](PromptandArtificialIntelligence/assets/dados_missao.png)
*Trecho do código responsável por formular o prompt de contexto e realizar a chamada ao modelo via Ollama, passando os dados processados pelo sistema lógico.*

![Execução e Alerta Crítico](https://github.com/Isa-souza07/Global-Solution-Space-Connection/blob/main/Prompt%20and%20Artificial%20Intelligence/assets/alerta_critico.png)
*Execução do ciclo manual com parâmetros críticos. O sistema lógico emite a pontuação de risco e, em seguida, a Inteligência Artificial processa o contexto para recomendar o plano de contingência imediato.*
