# 🏙️ Neighborhood Action Dashboard — CitizenTech

**Global Solution 2026.2 — FIAP**

Painel comunitário interativo em modo texto (CLI) desenvolvido em Python para registrar, organizar, consultar e acompanhar ocorrências de infraestrutura e manutenção urbana em bairros.

---

## 👥 1. Equipe

* **Aldo Roschel** — RM 575601
* **Larissa Bressanini Lehn** — RM 575921
* **Nicole Luiza Mascarenhas Zerbato** — RM 575981

---

## 🏘️ 2. Comunidade Simulada

O sistema representa uma comunidade urbana dividida em **4 bairros padronizados** (`Centro`, `Bairro Alto`, `Bairro Norte` e `Bairro Sul`), onde moradores e gestores comunitários monitoram problemas cotidianos do espaço público divididos em **4 categorias**:
1. `iluminação` (ex.: postes apagados, cabos rompidos, falta de ponto de luz);
2. `acessibilidade` (ex.: calçadas danificadas, ausência de rampas para cadeirantes);
3. `limpeza` (ex.: acúmulo de lixo em terrenos, bueiros entupidos, banheiros sem manutenção);
4. `conservação de espaços coletivos` (ex.: grama alta em praças, equipamentos enferrujados).

### Linha do Tempo e Base de Dados Inicial
* **Tempo Simulado (`DIA_ATUAL = 20`):** As datas são representadas por números inteiros (dia 1, dia 2, ..., dia 20), permitindo medir o tempo de resolução e o tempo de espera por meio de subtrações diretas.
* **Dados Embutidos (`DADOS_INICIAIS` e `HISTORICO_INICIAL`):** O arquivo já inclui **14 registros de ocorrências** e **10 eventos históricos de mudança de status**.
  * **12 registros válidos (`001` a `012`):** Distribuídos entre os bairros e com diferentes status (`aberta`, `em análise` e `concluída`).
  * **2 registros propositalmente inconsistentes (`013` e `014`):** Incluídos na base simulada para testar e demonstrar a barreira de validação automática (`013` possui a categoria inválida `"conservação"` e `014` está com o campo obrigatório `"local"` vazio).

---

## 🗂️ 3. Estruturas de Dados e Justificativas

O sistema utiliza 6 estruturas de dados em memória, escolhidas estrategicamente de acordo com a operação que precisam realizar:

| Estrutura | Implementação no Código | Justificativa de Uso |
| :--- | :--- | :--- |
| **Lista** | `ocorrencias_lista` e `registros_inconsistentes` | Mantém a coleção completa de ocorrências válidas em ordem cronológica de inserção. É ideal para percorrer sequencialmente todos os registros em listagens gerais, aplicação de filtros e cálculos globais. |
| **Dicionário (Hash Map)** | `ocorrencias_dic` | Indexa cada ocorrência utilizando seu `id` como chave (`{"001": {...}}`). Garante busca direta e verificação de existência em tempo constante $\mathcal{O}(1)$ nas opções de consulta por ID e alteração de status, evitando percorrer toda a lista. |
| **Fila (FIFO — *First In, First Out*)** | `fila_abertas` | Armazena os IDs das ocorrências com status `"aberta"` na ordem exata de chegada. Garante justiça no atendimento comunitário: a demanda que entrou primeiro na fila (`fila_abertas[0]`) é a primeira a ser examinada e removida (`pop(0)`). |
| **Pilha (LIFO — *Last In, First Out*)** | `pilha_historico` | Armazena os eventos de mudança de status em ordem cronológica, onde o último evento adicionado fica no topo (`append`). Permite exibir o histórico de auditoria do evento mais recente para o mais antigo (`reversed(pilha_historico)`). |
| **Hierarquia (Árvore)** | `montar_hierarquia()` | Dicionário aninhado em três níveis (`Bairro` $\rightarrow$ `Categoria` $\rightarrow$ `Lista de IDs`). Justifica-se pela necessidade de agrupar territorialmente os problemas, permitindo visualizar a distribuição das demandas dentro de cada bairro e subcategoria. |
| **Matriz (Lista de Listas)** | `montar_matriz()` | Grade bidimensional $4 \times 3$ onde as linhas representam as `CATEGORIAS_VALIDAS` e as colunas representam os `STATUS_VALIDOS`. Facilita o cruzamento tabular e a soma rápida de linhas e colunas para alimentar o Painel de Indicadores. |

