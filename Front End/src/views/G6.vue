<template>
  <v-container grid-list-md text-xs-center>
    <v-layout row wrap>

      <v-flex md3>
        <h1>G6</h1>
      </v-flex>

      <v-flex md2></v-flex>

      <v-flex md7>
        <v-layout row wrap class="border">
          <v-flex md3>
            <h2>Trading</h2>
            <v-checkbox v-model="all_strategies" v-on:click="select_all" label="All Strategies"></v-checkbox>
            <ul>
              <v-checkbox v-on:click="check" v-model="selected" value="Primero" label="Primero"></v-checkbox>
              <v-checkbox v-on:click="check" v-model="selected" value="Jump" label="Jump"></v-checkbox>
              <v-checkbox v-on:click="check" v-model="selected" value="Sloth" label="Sloth"></v-checkbox>
            </ul>
            <v-checkbox class="up1" v-model="consolidate" label="Consolidate"></v-checkbox>
          </v-flex>

          <v-flex md3>
            <br>
            <v-select v-model="roster_type" :items="rosters" item-text="order_type" item-value="code" outline></v-select>
            <v-checkbox v-model="all_tickers" label="All tickers"></v-checkbox>
            <v-text-field v-model="all_tickers_textfield" v-on:keyup="all_tickers_func" label="Paste Tickers"></v-text-field>
            <br>
            <v-checkbox class="up" v-model="ll_caps_on" label="LL caps on"></v-checkbox>
          </v-flex>

          <v-flex md1></v-flex>
          
          <v-flex md3>
            <br>
            <v-text-field v-model="earnings_exit" clearable label="Earnings exit"></v-text-field>
            <v-text-field v-model="exclude" clearable label="Exclude"></v-text-field>
            <v-text-field v-model="custom_message" clearable label="Custom Message"></v-text-field>
            <br>
            <v-btn dark color="cyan" v-on:click="generate_clicked()">Generate<v-icon dark right>update</v-icon></v-btn>
          </v-flex>
        </v-layout>
      </v-flex>
    </v-layout>

    <!----------------------------Table Starts-------------------------->
    <v-data-table v-if="showTable" :headers="headers" :loading="loading" :hide-actions="actions" :items="df" class="elevation-1">
      <template slot="items" slot-scope="myprops">
        <td v-for="header in headers" v-bind:key="header.text" >{{  myprops.item[header.value] }}</td>
      </template>
    </v-data-table>
    <!----------------------------Table Ends---------------------------->

    <!----------------------------SnackBar Starts----------------------->
    <v-snackbar v-model="snackbar" :timeout="1000" :top="top">
      No Strategy Selected!!!
      <v-btn color="pink" flat @click="snackbar = false">Close</v-btn>
    </v-snackbar>
    <!----------------------------SnackBar Ends------------------------->

    <!----------------------------Modal Starts-------------------------->
    <v-dialog persistent v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title class="headline" primary-title>Trade generation in Progress</v-card-title>
        <v-card-text>
          {{ serverText }}
        </v-card-text>
        <v-card-actions v-if="show">
          <v-spacer></v-spacer>
          <v-btn color="primary" flat @click="dialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!----------------------------Modal Ends---------------------------->


  </v-container>
</template>


<script>
import Repository from "../Repository";

export default {
  name: "Menu",

  data: function() {
    return {
      selected: ['Primero','Jump','Sloth'],
      serverText: "Generating....",
      roster_type: "F",
      all_strategies: true,
      all_tickers: true,
      ll_caps_on: true,
      consolidate: false,
      all_tickers_textfield: "",
      earnings_exit: "",
      exclude: "",
      custom_message: "",

      // show dialog box and close button
      dialog: false,
      show: false,

      // show snackbar and set position
      snackbar: false,
      top: "top",

      rosters: [
        { code: "A", order_type: "MOC/VWAP" },
        { code: "B", order_type: "LOO" },
        { code: "C", order_type: "LMT regular" },
        { code: "D", order_type: "LMT manual" },
        { code: "E", order_type: "VWAP" },
        { code: "F", order_type: "MOC" },
        { code: "G", order_type: "LMT regular 50%" }
      ],

      // for data table
      showTable: false,
      headers: null,
      df: null,
      actions: true,
      loading: true,
    };
  },

  created: function(){
    this.main_table()
  },

  methods: {
    main_table: function(){
      Repository.getMainTable()
        .then(response => {
          this.df = response['df']
          this.headers = response['columns']
          this.showTable = true
        })
    },

    select_all: function() {
      if (this.all_strategies) {
        this.selected = ['Primero','Jump','Sloth']
      } 
      else {
        this.selected = []
      }
    },

    check: function() {
      if (this.selected.length == 3){
        this.all_strategies = true
      }
      else {
        this.all_strategies = false
      }
    },

    check_strats: function() {
      if (this.selected.length == 0) {
        var vm = this;
        vm.snackbar = true;
        return 0;
      }
    },

    generate_clicked: function() {
      if (this.check_strats() == 0) {
        return;
      }
      this.serverText = "Generating";
      this.show = false;
      this.dialog = true;

      var vm = this;

      Repository.get_Wilson(  
        (this.all_strategies = vm.all_strategies),
        (this.selected = vm.selected),
        (this.consolidate = vm.consolidate),
        (this.roster_type = vm.roster_type),
        (this.all_tickers = vm.all_tickers),
        (this.all_tickers_textfield = vm.all_tickers_textfield),
        (this.ll_caps_on = vm.ll_caps_on),
        (this.earnings_exit = vm.earnings_exit),
        (this.exclude = vm.exclude),
        (this.custom_message = vm.custom_message)
      ).then(response => {
        if (response == 'server_error'){
          vm.serverText = 'Internal Server Error 501'
        }
        else if (response['code'] == 'limit_exceed'){
          vm.serverText = response['message']
        }
        else if (response['code'] == 'no_trades'){
          vm.serverText = response['message']
        }
        else{
          const messages = response['message']
          for(let message of messages){
            vm.serverText += message
            vm.serverText += ' \n '
          }
        }
        vm.show = true
      });
    },

    all_tickers_func: function(){
      if (this.all_tickers_textfield == ""){
        this.all_tickers = true
      }
      else {
        this.all_tickers = false
      }
    },
  }

};
</script>


<style>

.v-input.v-input--selection-controls.v-input--checkbox.theme--light {
  margin-top: -1px;
  margin-bottom: -18px;
}

.v-text-field__details {
  display: none;
}

h2 {
  text-align: left;
}

.border {
  border: grey;
  border-style: double;
}

.elevation-1 {
  padding-top: 3%;
}

</style>