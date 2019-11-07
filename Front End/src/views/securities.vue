<template>
  <v-container grid-list-md text-xs-center>

    <v-layout row wrap class="down">
      <v-flex md3>
        <h1>Security Master</h1>
      </v-flex>
      <v-flex md4>
        <v-btn dark color="cyan" v-on:click="loginBox(newRows,editRows)">Update<v-icon dark right>update</v-icon></v-btn>
        <v-btn fab dark color="cyan" v-on:click="addRows()"><v-icon dark>add</v-icon></v-btn>
      </v-flex>
    
    <!----------------------------Data Table Starts-------------------------->
    <v-data-table v-if="show" :headers="headers" :hide-actions="actions" :loading="loading" :items="details" class="elevation-1">
      <template v-slot:items="props">
        <td class="justify-center layout px-0">
          <v-icon small class="mr-2" @click="editItem(props.item)"> edit</v-icon>
        </td>
        <td>{{ props.item.id }}</td>
        <td>{{ props.item.name }}</td>
        <td>{{ props.item.ticker_id }}</td>
        <td>{{ props.item.sector }}</td>
        <td>{{ props.item.subsector }}</td>
        <td>{{ props.item.active }}</td>
        <td>{{ props.item.deactivated_date }}</td>
        <td>{{ props.item.deactivated_reason }}</td>
        <td>{{ props.item.follow_up }}</td>
        <td>{{ props.item.follow_up_date }}</td>
      </template>
    </v-data-table>
    <!---------------------------- Data Table Ends--------------------------->


    <!----------------------------Dialog Box Starts-------------------------->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">{{ formTitle }}</span>
        </v-card-title>

        <v-card-text>
          <v-container grid-list-md>
            <v-layout wrap>
              <v-flex xs12 sm6 md4>
                <v-text-field v-model="editedItem.name" label="Name"></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md4>
                <v-text-field v-model="editedItem.ticker_id" label="Ticker ID"></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md4>
                <v-text-field v-model="editedItem.sector" label="Sector"></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md4>
                <v-text-field v-model="editedItem.subsector" label="Sub Sector"></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md4>
                <v-text-field v-model.number="editedItem.active" label="Active"></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md4>
                <v-text-field v-model="editedItem.deactivated_date" label="Deactivated Date"></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md4>
                <v-text-field v-model="editedItem.deactivated_reason" label="Deactivated Reason"></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md4>
                <v-text-field v-model="editedItem.follow_up" label="Follow Up"></v-text-field>
              </v-flex>
              <v-flex xs12 sm6 md4>
                <v-text-field v-model="editedItem.follow_up_date" label="Follow Up Date"></v-text-field>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="close">Cancel</v-btn>
          <v-btn color="blue darken-1" flat @click="save">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!----------------------------Dialog Box Ends---------------------------->
    

    <!----------------------------Dialog Box Starts-------------------------->
    <v-dialog v-model="passwordManager" max-width="300px">
      <v-card>
        <v-card-title>
          <span class="headline">Confirm Changes</span>
        </v-card-title>

        <v-card-text>
          <v-container grid-list-md>
            <v-layout row wrap>
                <v-text-field v-model="login.username" label="UserName"></v-text-field>
            </v-layout>
            <v-layout row wrap>
                <v-text-field v-model="login.password" :append-icon="showPass ? 'visibility' : 'visibility_off'" :type="showPass ? 'text' : 'password'" @click:append="showPass = !showPass" label="Password"></v-text-field>
            </v-layout>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" flat @click="checklogin(newRows, editRows)">Log In</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!----------------------------Dialog Box Ends---------------------------->


    <!----------------------------SnackBar Starts---------------------------->
    <v-snackbar v-model="snackbar" :timeout="1000" :top="top">
      {{ msg }}
      <v-btn color="pink" flat @click="snackbar = false">Close</v-btn>
    </v-snackbar>
    <!----------------------------SnackBar Ends------------------------------>
    </v-layout>

  </v-container>
