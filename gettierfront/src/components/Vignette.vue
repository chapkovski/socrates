<template>
  <v-container>
    <v-row>
      <v-col sm="12">
        <formatted-vignette
          :vignette="vignette"
          v-if="vignette"
        ></formatted-vignette>
        <v-btn color="warning" class="mr-4" @click="setAndRedirect">
          Copy to new
        </v-btn>
        <v-btn
          color="primary"
          class="mr-4"
          :to="{ name: 'edit_vignette', params: { id } }"
          >Edit</v-btn
        >
        <v-btn color="success" class="mr-4" @click="deleteVignette(id)"
          >Delete</v-btn
        >
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import FormattedVignette from "./FormattedVignette";
import { mapActions } from "vuex";
export default {
  props: ["id"],
  components: { FormattedVignette },
  data() {
    return {
      vignette: null,
    };
  },
  mounted() {
    this.$http.get(`/api/vignettes/${this.id}`).then((response) => {
      const vig = response.data;
      vig.choices = [
        { text: vig.yes_option, value: true },
        { text: vig.no_option, value: false },
      ];
      this.vignette = vig;
    });
  },
  methods: {
    ...mapActions(["deleteVignette", "setBuffer"]),
    setAndRedirect() {
      this.setBuffer(this.vignette);
      this.$router.push({ name: "create_vignette" });
    },
  },
};
</script>
