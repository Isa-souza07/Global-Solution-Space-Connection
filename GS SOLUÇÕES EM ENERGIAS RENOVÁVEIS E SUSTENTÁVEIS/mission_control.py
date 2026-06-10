# -*- coding: utf-8 -*-
"""mission_control_ai_mineracao_espacial_.ipynb
...
"""
areas_monitoradas = [
    "Temperatura da base de mineração",      # Temperatura interna dos módulos e túneis
    "Comunicação com a estação orbital",     # Link com a estação/colônia
    "Sistema de energia da mina",            # Reatores, painéis, baterias
    "Suporte de oxigênio da colônia",        # Vida dos mineradores
    "Estabilidade estrutural da escavação"   # Integridade de túneis/equipamentos
]

# Matriz de ciclos da missão
# [temperatura, comunicacao, bateria, oxigenio, estabilidade]
dados_missao = [
    [15, 92, 30, 96, 90],
    [22, 75, 72, 94, 85],
    [31, 65, 58, 91, 70],
    [36, 32, 38, 87, 25],
    [39, 28, 19, 88, 80],
    [34, 65, 32, 82, 66]
]

NOME_MISSAO = "Orion Mining Alpha"
EQUIPE = "Equipe Prospector"

def classificar_temperatura(t):
    if t < 18:
        return "ATENÇÃO"
    elif 18 <= t <= 30:
        return "NORMAL"
    elif 30 < t <= 35:
        return "ATENÇÃO"
    else:
        return "CRÍTICO"


def classificar_comunicacao(c):
    if c < 30:
        return "CRÍTICO"
    elif 30 <= c <= 59:
        return "ATENÇÃO"
    else:
        return "NORMAL"


def classificar_bateria(b):
    if b < 20:
        return "CRÍTICO"
    elif 20 <= b <= 49:
        return "ATENÇÃO"
    else:
        return "NORMAL"


def classificar_oxigenio(o):
    if o < 80:
        return "CRÍTICO"
    elif 80 <= o <= 89:
        return "ATENÇÃO"
    else:
        return "NORMAL"


def classificar_estabilidade(e):
    if e < 40:
        return "CRÍTICO"
    elif 40 <= e <= 69:
        return "ATENÇÃO"
    else:
        return "NORMAL"

def classificar_parametro(nome_area, valor):
    if nome_area == "Temperatura da base de mineração":
        return classificar_temperatura(valor)
    if nome_area == "Comunicação com a estação orbital":
        return classificar_comunicacao(valor)
    if nome_area == "Sistema de energia da mina":
        return classificar_bateria(valor)
    if nome_area == "Suporte de oxigênio da colônia":
        return classificar_oxigenio(valor)
    if nome_area == "Estabilidade estrutural da escavação":
        return classificar_estabilidade(valor)
    return "DESCONHECIDO"

PONTOS_STATUS = {
    "NORMAL": 0,
    "ATENÇÃO": 1,
    "CRÍTICO": 2
}

def classificar_ciclo_por_pontos(pontos):
    if 0 <= pontos <= 2:
        return "MISSÃO ESTÁVEL"
    elif 3 <= pontos <= 5:
        return "MISSÃO EM ATENÇÃO"
    elif pontos >= 6:
        return "MISSÃO CRÍTICA"

def descricao_curta(area, status):
    if area == "Temperatura da base de mineração":
        if status == "NORMAL":
            return "Temperatura interna estável para operação"
        elif status == "ATENÇÃO":
            return "Temperatura interna elevada, exigir monitoramento"
        else:
            return "Superaquecimento crítico nos módulos da mina"

    if area == "Comunicação com a estação orbital":
        if status == "NORMAL":
            return "Link de comunicação estável com a estação orbital"
        elif status == "ATENÇÃO":
            return "Comunicação intermitente com a estação orbital"
        else:
            return "Perda crítica de comunicação com a estação"

    if area == "Sistema de energia da mina":
        if status == "NORMAL":
            return "Geração e armazenamento de energia estáveis"
        elif status == "ATENÇÃO":
            return "Energia abaixo do ideal; painéis/baterias exigem atenção"
        else:
            return "Energia em nível crítico; risco de desligamento de sistemas"

    if area == "Suporte de oxigênio da colônia":
        if status == "NORMAL":
            return "Níveis de oxigênio adequados para os mineradores"
        elif status == "ATENÇÃO":
            return "Oxigênio abaixo do ideal em alguns setores"
        else:
            return "Oxigênio em nível crítico; risco à vida da equipe"

    if area == "Estabilidade estrutural da escavação":
        if status == "NORMAL":
            return "Estrutura da escavação estável"
        elif status == "ATENÇÃO":
            return "Estabilidade reduzida em túneis de mineração"
        else:
            return "Instabilidade crítica; risco de colapso da escavação"

    return ""

