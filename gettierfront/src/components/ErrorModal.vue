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
          {{errorText}}
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
    props:['errorText'],
    data () {
      return {
        dialog: true,
      }
    },
    
  computed:{
    ...mapState({instoreErrDlg:'errorDialog'}),
    errorDialog:{
      get: function(){
        return this.instoreErrDlg
      },
      set: function(){
        this.toggleErrorDialog()
      }
    }

  },
  methods:{...mapMutations(['toggleErrorDialog'])}
  }
</script>