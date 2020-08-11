<template>
  <v-app id="inspire">
    <v-app-bar app clipped-right color="blue" dark>
      <v-toolbar-title>
        <v-btn text outlined :to="{ name: 'home' }"> Vignette Manager</v-btn>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        :to="{ name: 'create_vignette' }"
        v-if="currentRouteName !== 'create_vignette'"
      >
        Create
      </v-btn>
      <router-view name='extrabtns'></router-view>
    </v-app-bar>

    <v-main dark>
      <v-container class="fill-height" >
        <v-row justify="center" align="center">
          <v-col>
            <router-view></router-view>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "Vignette",
  data() {
    return {};
  },
  computed: {
    currentRouteName() {
      return this.$route.name;
    },
  },
  methods: {},
};
</script>
