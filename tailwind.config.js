/** Build de produção — espelha o tailwind.config inline que rodava no CDN.
 *  Compila e purga as utilities usadas nas 4 páginas (+ inline JS). Visual idêntico ao CDN.
 *  Rodar:  npx tailwindcss@3.4.17 -c tailwind.config.js -i build/input.css -o public/tailwind.min.css --minify
 */
module.exports = {
  content: ['./ansiedade.html', './burnout.html', './medos.html', './index.html'],
  safelist: ['translate-y-full'], // única utility Tailwind adicionada via JS (barra fixa mobile)
  theme: {
    extend: {
      colors: {
        cream: { DEFAULT: '#F3EDE3', dark: '#E8DFD0' },
        rust:  { DEFAULT: '#5E2616', deep: '#2C2521' },
        terra: { DEFAULT: '#A86B4C', dark: '#8A5238' },
        clay:  { DEFAULT: '#9A7B4F', light: '#B89A6B' },
        sage:  { DEFAULT: '#9CA48B' },
        ink:   '#2C2521',
      },
      fontFamily: {
        serif: ['"Playfair Display"', 'Georgia', 'Cambria', 'serif'],
        sans:  ['Garet', 'Outfit', 'ui-sans-serif', 'system-ui', '-apple-system', '"Segoe UI"', 'sans-serif'],
      },
    },
  },
};
