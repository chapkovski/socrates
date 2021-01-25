<template>
  <v-app id="inspire">
    <error-modal></error-modal>
    <v-system-bar height="30" app>
      <timer
        :secsToEnd="secsTillAllowedExit"
        whatToDo="allowExitPermission"
        :progressMessage="msg_till_allowed_exit"
        color="blue"
      ></timer>
      <timer
        :secsToEnd="seconds_forced_exit"
        whatToDo="forceExit"
        :progressMessage="msg_forced_exit"
        color="red"
      ></timer>
    </v-system-bar>
    <v-navigation-drawer fixed permanent right class="chatdrawer">
      <h1>chat</h1>
      <chat></chat>
    </v-navigation-drawer>
    <v-main class="maincont">
      <v-container fluid fill-height>
        <v-row>
          <v-col>
            <formatted-vignette
              :vignette="vignette"
              :enabled="false"
              @answer-changed="answerChanged"
              @confidence-changed="confidenceChanged"
              v-if="vignette"
            ></formatted-vignette>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
    <v-footer app>
      <v-col>
        <transition
          name="custom-classes-transition"
          enter-active-class="animate__animated animate__backInDown"
          leave-active-class="animate__animated animate__backOutDown"
          appear
        >
          <v-btn large color="red" @click="formSubmit" v-if="chatExitAllowed">
            Next
          </v-btn>
        </transition>
      </v-col>
    </v-footer>
  </v-app>
</template>

<script>
import Chat from "./components/Chat.vue";
import FormattedVignette from "./components/FormattedVignette.vue";
import EndChat from "./components/EndChatModal.vue";
import ErrorModal from "./components/ErrorModal.vue";
import "animate.css";
import Timer from "./components/TimerTillEnd";
import { mapActions, mapState } from "vuex";
export default {
  name: "LayoutsDemosBaselineFlipped",
  props: {
    source: String,
  },
  components: {
    Timer,
    chat: Chat,
    EndChat,
    ErrorModal,
    // countdown: VueCountdown,
    FormattedVignette,
  },

  data() {
    return {
      timeLeft: 50,
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
      secsTillAllowedExit: window.seconds_till_allow_to_leave,
      msg_till_allowed_exit: window.msg_till_allowed_exit,
      seconds_forced_exit: window.seconds_forced_exit,
      msg_forced_exit: window.msg_forced_exit,
    };
  },
  computed: {
    ...mapState(["djangoErrors", "chatExitAllowed", 'chatExitForced']),
  },
  watch: {
    confidence(newVal, oldVal) {
      console.debug(`old value ${oldVal}`);
      console.debug(`new value ${newVal}`);
    },

    "$store.state.chatExitForced": function() {
      this.formSubmit();
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
<style>
.maincont {
  margin-right: 256px;
  overflow-y: scroll;
}
.chatdrawer {
  border: 0.1px solid lightgray;
  border-radius: 10px;
  height: calc(100% - 50px) !important;
  top: initial !important;
  bottom: 10px !important;
  margin-right: 10px;
  padding: 10px;
  -webkit-box-shadow: -1px -1px 5px 0px rgba(0, 0, 0, 0.46);
  -moz-box-shadow: -1px -1px 5px 0px rgba(0, 0, 0, 0.46);
  box-shadow: -1px -1px 5px 0px rgba(0, 0, 0, 0.46);
}
div.v-navigation-drawer__content {
  display: flex !important;
  flex-direction: column !important;
}
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
