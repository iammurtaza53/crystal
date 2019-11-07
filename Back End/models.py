# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Company(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    ticker_id = models.CharField(max_length=20, blank=True, null=True)
    sector = models.CharField(max_length=50, blank=True, null=True)
    subsector = models.CharField(max_length=50, blank=True, null=True)
    deactivated_date = models.CharField(max_length=-1, blank=True, null=True)
    deactivated_reason = models.CharField(max_length=-1, blank=True, null=True)
    follow_up = models.CharField(max_length=-1, blank=True, null=True)
    follow_up_date = models.CharField(max_length=-1, blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Fund(models.Model):
    co = models.ForeignKey(Company, models.DO_NOTHING, blank=True, null=True)
    is_active = models.BooleanField()
    most_recent = models.BooleanField()
    period_ending_month = models.CharField(max_length=10)
    period_ending_year = models.CharField(max_length=10)
    updatetime = models.DateTimeField()
    comments = models.CharField(max_length=150, blank=True, null=True)
    is_sales = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_cost_of_goods_sold_cogs_incl_d_a = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_cogs_excluding_d_a = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_depreciation_amortization_expense = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_depreciation = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_amortization_of_intangibles = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_amortization_of_deferred_charges = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_gross_income = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_sgna_expense = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_research_development = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_other_sgna = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_other_operating_expense = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_ebit_operating_income = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_nonoperating_income_net = models.DecimalField(db_column='is_nonoperating_income__net', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    is_nonoperating_interest_income = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_equity_in_earnings_of_affiliates = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_other_income_expense = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_interest_expense = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_gross_interest_expense = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_interest_capitalized = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_unusual_expense_net = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_fixed_assets_impairment = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_financial_assets_impairment = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_exceptional_provisions = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_reorganization_and_restructure_expense = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_goodwill_write_off = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_legal_claim_expense = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_other_intangible_assets_impairment = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_unrealized_investment_loss_gain = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_other_unusual_expense = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_pretax_income = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_income_taxes = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_consolidated_net_income = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_minority_interest = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_net_income = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_preferred_dividends = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_net_income_available_to_common = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_diluted_shares_outstanding = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_total_shares_outstanding = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_earnings_persistence = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_dividends_per_share = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_payout_ratio = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_ebitda = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_ebit = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_ebit_depreciation_amortization_expense = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_ttm_ebitda = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_ttm_ebitda_change_usd = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_ttm_ebitda_change_pct = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_ebitda_margin = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_ebitda_margin_change_seasonally_adj = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_ebit_margin = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_ebit_margin_change_seasonally_adj = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_gross_margin = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_gross_margin_change_seasonally_adj = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_gross_profit_as_percent_of_sg_a = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_change_seasonally_adj = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_ttm_gross_profit_as_percent_of_sg_a = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    is_ttm_gp_to_sg_a_change = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_assets = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_assets_cash_short_term_investments = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_cash_only = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_total_short_term_investments = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_total_current_assets = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_total_investments_and_advances = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_lt_investment_affiliate_companies = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_other_long_term_investments = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_long_term_note_receivable = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_total_assets = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_cash_cash_short_term_investments = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_long_term_investments = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_cash_merger_adjustment = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_cash_other = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_total_cash = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_liabilities_shareholders_equity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_liabilities_st_debt_curr_portion_lt_debt = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_accounts_payable = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_income_tax_payable = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_total_current_liabilities = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_liabilities_long_term_debt = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_total_liabilities = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_debt_st_debt_curr_portion_lt_debt = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_debt_long_term_debt = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_debt_merger_adjustment = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_debt_other = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_debt_total_debt = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_non_equity_reserves = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_preferred_stock_carrying_value = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_total_shareholders_equity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_accumulated_minority_interest = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_total_equity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_total_liabilities_shareholders_equity = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_book_value_per_share = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_tangible_book_value_per_share = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_working_capital = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_total_capital = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_supplemental_total_debt = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    bs_net_debt = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_net_income_starting_line = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_depreciation_depletion_amortization = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_depreciation_and_depletion = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_amortization_of_intangible_assets = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_deferred_taxes_investment_tax_credit = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_deferred_taxes = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_investment_tax_credit = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_operating_activities_other_funds = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_funds_from_operations = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_extraordinaries = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_changes_in_working_capital = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_receivables = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_inventories = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_accounts_payable = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_income_taxes_payable = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_other_accruals = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_other_assets_liabilities = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_net_operating_cash_flow = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_merger_expense = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_litigation_expense = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_acquisition_proforma = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_new_debt_expense = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_working_capital_adjustment = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_other = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_cfo_adjusted_mrq = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_fcf_adjusted_ltm = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_funds_from_operations_growth_usd = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_funds_from_operations_growth_pc = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_ffo_growth_ttm_average = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_ttm_funds_from_operations = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_ttm_funds_from_operations_growth = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_ttm_working_capital = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_investing_activities_capital_expenditures = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_capital_expenditures_fixed_assets = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_capital_expenditures_other_assets = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_net_assets_from_acquisitions = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_sale_of_fixed_assets_businesses = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_purchase_sale_of_investments = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_purchase_of_investments = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_sale_maturity_of_investments = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_investing_activities_other_funds = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_investing_activities_other_uses = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_investing_activities_other_sources = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_net_investing_cash_flow = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_total_capital_expenditures = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_normalize_adjustments = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_merger_adjustment = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_total_other = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_capex_adjusted_mrq = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_capex_adjusted_ltm = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_cash_dividends_paid = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_common_dividends = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_preferred_dividends = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_change_in_capital_stock = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_repurchase_of_common_preferred_stk = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_sale_of_common_preferred_stock = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_financing_activities_other_funds = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_financing_activities_other_uses = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_financing_activities_other_sources = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_net_financing_cash_flow = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_free_cash_flow = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_free_cf_per_share = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    cf_free_cf_yield_pct = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fund'

