<template>
  <div class="message-block">
    <div class="inner-message-block">
      <div
        v-for="(item, ind) in messages"
        :key="ind"
        :class="{
          message: true,
          me: item.source === id_in_group,
          other: item.source !==id_in_group,
          last: item.last,
          first: item.first,
        }"
      >
        {{ item.text }}
      </div>
    </div>
  </div>
</template>

<script>
import Message from "./SingleMessage.vue";
export default {
  components: {
    message: Message,
  },
  computed: {
    messages() {
      return this.$store.state.messages;
    },
    id_in_group(){return this.$store.state.id_in_group;}
  },
};
</script>
<style>
.message-block {
  flex-grow: 1;
  display: flex;
  margin-top: 10px;
  margin-bottom: 10px;
  margin-left: 10px;
  /* overflow: auto; */
  flex-direction: column-reverse;
  overflow: scroll;
  flex-basis:0
  /* max-height:calc(100vh - 140px); */
}
.inner-message-block {
  margin-bottom:64px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  overflow:visible;
  flex-basis:0
}
/* TODO: move message to separate component */
.message {
  max-width: 50%;
  border-radius: 4px;
  margin-bottom: 4px;
  min-height: 20px;
  padding-left: 10px;
  padding-right: 10px;
  padding-top: 5px;
  padding-bottom: 5px;
  
}
.message.me {
  align-self: flex-end;
  background-color: rgb(0, 132, 255);
  color: white;
  padding-right:10px;
}

.message.other {
  align-self: flex-start;
  background-color: rgb(241, 240, 240);
  color: black;
  padding-left:10px;
}

.message.other:not(.last):not(.first) {
  border-top-left-radius: 4px;
  border-bottom-left-radius: 4px;
}
.message.other.first {
  border-bottom-left-radius: 4px;
  border-top-left-radius: 18px;
  border-top-right-radius: 18px;
  border-bottom-right-radius: 18px;
}
.message.other.last {
  border-bottom-left-radius: 18px;
  border-bottom-right-radius: 18px;
  border-top-right-radius: 18px;
  border-top-left-radius: 4px;
}
.message.other.last.first {
  border-bottom-left-radius: 18px;
  border-top-left-radius: 18px;
}

.message.me.first {
  border-bottom-right-radius: 4px;
  border-top-right-radius: 18px;
}
.message.me.last {
  border-bottom-right-radius: 18px;
  border-top-right-radius: 4px;
}
.message.me.last.first {
  border-top-right-radius: 18px;
  border-bottom-right-radius: 18px;
}

.message.me:not(.last):not(.first) {
  border-top-right-radius: 4px;
  border-bottom-right-radius: 4px;
}

.message {
  border-radius: 18px;
}

.message.last {
  margin-bottom: 15px;
}
</style>
