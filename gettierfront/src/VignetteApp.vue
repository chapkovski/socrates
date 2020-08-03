<template>
  <v-app>
    <h1>Basic</h1>
    <ul>
      <li>
        <router-link :to="{ name: 'home' }">HOME</router-link>
      </li>
      <li>
        <router-link :to="{ name: 'create_vignette' }"
          >CREATE VIGNETTE</router-link
        >
      </li>
    </ul>

    <router-view class="view"></router-view>
  </v-app>
</template>

<script>
export default {
  name: "Vignette",

  data() {
    return {};
  },
  methods: {},
};
</script>
