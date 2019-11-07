from django.urls import path
from django.conf.urls import url, include
from . import views
from E2P.api import CompanyResource, FundResource, generate, getStrategies, getPNL,\
    updateDb, allocations, getLastUpdateTime, getParams, getG6Table,\
    checkLogin, updateCompanyTable, getPositionsCount, updateFundFiles,\
    updateCompanies, getDailyRanksTable, updateDailyRanks

company_resource = CompanyResource()
fund_resource = FundResource()

app_name = 'E2P'
urlpatterns = [
    # ex: /E2P/api/company
    url(r'^api/', include(company_resource.urls)),
    # ex: /E2P/api/fund
    url(r'^api/', include(fund_resource.urls)),
    # run file Wilson/main.py
    path('api/generate', generate, name='generate'),
    # run file Wilson/main.py
    path('api/df', getG6Table, name='df'),
    # run file E2P/G6/strategies
    path('api/strategies', getStrategies, name='getStrategies'),
    # run file E2P/G6/pnl
    path('api/pnl', getPNL, name='getPNL'),
    # run file E2P/G6/updateDB
    path('api/updateDB', updateDb, name='updateDB'),
    # run file E2P/G6/allocations
    path('api/allocations', allocations, name='allocations'),
    # run file E2P/G6/dbUpdateTime
    path('api/dbUpdateTime', getLastUpdateTime, name='dbUpdateTime'),
    # run file E2P/G6/getParams
    path('api/getParams', getParams, name='getParams'),
    # run file E2P/G6/getPositionsCount
    path('api/getPositionsCount', getPositionsCount, name='getPositionsCount'),
    # run file E2P/G6/login
    path('api/login', checkLogin, name='login'),
    # run file E2P/G6/updateCompanyTable
    path('api/updateCompanyTable', updateCompanyTable, name='updateCompanyTable'),
    # run file E2P/G6/dailyRanks
    path('api/dailyRanks', getDailyRanksTable, name='dailyRanks'),
    # run file E2P/G6/updateFundFiles
    path('api/updateFundFiles', updateFundFiles, name='updateFundFiles'),
    # run file E2P/G6/updateCompanies
    path('api/updateCompanies', updateCompanies, name='updateCompanies'),
    # run file E2P/G6/updateDailyRanks
    path('api/updateDailyRanks', updateDailyRanks, name='updateDailyRanks'),

]
