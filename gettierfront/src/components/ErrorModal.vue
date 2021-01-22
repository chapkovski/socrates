<template>
  <div class="text-center">
    <v-dialog
      v-model="errorDialog"
      width="500"
    >
      <template v-slot:activator="{ on, attrs }">
       <div></div>
      </template>

      <v-card>
        <v-card-title class="error">
          Error!
        </v-card-title>

        <v-card-text class='my-3'>
          Please check if you answer all the questions at this page
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            text
            @click="toggleErrorDialog()"
          >
            Ok
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import {  mapState ,mapMutations} from "vuex";
  export default {
    data () {
      return {
        dialog: true,
      }
    },
    
  computed:{
    ...mapState(['errorDialog']),
  },
  methods:{...mapMutations(['toggleErrorDialog'])}
  }
</script>