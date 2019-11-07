<template>
  <v-container grid-list-md text-xs-center>

     <v-layout row wrap class="down">
      <v-flex md3>
        <h1>PNL</h1>
      </v-flex>
    </v-layout>

    <!----------------------------Data Table Starts-------------------------->
    <v-card v-if="show">
      <v-card-title>
        <v-spacer></v-spacer>
        <v-text-field v-model="search" append-icon="search" label="Search" single-line hide-details></v-text-field>
      </v-card-title>
      <v-data-table :headers="headers" :hide-actions="actions" :loading="loading" :search="search" :items="details" class="elevation-1">
        <template slot="items" slot-scope="myprops">
          <td v-for="header in headers" v-bind:key="header.text" >{{  myprops.item[header.value] }}</td>
        </template>
      </v-data-table>
    </v-card>
    <!---------------------------- Data Table Starts------------------------->

  </v-container>
</template>


<script>
import Repository from "../Repository";

export default {
  name: "Menu",
  data() {
    return {
      details: null,
      loading: true,
      show: false,
      actions: true,
      search: '',

      headers: [
        { text: "", value: "index", sortable:false},
        { text: "Current A", value: "cur_A", sortable:false},
        { text: "Target A", value: "tar_A", sortable:false},
        { text: "Trade A", value: "trade_A", sortable:false},
        { text: "Current B", value: "cur_B", sortable:false},
        { text: "Target B", value: "tar_B", sortable:false},
        { text: "Trade B", value: "trade_B", sortable:false},
        { text: "Current Total", value: "cur_total", sortable:false},
        { text: "Target Total", value: "tar_total", sortable:false},
        { text: "Trade Total", value: "trade_total", sortable:false},
        { text: "Return", value: "return", sortable:false},
        { text: "Strategy A", value: "strat_A", sortable:false},
        { text: "Strategy B", value: "strat_B", sortable:false},
        { text: "Total", value: "total", sortable:false }
      ]
    };
  },

  created: function() {
    this.getPNL();
  },

  methods: {
    getPNL: function() {
      Repository.getPNL()
        .then(response => {
          this.details = response.df
          this.show = true
      })
    }
  }
};
</script>


<style scoped>
.down {
  padding-bottom: 60px;
}

h3{
  color: grey
}

table.v-table tbody td:first-child, table.v-table tbody td:not(:first-child), table.v-table tbody th:first-child, table.v-table tbody th:not(:first-child), table.v-table thead td:first-child, table.v-table thead td:not(:first-child), table.v-table thead th:first-child, table.v-table thead th:not(:first-child) {
  padding: 1px
}

.v-input.v-text-field.v-text-field--single-line.v-input--hide-details.theme--light{
  max-width: 20%
}
</style>