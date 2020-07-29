<template>
  <div class="chat-container">
    <message-wrapper></message-wrapper>
    <div class="input-block">
      <input
        v-model="content"
        type="text"
        placeholder="Type here..."
        @keyup.enter="sendMessage"
        @keydown.enter.prevent
      />
      <v-btn
        dark
        fab
        top
        right
        color="blue"
        :disabled="!status"
        @click="sendMessage"
        class="send-btn"
        :class="{ 'disable-events': emptyInput }"
      >
        <v-icon>mdi-send</v-icon>
      </v-btn>
    </div>
  </div>
</template>

<script>
import MessageWrapper from "./MessageWrapper.vue";
import { mapActions, mapState } from "vuex";
export default {
  components: {
    "message-wrapper": MessageWrapper,
  },
  data() {
    return {
      content: "",
    };
  },

  computed: {
    
    emptyInput() {
      return this.content.trim() === "";
    },
    id_in_group() {
      return this.$store.state.id_in_group;
    },
    ...mapState(
      {status: state=>state.socket.isConnected}
    )
  },
  watch: {
    status(newValue, oldValue) {
      console.debug(`Updating from ${oldValue} to ${newValue}`);
      if (newValue) {
        this.requestOldMessages();
      }
    },
  },
  created() {},
  methods: {
    ...mapActions({
      send_message: "sendMessage",
      requestOldMessages: "requestOldMessages",
    }),
    sendMessage() {
      if (this.content.trim() !== "") {
        const msg = {
          text: this.content,
          source: id_in_group,
        };
        this.send_message(msg);
        this.content = "";
      }
    },
  },
};
</script>
<style>
.input-block input {
  width: calc(100% - 10px);
  height: 50px;
  border-radius: 25px;
  margin-left: 5px;
  margin-right: 5px;
  margin-bottom: 1px;
  background-color: rgba(0, 0, 0, 0.05);
  padding: 5px;
  padding-left: 10px;
}
.input-block input:focus {
  border: none !important;
  outline: none !important;
}
.input-block {
  justify-self: flex-end;
  flex-grow: 0;
  display: flex;
  margin-bottom: 5px;
}
.chat-container {
  width: 100%;
  height: calc(100vh);
  /* background: lightyellow; */
  display: flex;
  flex-direction: column;
}
.send-btn {
  width: 48px !important;
  height: 48px !important;
  margin-right: 2px;
}
button.send-btn.disable-events {
  pointer-events: none;
  background-color: lightgrey !important;
}
</style>
