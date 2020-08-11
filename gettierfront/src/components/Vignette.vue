<template>
  <v-container>
    <v-row>
      <v-col sm="12">
        <formatted-vignette
          :vignette="vignette"
          v-if="vignette"
        ></formatted-vignette>
        
          <v-btn-toggle class="my-3" rounded>
          <v-btn color="warning"   @click="setAndRedirect">
            Copy to new
          </v-btn>
          <v-btn
            color="primary"
            
            :to="{ name: 'edit_vignette', params: { id } }"
            >Edit</v-btn
          >
          <v-btn color="success"  @click="deleteVignette(id)"
            >Delete</v-btn
          >
          </v-btn-toggle>
        
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
