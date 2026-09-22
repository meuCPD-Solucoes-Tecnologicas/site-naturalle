const toggle = document.querySelector(".nav-toggle");
const nav = document.querySelector(".site-nav");

if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  });
}

const filterBar = document.querySelector("[data-filters]");
if (filterBar) {
  const buttons = [...filterBar.querySelectorAll("[data-filter]")];
  const search = document.querySelector("[data-search]");
  const cards = [...document.querySelectorAll("[data-product]")];
  const empty = document.querySelector("[data-empty]");
  let current = "todos";

  const apply = () => {
    const query = (search?.value || "").trim().toLowerCase();
    let visible = 0;
    cards.forEach((card) => {
      const categories = card.dataset.category.split(" ");
      const name = card.dataset.name.toLowerCase();
      const show = (current === "todos" || categories.includes(current)) && (!query || name.includes(query));
      card.hidden = !show;
      if (show) visible += 1;
    });
    if (empty) empty.hidden = visible !== 0;
  };

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      current = button.dataset.filter;
      buttons.forEach((item) => item.classList.toggle("is-active", item === button));
      apply();
    });
  });
  search?.addEventListener("input", apply);
}

const form = document.querySelector("#contato-form");
if (form) {
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const nome = String(data.get("nome") || "").trim();
    const email = String(data.get("email") || "").trim();
    const telefone = String(data.get("telefone") || "").trim();
    const assunto = String(data.get("assunto") || "").trim();
    const mensagem = String(data.get("mensagem") || "").trim();
    const text = [
      `Olá, Naturalle. Meu nome é ${nome}.`,
      `E-mail: ${email}`,
      `Telefone: ${telefone}`,
      `Assunto: ${assunto}`,
      "",
      mensagem,
    ].join("\n");
    const channel = event.submitter?.dataset.channel || "whatsapp";
    if (channel === "email") {
      window.location.href = `mailto:vendas@naturalle.com.br?subject=${encodeURIComponent(assunto)}&body=${encodeURIComponent(text)}`;
    } else {
      window.open(`https://wa.me/5519998849460?text=${encodeURIComponent(text)}`, "_blank", "noopener");
    }
    const note = document.querySelector("[data-form-note]");
    if (note) note.hidden = false;
  });
}
