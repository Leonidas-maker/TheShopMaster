/* @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./App.{js,jsx,ts,tsx}", "./src/App.{js,jsx,ts,tsx}", "./src/**/*.{js,jsx,ts,tsx}", "./src/components/svg/*.{js,jsx,ts,tsx}", "./src/pages/loading/loading.tsx" ],
  darkMode: 'class',
  theme: {
    colors: {
      "darkBlue": "#050A30",
      "navyBlue": "#000C66",
      "blue": "#0000FF",
      "babyBlue": "#7EC8E3",
    },
    extend: {},
  },
  plugins: [],
}