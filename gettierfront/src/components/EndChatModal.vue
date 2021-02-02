<template>
  <div class="text-center" v-if='!chatExitForced'>
    <v-dialog v-model="isChatModalShown" width="700">
      <template v-slot:activator="{ on, attrs }">
        <div></div>
      </template>

      <v-card>
        <v-card-title class="primary">
          Information
        </v-card-title>

        <v-card-text class="my-3">
          Your partner has ended the chat. You can now provide your final answer.
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="isChatModalShown = false">
            Close
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapState, mapMutations,mapGetters } from "vuex";
export default {
  data() {
    return {};
  },

  computed: {
    ...mapState(["chatEndModal",'chatExitForced']),
    ...mapGetters(['chatEndedByPartner']),
    isChatModalShown: {
      get() {
        return this.chatEndedByPartner;
      },
      set(newVal) {
        this.setEndChatModel(newVal);
        if (!newVal) {
          this.forceExit();
        }
      },
    },
  },
  methods: { ...mapMutations(["setEndChatModel", "forceExit"]) },
};
</script>
