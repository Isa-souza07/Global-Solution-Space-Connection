# -*- coding: utf-8 -*-

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Dict, List, Optional, Tuple

# -----------------------------------------------------------------------------
# Configurações principais
# -----------------------------------------------------------------------------

NOME_MISSAO = "Orion Mining Alpha"
EQUIPE = "Equipe Prospector"

# Altere para False caso não queira tentar usar o Ollama.
USAR_IA_LOCAL = True
MODELO_OLLAMA = "llama3.2:1b"
URL_OLLAMA = "http://localhost:11434/api/chat"

areas_monitoradas = [
    "Temperatura da base de mineração",
    "Comunicação com a estação orbital",
    "Sistema de energia da mina",
    "Suporte de oxigênio da colônia",
    "Estabilidade estrutural da escavação",
]

# Matriz de ciclos da missão:
# [temperatura, comunicacao, energia, oxigenio, estabilidade]
dados_missao = [
    [15, 92, 30, 96, 90],
    [22, 75, 72, 94, 85],
    [31, 65, 58, 91, 70],
    [36, 32, 38, 87, 25],
    [39, 28, 19, 88, 80],
    [34, 65, 32, 82, 66],
]

# Perfil LIDAR da área de mineração.
# Cada tupla representa:
# (profundidade_em_metros, tipo_de_material, concentracao_de_minerio, risco_de_gas)
perfil_lidar = [
    (0, "regolito superficial", 5, 0),
    (10, "rocha compacta", 25, 10),
    (20, "veia rica em minério", 80, 20),
    (30, "rocha frágil", 45, 50),
    (40, "camada com gás preso", 15, 90),
]

PONTOS_STATUS = {
    "NORMAL": 0,
    "ATENÇÃO": 1,
    "CRÍTICO": 2,
}


# -----------------------------------------------------------------------------
# Funções de classificação dos sensores
# -----------------------------------------------------------------------------

def classificar_temperatura(valor: float) -> str:
    if valor < 18:
        return "ATENÇÃO"
    if 18 <= valor <= 30:
        return "NORMAL"
    if 30 < valor <= 35:
        return "ATENÇÃO"
    return "CRÍTICO"


def classificar_comunicacao(valor: float) -> str:
    if valor < 30:
        return "CRÍTICO"
    if 30 <= valor <= 59:
        return "ATENÇÃO"
    return "NORMAL"


def classificar_energia(valor: float) -> str:
    if valor < 20:
        return "CRÍTICO"
    if 20 <= valor <= 49:
        return "ATENÇÃO"
    return "NORMAL"


def classificar_oxigenio(valor: float) -> str:
    if valor < 80:
        return "CRÍTICO"
    if 80 <= valor <= 89:
        return "ATENÇÃO"
    return "NORMAL"


def classificar_estabilidade(valor: float) -> str:
    if valor < 40:
        return "CRÍTICO"
    if 40 <= valor <= 69:
        return "ATENÇÃO"
    return "NORMAL"


def classificar_parametro(nome_area: str, valor: float) -> str:
    if nome_area == "Temperatura da base de mineração":
        return classificar_temperatura(valor)
    if nome_area == "Comunicação com a estação orbital":
        return classificar_comunicacao(valor)
    if nome_area == "Sistema de energia da mina":
        return classificar_energia(valor)
    if nome_area == "Suporte de oxigênio da colônia":
        return classificar_oxigenio(valor)
    if nome_area == "Estabilidade estrutural da escavação":
        return classificar_estabilidade(valor)
    return "DESCONHECIDO"


def classificar_ciclo_por_pontos(pontos: float) -> str:
    if 0 <= pontos <= 2:
        return "MISSÃO ESTÁVEL"
    if 3 <= pontos <= 5:
        return "MISSÃO EM ATENÇÃO"
    return "MISSÃO CRÍTICA"


# -----------------------------------------------------------------------------
# Descrições e recomendações
# -----------------------------------------------------------------------------

