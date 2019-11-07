<template>
  <v-container grid-list-md text-xs-center>
    <v-layout row wrap>
      <v-flex xs3>
        <h1>Strategy Parameters</h1>
      </v-flex>
      <v-flex xs5>
        <v-btn dark color="cyan" v-on:click="updateParams()">Update<v-icon dark right>update</v-icon></v-btn>
      </v-flex>
    </v-layout>

    <v-layout row wrap v-if='show'>
      <v-flex xs4>
        <h3>Position thresholds</h3>
        <table style="width:100%">
          <tr>
            <th></th>
            <th colspan="2">Primero</th>
            <th colspan="2">Jump</th>
          </tr>
          <tr>
            <th></th>
            <th>Long</th>
            <th>Short</th>
            <th>Long</th>
            <th>Short</th>
          </tr>
          <tr class="align-columns">
            <th>CONS</th>
            <td><vue-numeric currency="%" currency-symbol-position="suffix" v-model.number="parameters['PRIMERO']['CONS']['LONG']"></vue-numeric></td>
            <td><vue-numeric currency="%" currency-symbol-position="suffix" v-model.number="parameters['PRIMERO']['CONS']['SHORT']"></vue-numeric></td>
            <td><vue-numeric currency="%" currency-symbol-position="suffix" v-model.number="parameters['JUMP']['CONS']['LONG']"></vue-numeric></td>
            <td><vue-numeric currency="%" currency-symbol-position="suffix" v-model.number="parameters['JUMP']['CONS']['SHORT']"></vue-numeric></td>
          </tr>
          <tr class="align-columns">
            <th>TECH</th>
            <td><vue-numeric currency="%" currency-symbol-position="suffix" v-model.number="parameters['PRIMERO']['TECH']['LONG']"></vue-numeric></td>
            <td><vue-numeric currency="%" currency-symbol-position="suffix" v-model.number="parameters['PRIMERO']['TECH']['SHORT']"></vue-numeric></td>
            <td><vue-numeric currency="%" currency-symbol-position="suffix" v-model.number="parameters['JUMP']['TECH']['LONG']"></vue-numeric></td>
            <td><vue-numeric currency="%" currency-symbol-position="suffix" v-model.number="parameters['JUMP']['TECH']['SHORT']"></vue-numeric></td>
          </tr>
          <tr class="align-columns">
            <th>INDU</th>
            <td><vue-numeric currency="%" currency-symbol-position="suffix" v-model.number="parameters['PRIMERO']['INDU']['LONG']"></vue-numeric></td>
            <td><vue-numeric currency="%" currency-symbol-position="suffix" v-model.number="parameters['PRIMERO']['INDU']['SHORT']"></vue-numeric></td>
            <td><vue-numeric currency="%" currency-symbol-position="suffix" v-model.number="parameters['JUMP']['INDU']['LONG']"></vue-numeric></td>
            <td><vue-numeric currency="%" currency-symbol-position="suffix" v-model.number="parameters['JUMP']['INDU']['SHORT']"></vue-numeric></td>
          </tr>
          <tr class="align-columns">
            <th>STPL</th>
            <td><vue-numeric currency="%" currency-symbol-position="suffix" v-model.number="parameters['PRIMERO']['STPL']['LONG']"></vue-numeric></td>
            <td><vue-numeric currency="%" currency-symbol-position="suffix" v-model.number="parameters['PRIMERO']['STPL']['SHORT']"></vue-numeric></td>
            <td><vue-numeric currency="%" currency-symbol-position="suffix" v-model.number="parameters['JUMP']['STPL']['LONG']"></vue-numeric></td>
            <td><vue-numeric currency="%" currency-symbol-position="suffix" v-model.number="parameters['JUMP']['STPL']['SHORT']"></vue-numeric></td>
          </tr>
        </table>
      </v-flex>

      <v-flex xs3></v-flex>

      <v-flex xs2>
        <h3>Rebalance thresholds</h3>
        <table style="width:100%">
          <tr>
            <th></th>
            <th>Long</th>
            <th>Short</th>
          </tr>
          <tr class="align-columns">
            <th>Primero</th>
            <td><vue-numeric currency="%" currency-symbol-position="suffix" v-model.number="parameters['primero_long']"></vue-numeric></td>
            <td><vue-numeric currency="%" currency-symbol-position="suffix" v-model.number="parameters['primero_short']"></vue-numeric></td>
          </tr>
          <tr class="align-columns">
            <th>Jump</th>
            <td><vue-numeric currency="%" currency-symbol-position="suffix" v-model.number="parameters['jump_long']"></vue-numeric></td>
            <td><vue-numeric currency="%" currency-symbol-position="suffix" v-model.number="parameters['jump_short']"></vue-numeric></td>
          </tr>
        </table>
      </v-flex>
    </v-layout>

    <v-layout row wrap class="down1" v-if="showTable">
      <v-flex xs5>
        <h3>Position count</h3>
        <table style="width:100%">
          <tr>
            <th></th>
            <th colspan="2">Primero</th>
            <th colspan="2">Jump</th>
            <th colspan="2">Total</th>
          </tr>
          <tr>
            <th></th>
            <th>Long</th>
            <th>Short</th>
            <th>Long</th>
            <th>Short</th>
            <th>Long</th>
            <th>Short</th>
          </tr>
          <tr class="align-columns">
            <th>CONS</th>
            <td>{{ positionsCount['longA'][0] }}</td>
            <td>{{ positionsCount['shortA'][0] }}</td>
            <td>{{ positionsCount['longB'][0] }}</td>
            <td>{{ positionsCount['shortB'][0] }}</td>
            <td>{{ positionsCount['TOTAL_LONG'][0] }}</td>
            <td>{{ positionsCount['TOTAL_SHORT'][0] }}</td>
          </tr>
          <tr class="align-columns">
            <th>TECH</th>
            <td>{{ positionsCount['longA'][2] }}</td>
            <td>{{ positionsCount['shortA'][2] }}</td>
            <td>{{ positionsCount['longB'][2] }}</td>
            <td>{{ positionsCount['shortB'][2] }}</td>
            <td>{{ positionsCount['TOTAL_LONG'][2] }}</td>
            <td>{{ positionsCount['TOTAL_SHORT'][2] }}</td>
          </tr>
          <tr class="align-columns">
            <th>INDU</th>
            <td>{{ positionsCount['longA'][3] }}</td>
            <td>{{ positionsCount['shortA'][3] }}</td>
            <td>{{ positionsCount['longB'][3] }}</td>
            <td>{{ positionsCount['shortB'][3] }}</td>
            <td>{{ positionsCount['TOTAL_LONG'][3] }}</td>
            <td>{{ positionsCount['TOTAL_SHORT'][3] }}</td>
          </tr>
          <tr class="align-columns">
            <th>STPL</th>
            <td>{{ positionsCount['longA'][1] }}</td>
            <td>{{ positionsCount['shortA'][1] }}</td>
            <td>{{ positionsCount['longB'][1] }}</td>
            <td>{{ positionsCount['shortB'][1] }}</td>
            <td>{{ positionsCount['TOTAL_LONG'][1] }}</td>
            <td>{{ positionsCount['TOTAL_SHORT'][1] }}</td>
          </tr>
          <tr class="align-columns">
            <th>Total</th>
            <td>{{ positionsCount['longA'][4] }}</td>
            <td>{{ positionsCount['shortA'][4] }}</td>
            <td>{{ positionsCount['longB'][4] }}</td>
            <td>{{ positionsCount['shortB'][4] }}</td>
            <td>{{ positionsCount['TOTAL_LONG'][4] }}</td>
            <td>{{ positionsCount['TOTAL_SHORT'][4] }}</td>
          </tr>
        </table>
      </v-flex>
    </v-layout>

    <!----------------------------SnackBar Starts----------------------->
    <v-snackbar v-model="snackbar" :timeout="1000" :top="top" :right="right">
      Values Updated
      <v-btn color="info" flat @click="snackbar = false">Close</v-btn>
    </v-snackbar>
    <!----------------------------SnackBar Ends------------------------->

  </v-container>
</template>


<script>
import Repository from "../Repository";
import VueNumeric from 'vue-numeric'

export default {
  name: "Menu",
  data() {
    return {
      parameters: null,
      positionsCount: null,
      show: false,
      showTable: false,

      // snackbar details and set position
      snackbar: false,
      top: "top",
      right: "right"
    };
  },

  components: {
    VueNumeric
  },

  created: function() {
    this.params();
    this.posCount()
  },

  methods: {
    params: function() {
      Repository.getParams()
        .then(response => {
          this.parameters = response
          this.show = true
      });
    },

    updateParams: function(){
      Repository.updateParams(this.parameters)
        .then(() => {
          this.snackbar = true
          this.posCount()
        })
    },

    posCount: function(){
      Repository.getPosCount()
        .then(response => {
          this.positionsCount = response
          this.showTable = true
        })
    }
  }
};
</script>


<style scoped>

tr.align-columns th,
h3 {
  text-align: left;
}

table {
  width: 100%;
  font-size: 13px;
  border-style: solid;
  border-color: #00bcd4
}

.down {
  padding-top: 25px;
}

.down1 {
  padding-top: 20px;
}

input {
  width: 85%;
  text-align: center;
  background: lightgray
}

</style>