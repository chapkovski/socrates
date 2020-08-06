<template>
  <v-form ref="form" v-model="valid" lazy-validation @submit.prevent>
    <v-container>
      <v-row>
        <v-col cols="12" md="4">
          <v-text-field
            v-model="body"
            :rules="nameRules"
            :counter="10"
            label="Vignette text"
            required
            @keydown.enter="saveVignette"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-btn
            :disabled="!valid"
            color="success"
            class="mr-4"
            @click="saveVignette"
          >
            Save
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<script>
export default {
  props: { id: { type: [String, Number], default: null, required: false } },
  data: () => ({
    valid: false,
    body: "",
    url: `/api/vignettes/`,
    axiosType: "post",
    nameRules: [
      (v) => !!v || "Vignette body is required",
      (v) => v.length >= 10 || "Vignette text must be at least  10 characters",
    ],
  }),
  mounted() {
    if (this.id) {
      this.url = `/api/vignettes/${this.id}/`;
      this.axiosType = "patch";
      this.$http
        .get(`/api/vignettes/${this.id}`)
        .then((response) => (this.body = response.data.body));
    }
  },

  created() {
    this.$http.defaults.xsrfHeaderName = "X-CSRFToken";
    this.$http.defaults.xsrfCookieName = "csrftoken";
  },

  methods: {
    saveVignette() {
      const val = this.$refs.form.validate();
      const payload = { body: this.body };
      if (val) {
        this.$http[this.axiosType](this.url, payload)
          .then((r) => {
            if (r.data && r.data.id) {
              this.$router.push({
                name: "vignette",
                params: { id: r.data.id },
              });
            }
          })
          .catch((error) => {
            console.debug(error.response.data);
            console.debug(error.response.status);
            console.debug(error.response.headers);
          });
      }
    },
  },
};
</script>
