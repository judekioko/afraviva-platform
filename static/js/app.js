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
});
