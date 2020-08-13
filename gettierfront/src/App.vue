<template>
  <v-app id="inspire">
    <end-chat></end-chat>

    <v-main>
      <v-container class=" main-container" fluid>
        <v-row align="center" justify="center" no-gutters class="limitoverflow">
          <v-col
            xl="10"
            lg="9"
            md="8"
            sm="6"
            xs="12"
            class="content-col fill-height"
          >
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
          <v-col
            xl="2"
            lg="3"
            md="4"
            sm="6"
            xs="12"
            class="chat-col fill-height"
          >
            <v-card
              class="m-3 content-card d-flex flex-grow-1 flex-column "
              outlined
            >
              <v-card-text class="d-flex flex-grow-1 flex-column">
                <chat></chat>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import Chat from "./components/Chat.vue";
import FormattedVignette from "./components/FormattedVignette.vue";
import EndChat from "./components/EndChatModal.vue";
import VueCountdown from "@chenfengyuan/vue-countdown";
import { mapActions } from "vuex";
export default {
  name: "LayoutsDemosBaselineFlipped",
  props: {
    source: String,
  },
  components: {
    chat: Chat,
    EndChat,
    countdown: VueCountdown,
    FormattedVignette,
  },

  data() {
    return {
      secondsToEnd: window.secondsToEnd,
      content: "",
      radios: "",
      choices: [],
      confidenceLevels: [...Array(11).keys()],
      confidence: "",
      chatMessages: [],
      currentRef: {},
      loading: false,
      totalChatHeight: 0,
      vignette: "",
      nextAvailable: secondsToEnd <= 0,
    };
  },
  watch: {
    confidence(newVal, oldVal) {
      console.debug(`old value ${oldVal}`);
      console.debug(`new value ${newVal}`);
    },
  },
  mounted() {
    const vignette_id = window.vignette_id;
    this.$http.get(`/api/vignettes/${vignette_id}`).then((response) => {
      this.vignette = response.data;
      this.choices = [
        { value: true, text: this.vignette.yes_option },
        { value: false, text: this.vignette.no_option },
      ];
      this.vignette.choices = this.choices;
    });
  },
  computed: {
    secondsForTimer() {
      return Math.max(0, this.secondsToEnd);
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
    ...mapActions(["sendDecision"]),
    chatEnded() {
      this.nextAvailable = true;
    },
    sendMessage() {
      if (this.content !== "") {
        console.debug("new message:", this.content);
        this.content = "";
      }
    },
    formSubmit() {
      console.debug("new form");
      document.getElementById("form").submit();
    },
  },
};
</script>
<style scoped>
.main-container {
  margin: 0px !important;
  padding: 0px !important;
}
.chat-col {
  height: calc(100vh) !important;
  display: flex;
  flex-direction: column;
}
.content-col {
  height: calc(100vh) !important;
  display: flex;
  flex-direction: column;
}
.content-card {
  flex-grow: 1;
}
.next-btn-wrapper {
  justify-self: flex-end;
}
.content-text {
  flex-grow: 1;
}
.content-card {
  display: flex;
  flex-direction: column;
}

.limitoverflow {
  overflow: auto;
}
</style>
