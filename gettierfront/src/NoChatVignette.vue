<template>
  <v-app id="inspire">
    <v-main>
      <v-container class=" main-container" fluid>
        <v-row align="center" justify="center" no-gutters class="limitoverflow">
          <v-col sm="12" class="content-col fill-height">
            <v-card
              class="m-3 content-card d-flex flex-grow-1 flex-column"
              outlined
            >
              <v-card-text class="d-flex flex-grow-1 flex-column">
                <formatted-vignette
                  :vignette="vignette"
                  :enabled="true"
                  @answer-changed="answerChanged"
                  @confidence-changed="confidenceChanged"
                  v-if="vignette"
                ></formatted-vignette>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { mapActions } from "vuex";
import FormattedVignette from "./components/FormattedVignette.vue";
export default {
  name: "VignetteNoChat",
  components: { FormattedVignette },
  data() {
    return { vignette: null };
  },

  mounted() {
    const path = window.path_to_vignette;
    this.$http.get(path).then((response) => {
      this.vignette = response.data;
      console.debug("VIGNETTE", this.vignette);
    });
  },
  computed: {
    currentRouteName() {
      return this.$route.name;
    },
  },
  methods: {
    answerChanged(val) {
      console.debug("ANSWER CHANGED!!!", val);
      this.sendDecision({ decision_type: "answer", value: val });
    },
    confidenceChanged(val) {
      console.debug("CONFIENDCE CHANGED!!!", val);
      this.sendDecision({ decision_type: "confidence", value: val });
    },

    ...mapActions(["sendMessage"]),
  },
};
</script>