def descricao_curta(area: str, status: str) -> str:
    descricoes = {
        "Temperatura da base de mineração": {
            "NORMAL": "Temperatura interna estável para operação.",
            "ATENÇÃO": "Temperatura interna fora da faixa ideal, exigindo monitoramento.",
            "CRÍTICO": "Superaquecimento crítico nos módulos da mina.",
        },
        "Comunicação com a estação orbital": {
            "NORMAL": "Link de comunicação estável com a estação orbital.",
            "ATENÇÃO": "Comunicação intermitente com a estação orbital.",
            "CRÍTICO": "Perda crítica de comunicação com a estação.",
        },
        "Sistema de energia da mina": {
            "NORMAL": "Geração e armazenamento de energia estáveis.",
            "ATENÇÃO": "Energia abaixo do ideal; baterias e painéis exigem atenção.",
            "CRÍTICO": "Energia em nível crítico; risco de desligamento de sistemas.",
        },
        "Suporte de oxigênio da colônia": {
            "NORMAL": "Níveis de oxigênio adequados para os mineradores.",
            "ATENÇÃO": "Oxigênio abaixo do ideal em alguns setores.",
            "CRÍTICO": "Oxigênio em nível crítico; risco à segurança da equipe.",
        },
        "Estabilidade estrutural da escavação": {
            "NORMAL": "Estrutura da escavação estável.",
            "ATENÇÃO": "Estabilidade reduzida em túneis de mineração.",
            "CRÍTICO": "Instabilidade crítica; risco de colapso da escavação.",
        },
    }
    return descricoes.get(area, {}).get(status, "Status não identificado.")


def recomendacao_por_area(area: str, status: str) -> Optional[str]:
    if status != "CRÍTICO":
        return None

    recomendacoes = {
        "Temperatura da base de mineração": "Reduzir a carga operacional e verificar o controle térmico da base.",
        "Comunicação com a estação orbital": "Tentar restabelecer o contato com a estação orbital e ativar canal reserva.",
        "Sistema de energia da mina": "Ativar modo de economia de energia e desligar equipamentos não essenciais.",
        "Suporte de oxigênio da colônia": "Acionar protocolo de suporte à vida e priorizar a segurança da equipe.",
        "Estabilidade estrutural da escavação": "Suspender a perfuração e evacuar setores com risco de colapso.",
    }
    return recomendacoes.get(area)


def recomendacao_geral(statuses_por_area: Dict[str, str]) -> str:
    for area, status in statuses_por_area.items():
        recomendacao = recomendacao_por_area(area, status)
        if recomendacao:
            return recomendacao

    if any(status == "ATENÇÃO" for status in statuses_por_area.values()):
        return "Monitorar sistemas em atenção e preparar plano de contingência."

    return "Manter operação normal e continuar monitoramento."


def conclusao_logica_missao(resumo: Dict[str, object]) -> str:
    classificacao = str(resumo["classificacao_final"])
    area_mais_afetada = str(resumo["area_mais_afetada"])
    tendencia = str(resumo["tendencia"])

    if classificacao == "MISSÃO CRÍTICA":
        decisao = (
            "A melhor decisão imediata é ativar o modo de segurança, reduzir operações "
            "não essenciais e priorizar energia, comunicação e suporte à vida."
        )
    elif classificacao == "MISSÃO EM ATENÇÃO":
        decisao = (
            "A equipe deve manter a missão ativa, mas com monitoramento reforçado "
            "e plano de contingência preparado."
        )
    else:
        decisao = "A missão pode continuar em operação normal, mantendo o monitoramento dos sensores."

    return (
        f"A saúde geral da missão foi classificada como {classificacao.lower()}. "
        f"{tendencia} A principal preocupação é a área de {area_mais_afetada.lower()}. "
        f"{decisao}"
    )


