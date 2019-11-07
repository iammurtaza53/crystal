const axios = require('axios');

const baseDomain = 'http://localhost:8000/E2P/api';

const generateUrl = `${baseDomain}/generate`;

const mainDfUrl = `${baseDomain}/df`;

const getStrategyTableUrl = `${baseDomain}/strategies`;

const getCompanyDetailsUrl = `${baseDomain}/companyDetails`;

const updateCompanyDetailsUrl = `${baseDomain}/updateCompanyTable`;

const getParamsUrl = `${baseDomain}/getParams`;

const getPosCountUrl = `${baseDomain}/getPositionsCount`;

const getPnlUrl = `${baseDomain}/pnl`;

const updateDbUrl = `${baseDomain}/updateDB`;

const allocationsUrl = `${baseDomain}/allocations`;

const dbUpdateTimeUrl = `${baseDomain}/dbUpdateTime`;

const checkLoginUrl = `${baseDomain}/login`;

const getDailyRanksUrl = `${baseDomain}/dailyRanks`;


export default ({
    get_Wilson(all_strategies, selected, consolidate, roster_type, all_tickers, all_tickers_textfield, ll_caps_on, earnings_exit, exclude, custom_message) {
        return axios.get(generateUrl, {
            params: {
                all_strategies: all_strategies,
                selected: selected,
                consolidate: consolidate,
                roster_type: roster_type,
                all_tickers: all_tickers,
                all_tickers_textfield: all_tickers_textfield,
                ll_caps_on: ll_caps_on,
                earnings_exit: earnings_exit,
                exclude: exclude,
                custom_message: custom_message
            },
            timeout: 1000 * 180
        }).then(response => {
            return response.data
        }).catch(() => {
            return 'server_error'
        })
    },

    getMainTable(){
        return axios.get(mainDfUrl,{
            timeout: 1000 * 180
        })
            .then(response => {
                return response.data
            }).catch(() => {
                return "Internal Server Error 501"
            })
    },

    getStrategyTable(strategy) {
        return axios.get(getStrategyTableUrl, {
            params: {
                strategy: strategy
            },
            timeout: 1000 * 180
        }).then(response => {
                return response.data
        }).catch(() => {
                return "Internal Server Error 501"
        })
    },

    getCompanyDetails(){
        return axios.get(getCompanyDetailsUrl, {
            timeout: 1000 * 180
        })
            .then(response => {
                return response.data.objects
            })
            .catch(() => {
                return "Internal Server Error 501"
            })

    },

    updateCompanyTable(data){
        return axios.post(updateCompanyDetailsUrl, {
            data: data,
            timeout: 1000 * 180
        })
            .then(() => {
                return "Rows Updated/Created"
            })
            .catch(() => {
                return "Internal Server Error 501"
            })
    },

    getParams(){
        return axios.get(getParamsUrl, {
            timeout: 1000 * 180
        })
            .then(response => {
                return response.data
            })
            .catch(() => {
                return "Internal Server Error 501"
            })
    },

    getPosCount(){
        return axios.get(getPosCountUrl, {
            timeout: 1000 * 180
        })
            .then(response => {
                return response.data['positions_count']
            }).catch(() => {
                return "Internal Server Error 501"
            })
    },
    
    updateParams(data){
        return axios.post(getParamsUrl,
            {
                "PRIMERO": {
                    "CONS": {
                        "LONG": data['PRIMERO']['CONS']['LONG'],
                        "SHORT": data['PRIMERO']['CONS']['SHORT']
                    },
                    "STPL": {
                        "LONG": data['PRIMERO']['STPL']['LONG'],
                        "SHORT": data['PRIMERO']['STPL']['SHORT']
                    },
                    "TECH": {
                        "LONG": data['PRIMERO']['TECH']['LONG'],
                        "SHORT": data['PRIMERO']['TECH']['SHORT']
                    },
                    "INDU": {
                        "LONG": data['PRIMERO']['INDU']['LONG'],
                        "SHORT": data['PRIMERO']['INDU']['SHORT']
                    }
                },
            
                "JUMP": {
                    "CONS": {
                        "LONG": data['JUMP']['CONS']['LONG'],
                        "SHORT": data['JUMP']['CONS']['SHORT']
                    },
                    "STPL": {
                        "LONG": data['JUMP']['STPL']['LONG'],
                        "SHORT": data['JUMP']['STPL']['SHORT']
                    },
                    "TECH": {
                        "LONG": data['JUMP']['TECH']['LONG'],
                        "SHORT": data['JUMP']['TECH']['SHORT']
                    },
                    "INDU": {
                        "LONG": data['JUMP']['INDU']['LONG'],
                        "SHORT": data['JUMP']['INDU']['SHORT']
                    }
                },
                "primero_long": data['primero_long'],
                "primero_short": data['primero_short'],
                "jump_long": data['jump_long'],
                "jump_short": data['jump_short']
        },
        {
            timeout: 1000 * 180
        }).then(() => {
                return "Values Updated"
        }).catch(() => {
                return "Internal Server Error 501"
        })
    },

    getPNL(){
        return axios.get(getPnlUrl, {
            timeout: 1000 * 180
        })
            .then(response => {
                return response.data
            })
            .catch(() => {
                return "Internal Server Error 501"
            })
    },

    updateDb(data){
        return axios.get(updateDbUrl, {
            params: {
                excel_files: data
            }
        }).then(response => {
            return response.data
        }).catch(() => {
            return "Internal Server Error 501"
        })
    },

    updateComents(data){
        return axios.post(updateDbUrl, {
            data: data,
        }).then(response => {
            return response.data
        }).catch(() => {
            return "Internal Server Error 501"
        })
    },

    getDbUpdateTime(){
        return axios.get(dbUpdateTimeUrl, {
            timeout: 1000 * 180
        })
            .then(response => {
                return response.data['time']
            }).catch(() => {
                return "Internal Server Error 501"
            })
    },

    postDbUpdateTime(){
        return axios.post(dbUpdateTimeUrl)
            .then(response => {
                return response.data
            }).catch(() => {
                return "Internal Server Error 501"
            })
    },

    getAllocations(){
        return axios.get(allocationsUrl)
            .then(response => {
                return response.data
            })
            .catch(() => {
                return "Internal Server Error 510"
            })
    },

    updateAllocations(portfolio, within, target, strategy_allocations){ 
        return axios.post(allocationsUrl, {
            portfolio: portfolio,
            within: within,
            target: target,
            strategy_allocations: strategy_allocations
        }, {
            timeout: 1000 * 180
        }).then(response => {
                return response.data
        }).catch(() => {
                return "Internal Server Error 501"
            })
    },

    checkLogin(login){
        return axios.post(checkLoginUrl, {data:login}).
            then(response => {
                return response.data
            }).catch(() => {
                return "Internal Server Error 501"
            })
    },

    getDailyRanksTable(strategy){
        return axios.get(getDailyRanksUrl, {
            params: {
                strategy: strategy
            },
            timeout: 1000 * 180
        }).then(response => {
                console.log(response.data)
                return response.data
        }).catch(() => {
                return "Internal Server Error 501"
        })
    },

})