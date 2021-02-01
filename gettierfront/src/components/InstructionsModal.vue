<template>
  <div class="text-center">
    <v-dialog v-model="instructionsShow" width="700">
      <template v-slot:activator="{ on, attrs }">
        <div></div>
      </template>

      <v-card>
        <v-card-title class="success">
          Instructions
        </v-card-title>

        <v-card-text class="my-3" v-html='instructions'>
           
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="toggleInstructionsDialog()">
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
    return {
      instructions:window.instructions
    };
  },

  computed: {
    ...mapState({instShowFromStore:'instructionsShow'}),
    instructionsShow: {
      get(){
        return this.instShowFromStore
      },
      set(newVal){this.toggleInstructionsDialog()},
    }
  },
  methods: { ...mapMutations(["toggleInstructionsDialog"]) },
};
</script>
