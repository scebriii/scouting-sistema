/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'tactical-dark': '#0a0a0f',
        'tactical-surface': '#13131a',
        'tactical-primary': '#4d8eff',
        'tactical-tertiary': '#4edea3',
        'tactical-error': '#ef4444',
        'tactical-warning': '#f59e0b',
        'tactical-glass': 'rgba(19, 19, 26, 0.8)',
      },
      fontFamily: {
        'sans': ['Inter', 'sans-serif'],
        'mono': ['JetBrains Mono', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'slide-in': 'slideIn 0.3s ease-out',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(77, 142, 255, 0.3)' },
          '100%': { boxShadow: '0 0 20px rgba(77, 142, 255, 0.6)' },
        },
        slideIn: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}
