<template>
  <v-container grid-list-md text-xs-center>

    <v-layout row wrap v-if="show">
      <v-flex md5>
          <v-layout row wrap>
           <v-flex md6><h1>Capital Allocation</h1></v-flex>
           <v-flex md6 class="down">
             <v-btn dark color="cyan" v-on:click="update()">Update<v-icon dark right>cloud_upload</v-icon></v-btn>
             </v-flex>
          </v-layout>

          <v-layout row wrap class="down">
                <h4>Portfolio NAV &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</h4> 
                <input class="portfolio" v-model.number="portfolio">
          </v-layout>

          <v-layout row wrap class="down">
            <table>
              <thead>
                <tr>
                  <th>Strategy Name</th>
                  <th>PRIMERO</th>
                  <th>JUMP</th>
                </tr>
              </thead>

              <tr>
                <th>Strategy Allocation (%)</th>
                <td><vue-numeric :minus="minus" :precision="precision"  currency="%" currency-symbol-position="suffix" v-model.number="strategy_allocations['primero'][0]"></vue-numeric></td>
                <td><vue-numeric :minus="minus" :precision="precision"  currency="%" currency-symbol-position="suffix"  v-model.number="strategy_allocations['jump'][0]"></vue-numeric></td>
              </tr>

              <tr>
                <th>Strategy Allocation ($)</th>
                <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="strategy_allocations['primero'][1]"></vue-numeric></td>
                <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="strategy_allocations['jump'][1]"></vue-numeric></td>
              </tr>
            </table>
          </v-layout>

          <v-layout row wrap class="down1">
                   <h3>Within Strategy Sector Allocations</h3>
            <table >
                <tr>
                  <th>CONS</th>
                  <td><vue-numeric :minus="minus" :precision="precision"  currency="%" currency-symbol-position="suffix"  v-model.number="within['primero'][0]"></vue-numeric></td>
                  <td><vue-numeric :minus="minus" :precision="precision"  currency="%" currency-symbol-position="suffix"  v-model.number="within['jump'][0]"></vue-numeric></td>
                </tr>

                <tr>
                  <th>INDU</th>
                  <td><vue-numeric :minus="minus" :precision="precision"  currency="%" currency-symbol-position="suffix"  v-model.number="within['primero'][1]"></vue-numeric></td>
                  <td><vue-numeric :minus="minus" :precision="precision"  currency="%" currency-symbol-position="suffix"  v-model.number="within['jump'][1]"></vue-numeric></td>
                </tr>
      
                <tr>
                  <th>STPL</th>
                  <td><vue-numeric :minus="minus" :precision="precision"  currency="%" currency-symbol-position="suffix"  v-model.number="within['primero'][2]"></vue-numeric></td>
                  <td><vue-numeric :minus="minus" :precision="precision"  currency="%" currency-symbol-position="suffix"  v-model.number="within['jump'][2]"></vue-numeric></td>
                </tr>

                <tr>
                  <th>TECH</th>
                  <td><vue-numeric :minus="minus" :precision="precision"  currency="%" currency-symbol-position="suffix"  v-model.number="within['primero'][3]"></vue-numeric></td>
                  <td><vue-numeric :minus="minus" :precision="precision"  currency="%" currency-symbol-position="suffix"  v-model.number="within['jump'][3]"></vue-numeric></td>
                </tr>

                <tr>
                  <th>Total</th>
                  <td><vue-numeric :minus="minus" read-only currency="%" currency-symbol-position="suffix" v-model="within['primero'][4]"></vue-numeric></td>
                  <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="within['jump'][4]"></vue-numeric> %</td>
                </tr>
                <br>
                <tr>
                  <th>Strategy LMV (Target)</th>
                   <td><vue-numeric :minus="minus" :precision="precision"  currency="%" currency-symbol-position="suffix"  v-model.number="target['primero'][0]"></vue-numeric></td>
                   <td><vue-numeric :minus="minus" :precision="precision"  currency="%" currency-symbol-position="suffix"  v-model.number="target['jump'][0]"></vue-numeric></td>
                </tr>
                <tr>
                  <th>Strategy SMV (Target)</th>
                   <td><vue-numeric :minus="minus" read-only currency="%"  currency-symbol-position="suffix" :precision="precision" v-model="target['primero'][1]"></vue-numeric></td>
                   <td><vue-numeric :minus="minus" read-only currency="%"  currency-symbol-position="suffix" :precision="precision" v-model="target['jump'][1]"></vue-numeric></td>
                </tr>
                <tr>
                  <th>CONS</th>
                  <td><vue-numeric :minus="minus" :precision="precision"  currency="%" currency-symbol-position="suffix"  v-model.number="target['primero'][2]"></vue-numeric></td>
                  <td><vue-numeric :minus="minus" :precision="precision"  currency="%" currency-symbol-position="suffix"  v-model.number="target['jump'][2]"></vue-numeric></td>
                </tr>
                <tr>
                  <th>INDU</th>
                  <td><vue-numeric :minus="minus" :precision="precision"  currency="%" currency-symbol-position="suffix"  v-model.number="target['primero'][3]"></vue-numeric></td>
                  <td><vue-numeric :minus="minus" :precision="precision"  currency="%" currency-symbol-position="suffix"  v-model.number="target['jump'][3]"></vue-numeric></td>
                </tr>
                <tr>
                  <th>STPL</th>
                  <td><vue-numeric :minus="minus" :precision="precision"  currency="%" currency-symbol-position="suffix"  v-model.number="target['primero'][4]"></vue-numeric></td>
                  <td><vue-numeric :minus="minus" :precision="precision"  currency="%" currency-symbol-position="suffix"  v-model.number="target['jump'][4]"></vue-numeric></td>
                </tr>
                <tr>
                  <th>TECH</th>
                  <td><vue-numeric :minus="minus" :precision="precision"  currency="%" currency-symbol-position="suffix"  v-model.number="target['primero'][5]"></vue-numeric></td>
                  <td><vue-numeric :minus="minus" :precision="precision"  currency="%" currency-symbol-position="suffix"  v-model.number="target['jump'][5]"></vue-numeric></td>
                </tr>
            </table>
          </v-layout> 
      </v-flex>

      <v-flex md2></v-flex>

      <v-flex md5>
        <v-layout row wrap class="down">
          <table class="view">
            <thead>
              <th>Sector Allocation ($)</th>
              <tr></tr>
              <tr></tr>
              </thead>
            <tr>
              <th>CONS</th>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="sector_allocations['primero'][0]"></vue-numeric></td>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="sector_allocations['jump'][0]"></vue-numeric></td>
            </tr>
            <tr>
              <th>INDU</th>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="sector_allocations['primero'][1]"></vue-numeric></td>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="sector_allocations['primero'][1]"></vue-numeric></td>
            </tr>
            <tr>
              <th>STPL</th>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="sector_allocations['primero'][2]"></vue-numeric></td>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="sector_allocations['primero'][2]"></vue-numeric></td>
            </tr>
            <tr>
              <th>TECH</th>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="sector_allocations['primero'][3]"></vue-numeric></td>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="sector_allocations['primero'][3]"></vue-numeric></td>
            </tr>
            <tr>
              <th>TOTAL</th>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="sector_allocations['primero'][4]"></vue-numeric></td>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="sector_allocations['primero'][4]"></vue-numeric></td>
            </tr>
            <br>
            <thead>
              <th>Allocation of Portfolio</th>
              <tr></tr>
              <tr></tr>
              </thead>
            <tr>
              <th>CONS</th>
              <td><vue-numeric :minus="minus" currency="%" currency-symbol-position="suffix" read-only :precision="precision" v-model="allocations_portfolio['primero'][0]"></vue-numeric></td>
              <td><vue-numeric :minus="minus" currency="%" currency-symbol-position="suffix" read-only :precision="precision" v-model="allocations_portfolio['jump'][0]"></vue-numeric></td>
            </tr>
            <tr>
              <th>INDU</th>
              <td><vue-numeric :minus="minus" currency="%" currency-symbol-position="suffix" read-only :precision="precision" v-model="allocations_portfolio['primero'][1]"></vue-numeric></td>
              <td><vue-numeric :minus="minus" currency="%" currency-symbol-position="suffix" read-only :precision="precision" v-model="allocations_portfolio['jump'][1]"></vue-numeric></td>
            </tr>
            <tr>
              <th>STPL</th>
              <td><vue-numeric :minus="minus" currency="%" currency-symbol-position="suffix" read-only :precision="precision" v-model="allocations_portfolio['primero'][2]"></vue-numeric></td>
              <td><vue-numeric :minus="minus" currency="%" currency-symbol-position="suffix" read-only :precision="precision" v-model="allocations_portfolio['jump'][2]"></vue-numeric></td>
            </tr>
            <tr>
              <th>TECH</th>
              <td><vue-numeric :minus="minus" currency="%" currency-symbol-position="suffix" read-only :precision="precision" v-model="allocations_portfolio['primero'][3]"></vue-numeric></td>
              <td><vue-numeric :minus="minus" currency="%" currency-symbol-position="suffix" read-only :precision="precision" v-model="allocations_portfolio['jump'][3]"></vue-numeric></td>
            </tr>
            <tr>
              <th>TOTAL</th>
              <td><vue-numeric :minus="minus" currency="%" currency-symbol-position="suffix" read-only :precision="precision" v-model="allocations_portfolio['primero'][4]"></vue-numeric></td>
              <td><vue-numeric :minus="minus" currency="%" currency-symbol-position="suffix" read-only :precision="precision" v-model="allocations_portfolio['jump'][4]"></vue-numeric></td>
            </tr>
            <br>
            <thead>
              <th>LMV of Allocation (goes into books)</th>
              <tr></tr>
              <tr></tr>
              </thead>
             <tr>
              <th>CONS</th>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="lmv['primero'][0]"></vue-numeric></td>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="lmv['jump'][0]"></vue-numeric></td>
            </tr>
            <tr>
              <th>INDU</th>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="lmv['primero'][1]"></vue-numeric></td>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="lmv['primero'][1]"></vue-numeric></td>
            </tr>
            <tr>
              <th>STPL</th>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="lmv['primero'][2]"></vue-numeric></td>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="lmv['primero'][2]"></vue-numeric></td>
            </tr>
            <tr>
              <th>TECH</th>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="lmv['primero'][3]"></vue-numeric></td>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="lmv['primero'][3]"></vue-numeric></td>
            </tr>
            <tr>
              <th>TOTAL</th>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="lmv['primero'][4]"></vue-numeric></td>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="lmv['primero'][4]"></vue-numeric></td>
            </tr>
            <br>
            <thead>
              <th>SMV of Allocation (goes into books)</th>
              <tr></tr>
              <tr></tr>
              </thead>
            <tr>
              <th>CONS</th>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="smv['primero'][0]"></vue-numeric></td>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="smv['jump'][0]"></vue-numeric></td>
            </tr>
            <tr>
              <th>INDU</th>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="smv['primero'][1]"></vue-numeric></td>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="smv['jump'][1]"></vue-numeric></td>
            </tr>
            <tr>
              <th>TECH</th>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="smv['primero'][2]"></vue-numeric></td>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="smv['jump'][2]"></vue-numeric></td>
            </tr>
            <tr>
              <th>STPL</th>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="smv['primero'][3]"></vue-numeric></td>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="smv['jump'][3]"></vue-numeric></td>
            </tr>
            <tr>
              <th>TOTAL</th>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="smv['primero'][4]"></vue-numeric></td>
              <td><vue-numeric :minus="minus" read-only :precision="precision" v-model="smv['jump'][4]"></vue-numeric></td>
            </tr>

          </table>
        </v-layout>
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
      show: false,
      portfolio: null,
      strategy_allocations: null,
      allocations_portfolio: null,
      within: null,
      target: null,
      sector_allocations: null,
      lmv: null,
      smv: null,
      minus: true,
      precision: 2,

      // snackbar details and set position
      snackbar: false,
      top: "top",
      right: "right"
    };
  },

  mounted: function() {
    this.getAllocations();
  },

  components: {
    VueNumeric
  },

  methods: {
    getAllocations: function() {
      Repository.getAllocations().then(response => {
        (this.portfolio = response["portfolio"]),
        (this.strategy_allocations = response["strategy_allocations"]),
        (this.allocations_portfolio = response["allocations_portfolio"]),
        (this.within = response["within"]),
        (this.target = response["target"]),
        (this.lmv = response["lmv_allocations"]),
        (this.smv = response["smv_allocations"]),
        (this.sector_allocations = response["sector_allocations"]),
        this.show = true;
      });
    },

    update: function() {
      Repository.updateAllocations(this.portfolio, this.within, this.target, this.strategy_allocations)
        .then(response => {
          if (response){
            this.getAllocations()
            this.snackbar = true
          }
        })
    }
  }
};
</script>


<style scoped>
input {
  width: 50%;
  text-align: center;
  background: lightgray
}

input.portfolio{
  width: 100px;
  text-align: center;
}

.down1 {
  padding-top: 3% !important;
}

.down {
  padding-top: 3% !important;
}

table.view {
  width: 100%;
  font-size: 85%;
  border-style: solid;
  border-color: #00bcd4
}

table{
  width: 100%;
  font-size: 13px;
  border-style: solid;
  border-color: #00bcd4
}

h3{
  color:blue
}

</style>