---

## ⚙️ 4. Regras Lógicas e de Negócio

O sistema aplica regras estritas para garantir a integridade dos dados desde a carga inicial até as interações do usuário:

1. **Validação de Entrada (`validar_ocorrencia`):**
   * Todos os campos em `CAMPOS_OBRIGATORIOS` (`id`, `bairro`, `categoria`, `descricao`, `local`, `dia_abertura`, `status`) devem existir e não podem ser vazios ou `None`.
   * O `id` deve ser único (não pode constar em `ocorrencias_dic`).
   * Os valores de `bairro`, `categoria` e `status` devem pertencer estritamente às listas padronizadas (`BAIRROS_VALIDOS`, `CATEGORIAS_VALIDAS`, `STATUS_VALIDOS`).
   * `dia_abertura` deve ser do tipo inteiro (`int`).
   * Se `status == "concluída"`, o campo `dia_conclusao` passa a ser obrigatoriamente um número inteiro (`int`). Caso contrário, permanece `None`.
2. **Isolamento de Inconsistências:**
   * Registros que violam qualquer regra acima são barrados na carga inicial e armazenados em `registros_inconsistentes` junto à lista de motivos. Eles **não entram** nos cálculos de indicadores nem nas buscas.
3. **Regras de Transição de Status (`validar_mudanca_status`):**
   * **Mudança redundante bloqueada:** Uma ocorrência não pode ter seu status alterado para o mesmo status em que já se encontra.
   * **Proibição de regressão direta para aberta:** Uma ocorrência `"concluída"` não pode voltar para `"aberta"`. Caso o problema persista e ela precise ser reaberta, deve ir para `"em análise"`.
   * **Sincronização com a Fila:** Ao sair do status `"aberta"`, o ID da ocorrência é removido de `fila_abertas`. Se uma ocorrência voltar para `"aberta"`, seu ID retorna ao final da fila.

---

## 🧮 5. Expressões Booleanas

As decisões lógicas do código são governadas por expressões booleanas compostas utilizando operadores lógicos (`and`, `or`, `not`) e relacionais. As principais são:

### A. Filtro Combinado de Categoria e Status (`listar_por_filtro`)
```python
(cat == "" or o["categoria"] == cat) and (stat == "" or o["status"] == stat)
```
* **Proposições:**
  * $P$: `cat == ""` (usuário não aplicou filtro de categoria)
  * $Q$: `o["categoria"] == cat` (categoria da ocorrência coincide com o filtro)
  * $R$: `stat == ""` (usuário não aplicou filtro de status)
  * $S$: `o["status"] == stat` (status da ocorrência coincide com o filtro)
* **Fórmula Lógica:** $(P \lor Q) \land (R \lor S)$
* **Funcionamento:** A ocorrência só é incluída no resultado se satisfizer a condição de categoria **E** a condição de status simultaneamente. Dentro de cada parêntese, o operador `or` ($\lor$) permite que o filtro funcione tanto quando o usuário escolhe uma opção específica quanto quando pressiona `Enter` para aceitar todas.

### B. Verificação de Campos Obrigatórios (`validar_ocorrencia`)
```python
campo not in registro or registro[campo] == "" or registro[campo] is None
```
* **Fórmula Lógica:** $\neg E \lor V \lor N$ (onde $E$ é a existência da chave, $V$ é string vazia e $N$ é valor nulo). Basta que **uma** dessas condições seja verdadeira para que o campo seja considerado ausente/inválido.

