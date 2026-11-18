"""
Neighborhood Action Dashboard
Global Solution 2026.2 - CitizenTech - FIAP

Painel comunitário em modo texto para registrar, organizar, consultar e
acompanhar ocorrências de infraestrutura e manutenção em bairros.

Equipe:
    RM 575601 - Aldo Roschel
    RM 575921 - Larissa Bressanini Lehn
    RM 575981 - Nicole Luiza Mascarenhas Zerbato
    RM 575105 - Kelven Carlos Luiz de Souza

Como executar (a partir da pasta raiz do repositório):
    python src/sistema.py

Os dados simulados estão embutidos neste arquivo, nas listas
DADOS_INICIAIS (ocorrências) e HISTORICO_INICIAL (eventos de status).
"""

# ---------------------------------------------------------------------------
# 1. CONFIGURAÇÕES E VALORES PADRONIZADOS
# ---------------------------------------------------------------------------

# Dia atual da simulação. As datas são "dias simulados" (dia 1, dia 2, ...),
# o que permite calcular tempos de atendimento com uma simples subtração.
DIA_ATUAL = 20

BAIRROS_VALIDOS = ["Centro", "Bairro Alto", "Bairro Norte", "Bairro Sul"]

CATEGORIAS_VALIDAS = [
    "iluminação",
    "acessibilidade",
    "limpeza",
    "conservação de espaços coletivos",
]

STATUS_VALIDOS = ["aberta", "em análise", "concluída"]

SIGNIFICADO_STATUS = {
    "aberta": "registrada e aguardando a primeira análise (fica na fila de atendimento)",
    "em análise": "já examinada pela equipe; está sendo avaliada ou encaminhada",
    "concluída": "o problema foi resolvido e a ocorrência foi encerrada",
}

# Campos que toda ocorrência precisa ter preenchidos.
CAMPOS_OBRIGATORIOS = ["id", "bairro", "categoria", "descricao", "local", "dia_abertura", "status"]

# ---------------------------------------------------------------------------
# 2. DADOS SIMULADOS INICIAIS (fictícios, sem dados pessoais)
# ---------------------------------------------------------------------------
# dia_abertura / dia_conclusao = dias simulados. dia_conclusao só é preenchido
# quando a ocorrência está concluída (caso contrário, fica None).
# Os registros 013 e 014 têm erros DE PROPÓSITO para testar a validação.

DADOS_INICIAIS = [
    {"id": "001", "bairro": "Bairro Alto", "categoria": "iluminação", "descricao": "Poste apagado na rua principal", "local": "Rua principal", "dia_abertura": 1, "status": "em análise", "dia_conclusao": None},
    {"id": "002", "bairro": "Bairro Alto", "categoria": "acessibilidade", "descricao": "Calçada danificada impedindo a passagem de cadeirantes", "local": "Avenida central", "dia_abertura": 2, "status": "concluída", "dia_conclusao": 9},
    {"id": "003", "bairro": "Bairro Sul", "categoria": "limpeza", "descricao": "Acúmulo de lixo em terreno baldio", "local": "Terreno próximo à escola", "dia_abertura": 3, "status": "aberta", "dia_conclusao": None},
    {"id": "004", "bairro": "Centro", "categoria": "iluminação", "descricao": "Falta de ponto de luz na praça", "local": "Praça da Matriz", "dia_abertura": 3, "status": "concluída", "dia_conclusao": 12},
    {"id": "005", "bairro": "Bairro Norte", "categoria": "acessibilidade", "descricao": "Calçada quebrada em frente ao mercado", "local": "Rua do mercado", "dia_abertura": 4, "status": "em análise", "dia_conclusao": None},
    {"id": "006", "bairro": "Centro", "categoria": "limpeza", "descricao": "Banheiros do parque sem manutenção adequada", "local": "Parque municipal", "dia_abertura": 5, "status": "aberta", "dia_conclusao": None},
    {"id": "007", "bairro": "Centro", "categoria": "conservação de espaços coletivos", "descricao": "Grama alta na praça", "local": "Praça central", "dia_abertura": 6, "status": "concluída", "dia_conclusao": 10},
    {"id": "008", "bairro": "Bairro Norte", "categoria": "iluminação", "descricao": "Cabos de iluminação pública rompidos", "local": "Rua do teatro", "dia_abertura": 7, "status": "em análise", "dia_conclusao": None},
    {"id": "009", "bairro": "Bairro Sul", "categoria": "limpeza", "descricao": "Resíduos acumulados em bueiros", "local": "Rua marginal", "dia_abertura": 8, "status": "aberta", "dia_conclusao": None},
    {"id": "010", "bairro": "Bairro Alto", "categoria": "acessibilidade", "descricao": "Local sem rampa para cadeirantes", "local": "Entrada do posto de saúde", "dia_abertura": 9, "status": "aberta", "dia_conclusao": None},
    {"id": "011", "bairro": "Centro", "categoria": "conservação de espaços coletivos", "descricao": "Equipamentos de ginástica com sinais de ferrugem", "local": "Praça de esportes", "dia_abertura": 10, "status": "em análise", "dia_conclusao": None},
    {"id": "012", "bairro": "Bairro Sul", "categoria": "limpeza", "descricao": "Paredes pichadas na quadra", "local": "Quadra poliesportiva", "dia_abertura": 11, "status": "aberta", "dia_conclusao": None},
    # Inconsistente: categoria fora da lista padronizada
    {"id": "013", "bairro": "Bairro Norte", "categoria": "conservação", "descricao": "Banco quebrado no ponto de ônibus", "local": "Ponto de ônibus da avenida", "dia_abertura": 12, "status": "aberta", "dia_conclusao": None},
    # Inconsistente: campo obrigatório "local" vazio
    {"id": "014", "bairro": "Bairro Alto", "categoria": "iluminação", "descricao": "Lâmpada piscando durante a noite", "local": "", "dia_abertura": 13, "status": "aberta", "dia_conclusao": None},
]