def conclusao_logica_ciclo(info: List[Dict[str, object]], total_pontos: int, classificacao: str, recomendacao: str) -> str:
    areas_criticas = [item["area"] for item in info if item["status"] == "CRÍTICO"]
    areas_atencao = [item["area"] for item in info if item["status"] == "ATENÇÃO"]

    texto = [f"1) A sonda apresenta classificação {classificacao.lower()} neste ciclo, com {total_pontos} ponto(s) de risco."]

    texto.append("2) Principais riscos e pontos de atenção:")
    if areas_criticas:
        for area in areas_criticas:
            texto.append(f"- {area}: estado crítico.")
    if areas_atencao:
        for area in areas_atencao:
            texto.append(f"- {area}: requer monitoramento.")
    if not areas_criticas and not areas_atencao:
        texto.append("- Nenhum risco relevante identificado no ciclo.")

    texto.append(f"3) Ação imediata recomendada: {recomendacao}")
    return "\n".join(texto)


# -----------------------------------------------------------------------------
# Integração opcional com Ollama
# -----------------------------------------------------------------------------

def chamar_ollama(system_prompt: str, user_message: str, timeout: int = 30) -> Optional[str]:
    """
    Tenta chamar o Ollama local sem depender da biblioteca 'ollama'.
    Isso evita precisar usar pip install dentro do código.
    """
    if not USAR_IA_LOCAL:
        return None

    payload = {
        "model": MODELO_OLLAMA,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "stream": False,
    }

    dados = json.dumps(payload).encode("utf-8")
    requisicao = urllib.request.Request(
        URL_OLLAMA,
        data=dados,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(requisicao, timeout=timeout) as resposta:
            conteudo = json.loads(resposta.read().decode("utf-8"))
            return conteudo.get("message", {}).get("content")
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, KeyError):
        return None


def conclusao_ia_missao(resumo: Dict[str, object]) -> str:
    linhas_risco_area = []
    for area, pontos in resumo["risco_por_area"].items():
        linhas_risco_area.append(f"- {area}: {pontos} pontos")
    texto_risco_area = "\n".join(linhas_risco_area)

    system_prompt = (
        "Você é o diretor de controle de uma missão de mineração espacial. "
        "Você recebe um resumo numérico da missão e deve sugerir a melhor tomada de decisão operacional. "
        "Use linguagem clara, em português, pensando em segurança, energia, comunicação e suporte à vida."
    )

    user_message = (
        "Resumo consolidado da missão:\n"
        f"- Classificação final: {resumo['classificacao_final']}\n"
        f"- Tendência: {resumo['tendencia']}\n"
        f"- Risco médio da missão: {resumo['risco_medio']:.2f}\n"
        f"- Ciclo mais crítico: {resumo['ciclo_mais_critico']} ({resumo['maior_pontuacao']} pontos)\n"
        f"- Quantidade de ciclos críticos: {resumo['qt_ciclos_criticos']}\n"
        f"- Área mais afetada: {resumo['area_mais_afetada']}\n"
        f"- Pontuação acumulada por área:\n{texto_risco_area}\n\n"
        "Responda em 3 a 5 frases, explicando a saúde geral da missão, "
        "a principal preocupação e a melhor decisão operacional imediata."
    )

    resposta = chamar_ollama(system_prompt, user_message)
    if resposta:
        return resposta

    return conclusao_logica_missao(resumo)


def analise_ia_ciclo_manual(info: List[Dict[str, object]], total_pontos: int, classificacao: str, recomendacao: str) -> str:
    linhas = []
    for item in info:
        area = str(item["area"])
        valor = item["valor"]
        status = item["status"]
        desc = item["descricao"]
        unidade = "°C" if "Temperatura" in area else "%"
        linhas.append(f"- {area}: {valor}{unidade} ({status}, {desc})")
    resumo_ciclo = "\n".join(linhas)

    system_prompt = (
        "Você é o computador de bordo de uma sonda de mineração espacial. "
        "Recebe as leituras de um ciclo já classificadas e deve sugerir a melhor ação imediata."
    )

    user_message = (
        "Dados do ciclo da missão:\n"
        f"{resumo_ciclo}\n\n"
        f"Pontuação total de risco: {total_pontos}\n"
        f"Classificação do ciclo: {classificacao}\n"
        f"Recomendação lógica atual: {recomendacao}\n\n"
        "Responda em português no formato:\n"
        "1) Situação da sonda neste ciclo.\n"
        "2) Principais riscos e pontos de atenção.\n"
        "3) Ação imediata recomendada."
    )

    resposta = chamar_ollama(system_prompt, user_message)
    if resposta:
        return resposta

    return conclusao_logica_ciclo(info, total_pontos, classificacao, recomendacao)


