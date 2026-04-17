import { defineStore } from 'pinia';
import { ref, watch, onMounted } from 'vue';

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref(localStorage.getItem('theme') === 'dark');

  function applyTheme() {
    const root = document.documentElement;
    const themeName = isDark.value ? 'aura-dark-blue' : 'aura-light-blue';
    
    if (isDark.value) {
      root.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      root.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
    
    switchPrimeVueTheme(themeName);
  }

  function switchPrimeVueTheme(themeName) {
    const themeLink = document.getElementById('theme-link');
    if (themeLink) {
      // Using unpkg CDN for reliable dynamic switching in all environments
      themeLink.setAttribute('href', `https://unpkg.com/primevue@3.39.0/resources/themes/${themeName}/theme.css`);
    } else {
      // Fallback: try to find any primevue theme link
      const links = document.getElementsByTagName('link');
      for (let link of links) {
        if (link.getAttribute('href')?.includes('primevue/resources/themes/')) {
          link.setAttribute('href', `https://unpkg.com/primevue@3.39.0/resources/themes/${themeName}/theme.css`);
          break;
        }
      }
    }
  }

  function toggle() {
    isDark.value = !isDark.value;
  }

  // Initial apply
  onMounted(() => {
    applyTheme();
  });

  watch(isDark, applyTheme);

  return { isDark, toggle };
});
