<template>
  <v-app id="inspire">
    <error-modal></error-modal>
    <v-system-bar height="30" app><div>pizda</div> </v-system-bar>

    <v-main>
      <v-container fluid fill-height>
        <v-row :style="{ height: '100%' }" class="d-flex">
          <v-col cols="9">
            <v-card>
              <v-card-text>
                <formatted-vignette
                  :vignette="vignette"
                  :enabled="true"
                  @answer-changed="answerChanged"
                  @confidence-changed="confidenceChanged"
                  v-if="vignette"
                />
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="3">
            <v-card class="flex-grow-1 d-flex flex-column" height="100%">
              <v-card-text height="100%" class="flex-grow-1 d-flex">
                <chat></chat>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
    <v-footer app>
      <v-col>
        <v-btn large color="red" @click="formSubmit">Next</v-btn>
      </v-col>
    </v-footer>
  </v-app>
</template>

<script>
import Chat from "./components/Chat.vue";
import FormattedVignette from "./components/FormattedVignette.vue";
import EndChat from "./components/EndChatModal.vue";
import ErrorModal from "./components/ErrorModal.vue";
import VueCountdown from "@chenfengyuan/vue-countdown";
import { mapActions, mapState } from "vuex";
export default {
  name: "LayoutsDemosBaselineFlipped",
  props: {
    source: String,
  },
  components: {
    chat: Chat,
    EndChat,
    ErrorModal,
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
    const path = window.path_to_vignette;
    console.debug("PATH", path);
    this.$http
      .get(path)
      .then((response) => {
        this.vignette = response.data;
      })
      .catch((e) => console.debug(e));
  },
  computed: {
    ...mapState(["djangoErrors"]),
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
  /* height: calc(100vh) !important; */
  display: flex;
  flex-direction: column;
}
.content-col {
  /* height: calc(100vh) !important; */
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
