/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#e6f7ee',
          100: '#c3ebcf',
          200: '#9fdfb0',
          300: '#7ad391',
          400: '#56c972',
          500: '#00A651',
          600: '#008f46',
          700: '#00783a',
          800: '#00612f',
          900: '#004a23',
        },
      },
    },
  },
  plugins: [],
}
