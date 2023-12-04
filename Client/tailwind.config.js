/* @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./App.{js,jsx,ts,tsx}",
    "./src/App.{js,jsx,ts,tsx}",
    "./src//*.{js,jsx,ts,tsx}",
    "./src/components/svg/*.{js,jsx,ts,tsx}"
  ],
  darkMode: 'class',
  theme: {
    extend: {},
  },
  plugins: [],
}