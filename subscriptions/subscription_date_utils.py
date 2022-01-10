import datetime
from dateutil import relativedelta
import calendar
import logging

HURRICANE_SEASON_START_MONTH = 6
HURRICANE_SEASON_END_MONTH = 11


def should_suspend_subscription(plan_type, next_billing_date):
    return plan_type == "MONTHLY" and next_billing_date.month > HURRICANE_SEASON_END_MONTH


def get_next_start_of_hurricane_season():
    today = datetime.date.today()
    next_hurricane_season = today + relativedelta.relativedelta(month=6, day=1)
    if today.month >= HURRICANE_SEASON_START_MONTH:
        next_hurricane_season = today + relativedelta.relativedelta(years=1, month=6, day=1)
    return next_hurricane_season


def get_initial_subscription_billing_date(plan_type, today):
    if plan_type == "MONTHLY":
        return get_monthly_initial_subscription_billing_date(today)
    if plan_type == "SEASONAL":
        return get_yearly_initial_subscription_billing_date(today)

    raise Exception(f"Provided plan type of {plan_type} is not valid.")


def get_monthly_initial_subscription_billing_date(today):
    # If after this year's hurricane season (December, basically), bill them on july 1st of next year
    if today.month > HURRICANE_SEASON_END_MONTH:
        next_billing_date = today + relativedelta.relativedelta(years=1, month=7, day=1)
        initial_charge_multiplier = 1
    # If it's the last month of hurricane season, next billing date will be June 1st
    elif today.month == HURRICANE_SEASON_END_MONTH:
        next_billing_date = today + relativedelta.relativedelta(years=1, month=6, day=1)
        initial_charge_multiplier = 1
    # If hurricane season hasn't happened yet, bill them on july 1st of the current year
    elif today.month < HURRICANE_SEASON_START_MONTH:
        next_billing_date = today + relativedelta.relativedelta(month=7, day=1)
        initial_charge_multiplier = 1
    elif today.day == 1:
        next_billing_date = today + relativedelta.relativedelta(months=1, day=1)
        initial_charge_multiplier = 1
    else:
        next_billing_date = today + relativedelta.relativedelta(months=1, day=1)
        days_in_current_month = calendar.monthrange(today.year, today.month)[1]
        initial_charge_multiplier = (days_in_current_month - today.day + 1) / days_in_current_month

    logging.info("Initial calculated billing date: {}".format(next_billing_date))
    return next_billing_date, initial_charge_multiplier


def get_yearly_initial_subscription_billing_date(today):
    # If after this year's hurricane season (December, basically), bill them on the hurricane season the year after next
    if today.month > HURRICANE_SEASON_END_MONTH:
        next_billing_date = today + relativedelta.relativedelta(years=2, month=6, day=1)
        # If hurricane season hasn't happened yet, bill them at the start of next year's hurricane season
    elif today.month < HURRICANE_SEASON_START_MONTH:
        next_billing_date = today + relativedelta.relativedelta(years=1, month=6, day=1)
    else:
        next_billing_date = today + relativedelta.relativedelta(years=1)
    initial_charge_multiplier = 1
    return next_billing_date, initial_charge_multiplier