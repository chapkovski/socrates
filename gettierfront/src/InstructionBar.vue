<template>
  <v-app id="instructionBar" :style="{position:'absolute'}">
    <instructions-modal></instructions-modal>
     <v-system-bar height="55" app class='justify-content-end'>
               <v-btn
          large
          color="blue"
          @click="toggleInstructionsDialog"
          class="mx-3 white--text"
        >
          <v-icon x-large>info</v-icon>
          Show instructions
        </v-btn>
    </v-system-bar>

   
  </v-app>
</template>

<script>
import InstructionsModal from "./components/InstructionsModal";
import { mapActions, mapState, mapMutations } from "vuex";
export default {
  components: {InstructionsModal},
  data() {
    return {};
  },
  computed: {},
  mounted() {},
  methods: {    ...mapMutations(["toggleInstructionsDialog"]),},
};
</script>
