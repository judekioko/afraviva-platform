/** AfraViva brand tokens, carried over from homes.afraviva.com's assets/css/styles.css */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./*/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        forest: { DEFAULT: "#2C4A3B", dark: "#1B2F26" },
        gold: { DEFAULT: "#B98A46", text: "#8A6323" },
        rust: "#A8452C",
        cocoa: "#3E2A1B",
        paper: { DEFAULT: "#FBF9F2", alt: "#F1ECDC" },
        line: "#E3DDC8",
        muted: "#6E6A5C",
        ink: "#23291F",
      },
      fontFamily: {
        // Poppins throughout (headings and body alike) so the site reads
        // consistently with the bold, rounded wordmark in the AfraViva logo,
        // instead of mixing in a separate serif/sans pairing.
        serif: ["Poppins", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "sans-serif"],
        sans: ["Poppins", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "sans-serif"],
        mono: ["IBM Plex Mono", "SFMono-Regular", "Menlo", "monospace"],
      },
      borderRadius: {
        DEFAULT: "3px",
      },
    },
  },
  plugins: [],
};
