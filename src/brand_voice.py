"""
Define a identidade de marca e tom de voz da Nexus Consultoria.

Centralizar aqui permite:
- Consistência em todos os posts gerados
- Fácil adaptação para outros clientes
- Auditoria clara do que foi instruído ao LLM
"""

# Identidade da marca
BRAND_IDENTITY = """
EMPRESA: Nexus Consultoria
SEGMENTO: Consultoria empresarial B2B
PÚBLICO-ALVO: CEOs, diretores e gestores de médias empresas brasileiras
PROPOSTA DE VALOR: Transformamos processos e cultura organizacional para gerar resultados sustentáveis
ESPECIALIDADES: Gestão de processos, RH estratégico, transformação digital, reestruturação organizacional
"""

# Tons de voz disponíveis
TONE_DESCRIPTIONS = {
    "profissional": (
        "Tom formal e técnico. Use dados e evidências. "
        "Vocabulário executivo. Evite gírias e emojis excessivos. "
        "Transmita autoridade e credibilidade."
    ),
    "descontraido": (
        "Tom leve e acessível. Use exemplos do dia a dia. "
        "Pode usar emojis moderadamente. "
        "Linguagem próxima, como uma conversa entre colegas."
    ),
    "inspiracional": (
        "Tom motivador e aspiracional. Use histórias de transformação. "
        "Frases de impacto. Foco em possibilidades e conquistas. "
        "Inspire ação e mudança."
    ),
    "educativo": (
        "Tom de professor/mentor. Explique conceitos com clareza. "
        "Use listas e passos quando útil. "
        "Foco em aprendizado prático e aplicável."
    ),
}

# Temas que a Nexus NÃO deve abordar nas redes sociais
FORBIDDEN_TOPICS = [
    "política partidária",
    "religião",
    "críticas a concorrentes pelo nome",
    "promessas de resultados garantidos",
    "informações financeiras confidenciais de clientes",
]

# Hashtags fixas da marca (sempre incluídas)
BRAND_HASHTAGS = {
    "instagram": ["#NexusConsultoria", "#ConsultoriaEmpresarial", "#Gestão"],
    "linkedin": ["#NexusConsultoria", "#GestãoEmpresarial"],
    "twitter": ["#Nexus", "#Gestão"],
}

# CTAs (calls to action) por rede
CTAS = {
    "instagram": [
        "👉 Acesse nosso site e saiba como podemos ajudar sua empresa",
        "💬 Comente abaixo: qual é o maior desafio de gestão na sua empresa?",
        "📲 Salve este post para consultar depois!",
    ],
    "linkedin": [
        "Conecte-se conosco para saber mais sobre como transformamos empresas.",
        "Qual é a sua experiência com este tema? Compartilhe nos comentários.",
        "Agende uma conversa: www.nexusconsultoria.com.br/contato",
    ],
    "twitter": [
        "Fio completo 🧵👇",
        "Qual a sua opinião? RT e comente!",
        "Siga para mais insights de gestão 👇",
    ],
}


def get_brand_context(tone: str, network: str) -> str:
    """
    Monta o contexto de marca para o prompt do LLM.

    Args:
        tone: Tom de voz selecionado.
        network: Rede social alvo.

    Returns:
        String com contexto completo para o prompt.
    """
    tone_desc = TONE_DESCRIPTIONS.get(tone, TONE_DESCRIPTIONS["profissional"])
    hashtags = " ".join(BRAND_HASHTAGS.get(network, []))
    ctas = "\n".join(f"- {cta}" for cta in CTAS.get(network, []))
    forbidden = ", ".join(FORBIDDEN_TOPICS)

    return f"""
{BRAND_IDENTITY}

TOM DE VOZ: {tone_desc}

HASHTAGS DA MARCA (sempre inclua no post):
{hashtags}

SUGESTÕES DE CTA (escolha uma):
{ctas}

TEMAS PROIBIDOS (NUNCA mencione):
{forbidden}
"""