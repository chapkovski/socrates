<template>
  <v-app id="inspire">
    <error-modal
      error-text="Please check if you answer all the questions at this page"
    />
    <v-main>
      <v-container class="main-container h-100 d-flex fill-height" fluid>
        <v-row v-if='original_ego_answer'>
          <v-col>
            <v-sheet color="white" elevation="1" width="100%" rounded>
              <v-container>
                <v-row>
                  <v-col>
                    <div class="m-3">
                      When you first answered this question you chose an option:
                      <b>{{ original_ego_answer }}</b>
                    </div>
                  </v-col>
                </v-row>
              </v-container>
            </v-sheet>
          </v-col>
        </v-row>
        <v-row
          align="center"
          justify="center"
          no-gutters
          class="limitoverflow h-100 fill-height"
        >
          <v-col sm="12" class="content-col fill-height d-flex flex-column">
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
              <v-card-actions>
                <v-btn x-large color="red" @click="validateAndSubmit"
                  >Submit answer</v-btn
                >
                <input
                  type="hidden"
                  :value="Intl.DateTimeFormat().resolvedOptions().timeZone"
                  name="timezone"
                />
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { mapActions } from "vuex";
import ErrorModal from "./components/ErrorModal.vue";
import FormattedVignette from "./components/FormattedVignette.vue";
export default {
  name: "VignetteNoChat",
  components: { FormattedVignette, ErrorModal },
  data() {
    return { vignette: null, original_ego_answer: window.original_ego_answer };
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
    ...mapActions(["sendDecision"]),
    answerChanged(val) {
      console.debug("ANSWER CHANGED!!!", val);
      this.sendDecision({ decision_type: "answer", value: val });
    },
    confidenceChanged(val) {
      console.debug("CONFIENDCE CHANGED!!!", val);
      this.sendDecision({ decision_type: "confidence", value: val });
    },

    validateAndSubmit() {
      console.debug("new form");
      document.getElementById("form").submit();
    },
  },
};
</script>
