import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          base: "#0D1117",
          surface: "#161B22",
          surface2: "#21262D",
          border: "#30363D",
          text: "#C9D1D9",
          muted: "#8B949E",
          bright: "#F0F6FC",
        },
        brand: {
          DEFAULT: "#8B5CF6", // Electric Violet
          hover: "#7C3AED",
          glow: "rgba(139, 92, 246, 0.25)",
        },
        safe: {
          DEFAULT: "#10B981", // Emerald Green
          glow: "rgba(16, 185, 129, 0.2)",
        },
        warning: {
          DEFAULT: "#F59E0B", // Amber Orange
          glow: "rgba(245, 158, 11, 0.2)",
        },
        critical: {
          DEFAULT: "#EF4444", // Crimson Red
          glow: "rgba(239, 68, 68, 0.2)",
        },
      },
      fontFamily: {
        mono: ["JetBrains Mono", "Fira Code", "Courier New", "monospace"],
      },
      boxShadow: {
        "neo-sm": "2px 2px 0px #30363D",
        "neo": "4px 4px 0px #30363D",
        "neo-brand": "4px 4px 0px #8B5CF6",
        "neo-safe": "4px 4px 0px #10B981",
        "neo-crit": "4px 4px 0px #EF4444",
      },
    },
  },
  plugins: [],
};

export default config;
