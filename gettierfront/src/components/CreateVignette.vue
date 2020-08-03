<template>
  <v-form ref="form" v-model="valid" lazy-validation>
    <v-container>
      <v-row>
        <v-col cols="12" md="4">
          <v-text-field
            v-model="body"
            :rules="nameRules"
            :counter="10"
            label="Vignette text"
            required
            @keyup.enter="validate"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-btn
            :disabled="!valid"
            color="success"
            class="mr-4"
            @click="validate"
          >
            Validate
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
  </v-form>
</template>

<script>
import axios from "axios";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";
export default {
  created() {
    console.debug(this.$cookies.get("csrftoken"));
  },
  data: () => ({
    valid: false,
    body: "",

    nameRules: [
      (v) => !!v || "Vignette body is required",
      (v) => v.length >= 10 || "Vignette text must be at least  10 characters",
    ],
  }),
  methods: {
    validate() {
      console.debug("validation");
      const val = this.$refs.form.validate();
      const payload = { body: this.body };
      if (val) {
        axios
          .post("/api/vignettes/", payload)
          .then((r) => {
            console.debug(r.data, r.data.id,'asdf')
            if (r.data && r.data.id) {
              this.$router.push({
                name: "vignette",
                params: { id: r.data.id },
              });
            }
          })
          .catch((error) => {
            console.log(error.response.data);
            console.log(error.response.status);
            console.log(error.response.headers);
          });
      }
    },
  },
};
</script>