def recomendacao_por_area(area, status):
    if status != "CRÍTICO":
        return None

    if area == "Temperatura da base de mineração":
        return "Reduzir carga dos reatores e desacelerar perfuração em setores quentes."
    if area == "Comunicação com a estação orbital":
        return "Redirecionar comunicações para canais redundantes e suspender operações de risco."
    if area == "Sistema de energia da mina":
        return "Ativar modo de economia de energia e priorizar sistemas vitais da colônia."
    if area == "Suporte de oxigênio da colônia":
        return "Evacuar túneis menos ventilados e priorizar suporte à vida nos setores habitados."
    if area == "Estabilidade estrutural da escavação":
        return "Interromper perfurações e reforçar escoramentos nas galerias críticas."

    return None
def recomendacao_geral(statuses_por_area):
    for area, status in statuses_por_area.items():
        if status == "CRÍTICO":
            rec = recomendacao_por_area(area, status)
            if rec:
                return rec

    if any(status == "ATENÇÃO" for status in statuses_por_area.values()):
        return "Monitorar sistemas em atenção e preparar plano de contingência."

    return "Manter operação normal e continuar monitoramento."

def avaliar_ciclo(ciclo):
    info = []
    total_pontos = 0
    statuses_por_area = {}

    for nome_area, valor in zip(areas_monitoradas, ciclo):
        status = classificar_parametro(nome_area, valor)
        pontos = PONTOS_STATUS[status]
        desc = descricao_curta(nome_area, status)

        info.append({
            "area": nome_area,
            "valor": valor,
            "status": status,
            "pontos": pontos,
            "descricao": desc
        })

        statuses_por_area[nome_area] = status
        total_pontos += pontos

    classificacao_ciclo = classificar_ciclo_por_pontos(total_pontos)
    recomendacao = recomendacao_geral(statuses_por_area)

    return info, total_pontos, classificacao_ciclo, recomendacao

def analisar_missao(dados):
    qt_ciclos = len(dados)

    # Acúmulos
    risco_ciclos = []  # pontuação total de cada ciclo
    risco_por_area = {area: 0 for area in areas_monitoradas}
    qt_ciclos_criticos = 0
    soma_colunas = [0, 0, 0, 0, 0]

    ciclo_mais_critico = None
    maior_pontuacao = -1

    # Resultados detalhados por ciclo para impressão
    resultados_ciclos = []

    for idx, ciclo in enumerate(dados, start=1):
        info, total_pontos, classificacao_ciclo, recomendacao = avaliar_ciclo(ciclo)

        # Acumular risco por área
        for item in info:
            risco_por_area[item["area"]] += item["pontos"]

        # Contar críticos, achar ciclo mais crítico
        if classificacao_ciclo == "MISSÃO CRÍTICA":
            qt_ciclos_criticos += 1
        if total_pontos > maior_pontuacao:
            maior_pontuacao = total_pontos
            ciclo_mais_critico = idx

        # Acumular risco do ciclo
        risco_ciclos.append(total_pontos)

        # Acumular colunas para médias
        for i, valor in enumerate(ciclo):
            soma_colunas[i] += valor

        resultados_ciclos.append({
            "indice": idx,
            "ciclo": ciclo,
            "info": info,
            "total_pontos": total_pontos,
            "classificacao": classificacao_ciclo,
            "recomendacao": recomendacao
        })

    # Tendência (primeiro x último ciclo)
    risco_primeiro = risco_ciclos[0]
    risco_ultimo = risco_ciclos[-1]
    if risco_ultimo > risco_primeiro:
        tendencia = "A missão apresentou tendência de piora."
    elif risco_ultimo < risco_primeiro:
        tendencia = "A missão apresentou tendência de melhora."
    else:
        tendencia = "A missão permaneceu estável em relação ao início."

    # Área mais afetada
    area_mais_afetada = max(risco_por_area, key=risco_por_area.get)

    # Médias
    medias = [soma / qt_ciclos for soma in soma_colunas]
    media_temperatura, media_comunicacao, media_bateria, media_oxigenio, media_estabilidade = medias

    risco_total = sum(risco_ciclos)
    risco_medio = risco_total / qt_ciclos

    # Classificação final da missão
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
        "media_temperatura": media_temperatura,
        "media_comunicacao": media_comunicacao,
        "media_bateria": media_bateria,
        "media_oxigenio": media_oxigenio,
        "media_estabilidade": media_estabilidade,
        "classificacao_final": classificacao_final
    }

    return resultados_ciclos, resumo_final