HISTORICO_INICIAL = [
    {"id": "002", "status_antigo": "aberta", "status_novo": "em análise", "dia": 3, "justificativa": "Equipe de vistoria agendada"},
    {"id": "001", "status_antigo": "aberta", "status_novo": "em análise", "dia": 4, "justificativa": "Solicitação encaminhada à equipe de iluminação"},
    {"id": "004", "status_antigo": "aberta", "status_novo": "em análise", "dia": 5, "justificativa": "Local vistoriado pela equipe técnica"},
    {"id": "007", "status_antigo": "aberta", "status_novo": "em análise", "dia": 7, "justificativa": "Roçada incluída na programação semanal"},
    {"id": "008", "status_antigo": "aberta", "status_novo": "em análise", "dia": 8, "justificativa": "Área isolada por segurança e aguardando reparo"},
    {"id": "002", "status_antigo": "em análise", "status_novo": "concluída", "dia": 9, "justificativa": "Calçada reformada e rampa refeita"},
    {"id": "005", "status_antigo": "aberta", "status_novo": "em análise", "dia": 9, "justificativa": "Vistoria realizada e orçamento solicitado"},
    {"id": "007", "status_antigo": "em análise", "status_novo": "concluída", "dia": 10, "justificativa": "Grama cortada e praça limpa"},
    {"id": "011", "status_antigo": "aberta", "status_novo": "em análise", "dia": 11, "justificativa": "Equipamentos avaliados para manutenção"},
    {"id": "004", "status_antigo": "em análise", "status_novo": "concluída", "dia": 12, "justificativa": "Novo ponto de luz instalado"},
]

# ---------------------------------------------------------------------------
# 3. ESTRUTURAS DE DADOS DO SISTEMA
# ---------------------------------------------------------------------------

ocorrencias_lista = []         # LISTA: todas as ocorrências válidas, em ordem de registro
ocorrencias_dic = {}           # DICIONÁRIO: acesso direto à ocorrência pelo ID
fila_abertas = []              # FILA (FIFO): IDs ainda não examinados, por ordem de registro
pilha_historico = []           # PILHA (LIFO): eventos de mudança de status (topo = mais recente)
registros_inconsistentes = []  # registros barrados pela validação, com o motivo


# ---------------------------------------------------------------------------
# 4. VALIDAÇÃO E CARGA DOS DADOS
# ---------------------------------------------------------------------------

