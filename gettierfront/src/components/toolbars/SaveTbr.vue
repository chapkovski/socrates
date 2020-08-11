<template>
  <div>
    <v-btn @click="savingRequested">
      Save
    </v-btn>
  </div>
</template>

<script>
import { mapActions } from "vuex";
export default {
  data() {
    return {};
  },
  mounted() {},
  methods: {
    ...mapActions(["savingRequested",  ]),
  },
  created() {},
};
</script>
