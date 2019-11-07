<template>
  <v-container grid-list-md text-xs-center>
    <v-layout row wrap class="down">
      <v-flex md3>
        <h1>Historical ranks</h1>
      </v-flex>
      <v-flex md2></v-flex>
      <v-flex md2>
        <v-select v-model="strategy" :items="strategies" outline></v-select>
      </v-flex>
      <v-flex md2>
        <v-select v-model="type" :items="tableColumns" item-text="column" item-value="type" outline></v-select>
      </v-flex>
      <v-flex md1>
        <v-btn dark color="cyan" v-on:click="filter()">Filter</v-btn>
      </v-flex>
      <!-- <v-flex md1>
        <v-btn dark color="cyan">Download</v-btn>
      </v-flex> -->
    </v-layout>

    <!----------------------------Table Starts-------------------------->
      <v-data-table v-if="showTable" :headers="headers" :loading="loading" :items="df">
        <template slot="items" slot-scope="myprops">
          <td v-for="header in headers" v-bind:key="header.text">{{ myprops.item[header.value] }}</td>
        </template>
      </v-data-table>
    <!----------------------------Table Ends---------------------------->

    <!----------------------------Table Starts-------------------------->
      <v-data-table v-if="showTable2" :hide-actions="actions" :hide-headers="hide_headers" :headers="headers2" :items="df2" class="elevation-1">
        <template slot="items" slot-scope="myprops">
          <td v-for="header in headers2" v-bind:key="header.text">{{ myprops.item[header.value] }}</td>
        </template>
      </v-data-table>
    <!----------------------------Table Ends---------------------------->

  </v-container>
</template>

<script>
import Repository from "../Repository";

export default {
  name: "HistRanks",

  data() {
    return {
      //select strategy
      strategy: "Primero",
      strategies: ["Primero", "Jump", "Sloth"],

      //select table column
      type: "rank",
      tableColumns: [
        { type: "rank", column: "Rank" },
        { type: "yield_field", column: "Yield" },
        { type: "net_income", column: "Numerator" },
        { type: "market_cap", column: "Denominator" }
      ],

      // for data table1
      showTable: false,
      headers: null,
      df: null,
      loading: true,

      // for data table1
      showTable2: false,
      actions: true,
      hide_headers: true,
      headers2: null,
      df2: null
    };
  },

  created: function() {
    this.fetchDailyRanksTable();
  },

  methods: {
    fetchDailyRanksTable: function() {
      Repository.getDailyRanksTable(this.type).then(response => {
        this.df = response["df"];
        this.headers = response["columns"];
        this.showTable = true;
        this.df2 = response["df2"];
        this.headers2 = response["columns2"];
        this.showTable2 = true
      });
    },

    filter: function() {
      this.fetchDailyRanksTable();
    }
  }
};
</script>


<style scoped>
.down {
  padding-bottom: 60px;
}
.v-select.v-text-field {
  max-width: 10rem;
}
</style>


        