def validar_ocorrencia(registro, ids_existentes):
    """Devolve a lista de problemas encontrados no registro (lista vazia = registro válido)."""
    problemas = []

    for campo in CAMPOS_OBRIGATORIOS:
        if campo not in registro or registro[campo] == "" or registro[campo] is None:
            problemas.append(f"campo obrigatório '{campo}' ausente")

    if registro["id"] != "" and registro["id"] in ids_existentes:
        problemas.append("identificador duplicado")

    if registro["bairro"] != "" and registro["bairro"] not in BAIRROS_VALIDOS:
        problemas.append(f"bairro desconhecido: '{registro['bairro']}'")

    if registro["categoria"] != "" and registro["categoria"] not in CATEGORIAS_VALIDAS:
        problemas.append(f"categoria desconhecida: '{registro['categoria']}'")

    if registro["status"] != "" and registro["status"] not in STATUS_VALIDOS:
        problemas.append(f"status desconhecido: '{registro['status']}'")

    if registro["dia_abertura"] is not None and type(registro["dia_abertura"]) != int:
        problemas.append("dia de abertura não é um número inteiro")

    # Uma ocorrência concluída precisa informar o dia em que foi concluída.
    if registro["status"] == "concluída" and not type(registro.get("dia_conclusao")) == int:
        problemas.append("ocorrência concluída sem dia de conclusão")

    return problemas


def carregar_dados():
    """Monta todas as estruturas a partir dos dados iniciais embutidos no código."""
    ocorrencias_lista.clear()
    ocorrencias_dic.clear()
    fila_abertas.clear()
    pilha_historico.clear()
    registros_inconsistentes.clear()

    # Ocorrências: só entram na base as que passam na validação.
    # dict(...) cria uma cópia, para que os dados iniciais não sejam alterados
    # e possam ser recarregados depois (opção 12 do menu).
    for dados in DADOS_INICIAIS:
        registro = dict(dados)
        problemas = validar_ocorrencia(registro, ocorrencias_dic)
        if problemas:
            registros_inconsistentes.append({"registro": registro, "problemas": problemas})
        else:
            ocorrencias_lista.append(registro)
            ocorrencias_dic[registro["id"]] = registro

    # Fila: ocorrências abertas (ainda não examinadas) na ordem em que foram registradas.
    for ocorrencia in ocorrencias_lista:
        if ocorrencia["status"] == "aberta":
            fila_abertas.append(ocorrencia["id"])

    # Pilha: eventos do histórico empilhados em ordem cronológica.
    for evento in HISTORICO_INICIAL:
        if evento["id"] in ocorrencias_dic and evento["status_novo"] in STATUS_VALIDOS:
            pilha_historico.append(dict(evento))


# ---------------------------------------------------------------------------
# 5. FUNÇÕES AUXILIARES DE ENTRADA E EXIBIÇÃO
# ---------------------------------------------------------------------------

def normalizar_id(texto):
    """Permite digitar '1' ou '001' para a mesma ocorrência."""
    texto = texto.strip()
    if texto.isdigit():
        return texto.zfill(3)
    return texto


def escolher_opcao(titulo, opcoes, permitir_vazio=False):
    """Mostra opções numeradas e devolve a opção escolhida (evita erros de digitação e acentos)."""
    print(titulo)
    for i in range(len(opcoes)):
        print(f"  {i + 1}. {opcoes[i]}")
    if permitir_vazio:
        print("  (pressione Enter para não filtrar)")

    while True:
        resposta = input("Digite o número da opção: ").strip()
        if permitir_vazio and resposta == "":
            return ""
        if resposta.isdigit() and 1 <= int(resposta) <= len(opcoes):
            return opcoes[int(resposta) - 1]
        print(f"Opção inválida. Digite um número de 1 a {len(opcoes)}.")


def ler_texto_obrigatorio(rotulo, minimo=3):
    """Lê um texto e só aceita se não estiver vazio e tiver um tamanho mínimo."""
    while True:
        texto = input(rotulo).strip()
        if texto == "" or len(texto) < minimo:
            print(f"Campo obrigatório. Escreva pelo menos {minimo} caracteres.")
        else:
            return texto


