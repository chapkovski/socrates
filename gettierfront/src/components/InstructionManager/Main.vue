<template>
  <v-app >
    <v-app-bar app clipped-right color="blue" dark>
      <v-toolbar-title>
        <v-btn-toggle>
        <v-btn   color='warning' href="/"> back to oTree</v-btn>
        <v-btn text outlined :to="{ name: 'home' }"> Instruction Manager</v-btn>
        </v-btn-toggle>
      </v-toolbar-title>
      <v-spacer></v-spacer>


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
  name: "InstructionManager",
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

