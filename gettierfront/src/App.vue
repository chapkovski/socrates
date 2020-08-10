<template>
  <v-app id="inspire">
    <end-chat></end-chat>

    <v-main>
      <v-container class="fill-height main-container" fluid>
        <v-row align="center" justify="center" no-gutters class="">
          <v-col
            xl="10"
            lg="9"
            md="8"
            sm="6"
            xs="12"
            class="content-col fill-height"
          >
            <v-card class="m-3 content-card d-flex flex-column" outlined>
              <v-card-text class="content-text d-flex flex-column">
                <v-alert
                  v-if="!nextAvailable"
                  border="bottom"
                  colored-border
                  type="warning"
                  elevation="2"
                >
                  <countdown :time="secondsForTimer" @end="chatEnded">
                    <template slot-scope="props"
                      >Time Remaining till the end of chat：{{
                        props.minutes
                      }}
                      minutes, {{ props.seconds }} seconds.</template
                    >
                  </countdown>
                </v-alert>
                <v-card shaped min-height="300px" elevation="24" class='mb-5'>
                  <v-card-text class="m-3">
                    <div
                      v-html="vignette && vignette.body"
                      class="vignette-body light"
                    ></div>
                  </v-card-text>
                </v-card>
                <div class="question-wrapper mt-auto">
                  <h5>{{ vignette.question }}</h5>

                  <v-radio-group v-model="radios" :mandatory="false">
                    <v-radio
                      v-for="(choice, ind) in choices"
                      :label="choice.text"
                      :value="choice.value"
                      :key="ind"
                    ></v-radio>
                  </v-radio-group>
                  <v-card flat class="">
                    <v-card-text>
                      <v-row align="center" justify="center">
                        <v-col cols="12">
                          <h5 class="text-center">
                            How confident you are in your answer at the scale
                            from 0 to 10
                          </h5>
                        </v-col>
                        <v-btn-toggle v-model="confidence">
                          <v-btn
                            v-for="(i, ind) in confidenceLevels"
                            :key="ind"
                            :value="i"
                          >
                            {{ i }}
                          </v-btn>
                        </v-btn-toggle>
                      </v-row>
                    </v-card-text>
                  </v-card>
                </div>
              </v-card-text>
              <v-card-actions class="next_btn_wrapper">
                <v-btn color="primary" @click="formSubmit" v-if="nextAvailable"
                  >Next</v-btn
                >
              </v-card-actions>
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
              class="m-3 content-card d-flex flex-grow-1 flex-column"
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
import EndChat from "./components/EndChatModal.vue";
import VueCountdown from "@chenfengyuan/vue-countdown";

export default {
  name: "LayoutsDemosBaselineFlipped",
  props: {
    source: String,
  },
  components: {
    chat: Chat,
    EndChat,
    countdown: VueCountdown,
  },

  data() {
    return {
      secondsToEnd: window.secondsToEnd,
      content: "",
      radios: "",
      choices: [],
      confidenceLevels:[... Array(11).keys()],
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
    });
  },
  computed: {
    secondsForTimer() {
      return Math.max(0, this.secondsToEnd);
    },
  },
  methods: {
    chatEnded() {
      console.debug("ChAT ENDED", this.secondsToEnd);
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

.light::-webkit-scrollbar {
  width: 15px;
}

.light::-webkit-scrollbar-track {
  background: #e6e6e6;
  border-left: 1px solid #dadada;
}

.light::-webkit-scrollbar-thumb {
  background: #b0b0b0;
  border: solid 3px #e6e6e6;
  border-radius: 7px;
}

.light::-webkit-scrollbar-thumb:hover {
  background: black;
}

.vignette-body {
  max-height: 500px;
  overflow: auto;
}
</style>
