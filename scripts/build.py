#!/usr/bin/env python3
"""Gera o site estático da Naturalle a partir de data/site.json."""

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "data" / "site.json").read_text())
COMPANY = DATA["company"]
PRODUCTS = {item["slug"]: item for item in DATA["products"]}
CATEGORIES = {item["id"]: item for item in DATA["categories"]}

CAT_LABEL = {"humana": "Nutrição Humana", "animal": "Nutrição Animal"}


def esc(value):
    return html.escape(str(value or ""), quote=True)


def prefix(depth):
    return "../" * depth


def asset(depth, path):
    return f"{prefix(depth)}{path}"


def paragraphs(items):
    return "".join(f"<p>{esc(item)}</p>" for item in items)


def condition_label(value):
    mapping = {"Min": "Mínimo", "Máx": "Máximo", "Mínimo": "Mínimo", "Máximo": "Máximo"}
    return mapping.get(value, value)


def parameter_label(value):
    if value == "Atividade Ureátiva":
        return "Atividade ureática"
    return value


def head(depth, title, description, canonical):
    p = prefix(depth)
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <link rel="canonical" href="{esc(canonical)}">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{esc(canonical)}">
  <meta name="theme-color" content="#0f3d2a">
  <link rel="icon" href="{p}assets/favicon-32.png" sizes="32x32">
  <link rel="apple-touch-icon" href="{p}assets/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,520;9..144,620&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{p}assets/css/styles.css">
</head>
<body>
<a class="skip" href="#conteudo">Ir para o conteúdo</a>
"""


def header(depth, active):
    p = prefix(depth)

    def item(key, href, label):
        cls = "is-active" if active == key else ""
        return f'<a class="{cls}" href="{p}{href}">{label}</a>'

    return f"""
<header class="site-header">
  <div class="topbar">
    <div class="container topbar__inner">
      <a href="mailto:{esc(COMPANY['email'])}">{esc(COMPANY['email'])}</a>
      <a href="tel:{esc(COMPANY['phoneTel'])}">{esc(COMPANY['phoneDisplay'])}</a>
      <a class="topbar__grow" href="{esc(COMPANY['linkedin'])}" target="_blank" rel="noopener">LinkedIn</a>
    </div>
  </div>
  <div class="container nav">
    <a class="logo" href="{p}"><img src="{p}assets/images/logo-naturalle.png" alt="Naturalle"></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
    <nav class="site-nav" id="site-nav" aria-label="Principal">
      {item("home", "", "Home")}
      {item("about", "quem-somos/", "Quem somos")}
      <div class="nav-drop">
        {item("products", "produtos/", "Produtos")}
        <div class="nav-drop__menu">
          <a href="{p}produtos/">Todos os produtos</a>
          <a href="{p}produtos/nutricao-humana/">Nutrição Humana</a>
          <a href="{p}produtos/nutricao-animal/">Nutrição Animal</a>
        </div>
      </div>
      {item("contact", "contato/", "Contato")}
      <a class="btn" href="{p}contato/">Fale conosco</a>
    </nav>
  </div>
</header>
<main id="conteudo">
"""


def footer(depth):
    p = prefix(depth)
    product_links = "\n".join(
        f'<li><a href="{p}produtos/{esc(item["slug"])}/">{esc(item["title"])}</a></li>'
        for item in DATA["products"][:5]
    )
    return f"""
</main>
<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <img class="footer-logo" src="{p}assets/images/logo-naturalle-branco.png" alt="Naturalle">
      <p>Há mais de 30 anos, a Naturalle desenvolve processos industriais únicos de fabricação e controle, buscando a melhor padronização e a mais alta qualidade possível em seus produtos.</p>
    </div>
    <div>
      <h3>Navegação</h3>
      <ul>
        <li><a href="{p}">Home</a></li>
        <li><a href="{p}quem-somos/">Quem somos</a></li>
        <li><a href="{p}produtos/nutricao-humana/">Nutrição Humana</a></li>
        <li><a href="{p}produtos/nutricao-animal/">Nutrição Animal</a></li>
        <li><a href="{p}contato/">Contato</a></li>
        <li><a href="{p}privacidade/">Política de Privacidade</a></li>
      </ul>
    </div>
    <div>
      <h3>Produtos</h3>
      <ul>
        {product_links}
        <li><a href="{p}produtos/">Ver todos</a></li>
      </ul>
    </div>
    <div>
      <h3>Contato</h3>
      <ul>
        <li><a href="mailto:{esc(COMPANY['email'])}">{esc(COMPANY['email'])}</a></li>
        <li><a href="tel:{esc(COMPANY['phoneTel'])}">{esc(COMPANY['phoneDisplay'])}</a></li>
        <li><a href="https://wa.me/{esc(COMPANY['whatsapp'])}" target="_blank" rel="noopener">WhatsApp</a></li>
        <li><a href="{esc(COMPANY['linkedin'])}" target="_blank" rel="noopener">LinkedIn</a></li>
      </ul>
    </div>
  </div>
  <div class="container legal-line">
    <span>© 2026 Naturalle. CNPJ {esc(COMPANY['cnpj'])}.</span>
    <a href="{p}privacidade/">Política de Privacidade</a>
  </div>
