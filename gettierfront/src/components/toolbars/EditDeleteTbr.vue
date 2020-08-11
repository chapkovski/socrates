<template>
  <v-btn-toggle rounded>
    <v-btn @click="copyVignette(id)" color="warning">
      Copy to new
    </v-btn>
    <v-btn :to="{ name: 'edit_vignette', params: { id } }" color="primary">
      Edit
    </v-btn>
    <v-btn color="success" @click="onDelete">
      Delete
    </v-btn>
  </v-btn-toggle>
</template>

<script>
import { mapActions } from "vuex";
export default {
  props: ["id"],
  data() {
    return {};
  },
  mounted() {},
  methods: {
    ...mapActions(["deleteVignette", "copyVignette"]),
    onEdit() {},

    onDelete() {
      console.debug("DELTETE", this.id);
      this.deleteVignette(this.id);
    },
  },
};
</script>
