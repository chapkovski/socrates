<template>
  <v-form ref="form" v-model="valid"  @submit.prevent>
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-text-field
            label="Title"
            placeholder="Title"
            outlined
            required
            v-model="vignette.title"
    :rules="[rules.required]"
 
          />
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
            v-model="vignette.question"
            label="Question"
            placeholder="Type question text here"

            outlined

 
            :rules="[rules.required]"
          />
        </v-col>
        <v-col cols="12" sm="12" md="12">
          <v-text-field
            v-model="vignette.yes_option"
            label="Option for 'yes'"
            placeholder="Option for 'Yes'"
            outlined
            :rules="[rules.required]"
          />
        </v-col>
        <v-col cols="12" sm="12" md="12">
          <v-text-field
            label="Option for 'No'"
            placeholder="Option for 'No'"
            
            outlined
            v-model="vignette.no_option"
 
                                  :rules="[rules.required]"
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="12" md="12">
          <v-radio-group
           v-model="vignette.correct"
            row
                      :rules="[rules.required]"
                      >
            <template v-slot:label>
              <div>Correct answer</strong></div>
            </template>
            <v-radio label="No" :value="false"></v-radio>
            <v-radio label="Yes" :value="true"></v-radio>
          </v-radio-group>
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
import { mapState, mapActions } from "vuex";
export default {
  components: {
    editor: Editor,
  },
  props: { id: { type: [String, Number], default: null, required: false } },
  data: () => ({
    valid: false,
    body: "",
    vignette: {
      body: "",
      title: "",
      question: "",
      yes_option: "",
      no_option: "",
      correct:"",
    },
    errorMessages: "",
    title: "",
    yesOption: "",
    noOption: "",
    url: `/api/vignettes/`,
    axiosType: "post",
    rules: {required: (value) => {if (value===null || value==='' || value===undefined) {return 'required'}}},
    nameRules: [
      
      (v) => !!v || "Vignette body is required",
      (v) => v.length >= 10 || "Vignette text must be at least  10 characters",
    ],
  }),
  computed: { ...mapState(["saving", "bufferForNew"]) },
  watch: {
    saving(newVal, oldVal) {
      console.debug("SAVING INNITATED - CHECKING WITHING!!");
      this.savingStopRequested();
      this.saveVignette();
    },
  },
  mounted() {
    if (this.id) {
      this.url = `/api/vignettes/${this.id}/`;
      this.axiosType = "patch";
      this.$http.get(`/api/vignettes/${this.id}`).then((response) => {
        this.vignette = response.data;
       
      });
    } else {
      if (this.bufferForNew) {
        this.vignette = this.bufferForNew;
        this.vignette.title += " 1";
        this.emptyBuffer();
      }
    }
  },

  created() {
    this.$http.defaults.xsrfHeaderName = "X-CSRFToken";
    this.$http.defaults.xsrfCookieName = "csrftoken";
  },

  methods: {
    ...mapActions(["savingStopRequested", "emptyBuffer"]),
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

      if (this.valid ) {
 
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
