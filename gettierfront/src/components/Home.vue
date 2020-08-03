<template>
  <ul>
    <li v-for="(item, index) in info" :key="index" v-if="item.body">
      <router-link :to="{ name: 'vignette', params: { id: item.id } }">
        VIGNETTE {{ item.body }}
      </router-link>
    </li>
  </ul>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      info: [],
    };
  },
  mounted() {
    axios
      .get("/api/vignettes/")
      .then((response) => (this.info = response.data));
  },
};
</script>