# 13. Perfil LIDAR da área de mineração
# Cada tupla: (profundidade_em_metros, tipo_de_material, concentração_de_minerio(0-100), risco_de_gas(0-100))

perfil_lidar = [
    (0,  "regolito superficial",   5,  0),
    (10, "rocha compacta",        25, 10),
    (20, "veia rica em minério",  80, 20),
    (30, "rocha frágil",          45, 50),
    (40, "camada com gás preso",  15, 90),
]

# Escolha automática do alvo de perfuração a partir do perfil LIDAR

def escolher_alvo_perfuracao(perfil, risco_gas_max=60, profundidade_max=50):
    """
    Escolhe a melhor profundidade de perfuração com base no perfil LIDAR.
    Critério simples: maior concentração de minério com risco de gás aceitável.
    """
    melhor_alvo = None
    melhor_score = -1

    for profundidade, tipo, conc_minerio, risco_gas in perfil:
        if profundidade > profundidade_max:
            continue
        if risco_gas > risco_gas_max:
            continue

        # Score simples: concentração de minério penalizada pelo risco de gás
        score = conc_minerio - risco_gas * 0.3
        if score > melhor_score:
            melhor_score = score
            melhor_alvo = {
                "profundidade": profundidade,
                "tipo": tipo,
                "conc_minerio": conc_minerio,
                "risco_gas": risco_gas,
                "score": score,
            }

    return melhor_alvo

# Demonstração: LIDAR + decisão da IA sobre perfuração

# 1) Escolher o melhor alvo com base no perfil LIDAR
melhor_alvo = escolher_alvo_perfuracao(perfil_lidar, risco_gas_max=70, profundidade_max=40)

print("===== PLANEJAMENTO DE PERFURAÇÃO (LIDAR) ====")
if melhor_alvo:
    print(
        f"Melhor alvo: {melhor_alvo['profundidade']} m | "
        f"{melhor_alvo['tipo']} | "
        f"minério={melhor_alvo['conc_minerio']} | "
        f"risco de gás={melhor_alvo['risco_gas']}"
    )
else:
    print("Nenhum alvo seguro encontrado com os limites atuais.")

# 2) Obter o resumo da missão (já usa seus dados e regras)
_, resumo_missao = analisar_missao(dados_missao)

# 12. Entrada manual de um ciclo da missão

def ler_ciclo_manual():
    print("=== Nova leitura manual da missão ===")
    temperatura = float(input("Temperatura da base de mineração (°C): "))
    comunicacao = float(input("Comunicação com a estação orbital (%): "))
    bateria = float(input("Sistema de energia da mina / baterias (%): "))
    oxigenio = float(input("Suporte de oxigênio da colônia (%): "))
    estabilidade = float(input("Estabilidade estrutural da escavação (%): "))
    return [temperatura, comunicacao, bateria, oxigenio, estabilidade]

# Ler ciclo a partir do usuário
ciclo_manual = ler_ciclo_manual()

# Analisar ciclo pelas regras
info, total_pontos, classificacao_ciclo, recomendacao = avaliar_ciclo(ciclo_manual)

print("\n===== CICLO MANUAL — ANÁLISE PELAS REGRAS =====")
for item in info:
    area = item["area"]
    valor = item["valor"]
    status = item["status"]
    desc = item["descricao"]
    unidade = "°C" if "Temperatura" in area else "%"
    print(f"{area}: {valor}{unidade} | {status} | {desc}")

print(f"\nPontuação de risco do ciclo: {total_pontos}")
print(f"Classificação do ciclo: {classificacao_ciclo}")
print(f"Recomendação lógica: {recomendacao}")

