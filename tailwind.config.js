/** @type {import('tailwindcss').Config} */
module.exports = {  
  darkMode: 'media',
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js",
    "./node_modules/flowbite/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        background: "rgb(var(--background-primary) / <alpha-value>)",
        background2: "rgb(var(--background-secondary) / <alpha-value>)",
        primary: "rgb(var(--primary-color) / <alpha-value>)",
        secondary: "rgb(var(--secondary-color) / <alpha-value>)"
      },
    },
  },
  plugins: [
    require("flowbite/plugin"),
    require('tailwind-scrollbar')
  ],
}