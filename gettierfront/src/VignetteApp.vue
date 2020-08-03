<template>
  <div>
    <h1>Basic</h1>
    <ul>
      <li>
        <router-link :to="{ name: 'home' }">HOME</router-link>
      </li>
    </ul>

    <router-view class="view"></router-view>
  </div>
</template>

<script>
export default {
  name: "Vignette",

  data() {
    return {};
  },
  methods: {
    navigateAndIncrement() {
      const increment = () => this.n++;
      if (this.$route.path === "/") {
        this.$router.push("/foo", increment);
      } else {
        this.$router.push("/", increment);
      }
    },
  },
};
</script>