# -----------------------------------------------------------------------------
# Núcleo de análise da missão
# -----------------------------------------------------------------------------

def avaliar_ciclo(ciclo: List[float]) -> Tuple[List[Dict[str, object]], int, str, str]:
    info = []
    total_pontos = 0
    statuses_por_area = {}

    for nome_area, valor in zip(areas_monitoradas, ciclo):
        status = classificar_parametro(nome_area, valor)
        pontos = PONTOS_STATUS[status]
        descricao = descricao_curta(nome_area, status)

        info.append({
            "area": nome_area,
            "valor": valor,
            "status": status,
            "pontos": pontos,
            "descricao": descricao,
        })

        statuses_por_area[nome_area] = status
        total_pontos += pontos

    classificacao_ciclo = classificar_ciclo_por_pontos(total_pontos)
    recomendacao = recomendacao_geral(statuses_por_area)

    return info, total_pontos, classificacao_ciclo, recomendacao


def analisar_missao(dados: List[List[float]]) -> Tuple[List[Dict[str, object]], Dict[str, object]]:
    qt_ciclos = len(dados)
    risco_ciclos = []
    risco_por_area = {area: 0 for area in areas_monitoradas}
    qt_ciclos_criticos = 0
    soma_colunas = [0, 0, 0, 0, 0]
    ciclo_mais_critico = None
    maior_pontuacao = -1
    resultados_ciclos = []

    for indice, ciclo in enumerate(dados, start=1):
        info, total_pontos, classificacao_ciclo, recomendacao = avaliar_ciclo(ciclo)

        for item in info:
            risco_por_area[str(item["area"])] += int(item["pontos"])

        if classificacao_ciclo == "MISSÃO CRÍTICA":
            qt_ciclos_criticos += 1

        if total_pontos > maior_pontuacao:
            maior_pontuacao = total_pontos
            ciclo_mais_critico = indice

        risco_ciclos.append(total_pontos)

        for i, valor in enumerate(ciclo):
            soma_colunas[i] += valor

        resultados_ciclos.append({
            "indice": indice,
            "ciclo": ciclo,
            "info": info,
            "total_pontos": total_pontos,
            "classificacao": classificacao_ciclo,
            "recomendacao": recomendacao,
        })

    risco_primeiro = risco_ciclos[0]
    risco_ultimo = risco_ciclos[-1]

    if risco_ultimo > risco_primeiro:
        tendencia = "A missão apresentou tendência de piora."
    elif risco_ultimo < risco_primeiro:
        tendencia = "A missão apresentou tendência de melhora."
    else:
        tendencia = "A missão permaneceu estável em relação ao início."

    area_mais_afetada = max(risco_por_area, key=risco_por_area.get)
    medias = [soma / qt_ciclos for soma in soma_colunas]
    risco_total = sum(risco_ciclos)
    risco_medio = risco_total / qt_ciclos
    classificacao_final = classificar_ciclo_por_pontos(risco_medio)

    resumo_final = {
        "qt_ciclos": qt_ciclos,
        "resultados_ciclos": resultados_ciclos,
        "risco_ciclos": risco_ciclos,
        "ciclo_mais_critico": ciclo_mais_critico,
        "maior_pontuacao": maior_pontuacao,
        "risco_medio": risco_medio,
        "qt_ciclos_criticos": qt_ciclos_criticos,
        "tendencia": tendencia,
        "risco_por_area": risco_por_area,
        "area_mais_afetada": area_mais_afetada,
        "media_temperatura": medias[0],
        "media_comunicacao": medias[1],
        "media_energia": medias[2],
        "media_oxigenio": medias[3],
        "media_estabilidade": medias[4],
        "classificacao_final": classificacao_final,
    }

    return resultados_ciclos, resumo_final


# -----------------------------------------------------------------------------
# Planejamento LIDAR
# -----------------------------------------------------------------------------