def gerar_novo_id():
    """Novo ID = maior ID já usado + 1 (inclui registros inconsistentes para não repetir códigos)."""
    maior = 0
    for ocorrencia in ocorrencias_lista:
        if int(ocorrencia["id"]) > maior:
            maior = int(ocorrencia["id"])
    for item in registros_inconsistentes:
        id_registro = item["registro"]["id"]
        if id_registro.isdigit() and int(id_registro) > maior:
            maior = int(id_registro)
    return str(maior + 1).zfill(3)


def exibir_tabela_ocorrencias(lista):
    print(f"{'ID':<4} | {'Categoria':<32} | {'Bairro':<12} | {'Status':<10} | Local")
    print("-" * 95)
    for o in lista:
        print(f"{o['id']:<4} | {o['categoria']:<32} | {o['bairro']:<12} | {o['status']:<10} | {o['local']}")
    print(f"\n{len(lista)} ocorrência(s) exibida(s).")


def porcentagem(parte, total):
    if total == 0:
        return 0.0
    return parte / total * 100


# ---------------------------------------------------------------------------
# 6. ESTRUTURAS DERIVADAS: HIERARQUIA E MATRIZ
# ---------------------------------------------------------------------------

def montar_hierarquia():
    """Hierarquia (árvore): bairro -> categoria -> lista de IDs de ocorrências."""
    hierarquia = {}
    for o in ocorrencias_lista:
        bairro = o["bairro"]
        categoria = o["categoria"]
        if bairro not in hierarquia:
            hierarquia[bairro] = {}
        if categoria not in hierarquia[bairro]:
            hierarquia[bairro][categoria] = []
        hierarquia[bairro][categoria].append(o["id"])
    return hierarquia


def montar_matriz():
    """Matriz (lista de listas): linhas = categorias, colunas = status, valores = quantidades."""
    matriz = []
    for _ in CATEGORIAS_VALIDAS:
        matriz.append([0] * len(STATUS_VALIDOS))

    for o in ocorrencias_lista:
        linha = CATEGORIAS_VALIDAS.index(o["categoria"])
        coluna = STATUS_VALIDOS.index(o["status"])
        matriz[linha][coluna] += 1
    return matriz


# ---------------------------------------------------------------------------
# 7. FUNCIONALIDADES DO MENU
# ---------------------------------------------------------------------------

def listar_todas():
    print("\n=== TODAS AS OCORRÊNCIAS ===")
    exibir_tabela_ocorrencias(ocorrencias_lista)