</footer>
<a class="wa" href="https://wa.me/{esc(COMPANY['whatsapp'])}" target="_blank" rel="noopener">WhatsApp</a>
<script src="{p}assets/js/main.js"></script>
</body>
</html>
"""


def write_page(relative, content):
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(relative)


def chips(categories):
    return "".join(f'<span class="chip">{esc(CAT_LABEL[item])}</span>' for item in categories)


def product_card(depth, product):
    p = prefix(depth)
    summary = product["description"][0]
    if len(summary) > 150:
        summary = summary[:147].rsplit(" ", 1)[0] + "…"
    cats = " ".join(product["categories"])
    return f"""
<a class="product-card" data-product data-category="{esc(cats)}" data-name="{esc(product['title'])}" href="{p}produtos/{esc(product['slug'])}/">
  <img src="{asset(depth, product['image'])}" alt="{esc(product['title'])}">
  <div class="product-card__body">
    <div class="chips">{chips(product['categories'])}</div>
    <h3>{esc(product['title'])}</h3>
    <p>{esc(summary)}</p>
    <span class="linkish">Ver ficha técnica</span>
  </div>
</a>
"""


def card_grid(depth, slugs):
    cards = "\n".join(product_card(depth, PRODUCTS[slug]) for slug in slugs)
    return f'<div class="card-grid">{cards}</div>'


def home():
    depth = 0
    humana = CATEGORIES["humana"]
    animal = CATEGORIES["animal"]
    body = f"""
<section class="hero">
  <div class="container hero__grid">
    <div>
      <p class="eyebrow">Ingredientes vegetais</p>
      <h1>Especialistas em desenvolver soluções com ingredientes vegetais</h1>
      <p class="lead">Com a premissa de que os ingredientes de origem vegetal são matrizes alimentares essenciais, completas e fundamentais para o suprimento e a segurança alimentar global, a Naturalle dedica sua trajetória de mais de três décadas à pesquisa, desenvolvimento e fornecimento de insumos derivados dessas fontes.</p>
      <div class="hero__actions">
        <a class="btn" href="produtos/">Conhecer os produtos</a>
        <a class="btn btn--ghost" href="contato/">Falar com vendas</a>
      </div>
    </div>
    <div class="hero__visual">
      <img class="hero__photo" src="assets/images/categorias/nutricao-humana.webp" alt="Ingredientes para nutrição humana">
      <img class="hero__photo hero__photo--b" src="assets/images/categorias/nutricao-animal.webp" alt="Ingredientes para nutrição animal">
      <p class="hero__badge"><strong>+30 anos</strong><span>produzindo alimentos derivados de vegetais</span></p>
    </div>
  </div>
</section>
<section>
  <div class="container stats">
    <div class="stat"><strong>+30</strong><span>anos de experiência</span></div>
    <div class="stat"><strong>2</strong><span>linhas: humana e animal</span></div>
    <div class="stat"><strong>{len(PRODUCTS)}</strong><span>ingredientes no portfólio</span></div>
    <div class="stat"><strong>Brasil</strong><span>atuação em todo o país</span></div>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="section__head">
      <div>
        <p class="eyebrow">Linhas</p>
        <h2>Nossos produtos</h2>
      </div>
      <p>Conheça as linhas de nutrição humana e nutrição animal.</p>
    </div>
    <div class="category-grid">
      <a class="category-card" href="produtos/nutricao-humana/">
        <img src="{esc(humana['image'])}" alt="Nutrição Humana">
        <div class="category-card__body">
          <h3>Nutrição Humana</h3>
          <p>{esc(humana['summary'])}</p>
          <span class="linkish">Ver produtos</span>
        </div>
      </a>
      <a class="category-card" href="produtos/nutricao-animal/">
        <img src="{esc(animal['image'])}" alt="Nutrição Animal">
        <div class="category-card__body">
          <h3>Nutrição Animal</h3>
          <p>{esc(animal['summary'])}</p>
          <span class="linkish">Ver produtos</span>
        </div>
      </a>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="container">
    <div class="section__head">
      <div>
        <p class="eyebrow">Portfólio</p>
        <h2>Ingredientes para a indústria</h2>
      </div>
      <a class="btn btn--ghost" href="produtos/">Ver todos</a>
    </div>
    {card_grid(depth, [item['slug'] for item in DATA['products']])}
  </div>