def escolher_alvo_perfuracao(perfil: List[Tuple[int, str, int, int]], risco_gas_max: int = 60, profundidade_max: int = 50) -> Optional[Dict[str, object]]:
    melhor_alvo = None
    melhor_score = -1.0

    for profundidade, tipo, concentracao_minerio, risco_gas in perfil:
        if profundidade > profundidade_max:
            continue
        if risco_gas > risco_gas_max:
            continue

        score = concentracao_minerio - (risco_gas * 0.3)
        if score > melhor_score:
            melhor_score = score
            melhor_alvo = {
                "profundidade": profundidade,
                "tipo": tipo,
                "conc_minerio": concentracao_minerio,
                "risco_gas": risco_gas,
                "score": score,
            }

    return melhor_alvo


def analise_ia_perfuracao(melhor_alvo: Optional[Dict[str, object]], resumo_missao: Dict[str, object]) -> str:
    if melhor_alvo is None:
        return (
            "O perfil LIDAR não encontrou um alvo de perfuração seguro dentro dos limites atuais. "
            "A recomendação é revisar os parâmetros ou buscar outra região de mineração."
        )

    system_prompt = (
        "Você é o sistema de planejamento de perfuração de uma sonda de mineração espacial. "
        "Avalie se vale a pena perfurar até o alvo sugerido pelo LIDAR, considerando segurança e estado da missão."
    )

    user_message = (
        "Melhor alvo sugerido pelo LIDAR:\n"
        f"- Profundidade: {melhor_alvo['profundidade']} m\n"
        f"- Tipo de material: {melhor_alvo['tipo']}\n"
        f"- Concentração de minério: {melhor_alvo['conc_minerio']}\n"
        f"- Risco de gás: {melhor_alvo['risco_gas']}\n"
        f"- Score técnico: {melhor_alvo['score']:.2f}\n\n"
        "Resumo da missão:\n"
        f"- Classificação final: {resumo_missao['classificacao_final']}\n"
        f"- Tendência: {resumo_missao['tendencia']}\n"
        f"- Área mais afetada: {resumo_missao['area_mais_afetada']}\n"
        f"- Risco médio: {resumo_missao['risco_medio']:.2f}\n\n"
        "Responda em português no formato:\n"
        "1) Situação da sonda neste ciclo.\n"
        "2) Principais precauções a tomar.\n"
        "3) Decisão final: perfurar agora, adiar ou evitar."
    )

    resposta = chamar_ollama(system_prompt, user_message)
    if resposta:
        return resposta

    classificacao = str(resumo_missao["classificacao_final"])
    risco_gas = int(melhor_alvo["risco_gas"])

    if classificacao == "MISSÃO CRÍTICA":
        decisao = "adiar a perfuração, pois a missão já apresenta risco elevado."
    elif risco_gas >= 50:
        decisao = "adiar a perfuração até reduzir ou mapear melhor o risco de gás."
    else:
        decisao = "perfurar com cautela, mantendo sensores de gás e estabilidade ativos."

    return (
        "1) A sonda possui um alvo de mineração viável identificado pelo LIDAR. "
        f"O melhor ponto está a {melhor_alvo['profundidade']} m, com concentração de minério "
        f"igual a {melhor_alvo['conc_minerio']} e risco de gás igual a {risco_gas}.\n"
        "2) Principais precauções a tomar:\n"
        "- Monitorar gás preso antes de iniciar a perfuração.\n"
        "- Verificar estabilidade estrutural da escavação.\n"
        "- Manter energia e comunicação em condição segura.\n"
        f"3) Decisão final: {decisao}"
    )


# -----------------------------------------------------------------------------
# Entrada e impressão
# -----------------------------------------------------------------------------

def ler_numero(mensagem: str, minimo: float, maximo: float) -> float:
    while True:
        entrada = input(mensagem).strip().replace(",", ".")
        try:
            valor = float(entrada)
            if minimo <= valor <= maximo:
                return valor
            print(f"Digite um valor entre {minimo} e {maximo}.")
        except ValueError:
            print("Valor inválido. Digite apenas números.")