def exibir_indicadores():
    print("\n================ PAINEL DE INDICADORES ================")
    total = len(ocorrencias_lista)
    print(f"Dia atual da simulação: {DIA_ATUAL}")
    print(f"Total de ocorrências válidas: {total}")
    print(f"Registros inconsistentes isolados: {len(registros_inconsistentes)}")
    if total == 0:
        print("Não há ocorrências para calcular indicadores.")
        return

    matriz = montar_matriz()

    # --- Quantidade e proporção por status (soma das colunas da matriz) ---
    print("\n1) Ocorrências por STATUS")
    print("   Fórmula: porcentagem = quantidade do status / total x 100")
    print(f"   {'Status':<12} | {'Qtd':>4} | {'%':>7}")
    print("   " + "-" * 29)
    totais_status = []
    for j in range(len(STATUS_VALIDOS)):
        soma = 0
        for i in range(len(CATEGORIAS_VALIDAS)):
            soma += matriz[i][j]
        totais_status.append(soma)
        print(f"   {STATUS_VALIDOS[j]:<12} | {soma:>4} | {porcentagem(soma, total):>6.2f}%")

    # --- Quantidade e proporção por categoria (soma das linhas da matriz) ---
    print("\n2) Ocorrências por CATEGORIA")
    print("   Fórmula: porcentagem = quantidade da categoria / total x 100")
    print(f"   {'Categoria':<32} | {'Qtd':>4} | {'%':>7}")
    print("   " + "-" * 49)
    totais_categoria = []
    for i in range(len(CATEGORIAS_VALIDAS)):
        soma = 0
        for j in range(len(STATUS_VALIDOS)):
            soma += matriz[i][j]
        totais_categoria.append(soma)
        print(f"   {CATEGORIAS_VALIDAS[i]:<32} | {soma:>4} | {porcentagem(soma, total):>6.2f}%")

    # --- Matriz categoria x status ---
    print("\n3) Matriz CATEGORIA x STATUS")
    cabecalho = f"   {'Categoria':<32}"
    for status in STATUS_VALIDOS:
        cabecalho += f" | {status:>10}"
    print(cabecalho + f" | {'Total':>5}")
    print("   " + "-" * 80)
    for i in range(len(CATEGORIAS_VALIDAS)):
        linha = f"   {CATEGORIAS_VALIDAS[i]:<32}"
        for j in range(len(STATUS_VALIDOS)):
            linha += f" | {matriz[i][j]:>10}"
        print(linha + f" | {totais_categoria[i]:>5}")
    linha_total = f"   {'Total':<32}"
    for soma in totais_status:
        linha_total += f" | {soma:>10}"
    print(linha_total + f" | {total:>5}")

    # --- Indicadores adicionais ---
    pendentes = 0
    soma_espera = 0
    concluidas = 0
    soma_conclusao = 0
    for o in ocorrencias_lista:
        if o["status"] == "aberta" or o["status"] == "em análise":
            pendentes += 1
            soma_espera += DIA_ATUAL - o["dia_abertura"]
        elif o["status"] == "concluída":
            concluidas += 1
            soma_conclusao += o["dia_conclusao"] - o["dia_abertura"]

    print("\n4) Indicadores adicionais")
    print(f"   Pendências (abertas + em análise): {pendentes} de {total} "
          f"({porcentagem(pendentes, total):.2f}%)")
    print(f"   Ocorrências aguardando na fila (ainda não examinadas): {len(fila_abertas)}")
    if concluidas > 0:
        media_conclusao = soma_conclusao / concluidas
        print("   Tempo médio até a conclusão = soma(dia_conclusão - dia_abertura) / concluídas")
        print(f"      = {soma_conclusao} / {concluidas} = {media_conclusao:.2f} dias")
    else:
        print("   Tempo médio até a conclusão: nenhuma ocorrência concluída ainda.")
    if pendentes > 0:
        media_espera = soma_espera / pendentes
        print("   Tempo médio de espera das pendentes = soma(dia_atual - dia_abertura) / pendentes")
        print(f"      = {soma_espera} / {pendentes} = {media_espera:.2f} dias")

    # --- Interpretação automática ---
    maior_qtd = max(totais_categoria)
    categorias_mais_frequentes = []
    for i in range(len(CATEGORIAS_VALIDAS)):
        if totais_categoria[i] == maior_qtd:
            categorias_mais_frequentes.append(CATEGORIAS_VALIDAS[i])

    pendentes_por_bairro = {}
    for o in ocorrencias_lista:
        if o["status"] != "concluída":
            if o["bairro"] not in pendentes_por_bairro:
                pendentes_por_bairro[o["bairro"]] = 0
            pendentes_por_bairro[o["bairro"]] += 1
    bairro_critico = ""
    maior_pendencia = 0
    for bairro in pendentes_por_bairro:
        if pendentes_por_bairro[bairro] > maior_pendencia:
            maior_pendencia = pendentes_por_bairro[bairro]
            bairro_critico = bairro

    print("\n5) Interpretação")
    print(f"   - Categoria(s) mais frequente(s): {', '.join(categorias_mais_frequentes)} "
          f"({maior_qtd} ocorrência(s)).")
    if bairro_critico != "":
        print(f"   - Bairro com mais pendências: {bairro_critico} ({maior_pendencia}).")
    if porcentagem(pendentes, total) > 50:
        print("   - A maior parte das demandas ainda não foi resolvida: o conjunto simulado")
        print("     sugere que a comunidade precisa de mais agilidade no atendimento.")
    else:
        print("   - A maior parte das demandas já foi resolvida: o atendimento está")
        print("     acompanhando o volume de registros da comunidade.")
    print("=======================================================")


