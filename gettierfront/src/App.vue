<template>
  <v-app id="inspire">
    <end-chat></end-chat>
    <count-down></count-down>
    <v-main>
      <v-container class="fill-height main-container" fluid>
        <v-row align="center" justify="center" no-gutters class="">
          <v-col sm="6" class="content-col fill-height">
            <v-card class="m-3 content-card" outlined>
              <div v-html="vignette && vignette.body"></div>
              <v-container fluid>
                <p>{{ (radios && radios.text) || "" }}</p>
                <v-radio-group v-model="radios" :mandatory="false">
                  <v-radio
                    v-for="(choice, ind) in choices"
                    :label="choice.text"
                    :value="choice"
                    :key="ind"
                  ></v-radio>
                </v-radio-group>
              </v-container>
              <v-card-actions>
                <v-btn color="primary" @click="formSubmit">Next</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
          <v-col sm="6" class="chat-col">
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
import CountDown from "./components/CountDown.vue";
export default {
  name: "LayoutsDemosBaselineFlipped",
  props: {
    source: String,
  },
  components: {
    chat: Chat,
    EndChat,
    CountDown,
  },
  data() {
    return {
      content: "",
      radios: "",
      choices: [],
      chatMessages: [],
      currentRef: {},
      loading: false,
      totalChatHeight: 0,
      vignette: "",
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
  methods: {
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
<style>
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
</style>
