<!-- src/App.vue -->
<template>
  <div id="app">
    <NavBar v-if="!isAuthPage" />
    <main :class="{ 'auth-layout': isAuthPage }">
      <router-view />
    </main>
    <AppFooter v-if="!isAuthPage" />
    <Toast />
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '@/components/common/NavBar.vue'
import AppFooter from '@/components/common/AppFooter.vue'
import Toast from '@/components/common/Toast.vue'

export default {
  name: 'App',
  components: {
    NavBar,
    AppFooter,
    Toast
  },
  setup() {
    const route = useRoute()
    const isAuthPage = computed(() => route.meta?.hideLayout)
    
    return {
      isAuthPage
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Inter', sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
}

.auth-layout {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}
</style>