export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#0A192F", // Deep Navy
        secondary: "#F1F5F9", // Slate 100
        accent: { 500: "#4F46E5", 400: "#6366F1", 600: "#4338CA" }, // Indigo
        muted: "#6B7280",
      },
      fontFamily: {
        sans: ["Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
};