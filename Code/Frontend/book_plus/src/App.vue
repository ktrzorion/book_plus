<template>
  <NavBar/>
  <router-view />
  <FooterAll class="footer"/>
</template>

<style>
body {
  background-attachment: fixed;
  background-position: center;
  background-repeat: no-repeat;
  background-image: url('../src/assets/bg.jpeg');
}

.footer{
  padding-bottom: 20px;
  bottom: 0;
  z-index: 1;
}
</style>

<script>
import NavBar from './components/NavBar.vue';
import FooterAll from './components/FooterAll.vue';

export default {
  components: {
    NavBar,
    FooterAll,
  },
  methods: {
    showAlert(message, type) {
      this.$store.commit('showAlert', { message, type });
    },
  }
};
</script>./components/FooterAll.vue