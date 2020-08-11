<template>
  <v-container>
    <v-row>
      <v-col sm="12">
        <formatted-vignette :vignette="vignette" v-if='vignette'></formatted-vignette>
        <v-btn
          color="primary"
          class="mr-4"
          :to="{ name: 'edit_vignette', params: { id } }"
          >EDIT</v-btn
        >
        <v-btn color="success" class="mr-4" @click="deleteVignette"
          >DELETE</v-btn
        >
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import FormattedVignette from "./FormattedVignette";
export default {
  props: ["id"],
  components: { FormattedVignette },
  data() {
    return {
      vignette: null,
    };
  },
  mounted() {
    this.$http
      .get(`/api/vignettes/${this.id}`)

      .then((response) => {
        const vig = response.data;
        vig.choices = [
          { text: vig.yes_option, value: true },
          { text: vig.no_option, value: false },
        ];
        console.debug("VIG", vig);
        this.vignette = vig;
      });
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
