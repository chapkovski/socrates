<template>
  <div>
    <div>VIGNETTE {{ id }}:</div>
    <div v-if="info">BODY {{ info.body }}</div>
    <v-btn color="primary" class="mr-4" :to="{ name: 'edit_vignette', params: { id } }">EDIT</v-btn>
    <v-btn color="success" class="mr-4" @click="deleteVignette">DELETE</v-btn>
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
    this.$http
      .get(`/api/vignettes/${this.id}`)
      .then((response) => (this.info = response.data));
  },
  methods: {
    deleteVignette() {
      this.$http
        .delete(`/api/vignettes/${this.id}`)
        .then((response) => {
          console.debug("gonna delete", this.id);
          this.$router.push({
            name: "home",
          });
        })
        .catch((error) => console.debug(error));
    },
  },
};
</script>
