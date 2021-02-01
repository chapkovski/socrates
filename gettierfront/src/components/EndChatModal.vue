<template>
  <div class="text-center">
    <v-dialog v-model="isChatModalShown" width="700">
      <template v-slot:activator="{ on, attrs }">
        <div></div>
      </template>

      <v-card>
        <v-card-title class="error">
          Attention
        </v-card-title>

        <v-card-text class="my-3">
          Your partner has left the chat!
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
import { mapState, mapMutations } from "vuex";
export default {
  data() {
    return {};
  },

  computed: {
    ...mapState(["chatEndModal"]),
    isChatModalShown: {
      get() {
        return this.chatEndModal;
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