</section>
<section class="section" style="padding-top:10px">
  <div class="container why">
    <div>
      <p class="eyebrow">Por que escolher a Naturalle?</p>
      <h2>Temos os diferenciais que sua empresa precisa</h2>
      <p class="lead">Nos esforçamos para sermos os melhores em nosso segmento. Por isso, investimos em treinamento e alto padrão de qualidade para oferecer a melhor experiência de compra aos nossos clientes.</p>
    </div>
    <div class="why__list">
      <div class="why__item"><span>01</span><strong>Produtos à pronta entrega</strong></div>
      <div class="why__item"><span>02</span><strong>Produtos padronizados</strong></div>
      <div class="why__item"><span>03</span><strong>Facilidade de logística</strong></div>
      <div class="why__item"><span>04</span><strong>Rigoroso padrão de qualidade</strong></div>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="container">
    <div class="band">
      <div>
        <h2>Fale com a Naturalle</h2>
        <p>Preencha os dados de contato e retornamos para entender a aplicação, o volume e a especificação que a sua indústria precisa.</p>
      </div>
      <a class="btn btn--light" href="contato/">Enviar mensagem</a>
    </div>
  </div>
</section>
"""
    title = "Naturalle | Ingredientes vegetais para a indústria"
    description = "Produzimos alimentos derivados de vegetais, como farinhas de soja, arroz e milho, proteínas e ingredientes para nutrição humana e animal."
    page = head(depth, title, description, COMPANY["url"] + "/") + header(depth, "home") + body + footer(depth)
    write_page("index.html", page)


def about():
    depth = 1
    values = ["Ética", "Qualidade", "Inovação", "Foco no cliente", "Sustentabilidade", "Transparência", "Respeito"]
    value_html = "".join(f'<span class="chip">{esc(item)}</span>' for item in values)
    pillars = [
        ("Origem vegetal", "Nossa expertise começou na soja e evolui continuamente para novas matérias-primas vegetais, acompanhando as tendências do mercado e as necessidades da indústria."),
        ("Tecnologia e inovação", "Investimos em pesquisa, desenvolvimento e processos para oferecer ingredientes com alto desempenho, segurança e qualidade."),
        ("Parceria com o cliente", "Mais do que fornecer ingredientes, buscamos entender cada aplicação para construir soluções que agreguem valor aos produtos dos nossos clientes."),
        ("Compromisso com o futuro", "Crescemos de forma responsável, valorizando pessoas, relações de confiança e práticas sustentáveis em toda a cadeia produtiva."),
    ]
    pillar_html = "".join(
        f'<article class="pillar"><h3>{esc(title)}</h3><p>{esc(text)}</p></article>' for title, text in pillars
    )
    diffs = ["+30 anos de experiência", "Portfólio de ingredientes vegetais", "Controle de qualidade rigoroso", "Atendimento técnico especializado", "Atuação em todo o Brasil"]
    diff_html = "".join(f'<div class="value"><strong>{esc(item)}</strong></div>' for item in diffs)
    body = f"""
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">Sobre nós</p>
    <h1>Há mais de 30 anos desenvolvendo soluções e produtos para a indústria de alimentos</h1>
    <p>Há mais de 30 anos, a Naturalle desenvolve ingredientes de origem vegetal para os mercados de alimentação humana e animal. Com uma sólida trajetória iniciada na soja, a empresa amplia continuamente seu portfólio por meio de inovação, pesquisa e tecnologia, oferecendo soluções que atendem às demandas de um mercado em constante evolução.</p>
  </div>
