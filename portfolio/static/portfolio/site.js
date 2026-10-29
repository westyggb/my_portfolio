(() => {
  const navToggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector(".nav-links");

  if (navToggle && nav) {
    navToggle.addEventListener("click", () => {
      const isOpen = navToggle.getAttribute("aria-expanded") === "true";
      navToggle.setAttribute("aria-expanded", String(!isOpen));
      nav.classList.toggle("is-open", !isOpen);
    });
    nav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => {
        navToggle.setAttribute("aria-expanded", "false");
        nav.classList.remove("is-open");
      });
    });
  }

  const cards = [...document.querySelectorAll(".project-card")];
  const chips = [...document.querySelectorAll(".filter-chip")];
  const search = document.querySelector(".project-search input");
  const noResults = document.querySelector(".no-results");
  let activeFilter = "all";

  const filterProjects = () => {
    const query = (search?.value || "").trim().toLocaleLowerCase("uk");
    let shown = 0;
    cards.forEach((card) => {
      const matchesCategory = activeFilter === "all" || card.dataset.category === activeFilter;
      const matchesSearch = !query || card.dataset.search.toLocaleLowerCase("uk").includes(query);
      card.hidden = !(matchesCategory && matchesSearch);
      if (!card.hidden) shown += 1;
    });
    if (noResults) noResults.hidden = shown !== 0;
  };

  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      activeFilter = chip.dataset.filter;
      chips.forEach((item) => item.classList.toggle("is-active", item === chip));
      filterProjects();
    });
  });
  search?.addEventListener("input", filterProjects);

  const revealItems = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries, currentObserver) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          currentObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealItems.forEach((item) => observer.observe(item));
  } else {
    revealItems.forEach((item) => item.classList.add("is-visible"));
  }
})();
