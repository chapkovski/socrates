<template>
  <v-form ref="form" v-model="valid" lazy-validation @submit.prevent>
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-text-field
            label="Title"
            placeholder="Title"
            outlined
            required
            v-model="vignette.title"
            @input="resetError('title')"
            :error-messages="(errorMessages && errorMessages.title) || ''"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="12">
          <editor
            apiKey="dd5t8ihbpp4aoey9nk77duse46qy5wjekpnb87wdivh44fw5"
            v-model="vignette.body"
            :init="{
              plugins: 'image',
              height: 300,
              width: '100%',
              menubar: 'file edit view insert format tools table tc help',
              toolbar:
                'undo redo | image | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | a11ycheck ltr rtl | showcomments addcomment',

              selector: 'textarea', // change this value according to your HTML
              file_picker_types: 'file image media',
            }"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" sm="12" md="12">
          <v-text-field
            label="Question"
            placeholder="Type question text here"
            required
            outlined
            v-model="vignette.question"
            @input="resetError('question')"
            :error-messages="(errorMessages && errorMessages.question) || ''"
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="12" md="12">
          <v-text-field
            label="Option for 'yes'"
            placeholder="Option for 'Yes'"
            outlined
            v-model="vignette.yes_option"
            @input="resetError('yes_option')"
            :error-messages="(errorMessages && errorMessages.yes_option) || ''"
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="12" md="12">
          <v-text-field
            label="Option for 'No'"
            placeholder="Option for 'No'"
            @input="resetError('no_option')"
            outlined
            v-model="vignette.no_option"
            :error-messages="(errorMessages && errorMessages.no_option) || ''"
          ></v-text-field>
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
import Editor from "@tinymce/tinymce-vue";
export default {
  props: { id: { type: [String, Number], default: null, required: false } },
  components: {
    editor: Editor,
  },
  data: () => ({
    valid: false,
    body: "",
    vignette: {
      body: "",
      title: "",
      question: "",
      yes_option: "",
      no_option: "",
    },
    errorMessages: "",
    title: "",
    yesOption: "",
    noOption: "",
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
      this.$http.get(`/api/vignettes/${this.id}`).then((response) => {
        this.vignette = response.data;
      });
    }
  },

  created() {
    this.$http.defaults.xsrfHeaderName = "X-CSRFToken";
    this.$http.defaults.xsrfCookieName = "csrftoken";
  },

  methods: {
    resetError(fieldName) {
      if (
        typeof this.errorMessages === "object" &&
        this.errorMessages !== null
      ) {
        this.errorMessages[fieldName] = "";
      }
    },
    saveVignette() {
      const val = this.$refs.form.validate();

      if (val) {
        this.valid = true;
        this.$http[this.axiosType](this.url, this.vignette)
          .then((r) => {
            if (r.data && r.data.id) {
              this.$router.push({
                name: "vignette",
                params: { id: r.data.id },
              });
            }
          })
          .catch((error) => {
            const { data, status } = error.response;
            if (status >= 300) {
              this.valid = false;
              this.errorMessages = data;
            }
          });
      }
    },
  },
};
</script>
