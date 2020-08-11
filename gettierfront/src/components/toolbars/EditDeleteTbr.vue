<template>
  <v-btn-toggle multiple group>
    <v-btn :to="{ name: 'edit_vignette', params: { id } }">
      Edit
    </v-btn>
    <v-btn color="danger" @click="onDelete">
      Delete
    </v-btn>
  </v-btn-toggle>
</template>

<script>
import {mapActions} from 'vuex'
export default {
  props: ["id"],
  data() {
    return {};
  },
  mounted() {
    console.debug("PROPS", this.id);
  },
  methods: {
    ...mapActions(['deleteVignette']),
    onEdit() {
      console.debug("EDIT");
    },
    onDelete() {
      console.debug("DELTETE", this.id);
      this.deleteVignette(this.id);
    },
  },
};
</script>
