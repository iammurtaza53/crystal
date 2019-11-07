<template>
  <v-container grid-list-md text-xs-center>
    <v-layout row wrap>
      <v-flex md4>
        <v-layout row wrap>
          <h1>Update Fundamental DB</h1>
          <v-flex md6>
            <v-checkbox
              color="info"
              v-model="all_sectors"
              v-on:click="select_all"
              label="All Sectors"
            ></v-checkbox>
            <ul>
              <v-checkbox
                color="info"
                class="line_height"
                v-on:click="check"
                v-model="selected"
                value="BELS Research Technology.xlsx"
                label="Technology"
              ></v-checkbox>
              <v-checkbox
                color="info"
                class="line_height"
                v-on:click="check"
                v-model="selected"
                value="BELS Research Industrials.xlsx"
                label="Industrials"
              ></v-checkbox>
              <v-checkbox
                color="info"
                class="line_height"
                v-on:click="check"
                v-model="selected"
                value="BELS Research Consumer.xlsx"
                label="Consumer"
              ></v-checkbox>
              <v-checkbox
                color="info"
                class="line_height"
                v-on:click="check"
                v-model="selected"
                value="BELS Research Healthcare.xlsx"
                label="Healthcare"
              ></v-checkbox>
              <v-checkbox
                color="info"
                class="line_height"
                v-on:click="check"
                v-model="selected"
                value="BELS Research REIT.xlsx"
                label="REIT"
              ></v-checkbox>
              <v-checkbox
                color="info"
                class="line_height"
                v-on:click="check"
                v-model="selected"
                value="BELS Research Financials.xlsx"
                label="Financials"
              ></v-checkbox>
            </ul>
          </v-flex>

          <v-flex md6>
            <v-btn class="line_down" dark color="cyan" v-on:click="upload()">
              Upload
              <v-icon dark right>cloud_upload</v-icon>
            </v-btn>
          </v-flex>
        </v-layout>
      </v-flex>

      <v-flex md6 class="test">
        Last Update: {{ date }}
        <v-textarea
          class="line_down1"
          v-model="text_db"
          outline
          height="300"
          :readonly="true"
          placeholder="Update status (script output)"
        ></v-textarea>
      </v-flex>
    </v-layout>

    <!-------------------------Progress Bar Starts---------------------->
    <v-layout row wrap>
      <v-flex md4></v-flex>
      <v-flex md4>
        <v-progress-linear :indeterminate="switchMe" color="info" :active="active"></v-progress-linear>
      </v-flex>
    </v-layout>
    <!-------------------------Progress Bar Ends------------------------>

    <!----------------------------Modal Starts-------------------------->
    <v-dialog persistent v-model="dialog" width="500">
      <v-card v-for="values in dbData" :key="values['time_difference']">
        <v-card-title
          class="headline"
          primary-title
        >Company {{values['company_name']}} has {{values['old_value']}} and {{values['new_value']}} values conflict</v-card-title>
        <v-card-text>
          <v-text-field v-model="values['comments']" label="Comments*"></v-text-field>
          <small>*if no comments provided. Row will not be updated</small>
        </v-card-text>
      </v-card>
      <v-card>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" flat @click="updateComments()">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!----------------------------Modal Ends---------------------------->

    <!----------------------------SnackBar Starts---------------------------->
    <v-snackbar v-model="snackbar" :timeout="1000" :top="top">
      {{ msg }}
      <v-btn color="pink" flat @click="snackbar = false">Close</v-btn>
    </v-snackbar>
    <!----------------------------SnackBar Ends------------------------------>
  </v-container>
</template>


<script>
import Repository from "../Repository";

export default {
  name: "Menu",

  data() {
    return {
      selected: [],
      all_sectors: false,
      date: "",
      text_db: "",
      switchMe: false,
      active: false,
      dialog: false,
      dbData: null,

      // show snackbar and set position
      snackbar: false,
      top: "top",
      msg: null
    };
  },

  created: function() {
    this.dbUpdateTime();
  },

  methods: {
    select_all: function() {
      if (this.all_sectors) {
        this.selected = [
          "BELS Research Technology.xlsx",
          "BELS Research Industrials.xlsx",
          "BELS Research Consumer.xlsx",
          "BELS Research Healthcare.xlsx",
          "BELS Research REIT.xlsx",
          "BELS Research Financials.xlsx"
        ];
      } else {
        this.selected = [];
      }
    },

    check: function() {
      if (this.selected.length == 6) {
        this.all_sectors = true;
      } else {
        this.all_sectors = false;
      }
    },

    upload: function() {
      if (this.checkSelected()) {
        this.active = true;
        this.switchMe = true;
        this.text_db = "";
        Repository.updateDb(this.selected).then(response => {
          this.date = Date();
          this.switchMe = false;
          this.active = false;
          this.text_db = response["message"];
          this.updateDbTime();
          this.dbUpdateTime();
          if (response["data"]) {
            this.dbData = response["data"];
            this.dialog = true;
          }
        });
      }
    },

    updateComments: function() {
      this.dialog = false;
      this.active = true;
      this.switchMe = true;
      Repository.updateComents(this.dbData).then(response => {
        this.switchMe = false;
        this.active = false;
        this.text_db = response;
      });
    },

    dbUpdateTime: function() {
      Repository.getDbUpdateTime().then(response => {
        this.date = response;
      });
    },

    updateDbTime: function() {
      Repository.postDbUpdateTime();
    },

    checkSelected: function() {
      if (this.selected.length == 0) {
        this.msg = "No Files Selected...";
        this.snackbar = true;
        return false;
      }
      return true;
    }
  }
};
</script>


<style scoped>
.line_height {
  margin-top: -30px;
}

.line_down {
  margin-top: 25px;
}

.line_down1 {
  margin-top: 5rem;
}

.test {
  margin-left: 9rem;
}
</style>