def ler_ciclo_manual() -> List[float]:
    print("\n=== Nova leitura manual da missão ===")
    temperatura = ler_numero("Temperatura da base de mineração (°C): ", -100, 150)
    comunicacao = ler_numero("Comunicação com a estação orbital (%): ", 0, 100)
    energia = ler_numero("Sistema de energia da mina (%): ", 0, 100)
    oxigenio = ler_numero("Suporte de oxigênio da colônia (%): ", 0, 100)
    estabilidade = ler_numero("Estabilidade estrutural da escavação (%): ", 0, 100)
    return [temperatura, comunicacao, energia, oxigenio, estabilidade]


def imprimir_dados_brutos(dados: List[List[float]]) -> None:
    print("\n--- DADOS DA MISSÃO ---")
    print(f"{'Ciclo':<8} {'Temp':>8} {'Comu':>8} {'Energia':>9} {'O2':>8} {'Estab':>8}")
    print("-" * 55)
    for indice, ciclo in enumerate(dados, start=1):
        print(
            f"{'Ciclo ' + str(indice):<8} "
            f"{ciclo[0]:>7}°C "
            f"{ciclo[1]:>7}% "
            f"{ciclo[2]:>8}% "
            f"{ciclo[3]:>7}% "
            f"{ciclo[4]:>7}%"
        )


def imprimir_relatorio(dados: List[List[float]]) -> None:
    resultados_ciclos, resumo = analisar_missao(dados)

    print("=" * 70)
    print("MISSION CONTROL AI — MINERAÇÃO ESPACIAL")
    print("=" * 70)
    print(f"Missão: {NOME_MISSAO}")
    print(f"Equipe: {EQUIPE}")
    print(f"Quantidade de ciclos analisados: {resumo['qt_ciclos']}")
    print("=" * 70)

    for ciclo_res in resultados_ciclos:
        print(f"\nCICLO {ciclo_res['indice']}")
        print("-" * 70)
        for item in ciclo_res["info"]:
            area = str(item["area"])
            valor = item["valor"]
            status = item["status"]
            descricao = item["descricao"]
            unidade = "°C" if "Temperatura" in area else "%"
            print(f"{area}: {valor}{unidade} | {status} | {descricao}")

        print(f"Pontuação de risco do ciclo: {ciclo_res['total_pontos']}")
        print(f"Classificação do ciclo: {ciclo_res['classificacao']}")
        print(f"Recomendação: {ciclo_res['recomendacao']}")

    print("\n" + "=" * 70)
    print("RELATÓRIO FINAL DA MISSÃO")
    print("=" * 70)
    print(f"Missão: {NOME_MISSAO}")
    print(f"Equipe: {EQUIPE}")
    print(f"Quantidade de ciclos analisados: {resumo['qt_ciclos']}")
    print(f"Média de temperatura: {resumo['media_temperatura']:.2f} °C")
    print(f"Média de comunicação: {resumo['media_comunicacao']:.2f}%")
    print(f"Média de energia: {resumo['media_energia']:.2f}%")
    print(f"Média de oxigênio: {resumo['media_oxigenio']:.2f}%")
    print(f"Média de estabilidade: {resumo['media_estabilidade']:.2f}%")
    print(f"Ciclo mais crítico: Ciclo {resumo['ciclo_mais_critico']}")
    print(f"Maior pontuação de risco: {resumo['maior_pontuacao']}")
    print(f"Risco médio da missão: {resumo['risco_medio']:.2f}")
    print(f"Quantidade de ciclos críticos: {resumo['qt_ciclos_criticos']}")
    print(f"Tendência da missão: {resumo['tendencia']}")

    print("\nPontuação acumulada por área:")
    for area, pontos in resumo["risco_por_area"].items():
        print(f"- {area}: {pontos} ponto(s)")

    print(f"\nÁrea mais afetada: {resumo['area_mais_afetada']}")
    print(f"Classificação final da missão: {resumo['classificacao_final']}")
    print("\nConclusão:")
    print(conclusao_ia_missao(resumo))


