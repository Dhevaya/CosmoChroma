module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#1f2937',
        secondary: '#6b7280',
        accent: '#3b82f6',
        'neutral-50': '#f9fafb',
        'neutral-100': '#f3f4f6',
        'neutral-200': '#e5e7eb',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      spacing: {
        'generous': '2rem',
      },
      borderRadius: {
        'xl': '0.75rem',
        '2xl': '1rem',
      },
      boxShadow: {
        'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
        'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
      },
    },
  },
  plugins: [],
}