def imprimir_relatorio(dados):
  resultados_ciclos, resumo = analisar_missao(dados)

  print("=" * 60)
  print("MISSION CONTROL AI — MINERAÇÃO ESPACIAL")
  print("=" * 60)
  print(f"Missão: {NOME_MISSAO}")
  print(f"Equipe: {EQUIPE}")
  print(f"Quantidade de ciclos analisados: {resumo['qt_ciclos']}")
  print("=" * 60)

  # Detalhe de cada ciclo
  for ciclo_res in resultados_ciclos:
      idx = ciclo_res["indice"]
      print(f"CICLO {idx}")
      print("-" * 60)
      for item in ciclo_res["info"]:
          area = item["area"]
          valor = item["valor"]
          status = item["status"]
          desc = item["descricao"]

          # Formatar unidade
          if "Temperatura" in area:
              unidade = "°C"
          else:
              unidade = "%"

          print(f"{area.split()[0]}: {valor} {unidade} | {status} | {desc}")
      print(f"Pontuação de risco do ciclo: {ciclo_res['total_pontos']}")
      print(f"Classificação do ciclo: {ciclo_res['classificacao']}")
      print(f"Recomendação: {ciclo_res['recomendacao']}")
      print()

  # Relatório final
  print("=" * 60)
  print("RELATÓRIO FINAL DA MISSÃO")
  print("=" * 60)
  print(f"Missão: {NOME_MISSAO}")
  print(f"Equipe: {EQUIPE}")
  print(f"Quantidade de ciclos analisados: {resumo['qt_ciclos']}")
  print(f"Média de temperatura: {resumo['media_temperatura']:.2f} °C")
  print(f"Média de comunicação: {resumo['media_comunicacao']:.2f}%")
  print(f"Média de bateria: {resumo['media_bateria']:.2f}%")
  print(f"Média de oxigênio: {resumo['media_oxigenio']:.2f}%")
  print(f"Média de estabilidade: {resumo['media_estabilidade']:.2f}%")
  print(f"Ciclo mais crítico: Ciclo {resumo['ciclo_mais_critico']}")
  print(f"Maior pontuação de risco: {resumo['maior_pontuacao']}")
  print(f"Risco médio da missão: {resumo['risco_medio']:.2f}")
  print(f"Quantidade de ciclos críticos: {resumo['qt_ciclos_criticos']}")
  print("Tendência da missão:")
  print(resumo["tendencia"])
  print("Pontuação acumulada por área:")
  for area, pontos in resumo["risco_por_area"].items():
    print(f"{area}: {pontos} pontos")
  print("Área mais afetada:")
  print(resumo["area_mais_afetada"])
  print("Classificação final da missão:")
  print(resumo["classificacao_final"])

def menu():
    print("=" * 60)
    print("MISSION CONTROL AI — MINERAÇÃO ESPACIAL")
    print("=" * 60)
    print(f"Missão: {NOME_MISSAO} | Equipe: {EQUIPE}")
    print("=" * 60)

    historico = []

    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1. Visualizar dados brutos da missão")
        print("2. Executar análise completa")
        print("3. Visualizar status do último ciclo")
        print("4. Histórico de análises")
        print("5. Planejamento de perfuração (LIDAR)")
        print("6. Encerrar sistema")
        print()

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\n--- DADOS DA MISSÃO ---")
            print(f"{'Ciclo':<8} {'Temp':>6} {'Comu':>6} {'Bat':>6} {'O2':>6} {'Est':>6}")
            print("-" * 42)
            for i, ciclo in enumerate(dados_missao, start=1):
                print(f"{'Ciclo '+str(i):<8} {ciclo[0]:>5}°C {ciclo[1]:>5}% {ciclo[2]:>5}% {ciclo[3]:>5}% {ciclo[4]:>5}%")

        elif opcao == "2":
            print("\nExecutando análise completa...")
            imprimir_relatorio(dados_missao)
            historico.append(f"Análise executada — {len(dados_missao)} ciclos analisados.")

        elif opcao == "3":
            ultimo = dados_missao[-1]
            info, pontos, classificacao, recomendacao = avaliar_ciclo(ultimo)
            print(f"\n--- STATUS DO ÚLTIMO CICLO (Ciclo {len(dados_missao)}) ---")
            for item in info:
                unidade = "°C" if "Temperatura" in item["area"] else "%"
                print(f"{item['area']}: {item['valor']}{unidade} | {item['status']} | {item['descricao']}")
            print(f"\nPontuação de risco: {pontos}")
            print(f"Classificação: {classificacao}")
            print(f"Recomendação: {recomendacao}")

        elif opcao == "4":
            print("\n--- HISTÓRICO ---")
            if not historico:
                print("Nenhuma análise realizada ainda.")
            else:
                for i, registro in enumerate(historico, start=1):
                    print(f"{i}. {registro}")

        elif opcao == "5":
            print("\n--- PLANEJAMENTO DE PERFURAÇÃO (LIDAR) ---")
            melhor_alvo = escolher_alvo_perfuracao(perfil_lidar, risco_gas_max=70, profundidade_max=40)
            if melhor_alvo:
                print(f"Melhor alvo: {melhor_alvo['profundidade']} m | {melhor_alvo['tipo']}")
                print(f"Minério: {melhor_alvo['conc_minerio']} | Risco de gás: {melhor_alvo['risco_gas']}")
            else:
                print("Nenhum alvo seguro encontrado com os limites atuais.")
            _, resumo_missao = analisar_missao(dados_missao)
            historico.append("Planejamento de perfuração LIDAR executado (sem IA).")

        elif opcao == "6":
            print("\nEncerrando Mission Control AI. Boa missão.")
            break

        else:
            print("Opção inválida. Tente novamente.")

menu()