</template>


<script>
import Repository from "../Repository";

export default {
  name: "Menu",

  data() {
    return {
      //array for edit rows
      editRows: [],

      //array for new rows
      newRows: [],

      // password manager
      passwordManager: false,
      showPass: false,
      login: {
        username: null,
        password: null
      },

      // show snackbar and set position
      snackbar: false,
      top: "top",
      msg: null,

      details: null,
      loading: true,
      show: false,
      dialog:false,
      actions: true,
      editedIndex: -1,
      editedItem: {
        name: '',
        ticker_id: '',
        sector: '',
        subsector: '',
        active: null,
        deactivated_date: '',
        deactivated_reason: '',
        follow_up: '',
        follow_up_date: ''
      },
      headers: [       
        { text: 'Actions', value: 'name', sortable: false},
        { text: 'ID', value: 'Id', sortable:false},
        { text: "Name", value: "name", sortable: false},
        { text: "Ticker ID", value: "ticker_id", sortable: false},
        { text: "Sector", value: "sector", sortable: false},
        { text: "Sub Sector", value: "subsector", sortable: false},
        { text: "Active", value: "active", sortable: false},
        { text: "Deactivated Date", value: "deactivated_date", sortable: false},
        { text: "Deactivated Reason", value: "deactivated_reason", sortable: false},
        { text: "Follow Up", value: "follow_up", sortable: false},
        { text: "Follow Up Date", value: "follow_up_date", sortable: false}
      ]
    };
  },

  computed:{
      formTitle() {
        return this.editedIndex === -1 ? 'New Row' : 'Edit Row'
      }
  },

  watch: {
      dialog (val) {
        val || this.close()
      }
  },

  created: function() {
    this.companyDetails();
  },
  
  methods: {
    companyDetails: function(){
      Repository.getCompanyDetails()
        .then(response => {
          this.details = response
          this.show = true
        });
    },

    editItem (item) {
        this.editedIndex = this.details.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
    },

    addRows: function() {
      this.dialog = true
    },

    loginBox: function(newRows, editRows) { 
      if(newRows.length == 0 && editRows.length ==0){
        this.msg = "No Rows need to be updated"
        this.snackbar = true
        return 
      }
      this.passwordManager = true
    },

    checklogin: function(newRows, editRows){
      this.passwordManager = false
      Repository.checkLogin(this.login)
        .then(response => {
          if (response == true){
            this.updateTable(newRows, editRows)
          }
          else{
            this.msg = "Wrong Username or Password"
            this.snackbar = true
          }
        })
    },

    updateTable(newRows, editRows){
      var data = {}
      if(newRows.length!=0){
        data['newRows'] = newRows
      }
      if(editRows.length!=0){
        data['editRows'] = editRows
      } 
      Repository.updateCompanyTable(data)
        .then(response => {
          this.msg = response
          this.snackbar = true
          this.newRows = []
          this.editRows = []
        })
    },

    close: function() {
        this.dialog = false
        setTimeout(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        }, 300)
    },

    save: function() {
      if (this.editedIndex > -1) {
        Object.assign(this.details[this.editedIndex], this.editedItem)
        this.editRows.push(this.details[this.editedIndex])
      } else {
        var last = Object.keys(this.details)[Object.keys(this.details).length-1];
        this.editedItem['id'] = parseInt(last) + 2
        this.details.push(this.editedItem)
        this.newRows.push(this.editedItem)
      }
      this.close()
    }
  }
};
</script>


<style scoped>
.down {
  padding-bottom: 60px;
}

table.v-table tbody td:first-child, table.v-table tbody td:not(:first-child), table.v-table tbody th:first-child, table.v-table tbody th:not(:first-child), table.v-table thead td:first-child, table.v-table thead td:not(:first-child), table.v-table thead th:first-child, table.v-table thead th:not(:first-child) {
  padding: 0 10px
}
</style>
        
