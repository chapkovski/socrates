<template>
  <v-form ref="form" v-model="valid" @submit.prevent>
    <editor
      apiKey="dd5t8ihbpp4aoey9nk77duse46qy5wjekpnb87wdivh44fw5"
      v-model="instruction.body"
      :init="{
        plugins: 'image',
        height: 500,
        width: '100%',
        menubar: 'file edit view insert format tools table tc help',
        toolbar:
          'undo redo | image | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | a11ycheck ltr rtl | showcomments addcomment',

        selector: 'textarea', // change this value according to your HTML
        file_picker_types: 'file image media',
      }"
    />
    <v-btn
      :disabled="!valid"
      color="success"
      class="mr-4"
      @click="saveInstructions"
    >
      Save
    </v-btn>
  </v-form>
</template>

<script>
import Editor from "@tinymce/tinymce-vue";
import { mapState, mapActions } from "vuex";

export default {
  components: { editor: Editor },
  props: ["id"],
  data: () => ({
    valid: true,
    axiosType: "patch",
    instruction: {},
  }),
  computed: {
    url() {
      return `/api/params/${this.id}/`;
    },
  },
  watch: {},

  created() {
    this.$http.defaults.xsrfHeaderName = "X-CSRFToken";
    this.$http.defaults.xsrfCookieName = "csrftoken";

    this.$http.get(`/api/params/${this.id}`).then((response) => {
      this.instruction = response.data;
    });
  },

  methods: {
    saveInstructions() {
      this.$refs.form.validate();

      if (this.valid) {
          console.debug('JOPKA', this.instruction)
        this.$http[this.axiosType](this.url, this.instruction)
          .then((r) => {
              console.debug("PIDZZZZZ", r)
            if (r.data && r.data.id) {
              this.$router.push({
                name: "home",
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
