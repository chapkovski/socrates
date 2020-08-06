<template>
  <v-form ref="form" v-model="valid" lazy-validation @submit.prevent>
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-text-field
            label="Title"
            placeholder="Title"
            outlined
            v-model="title"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="4">
          <editor
            apiKey="dd5t8ihbpp4aoey9nk77duse46qy5wjekpnb87wdivh44fw5"
            v-model="body"
            :init="{
              plugins: 'image',
              height: 300,
              menubar: 'file edit view insert format tools table tc help',
              toolbar:
                'undo redo | image | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | a11ycheck ltr rtl | showcomments addcomment',

              selector: 'textarea', // change this value according to your HTML
              file_picker_types: 'file image media',
            }"
          />
        </v-col>
      </v-row>
      <var>
        <v-col cols="12" sm="12" md="12">
          <v-text-field
            label="Option for 'yes'"
            placeholder="Option for 'Yes'"
            outlined
            v-model="yesOption"
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="12" md="12">
          <v-text-field
            label="Option for 'No'"
            placeholder="Option for 'No'"
            outlined
            v-model="noOption"
          ></v-text-field>
        </v-col>
      </var>
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
        this.body = response.data.body;
        this.title = response.data.title;
        this.yesOption = response.data.yesOption;
        this.noOption = response.data.noOption;
      });
    }
  },

  created() {
    this.$http.defaults.xsrfHeaderName = "X-CSRFToken";
    this.$http.defaults.xsrfCookieName = "csrftoken";
  },

  methods: {
    saveVignette() {
      const val = this.$refs.form.validate();
      const payload = {
        body: this.body,
        title: this.title,
        yes_option: this.yesOption,
        no_option: this.noOption,
      };
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
