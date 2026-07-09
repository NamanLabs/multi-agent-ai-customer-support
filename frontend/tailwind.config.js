/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: [
    "./pages/**/*.{js,jsx}",
    "./components/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          DEFAULT: "#1E3A5F",
          light: "#2C4E7C",
          dark: "#142943",
        },
        teal: {
          DEFAULT: "#00B8A9",
          light: "#3DD4C6",
          dark: "#008C80",
        },
        amber: {
          DEFAULT: "#F5A623",
          light: "#FFC15C",
        },
        paper: "#F5F6F8",
        "paper-dark": "#15181D",
        "card-dark": "#1E222A",
        ink: "#1A1D23",
        "ink-dark": "#E8E9EB",
        muted: "#6B7280",
        "muted-dark": "#8B909A",
      },
      fontFamily: {
        display: ["'Space Grotesk'", "sans-serif"],
        body: ["'Inter'", "sans-serif"],
        mono: ["'JetBrains Mono'", "monospace"],
      },
      borderRadius: {
        receipt: "4px",
      },
      boxShadow: {
        soft: "0 1px 2px rgba(20, 41, 67, 0.06), 0 4px 16px rgba(20, 41, 67, 0.06)",
        lift: "0 8px 24px rgba(20, 41, 67, 0.12)",
        glow: "0 0 0 3px rgba(0, 184, 169, 0.15)",
      },
      backgroundImage: {
        "navy-gradient": "linear-gradient(160deg, #1E3A5F 0%, #142943 100%)",
      },
      keyframes: {
        pulseDot: {
          "0%, 100%": { opacity: 1 },
          "50%": { opacity: 0.35 },
        },
        fadeUp: {
          from: { opacity: 0, transform: "translateY(8px)" },
          to: { opacity: 1, transform: "translateY(0)" },
        },
      },
      animation: {
        "pulse-dot": "pulseDot 2s ease-in-out infinite",
        "fade-up": "fadeUp 0.35s ease-out",
      },
    },
  },
  plugins: [],
};
