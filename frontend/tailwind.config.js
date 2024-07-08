/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{html,svelte,ts}'],
  theme: {
    extend: {
      boxShadow: {
        'none': 'none',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms')({
      strategy: 'class',
    }),
  ],
}