<template>
  <v-container grid-list-md text-xs-center>
    <v-layout row wrap class="down">
      <v-flex md3>
         <h1>Strategy B</h1>
      </v-flex>
    </v-layout>

    <!----------------------------Table Starts-------------------------->
    <v-data-table v-if="showTable" :hide-actions="actions" :loading="loading" :headers="headers" :items="df" class="elevation-1">
      <template slot="items" slot-scope="myprops">
        <td v-for="header in headers" v-bind:key="header.text" >{{  myprops.item[header.value] }}</td>
      </template>
    </v-data-table>
    <!----------------------------Table Ends---------------------------->
 
 </v-container>
</template>


<script>
import Repository from "../Repository";

export default {
  name: "Menu",

  data() {
    return {
      // for data table
      showTable: false,
      headers: null,
      df: null,
      actions: true,
      loading: true
    };
  },

  created: function(){
    this.strategy_B();
  },

  methods: {
    strategy_B: function(){
        Repository.getStrategyTable('B')
          .then(response => {
              this.df = response['df']
              this.headers = response['columns']
              this.showTable = true
          })
    }
  }
};
</script>


<style scoped>
.down{
    padding-bottom:60px
}

.elevation-1 {
  padding-top: 3%;
}

</style>