### C. Consistência de Conclusão (`validar_ocorrencia`)
```python
registro["status"] == "concluída" and not type(registro.get("dia_conclusao")) == int
```
* **Fórmula Lógica:** $C \land \neg I$ (onde $C$ é estar concluída e $I$ é possuir dia de conclusão inteiro). Identifica inconsistência apenas quando a ocorrência consta como concluída **e** não possui um dia de conclusão válido.

### D. Contabilização de Pendências (`exibir_indicadores`)
```python
o["status"] == "aberta" or o["status"] == "em análise"
```
* **Fórmula Lógica:** $A \lor E$. Agrupa ocorrências não finalizadas para o cálculo da taxa de pendência e do tempo médio de espera.

---

## 📊 6. Indicadores e Fórmulas

A opção **2 (Painel de Indicadores)** processa os dados válidos e apresenta métricas quantitativas acompanhadas de uma interpretação automática do cenário da comunidade:

1. **Proporção por Status e por Categoria:**
   $$\text{Porcentagem} = \left(\frac{\text{Quantidade do Grupo}}{\text{Total de Ocorrências Válidas}}\right) \times 100$$
2. **Taxa de Pendências:**
   $$\text{Taxa de Pendências} = \left(\frac{\text{Abertas} + \text{Em Análise}}{\text{Total de Ocorrências Válidas}}\right) \times 100$$
3. **Tempo Médio até a Conclusão** (considera apenas ocorrências com `status == "concluída"`):
   $$\text{Tempo Médio de Conclusão} = \frac{\sum (\text{dia\_conclusao} - \text{dia\_abertura})}{\text{Total de Concluídas}}$$
   * *Com os dados iniciais:* $\frac{(9-2) + (12-3) + (10-6)}{3} = \frac{7 + 9 + 4}{3} = \frac{20}{3} \approx 6,67 \text{ dias}$.
4. **Tempo Médio de Espera das Pendências** (considera ocorrências `"aberta"` ou `"em análise"` no `DIA_ATUAL = 20`):
   $$\text{Tempo Médio de Espera} = \frac{\sum (\text{DIA\_ATUAL} - \text{dia\_abertura})}{\text{Total de Pendências}}$$
   * *Com os dados iniciais:* $\frac{123}{9} \approx 13,67 \text{ dias}$.
5. **Interpretação Automática:**
   * Identifica a(s) categoria(s) com maior volume de chamados (`max(totais_categoria)`).
   * Aponta o **bairro mais crítico** (com maior acúmulo de ocorrências não concluídas).
   * Avalia a agilidade do atendimento: se as pendências superam $50\%$ do total, emite alerta indicando necessidade de maior agilidade; caso contrário, informa que o atendimento acompanha o ritmo da comunidade.

---

## 💻 7. Exemplos de Uso e Execução

### Como Executar
A partir da pasta raiz do repositório, execute no terminal (requer Python 3.8+, sem bibliotecas externas):
```bash
python src/sistema.py
```

### Exemplo 1: Atendendo a Próxima Ocorrência da Fila (Opção 7)
Demonstra o comportamento **FIFO** da fila de atendimento:
```text
Escolha uma opção: 7

--- FILA DE OCORRÊNCIAS NÃO EXAMINADAS ---
Ordem de atendimento: 003 -> 006 -> 009 -> 010 -> 012

Próxima: [003] limpeza - Acúmulo de lixo em terreno baldio
Bairro: Bairro Sul | Local: Terreno próximo à escola | Aberta no dia 3 (17 dia(s) aguardando)

Iniciar a análise desta ocorrência? (s/n): s
Ocorrência 003 retirada da fila e marcada como 'em análise'.
```