</section>
<section class="section">
  <div class="container value-grid">
    <article class="value"><h3>Nossa essência</h3><p>Desenvolver ingredientes vegetais com qualidade, inovação e responsabilidade para gerar valor aos nossos clientes.</p></article>
    <article class="value"><h3>Nosso propósito</h3><p>Contribuir para uma alimentação mais inovadora e sustentável por meio de soluções vegetais.</p></article>
    <article class="value"><h3>Nossa visão</h3><p>Ser referência em ingredientes vegetais, reconhecida pela excelência, inovação e confiança.</p></article>
    <article class="value"><h3>Nossos valores</h3><div class="values">{value_html}</div></article>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="container">
    <div class="section__head"><div><p class="eyebrow">O que nos define</p><h2>Como a Naturalle trabalha</h2></div></div>
    <div class="pillar-grid">{pillar_html}</div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="container">
    <div class="section__head"><div><p class="eyebrow">Diferenciais</p><h2>Por que escolher a Naturalle?</h2></div></div>
    <div class="value-grid">{diff_html}</div>
    <div class="hero__actions" style="margin-top:28px">
      <a class="btn" href="../produtos/nutricao-humana/">Nutrição Humana</a>
      <a class="btn btn--ghost" href="../produtos/nutricao-animal/">Nutrição Animal</a>
    </div>
  </div>
</section>
"""
    page = head(depth, "Quem somos | Naturalle", "Há mais de 30 anos produzimos ingredientes vegetais para nutrição humana e nutrição animal. Conheça a Naturalle.", COMPANY["url"] + "/quem-somos/")
    write_page("quem-somos/index.html", page + header(depth, "about") + body + footer(depth))


def products_index():
    depth = 1
    body = f"""
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">Portfólio</p>
    <h1>Produtos</h1>
    <p>Farinhas, proteínas e ingredientes vegetais para nutrição humana e nutrição animal, com padronização e fornecimento para a indústria.</p>
    <div class="filters" data-filters>
      <button class="is-active" type="button" data-filter="todos">Todos</button>
      <button type="button" data-filter="humana">Nutrição Humana</button>
      <button type="button" data-filter="animal">Nutrição Animal</button>
      <input data-search type="search" placeholder="Buscar ingrediente" aria-label="Buscar ingrediente">
    </div>
    {card_grid(depth, [item['slug'] for item in DATA['products']])}
    <p class="empty" data-empty hidden>Nenhum produto encontrado para essa busca.</p>
  </div>
</section>
"""
    page = head(depth, "Produtos | Naturalle", "Conheça as linhas de nutrição humana e nutrição animal da Naturalle.", COMPANY["url"] + "/produtos/")
    write_page("produtos/index.html", page + header(depth, "products") + body + footer(depth))


def category_page(category):
    depth = 2
    body = f"""
<section class="page-hero">
  <div class="container">
    <p class="breadcrumb"><a href="../../">Home</a> / <a href="../">Produtos</a> / {esc(category['title'])}</p>
    <p class="eyebrow">Linha</p>
    <h1>{esc(category['title'])}</h1>
    <p>{esc(category['summary'])}</p>
  </div>
</section>
<section class="section" style="padding-top:10px">
  <div class="container">
    {card_grid(depth, category['products'])}
  </div>
</section>
"""
    page = head(depth, f"{category['title']} | Naturalle", category["summary"], COMPANY["url"] + f"/produtos/{category['slug']}/")
    write_page(f"produtos/{category['slug']}/index.html", page + header(depth, "products") + body + footer(depth))


def specs(product):
    rows = [("Composição", " ".join(product["composition"]))]
    if product["application"]:
        rows.append(("Aplicação", product["application"]))
    rows.extend([
        ("Embalagem", product["packing"]),
        ("Validade", product["validity"]),
        ("Armazenamento", product["storage"]),
    ])
    return "".join(f"<div><dt>{esc(label)}</dt><dd>{esc(text)}</dd></div>" for label, text in rows if text)


def applications(product):
    blocks = []
    for group in product["applications"]:
        chips_html = "".join(f'<span class="chip">{esc(item)}</span>' for item in group["items"])
        blocks.append(f'<section class="app-block"><h3>{esc(group["title"])}</h3><div class="chips">{chips_html}</div></section>')
    return "".join(blocks)


def guarantees(product):
    data = product["guarantees"]
    if not data:
        return ""
    body = "".join(
        "<tr>"
        f"<td>{esc(parameter_label(row['parameter']))}</td>"
        f"<td>{esc(condition_label(row['condition']))}</td>"
        f"<td>{esc(row['value'])}</td>"
        "</tr>"
        for row in data["rows"]
    )
    return f"""
