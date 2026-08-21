/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        ink: { 900: "#0b0f14", 800: "#11161d", 700: "#1a2129" },
        accent: { 500: "#2563eb", 400: "#3b82f6" },
      },
    },
  },
  plugins: [],
};