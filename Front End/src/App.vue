<template>
  <v-app>
   <headers></headers>
    <v-content>
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
import headers from './components/headers'
export default {
  name: "App",
  components: { 'headers': headers },
};
</script>

<style scoped>
main.v-content {
   padding: 25px 0px 0px !important;
}
</style>