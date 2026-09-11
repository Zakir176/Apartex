/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // Primary accent — deep forest green, used sparingly
        accent: {
          DEFAULT: '#0A6640',
          hover:   '#085533',
          light:   '#F0FDF4',
          subtle:  '#F7FEF9',
          50:  '#F0FDF4',
          100: '#DCFCE7',
          200: '#BBF7D0',
          300: '#86EFAC',
          400: '#4ADE80',
          500: '#22C55E',
          600: '#16A34A',
          700: '#0A6640',
          800: '#085533',
          900: '#052E16',
        },
        // Owner workspace — near black, unified with text
        navy: {
          DEFAULT: '#111827',
          light:   '#F3F4F6',
          50:  '#F9FAFB',
          100: '#F3F4F6',
          500: '#374151',
          700: '#1F2937',
          900: '#111827',
        },
        // Surface system — clean greys, no warm tones
        surface: {
          DEFAULT: '#FFFFFF',
          alt:     '#F9FAFB',
          border:  '#E5E7EB',
          'border-strong': '#D1D5DB',
        },
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
      },
      fontSize: {
        'xs':   ['0.75rem',  { lineHeight: '1rem' }],
        'sm':   ['0.875rem', { lineHeight: '1.25rem' }],
        'base': ['1rem',     { lineHeight: '1.6' }],
        'lg':   ['1.125rem', { lineHeight: '1.75rem' }],
        'xl':   ['1.25rem',  { lineHeight: '1.75rem' }],
        '2xl':  ['1.5rem',   { lineHeight: '2rem' }],
        '3xl':  ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl':  ['2.25rem',  { lineHeight: '2.5rem' }],
        '5xl':  ['3rem',     { lineHeight: '1.15' }],
        '6xl':  ['3.75rem',  { lineHeight: '1.1' }],
      },
      borderRadius: {
        'sm':   '4px',
        'md':   '8px',
        'lg':   '12px',
        'xl':   '16px',
        '2xl':  '20px',
        'full': '9999px',
      },
      boxShadow: {
        'xs':         '0 1px 2px rgba(0,0,0,0.04)',
        'sm':         '0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)',
        'md':         '0 4px 8px rgba(0,0,0,0.06), 0 2px 4px rgba(0,0,0,0.04)',
        'lg':         '0 8px 24px rgba(0,0,0,0.08), 0 4px 8px rgba(0,0,0,0.04)',
        'xl':         '0 16px 48px rgba(0,0,0,0.10), 0 8px 16px rgba(0,0,0,0.05)',
        'accent':     '0 4px 14px rgba(10, 102, 64, 0.20)',
        'card':       '0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)',
        'card-hover': '0 8px 24px rgba(0,0,0,0.08), 0 4px 8px rgba(0,0,0,0.04)',
      },
      transitionDuration: {
        '150': '150ms',
        '200': '200ms',
        '250': '250ms',
        '400': '400ms',
      },
      maxWidth: {
        'content': '1200px',
      },
    },
  },
  plugins: [],
}