def cadastrar_ocorrencia():
    print("\n--- CADASTRAR NOVA OCORRÊNCIA ---")
    print("Não informe nomes, telefones ou endereços com número (privacidade).")
    novo_id = gerar_novo_id()

    bairro = escolher_opcao("\nBairro:", BAIRROS_VALIDOS)
    categoria = escolher_opcao("\nCategoria:", CATEGORIAS_VALIDAS)
    descricao = ler_texto_obrigatorio("\nDescrição breve do problema: ")
    local = ler_texto_obrigatorio("Local genérico (ex.: Praça central): ")

    nova = {
        "id": novo_id,
        "bairro": bairro,
        "categoria": categoria,
        "descricao": descricao,
        "local": local,
        "dia_abertura": DIA_ATUAL,
        "status": "aberta",
        "dia_conclusao": None,
    }

    # Mesma regra de validação usada nos dados iniciais.
    problemas = validar_ocorrencia(nova, ocorrencias_dic)
    if problemas:
        print("Cadastro recusado: " + "; ".join(problemas))
        return

    ocorrencias_lista.append(nova)       # lista: guarda o conjunto completo
    ocorrencias_dic[novo_id] = nova      # dicionário: acesso pelo ID
    fila_abertas.append(novo_id)         # fila: entra no fim, aguardando análise
    pilha_historico.append({             # pilha: registra o evento de abertura
        "id": novo_id,
        "status_antigo": "-",
        "status_novo": "aberta",
        "dia": DIA_ATUAL,
        "justificativa": "Ocorrência registrada",
    })
    print(f"\nOcorrência {novo_id} cadastrada com sucesso! Posição na fila: {len(fila_abertas)}.")


def validar_mudanca_status(status_atual, novo_status):
    """Regras para mudança de status. Devolve (permitido, mensagem)."""
    if novo_status not in STATUS_VALIDOS:
        return False, "Status desconhecido."
    elif novo_status == status_atual:
        return False, "A ocorrência já está com esse status. Nada foi alterado."
    elif status_atual == "concluída" and novo_status == "aberta":
        return False, ("Uma ocorrência concluída não volta para 'aberta'. "
                       "Para reabri-la, use 'em análise'.")
    else:
        return True, ""


def aplicar_mudanca_status(ocorrencia, novo_status, justificativa):
    """Atualiza o status, a fila e empilha o evento no histórico."""
    status_anterior = ocorrencia["status"]
    ocorrencia["status"] = novo_status

    if novo_status == "concluída":
        ocorrencia["dia_conclusao"] = DIA_ATUAL
    else:
        ocorrencia["dia_conclusao"] = None

    # Saiu de 'aberta': já foi examinada, então deixa a fila.
    if status_anterior == "aberta" and ocorrencia["id"] in fila_abertas:
        fila_abertas.remove(ocorrencia["id"])
    # Voltou para 'aberta': entra novamente no fim da fila.
    if novo_status == "aberta" and not ocorrencia["id"] in fila_abertas:
        fila_abertas.append(ocorrencia["id"])

    pilha_historico.append({
        "id": ocorrencia["id"],
        "status_antigo": status_anterior,
        "status_novo": novo_status,
        "dia": DIA_ATUAL,
        "justificativa": justificativa,
    })


def alterar_status():
    print("\n--- ALTERAR STATUS DE OCORRÊNCIA ---")
    id_oc = normalizar_id(input("ID da ocorrência: "))
    if id_oc not in ocorrencias_dic:
        print(f"Ocorrência '{id_oc}' não encontrada.")
        return

    ocorrencia = ocorrencias_dic[id_oc]
    print(f"Ocorrência {id_oc} - {ocorrencia['descricao']}")
    print(f"Status atual: {ocorrencia['status']}")

    novo_status = escolher_opcao("\nNovo status:", STATUS_VALIDOS)
    permitido, mensagem = validar_mudanca_status(ocorrencia["status"], novo_status)
    if not permitido:
        print(mensagem)
        return

    justificativa = ler_texto_obrigatorio("Justificativa da alteração: ")
    status_anterior = ocorrencia["status"]
    aplicar_mudanca_status(ocorrencia, novo_status, justificativa)
    print(f"Status alterado de '{status_anterior}' para '{novo_status}' e registrado no histórico.")