### Exemplo 2: Consultando Ocorrência por ID com Normalização (Opção 4)
O usuário pode digitar apenas `2` em vez de `002` graças à função `normalizar_id()`:
```text
Escolha uma opção: 4

--- CONSULTAR OCORRÊNCIA POR ID ---
ID da ocorrência: 2

ID:         002
Bairro:     Bairro Alto
Categoria:  acessibilidade
Descrição:  Calçada danificada impedindo a passagem de cadeirantes
Local:      Avenida central
Abertura:   dia 2
Status:     concluída (o problema foi resolvido e a ocorrência foi encerrada)
Conclusão:  dia 9 (7 dia(s) de atendimento)

Histórico desta ocorrência (mais recente primeiro):
  dia 9: em análise -> concluída | Calçada reformada e rampa refeita
  dia 3: aberta -> em análise | Equipe de vistoria agendada
```

### Exemplo 3: Verificando Registros Inconsistentes Isolados (Opção 10)
Demonstra a transparência na auditoria de dados inválidos:
```text
Escolha uma opção: 10

--- REGISTROS INCONSISTENTES (barrados pela validação) ---
Esses registros NÃO entram nas consultas nem nos indicadores até serem corrigidos
na lista DADOS_INICIAIS do código.

ID 013 - Banco quebrado no ponto de ônibus
   * categoria desconhecida: 'conservação'
ID 014 - Lâmpada piscando durante a noite
   * campo obrigatório 'local' ausente
```

---

## ♿🔒 8. Acessibilidade, Usabilidade e Privacidade

### Acessibilidade e Usabilidade no Terminal
* **Seleção por Números (`escolher_opcao`):** Para escolher bairros, categorias e status, o usuário digita apenas números (`1`, `2`, `3`...). Isso elimina erros de digitação, problemas com acentuação (como em `"iluminação"` ou `"concluída"`) e reduz a barreira para pessoas com pouca familiaridade digital.
* **Normalização de IDs (`normalizar_id`):** Aceita entradas como `4`, `04` ou `004`, preenchendo zeros à esquerda automaticamente (`zfill(3)`).
* **Linguagem Simples e Explicativa:** A opção **11 (Ajuda)** e as telas de consulta traduzem o significado de cada status em linguagem cidadã acessível, além de explicitar as fórmulas matemáticas no próprio painel de indicadores.
* **Compatibilidade com Leitores de Tela:** A interface utiliza apenas texto puro estruturado e divisores simples, sem depender de cores ou elementos gráficos complexos.

### Privacidade (*Privacy by Design* / LGPD)
* **Zero Dados Pessoais:** O sistema não coleta nem armazena nome, CPF, telefone, e-mail ou endereço residencial dos cidadãos.
* **Locais Genéricos e Aviso Ativo:** No momento do cadastro (Opção 3), o sistema exibe um alerta explícito orientando o usuário a informar apenas pontos de referência públicos (ex.: *"Praça central"*, *"Entrada do posto de saúde"*), prevenindo a exposição indevida de moradores.

---

## 🏁 9. Conclusões e Limitações

### Conclusões
O **Neighborhood Action Dashboard** cumpre o objetivo de oferecer uma ferramenta leve, auditável e educativa para a gestão de demandas comunitárias. O uso combinado de **Listas, Dicionários, Filas, Pilhas, Árvores e Matrizes** garante que cada funcionalidade opere na estrutura mais adequada — unindo rapidez na busca por ID, justiça na ordem de atendimento (FIFO), rastreabilidade histórica (LIFO) e clareza analítica nos indicadores matemáticos.

### Limitações Atuais e Trabalhos Futuros
1. **Persistência em Memória:** Os dados são mantidos em memória RAM durante a execução (a partir de `DADOS_INICIAIS`). Ao encerrar o programa (`Opção 0`), os novos cadastros daquela sessão não são salvos em disco. Uma evolução natural é a persistência em banco de dados relacional ou arquivos JSON/CSV.
2. **Datas Simuladas:** O uso de dias inteiros (`DIA_ATUAL = 20`) facilita a validação acadêmica e o cálculo didático das médias, mas em produção deve ser substituído por timestamps reais (`datetime`).
3. **Interface Monousuário (CLI):** Por rodar em terminal local, atende um operador por vez. Como próximo passo, a lógica de negócio já modulada pode ser conectada a uma API Web ou aplicativo móvel para acesso simultâneo pelos moradores do bairro.