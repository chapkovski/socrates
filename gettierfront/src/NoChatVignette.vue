<template>
  <div>
    <v-btn @click="snd">SEND</v-btn>
  </div>
</template>

<script>
import { mapActions } from "vuex";
export default {
  name: "VignetteNoChat",
  data() {
    return {};
  },
  computed: {
    currentRouteName() {
      return this.$route.name;
    },
  },
  methods: {
    snd() {
      this.sendMessage({whatever:'JOPPPA'});
    },
    ...mapActions(['sendMessage']),
  },
};
</script>
