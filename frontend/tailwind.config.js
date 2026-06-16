/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0B0F19',
        card: '#111827',
        primary: '#6366F1',
        secondary: '#8B5CF6',
        success: '#10B981'
      }
    },
  },
  plugins: [],
}
