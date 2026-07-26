import { defineStore } from 'pinia';

export const useCurrencyStore = defineStore('currency', {
  state: () => ({
    // Base currency for storage is USD ($)
    currentCurrency: 'ZMW', // Default to ZMW (Zambian Kwacha) for domestic primary market
    
    // Supported currencies and exchange rates relative to 1 USD
    currencies: [
      { code: 'ZMW', symbol: 'K', name: 'Zambian Kwacha', rate: 27.5, flag: '🇿🇲' },
      { code: 'USD', symbol: '$', name: 'US Dollar', rate: 1.0, flag: '🇺🇸' },
      { code: 'ZAR', symbol: 'R', name: 'South African Rand', rate: 18.5, flag: '🇿🇦' },
      { code: 'KES', symbol: 'KSh', name: 'Kenyan Shilling', rate: 130.0, flag: '🇰🇪' },
      { code: 'GBP', symbol: '£', name: 'British Pound', rate: 0.78, flag: '🇬🇧' },
      { code: 'EUR', symbol: '€', name: 'Euro', rate: 0.92, flag: '🇪🇺' }
    ]
  }),
  
  getters: {
    activeCurrencyObj: (state) => {
      return state.currencies.find(c => c.code === state.currentCurrency) || state.currencies[0];
    }
  },

  actions: {
    setCurrency(code) {
      if (this.currencies.some(c => c.code === code)) {
        this.currentCurrency = code;
        localStorage.setItem('apartex_user_currency', code);
      }
    },

    autoDetectCurrency() {
      const saved = localStorage.getItem('apartex_user_currency');
      if (saved && this.currencies.some(c => c.code === saved)) {
        this.currentCurrency = saved;
        return;
      }

      // Detect locale / time zone
      try {
        const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
        const userLang = navigator.language || '';

        if (timeZone.includes('Lusaka') || timeZone.includes('Harare') || userLang.includes('zm')) {
          this.currentCurrency = 'ZMW';
        } else if (timeZone.includes('Johannesburg') || userLang.includes('za')) {
          this.currentCurrency = 'ZAR';
        } else if (timeZone.includes('Nairobi') || userLang.includes('ke')) {
          this.currentCurrency = 'KES';
        } else if (timeZone.includes('London') || userLang.includes('gb')) {
          this.currentCurrency = 'GBP';
        } else if (timeZone.includes('Berlin') || timeZone.includes('Paris') || userLang.includes('fr') || userLang.includes('de')) {
          this.currentCurrency = 'EUR';
        } else {
          // Default to ZMW for local primary Zambian market, USD for fallback
          this.currentCurrency = 'ZMW';
        }
      } catch (err) {
        this.currentCurrency = 'ZMW';
      }
    },

    formatPrice(amountInUSD, targetCurrencyCode = null) {
      if (amountInUSD === null || amountInUSD === undefined || isNaN(amountInUSD)) {
        return 'K 0';
      }

      const currCode = targetCurrencyCode || this.currentCurrency;
      const currObj = this.currencies.find(c => c.code === currCode) || this.currencies[0];
      const convertedValue = Number(amountInUSD) * currObj.rate;

      // Format based on currency symbol style
      const formattedNum = new Intl.NumberFormat('en-US', {
        minimumFractionDigits: currObj.code === 'ZMW' || currObj.code === 'ZAR' || currObj.code === 'USD' ? 0 : 0,
        maximumFractionDigits: 2
      }).format(convertedValue);

      return `${currObj.symbol} ${formattedNum}`;
    }
  }
});