<section class="app-block">
  <h3>{esc(data['title'])}</h3>
  <div class="table-wrap">
    <table>
      <thead><tr><th>Parâmetro</th><th>Condição</th><th>Valor</th></tr></thead>
      <tbody>{body}</tbody>
    </table>
  </div>
</section>
"""


def product_page(product):
    depth = 2
    related = []
    for category in product["categories"]:
        for slug in CATEGORIES[category]["products"]:
            if slug != product["slug"] and slug not in related:
                related.append(slug)
    related = related[:3]
    from urllib.parse import quote
    wa = "https://wa.me/" + COMPANY["whatsapp"] + "?text=" + quote(f"Olá, Naturalle. Tenho interesse em {product['title']}.")
    body = f"""
<section class="page-hero">
  <div class="container product">
    <div class="product__photo">
      <img src="{asset(depth, product['image'])}" alt="{esc(product['title'])}">
    </div>
    <div class="prose">
      <p class="breadcrumb"><a href="../../">Home</a> / <a href="../">Produtos</a> / {esc(product['title'])}</p>
      <div class="chips">{chips(product['categories'])}</div>
      <h1>{esc(product['title'])}</h1>
      {paragraphs(product['description'])}
      <dl class="spec-list">{specs(product)}</dl>
      {applications(product)}
      {guarantees(product)}
      <div class="hero__actions">
        <a class="btn" href="{esc(wa)}" target="_blank" rel="noopener">Solicitar no WhatsApp</a>
        <a class="btn btn--ghost" href="../../contato/">Falar com vendas</a>
      </div>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="container">
    <div class="section__head"><div><h2>Outros ingredientes</h2></div></div>
    {card_grid(depth, related)}
  </div>
</section>
"""
    description = product["description"][0][:180]
    page = head(depth, f"{product['title']} | Naturalle", description, COMPANY["url"] + f"/produtos/{product['slug']}/")
    write_page(f"produtos/{product['slug']}/index.html", page + header(depth, "products") + body + footer(depth))


def contact():
    depth = 1
    body = f"""
<section class="page-hero">
  <div class="container">
    <p class="eyebrow">Contato</p>
    <h1>Fale com a Naturalle</h1>
    <p>Preencha os dados e retornamos em breve. A mensagem abre o WhatsApp ou o seu e-mail, com os dados já preenchidos.</p>
  </div>
</section>
<section class="section" style="padding-top:10px">
  <div class="container contact-grid">
    <aside class="panel contact-card">
      <h2>Canais</h2>
      <p><a href="mailto:{esc(COMPANY['email'])}">{esc(COMPANY['email'])}</a></p>
      <p><a href="tel:{esc(COMPANY['phoneTel'])}">{esc(COMPANY['phoneDisplay'])}</a></p>
      <p><a href="https://wa.me/{esc(COMPANY['whatsapp'])}" target="_blank" rel="noopener">WhatsApp</a></p>
      <p><a href="{esc(COMPANY['linkedin'])}" target="_blank" rel="noopener">LinkedIn</a></p>
      <p>CNPJ {esc(COMPANY['cnpj'])}</p>
    </aside>
    <form class="form" id="contato-form">
      <label>Nome completo<input name="nome" required autocomplete="name"></label>
      <label>E-mail<input name="email" type="email" required autocomplete="email"></label>
      <label>Telefone para contato<input name="telefone" required autocomplete="tel"></label>
      <label>Assunto<input name="assunto" required></label>
      <label>Mensagem<textarea name="mensagem" required></textarea></label>
      <div class="form__actions">
        <button class="btn" type="submit" data-channel="whatsapp">Enviar pelo WhatsApp</button>
        <button class="btn btn--ghost" type="submit" data-channel="email">Enviar por e-mail</button>
      </div>
      <p class="note" data-form-note hidden>Abrimos o canal escolhido com a sua mensagem.</p>
    </form>
  </div>
