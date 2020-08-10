<template>
  <v-card class="m-3 content-card d-flex flex-column" outlined>
    <v-card-text class="content-text d-flex flex-column">
      <v-card shaped min-height="300px" elevation="24" class="mb-5">
        <v-card-text class="m-3">
          <div
            v-html="vignette && vignette.body"
            class="vignette-body light"
          ></div>
        </v-card-text>
      </v-card>
      <div class="question-wrapper mt-auto">
        <h5>{{ vignette.question }}</h5>

        <v-radio-group v-model="answer" :mandatory="false">
          <v-radio
            :disabled="!enabled"
            v-for="(choice, ind) in vignette.choices"
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
                  How confident you are in your answer at the scale from
                  {{ minConf }} to
                  {{ maxConf }}
                </h5>
              </v-col>
              <v-btn-toggle v-model="confidence">
                <v-btn
                  :disabled="!enabled"
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
  </v-card>
</template>

<script>
import _ from "lodash";
export default {
  props: {
    vignette: {
      type: Object,
      default: () => {},
    },
    enabled: { type: Boolean, default: false },
  },
  data() {
    return {
      confidenceLevels: _.range(11),
      confidence: null,
      answer: null,
    };
  },
  computed: {
    minConf() {
      return Math.min(...this.confidenceLevels);
    },
    maxConf() {
      return Math.max(...this.confidenceLevels);
    },
  },
  watch: {
    confidence(val, oldVal) {
      this.$emit("confidence-changed", val);
    },
    answer(val, oldVal) {
      this.$emit("answer-changed", val);
    },
  },
  mounted() {
    console.debug("HOPA", this.confidenceLevels);
  },
  methods: {},
};
</script>