def atender_proxima_da_fila():
    print("\n--- FILA DE OCORRÊNCIAS NÃO EXAMINADAS ---")
    if not fila_abertas:
        print("A fila está vazia: todas as ocorrências já foram examinadas.")
        return

    print("Ordem de atendimento: " + " -> ".join(fila_abertas))
    proximo_id = fila_abertas[0]  # o primeiro que entrou é o primeiro a sair (FIFO)
    o = ocorrencias_dic[proximo_id]
    print(f"\nPróxima: [{o['id']}] {o['categoria']} - {o['descricao']}")
    print(f"Bairro: {o['bairro']} | Local: {o['local']} | Aberta no dia {o['dia_abertura']} "
          f"({DIA_ATUAL - o['dia_abertura']} dia(s) aguardando)")

    resposta = input("\nIniciar a análise desta ocorrência? (s/n): ").strip().lower()
    if resposta == "s" or resposta == "sim":
        fila_abertas.pop(0)
        aplicar_mudanca_status(o, "em análise", "Análise iniciada a partir da fila")
        print(f"Ocorrência {proximo_id} retirada da fila e marcada como 'em análise'.")
    else:
        print("Nenhuma alteração feita.")


def consultar_por_id():
    print("\n--- CONSULTAR OCORRÊNCIA POR ID ---")
    id_oc = normalizar_id(input("ID da ocorrência: "))
    if id_oc not in ocorrencias_dic:
        print(f"Ocorrência '{id_oc}' não encontrada.")
        return

    o = ocorrencias_dic[id_oc]  # acesso direto pelo dicionário
    print(f"\nID:         {o['id']}")
    print(f"Bairro:     {o['bairro']}")
    print(f"Categoria:  {o['categoria']}")
    print(f"Descrição:  {o['descricao']}")
    print(f"Local:      {o['local']}")
    print(f"Abertura:   dia {o['dia_abertura']}")
    print(f"Status:     {o['status']} ({SIGNIFICADO_STATUS[o['status']]})")
    if o["status"] == "concluída":
        print(f"Conclusão:  dia {o['dia_conclusao']} "
              f"({o['dia_conclusao'] - o['dia_abertura']} dia(s) de atendimento)")

    print("\nHistórico desta ocorrência (mais recente primeiro):")
    encontrou = False
    for evento in reversed(pilha_historico):
        if evento["id"] == id_oc:
            print(f"  dia {evento['dia']}: {evento['status_antigo']} -> {evento['status_novo']}"
                  f" | {evento['justificativa']}")
            encontrou = True
    if not encontrou:
        print("  Nenhum evento registrado.")


def listar_por_filtro():
    print("\n--- FILTRAR OCORRÊNCIAS ---")
    cat = escolher_opcao("Filtrar por categoria:", CATEGORIAS_VALIDAS, permitir_vazio=True)
    stat = escolher_opcao("\nFiltrar por status:", STATUS_VALIDOS, permitir_vazio=True)

    filtradas = []
    for o in ocorrencias_lista:
        # Filtro vazio aceita qualquer valor; filtro preenchido exige igualdade.
        if (cat == "" or o["categoria"] == cat) and (stat == "" or o["status"] == stat):
            filtradas.append(o)

    print(f"\nFiltro -> categoria: {cat or 'todas'} | status: {stat or 'todos'}\n")
    if not filtradas:
        print("Nenhuma ocorrência encontrada para esses filtros.")
    else:
        exibir_tabela_ocorrencias(filtradas)


def ver_historico_recente():
    print("\n--- HISTÓRICO RECENTE (PILHA: o topo é o evento mais recente) ---")
    if not pilha_historico:
        print("Nenhum evento registrado.")
        return

    quantidade = input("Quantos eventos deseja ver? (Enter = todos): ").strip()
    if quantidade.isdigit() and int(quantidade) > 0:
        limite = int(quantidade)
    else:
        limite = len(pilha_historico)

    exibidos = 0
    for evento in reversed(pilha_historico):  # percorre do topo para a base
        if exibidos >= limite:
            break
        print(f"  dia {evento['dia']:>2} | ID {evento['id']}: {evento['status_antigo']} -> "
              f"{evento['status_novo']} | {evento['justificativa']}")
        exibidos += 1
    print(f"\n{exibidos} de {len(pilha_historico)} evento(s) exibido(s).")


