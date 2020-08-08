<template>
  <v-card outlined>
    <v-card-title class="headline">Vignettes</v-card-title>
    <v-card-text>
      <v-list rounded >
        <v-list-item
          v-for="(item, i) in vignettes"
          class='slightlyrounded'
          :class="{ redback: i % 2 === 1 }"
          color="red"
          :key="i"
          :to="{ name: 'vignette', params: { id: item.id } }"
        >
          Vignette: <span class="vignette-title"> {{ item.title }}</span>
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
      vignettes: [],
    };
  },
  mounted() {
    axios
      .get("/api/vignettes/")
      .then((response) => (this.vignettes = response.data));
  },
};
</script>

<style scoped>
.vignette-title {
  font-style: italic;
}
.redback {
  background: #CFD8DC;
}
.slightlyrounded{
  border-color:lightgrey!important;
  border-width:thin;
  border-style:solid;
  
  border-radius:32px;
}
</style>
