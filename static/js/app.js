document.addEventListener("alpine:init", () => {
  Alpine.data("nav", () => ({
    open: false,
    toggle() { this.open = !this.open; },
    close() { this.open = false; },
  }));

  Alpine.data("faqItem", () => ({
    open: false,
    toggle() { this.open = !this.open; },
    symbol() { return this.open ? "−" : "+"; },
  }));

  Alpine.data("hero", () => ({
    slides: [
      {
        headline: "Empowering Africa's Next Generation of Impact",
        sub: "Blending talent, faith, and innovation to build sustainable businesses that uplift communities.",
      },
      {
        headline: "Uniting Africa's Visionaries for Progress",
        sub: "Fostering growth and opportunity through purpose-driven investments and partnerships.",
      },
      {
        headline: "Transforming Africa's Future with Purpose",
        sub: "Accelerating innovation and sustainability to create lasting change across the continent.",
      },
    ],
    index: 0,
    init() {
      setInterval(() => {
        this.index = (this.index + 1) % this.slides.length;
      }, 6000);
    },
    headline() { return this.slides[this.index].headline; },
    subhead() { return this.slides[this.index].sub; },
  }));
});

/* ---- reveal on scroll (same technique as homes.afraviva.com) ---- */
document.addEventListener("DOMContentLoaded", () => {
  const revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && revealEls.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("in"));
  }
});
