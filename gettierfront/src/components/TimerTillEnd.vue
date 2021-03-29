<template>
  <countdown :end-time="endTime" :style="{ width: '100%' }" @finish="toDo()">
    <template v-slot:process="anyYouWantedScopName">
      <v-progress-linear
        width="100%"
        height="25px"
        :color="color"
        :value="
          (anyYouWantedScopName.timeObj.leftTime / 1000 / secsToEnd) * 100
        "
      >
        {{ progressMessage }}: {{ anyYouWantedScopName.timeObj.m }}:
        {{ anyYouWantedScopName.timeObj.s }}
      </v-progress-linear>
    </template>
    <template v-slot:finish>
      <span>{{ timerFinish }}</span>
    </template>
  </countdown>
</template>

<script>
import { addSeconds } from "date-fns";
export default {
  name: "Timer",
  props: {
    secsToEnd: Number,
    progressMessage: String,
    whatToDo: String,
    color: String,
    timerFinish: String,
  },
  data() {
    const endTime = addSeconds(new Date(), this.secsToEnd);
    return {
      endTime: endTime,
    };
  },
  methods: {
    toDo() {
      this.$store.commit(this.whatToDo);
    },
  },
};
</script>
