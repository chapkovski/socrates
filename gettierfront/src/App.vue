<template>
  <v-app id="inspire">
    <end-chat></end-chat>
    <count-down></count-down>
    <v-main>
      <v-container class="fill-height main-container" fluid>
        <v-row align="center" justify="center" no-gutters>
          <v-col sm="12" class="chat-col">
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
    CountDown
  },
  data() {
    return {
      content: "",
      chatMessages: [],
      currentRef: {},
      loading: false,
      totalChatHeight: 0,
    };
  },
  methods: {
    sendMessage() {
      if (this.content !== "") {
        console.debug("new message:", this.content);
        this.content = "";
      }
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
</style>
