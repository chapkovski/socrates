<template>
  <v-app>
    <v-system-bar height="30" app>
       <timer
        :secsToEnd="secsTillAllowedExit"
        whatToDo="allowExitPermission"
        :progressMessage="msg_till_allowed_exit"
        color="blue"
      ></timer>
    </v-system-bar>
    <v-container fluid>
      <v-row>
        <v-col>
          <formatted-vignette
            :vignette="vignette"
            :enabled="false"
            v-if="vignette"
          ></formatted-vignette>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-textarea
            clearable
            clear-icon="mdi-close-circle"
            v-model="essay"
            placeholder="Write the essay here"
            outlined
          ></v-textarea>
        </v-col>
      </v-row>
      <input type="hidden" :value="essay" name="essay" />
    </v-container>
     <v-footer app>
      <v-col>
        <v-btn
          large
          color="blue"
          @click="toggleInstructionsDialog"
          class="mx-3 white--text"
        >
          <v-icon x-large>info</v-icon>
          Show instructions
        </v-btn>
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
import ErrorModal from "../ErrorModal.vue";
import FormattedVignette from "../FormattedVignette.vue";
import InstructionsModal from "../InstructionsModal";
import Timer from "../TimerTillEnd";
import {mapActions, mapState} from 'vuex'
export default {
  name: "Essay",
  components: { FormattedVignette, ErrorModal, InstructionsModal, Timer },
  data() {
    return {
      msg_till_allowed_exit: window.msg_till_allowed_exit,
      essay: "",
      secsTillAllowedExit: window.seconds_till_allow_to_leave,
    };
  },

  created() {
    this.getVignette();
  },
  computed: {...mapState(['vignette','chatExitAllowed'])},
  methods: {...mapActions(['getVignette'])},
};
</script>
