<template>
  <div id="app">
    <component :is="layout">
      <router-view/>
    </component>
  </div>
</template>

<script>
import DefaultLayout from "./layouts/DefaultLayout"
import LoginLayout from "./layouts/LoginLayout"
export default {
  components: {
    DefaultLayout,
    LoginLayout
  },
  computed: {
    layout() {
      return this.$route.meta.layout || 'default-layout'
    }
  }
}
</script>