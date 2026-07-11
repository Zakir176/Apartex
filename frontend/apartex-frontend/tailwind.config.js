/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        accent: {
          DEFAULT: '#E8621A',
          hover:   '#D4561A',
          light:   '#FEF0E8',
          subtle:  '#FDF6F2',
          50:  '#FDF6F2',
          100: '#FEF0E8',
          200: '#FDD5B8',
          300: '#FABA88',
          400: '#F48F4F',
          500: '#E8621A',
          600: '#D4561A',
          700: '#B84815',
          800: '#8F360E',
          900: '#6B2508',
        },
        navy: {
          DEFAULT: '#1B3A6B',
          light:   '#EEF2F9',
          50:  '#EEF2F9',
          100: '#D5E0F0',
          500: '#1B3A6B',
          700: '#122850',
          900: '#0A1830',
        },
        surface: {
          DEFAULT: '#FFFFFF',
          alt:     '#F1EFE9',
          border:  '#E5E2DB',
          'border-strong': '#C9C5BB',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
      },
      fontSize: {
        'xs':   ['0.75rem',  { lineHeight: '1rem' }],
        'sm':   ['0.875rem', { lineHeight: '1.25rem' }],
        'base': ['1rem',     { lineHeight: '1.5rem' }],
        'lg':   ['1.125rem', { lineHeight: '1.75rem' }],
        'xl':   ['1.25rem',  { lineHeight: '1.75rem' }],
        '2xl':  ['1.5rem',   { lineHeight: '2rem' }],
        '3xl':  ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl':  ['2.25rem',  { lineHeight: '2.5rem' }],
        '5xl':  ['3rem',     { lineHeight: '1.15' }],
        '6xl':  ['3.75rem',  { lineHeight: '1.1' }],
      },
      borderRadius: {
        'sm': '6px',
        'md': '10px',
        'lg': '16px',
        'xl': '24px',
        '2xl': '32px',
        'full': '9999px',
      },
      boxShadow: {
        'xs':     '0 1px 2px rgba(0,0,0,0.05)',
        'sm':     '0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04)',
        'md':     '0 4px 6px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.04)',
        'lg':     '0 10px 25px rgba(0,0,0,0.08), 0 4px 10px rgba(0,0,0,0.04)',
        'xl':     '0 20px 40px rgba(0,0,0,0.1), 0 8px 16px rgba(0,0,0,0.05)',
        'accent': '0 8px 25px rgba(232,98,26,0.25)',
        'card':   '0 2px 8px rgba(0,0,0,0.06), 0 1px 3px rgba(0,0,0,0.04)',
        'card-hover': '0 12px 32px rgba(0,0,0,0.1), 0 4px 12px rgba(0,0,0,0.06)',
      },
      backgroundImage: {
        'hero-gradient': 'linear-gradient(135deg, #F8F7F4 0%, #F1EFE9 100%)',
      },
      transitionDuration: {
        '150': '150ms',
        '250': '250ms',
        '400': '400ms',
      },
      maxWidth: {
        'content': '1400px',
      },
    },
  },
  plugins: [],
}
