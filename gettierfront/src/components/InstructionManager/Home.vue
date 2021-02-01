<template>
  <v-card outlined>
    <v-card-title class="headline">Instructions</v-card-title>
    <v-card-text>
      <v-list rounded>
        <v-list-item
          v-for="(item, i) in instructions"
          class="slightlyrounded"
          color="red"
          :key="i"
          :to="{ name: 'single_instruction', params: { id: item.id } }"
        >
          Instruction: <span class="vignette-title"> {{ item.name }}</span>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      instructions: [],
    };
  },
  mounted() {
    axios
      .get("/api/params/")
      .then((response) => (this.instructions = response.data));
  },
};
</script>

<style scoped>
.vignette-title {
  font-style: italic;
}
.redback {
  background: #cfd8dc;
}
.slightlyrounded {
  border-color: lightgrey !important;
  border-width: thin;
  border-style: solid;

  border-radius: 32px;
}
</style>