def visualizar_ultimo_ciclo(dados: List[List[float]]) -> None:
    ultimo = dados[-1]
    info, pontos, classificacao, recomendacao = avaliar_ciclo(ultimo)

    print(f"\n--- STATUS DO ÚLTIMO CICLO (Ciclo {len(dados)}) ---")
    for item in info:
        area = str(item["area"])
        unidade = "°C" if "Temperatura" in area else "%"
        print(f"{area}: {item['valor']}{unidade} | {item['status']} | {item['descricao']}")

    print(f"\nPontuação de risco: {pontos}")
    print(f"Classificação: {classificacao}")
    print(f"Recomendação: {recomendacao}")


def executar_ciclo_manual(historico: List[str]) -> None:
    ciclo_manual = ler_ciclo_manual()
    dados_missao.append(ciclo_manual)

    info, total_pontos, classificacao, recomendacao = avaliar_ciclo(ciclo_manual)

    print("\n===== CICLO MANUAL — ANÁLISE PELAS REGRAS =====")
    for item in info:
        area = str(item["area"])
        unidade = "°C" if "Temperatura" in area else "%"
        print(f"{area}: {item['valor']}{unidade} | {item['status']} | {item['descricao']}")

    print(f"\nPontuação de risco do ciclo: {total_pontos}")
    print(f"Classificação do ciclo: {classificacao}")
    print(f"Recomendação lógica: {recomendacao}")

    print("\n===== ANÁLISE AUTOMATIZADA — CICLO MANUAL =====")
    print(analise_ia_ciclo_manual(info, total_pontos, classificacao, recomendacao))

    historico.append(f"Ciclo manual inserido — classificação: {classificacao}.")


def executar_planejamento_lidar(historico: List[str]) -> None:
    print("\n--- PLANEJAMENTO DE PERFURAÇÃO (LIDAR) ---")
    melhor_alvo = escolher_alvo_perfuracao(perfil_lidar, risco_gas_max=70, profundidade_max=40)

    if melhor_alvo:
        print(f"Melhor alvo: {melhor_alvo['profundidade']} m | {melhor_alvo['tipo']}")
        print(f"Concentração de minério: {melhor_alvo['conc_minerio']}")
        print(f"Risco de gás: {melhor_alvo['risco_gas']}")
        print(f"Score técnico: {melhor_alvo['score']:.2f}")
    else:
        print("Nenhum alvo seguro encontrado com os limites atuais.")

    _, resumo_missao = analisar_missao(dados_missao)
    print("\nAnálise automatizada sobre a perfuração:")
    print(analise_ia_perfuracao(melhor_alvo, resumo_missao))

    historico.append("Análise de perfuração LIDAR executada.")


# -----------------------------------------------------------------------------
# Menu principal
# -----------------------------------------------------------------------------

def menu() -> None:
    historico = []

    while True:
        print("\n" + "=" * 70)
        print("MISSION CONTROL AI — MINERAÇÃO ESPACIAL")
        print("=" * 70)
        print(f"Missão: {NOME_MISSAO} | Equipe: {EQUIPE}")
        print("-" * 70)
        print("1. Visualizar dados brutos da missão")
        print("2. Executar análise completa")
        print("3. Visualizar status do último ciclo")
        print("4. Inserir novo ciclo manual")
        print("5. Planejamento de perfuração (LIDAR)")
        print("6. Histórico de análises")
        print("7. Encerrar sistema")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            imprimir_dados_brutos(dados_missao)

        elif opcao == "2":
            imprimir_relatorio(dados_missao)
            historico.append(f"Análise completa executada — {len(dados_missao)} ciclo(s) analisado(s).")

        elif opcao == "3":
            visualizar_ultimo_ciclo(dados_missao)

        elif opcao == "4":
            executar_ciclo_manual(historico)

        elif opcao == "5":
            executar_planejamento_lidar(historico)

        elif opcao == "6":
            print("\n--- HISTÓRICO ---")
            if not historico:
                print("Nenhuma análise realizada ainda.")
            else:
                for indice, registro in enumerate(historico, start=1):
                    print(f"{indice}. {registro}")

        elif opcao == "7":
            print("\nEncerrando Mission Control AI. Boa missão.")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()
