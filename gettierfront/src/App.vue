<template>
  <v-app id="inspire">
    <end-chat></end-chat>

    <v-main>
      <v-container class="fill-height main-container" fluid>
        <v-row align="center" justify="center" no-gutters class="">
          <v-col xl="10" lg='9' md='8'  sm='6' xs='12' class="content-col fill-height">
            <v-card class="m-3 content-card" outlined>
              <v-card-text class="content-text">
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

                <div v-html="vignette && vignette.body"></div>
                <h5>{{ vignette.question }}</h5>
                <v-container fluid>
                  
                  <v-radio-group v-model="radios" :mandatory="false">
                    <v-radio
                      v-for="(choice, ind) in choices"
                      :label="choice.text"
                      :value="choice.value"
                      :key="ind"
                      name='jjjjjs'
                    ></v-radio>
                  </v-radio-group>
                </v-container>
              </v-card-text>
              <v-card-actions class="next_btn_wrapper">
                <v-btn color="primary" @click="formSubmit" v-if="nextAvailable"
                  >Next</v-btn
                >
              </v-card-actions>
            </v-card>
          </v-col>
          <v-col xl="2" lg='3' md='4'  sm='6' xs='12' class="chat-col">
            <chat></chat>
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
      chatMessages: [],
      currentRef: {},
      loading: false,
      totalChatHeight: 0,
      vignette: "",
      nextAvailable: secondsToEnd <= 0,
    };
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
  border-left-color: black;
  border-left-width: 1px;
  border-left-style: solid;
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
</style>
