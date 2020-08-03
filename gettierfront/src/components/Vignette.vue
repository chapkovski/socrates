<template>
  <div>
    <div>VIGNETTE {{ id }}:</div>
    <div v-if="info">BODY {{ info.body }}</div>
  </div>
</template>

<script>
export default {
  props: ["id"],
  data() {
    return {
      info: null,
    };
  },
  mounted() {
    axios
      .get(`/api/vignettes/${this.id}`)
      .then((response) => (this.info = response.data));
  },
};
</script>