</section>
"""
    page = head(depth, "Contato | Naturalle", "Fale com a Naturalle pelo e-mail vendas@naturalle.com.br ou pelo telefone (19) 99884-9460.", COMPANY["url"] + "/contato/")
    write_page("contato/index.html", page + header(depth, "contact") + body + footer(depth))


def privacy():
    depth = 1
    sections = [
        ("Coleta de informações", [
            "Podemos coletar informações pessoais fornecidas diretamente pelo usuário, como nome, e-mail, telefone ou outras informações enviadas por meio de formulários de contato ou comunicações diretas.",
            "Também podem ser coletadas informações automaticamente, como endereço IP, tipo de navegador, páginas acessadas, duração da visita e dados obtidos por meio de cookies e tecnologias semelhantes.",
        ]),
        ("Uso das informações", [
            "As informações coletadas são utilizadas para responder dúvidas, solicitações ou contatos realizados pelo usuário; melhorar o conteúdo, funcionamento e experiência de navegação do site; e cumprir obrigações legais ou regulatórias.",
            "Os dados não serão utilizados para finalidades diferentes das aqui descritas sem o consentimento do usuário.",
        ]),
        ("Compartilhamento de dados", [
            "A Naturalle não vende, aluga ou compartilha dados pessoais com terceiros para fins comerciais. O compartilhamento poderá ocorrer apenas quando necessário para cumprimento de obrigações legais ou para o funcionamento do site, como serviços de hospedagem, formulários ou ferramentas de análise, sempre respeitando a confidencialidade das informações.",
        ]),
        ("Cookies", [
            "Este site pode utilizar cookies para melhorar a experiência do usuário. O usuário pode, a qualquer momento, configurar seu navegador para recusar ou alertar sobre o uso de cookies. A recusa pode afetar algumas funcionalidades do site.",
        ]),
        ("Armazenamento e segurança", [
            "Adotamos medidas técnicas e organizacionais adequadas para proteger os dados pessoais contra acessos não autorizados, perda, uso indevido, alteração ou divulgação.",
            "Os dados são armazenados apenas pelo tempo necessário para cumprir as finalidades para as quais foram coletados ou conforme exigido por lei.",
        ]),
        ("Direitos do usuário", [
            "De acordo com a Lei Geral de Proteção de Dados (Lei nº 13.709/2018 – LGPD), o usuário pode solicitar, a qualquer momento, acesso aos seus dados pessoais, correção ou atualização de informações, exclusão de dados pessoais e revogação de consentimentos concedidos.",
            "As solicitações podem ser feitas por meio do canal de contato disponível no site.",
        ]),
        ("Alterações nesta política", [
            "Esta Política de Privacidade pode ser atualizada periodicamente. Recomendamos que o usuário revise este conteúdo sempre que acessar o site.",
        ]),
        ("Contato", [
            "Em caso de dúvidas sobre esta Política de Privacidade ou sobre o tratamento de dados pessoais, entre em contato pelos canais disponibilizados no site.",
        ]),
    ]
    blocks = []
    for title, paras in sections:
        blocks.append(f"<h2>{esc(title)}</h2>" + paragraphs(paras))
    body = f"""
<section class="page-hero">
  <div class="container legal">
    <p class="eyebrow">Privacidade</p>
    <h1>Política de Privacidade</h1>
    <p>Última atualização: 29/01/2026</p>
    <p>A sua privacidade é importante para nós. Esta Política de Privacidade descreve como as informações dos usuários são coletadas, utilizadas, armazenadas e protegidas ao acessar o site https://naturalle.com.br, de titularidade da Naturalle, inscrita no CNPJ {esc(COMPANY['cnpj'])}.</p>
    <p>Ao utilizar este site, você concorda com os termos descritos nesta política.</p>
    {''.join(blocks)}
  </div>
</section>
"""
    page = head(depth, "Política de Privacidade | Naturalle", "Política de Privacidade da Naturalle, CNPJ 00.707.203/0001-12.", COMPANY["url"] + "/privacidade/")
    write_page("privacidade/index.html", page + header(depth, "") + body + footer(depth))


def sitemap():
    urls = ["", "quem-somos/", "produtos/", "produtos/nutricao-humana/", "produtos/nutricao-animal/", "contato/", "privacidade/"]
    urls += [f"produtos/{item['slug']}/" for item in DATA["products"]]
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in urls:
        body.append(f"  <url><loc>{COMPANY['url']}/{url}</loc></url>")
    body.append("</urlset>\n")
    (ROOT / "sitemap.xml").write_text("\n".join(body))
    (ROOT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: https://naturalle.com.br/sitemap.xml\n")


def main():
    home()
    about()
    products_index()
    for category in DATA["categories"]:
        category_page(category)
    for product in DATA["products"]:
        product_page(product)
    contact()
    privacy()
    sitemap()


if __name__ == "__main__":
    main()
