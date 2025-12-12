/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: {
          900: '#000000',     // Pure black
          800: '#0a0a0a',     // Almost black
          700: '#121212',
          600: '#1c1c1c',
        },
        primary: {
          400: '#818cf8',
          500: '#6366f1', // Indigo 500
          600: '#4f46e5', // Indigo 600
          glow: '#4f46e580', // Transparent for glows
        },
        accent: {
          cyan: '#06b6d4',
          pink: '#ec4899'
        }
      },
      fontFamily: {
        sans: ['Outfit', 'sans-serif'], // Now default
        mono: ['monospace'],
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'shimmer': 'shimmer 2s linear infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        shimmer: {
          'from': { backgroundPosition: '0 0' },
          'to': { backgroundPosition: '-200% 0' },
        }
      }
    },
  },
  plugins: [],
}
