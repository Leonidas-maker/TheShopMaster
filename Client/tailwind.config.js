/* @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./App.{js,jsx,ts,tsx}", "./src/App.{js,jsx,ts,tsx}", "./src/**/*.{js,jsx,ts,tsx}", "./src/components/svg/*.{js,jsx,ts,tsx}", "./src/pages/loading/loading.tsx" ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: '#0A1128',
        secondary: '#171717',
        font_primary: '#E0E0E2',
        font_secondary: '#B5BAD0'
      },
    },
  },
  plugins: [],
}