def exibir_hierarquia():
    print("\n--- OCORRÊNCIAS POR BAIRRO (HIERARQUIA bairro -> categoria -> ocorrências) ---")
    hierarquia = montar_hierarquia()
    for bairro in BAIRROS_VALIDOS:
        if bairro not in hierarquia:
            continue
        total_bairro = 0
        for categoria in hierarquia[bairro]:
            total_bairro += len(hierarquia[bairro][categoria])
        print(f"\n{bairro} ({total_bairro} ocorrência(s))")
        for categoria in hierarquia[bairro]:
            print(f"  └─ {categoria}")
            for id_oc in hierarquia[bairro][categoria]:
                o = ocorrencias_dic[id_oc]
                print(f"       └─ [{id_oc}] {o['descricao']} ({o['status']})")


def exibir_inconsistentes():
    print("\n--- REGISTROS INCONSISTENTES (barrados pela validação) ---")
    if not registros_inconsistentes:
        print("Nenhum registro inconsistente encontrado.")
        return
    print("Esses registros NÃO entram nas consultas nem nos indicadores até serem corrigidos")
    print("na lista DADOS_INICIAIS do código.\n")
    for item in registros_inconsistentes:
        r = item["registro"]
        print(f"ID {r['id'] or '(sem ID)'} - {r['descricao'] or '(sem descrição)'}")
        for problema in item["problemas"]:
            print(f"   * {problema}")


def exibir_ajuda():
    print("\n--- AJUDA ---")
    print("Escolha as opções digitando o número correspondente e pressione Enter.")
    print("IDs podem ser digitados com ou sem zeros à esquerda (ex.: 7 ou 007).")
    print("\nSignificado de cada status:")
    for status in STATUS_VALIDOS:
        print(f"  - {status}: {SIGNIFICADO_STATUS[status]}")
    print("\nRegras de mudança de status:")
    print("  - não é possível 'mudar' para o status que a ocorrência já tem;")
    print("  - uma ocorrência concluída não volta para 'aberta' (use 'em análise' para reabrir).")
    print("\nPrivacidade: o sistema usa apenas dados fictícios e locais genéricos.")
    print("Não cadastre nomes, telefones ou endereços com número.")


def recarregar_dados():
    resposta = input("Descartar as alterações desta sessão e voltar aos dados iniciais? (s/n): ")
    if resposta.strip().lower() in ["s", "sim"]:
        carregar_dados()
        print("Dados iniciais recarregados com sucesso.")
    else:
        print("Operação cancelada.")


# ---------------------------------------------------------------------------
# 8. MENU PRINCIPAL
# ---------------------------------------------------------------------------

def menu():
    print("=" * 55)
    print("        NEIGHBORHOOD ACTION DASHBOARD")
    print("   Painel comunitário de ocorrências - CitizenTech")
    print("=" * 55)
    print(f"{len(ocorrencias_lista)} ocorrências carregadas | "
          f"{len(fila_abertas)} na fila | "
          f"{len(registros_inconsistentes)} registro(s) inconsistente(s) isolado(s)")

    while True:
        print("\nMENU DE OPÇÕES:")
        print(" 1. Listar todas as ocorrências")
        print(" 2. Painel de indicadores")
        print(" 3. Cadastrar nova ocorrência")
        print(" 4. Consultar ocorrência por ID")
        print(" 5. Filtrar ocorrências por categoria e/ou status")
        print(" 6. Alterar status de uma ocorrência")
        print(" 7. Atender a próxima ocorrência da fila")
        print(" 8. Ver histórico recente (pilha)")
        print(" 9. Ver ocorrências por bairro (hierarquia)")
        print("10. Ver registros inconsistentes")
        print("11. Ajuda (significado dos status e regras)")
        print("12. Recarregar dados originais")
        print(" 0. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            listar_todas()
        elif opcao == "2":
            exibir_indicadores()
        elif opcao == "3":
            cadastrar_ocorrencia()
        elif opcao == "4":
            consultar_por_id()
        elif opcao == "5":
            listar_por_filtro()
        elif opcao == "6":
            alterar_status()
        elif opcao == "7":
            atender_proxima_da_fila()
        elif opcao == "8":
            ver_historico_recente()
        elif opcao == "9":
            exibir_hierarquia()
        elif opcao == "10":
            exibir_inconsistentes()
        elif opcao == "11":
            exibir_ajuda()
        elif opcao == "12":
            recarregar_dados()
        elif opcao == "0":
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida! Digite um número de 0 a 12.")


if __name__ == "__main__":
    carregar_dados()
    menu()
