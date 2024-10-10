/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}",
    './static/**/*.css', // If you have any CSS files that use Tailwind classes
    './static/**/*.js',  // If you use Tailwind classes in your JavaScript files
    './**/*.html' 
  ],
  
  theme: {
    extend: {},
  },
  plugins: [],
}

