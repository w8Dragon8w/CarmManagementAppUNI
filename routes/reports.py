import calendar
from constants import MONTHS
from models import Maintenance


def build_daily_report(available_maintenances: list[Maintenance], capacity: int) -> list[dict]:
    """Build the daily report for the Garage availability."""
    date_count = count_maintenance_by_date(available_maintenances)
    return generate_daily_report(date_count, capacity)


def count_maintenance_by_date(available_maintenances: list[Maintenance]) -> dict:
    """Counts the number of maintenance requests per day."""
    date_count = {}
    for maintenance in available_maintenances:
        scheduled_date = maintenance.scheduledDate
        date_count[scheduled_date] = date_count.get(scheduled_date, 0) + 1
    return date_count


def generate_daily_report(date_count: dict, capacity: int) -> list[dict]:
    """Generates the daily report based on date count and capacity."""
    response = []
    for maintenance_date, requests in date_count.items():
        date_report = {
            "date": str(maintenance_date),
            "requests": requests,
            "availableCapacity": capacity - requests
        }
        response.append(date_report)
    return response


def build_monthly_report(available_maintenances: list[Maintenance], start_year: int, end_year: int):
    """Builds the monthly report for the given range of years."""
    date_counts = build_year_month_obj(available_maintenances, start_year, end_year)
    return generate_monthly_report(date_counts, start_year, end_year)


def generate_monthly_report(date_counts: dict, start_year: int, end_year: int) -> list[dict]:
    """Generates the monthly report based on date counts."""
    report = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            report.append({
                "yearMonth": {
                    "year": year,
                    "month": MONTHS[month],
                    "leapYear": calendar.isleap(year),
                    "monthValue": month
                },
                "requests": date_counts[year].get(month, 0),
            })
    return report


def build_year_month_obj(available_maintenances: list[Maintenance], start_year: int, end_year: int):
    """Builds a dictionary to count maintenance requests per year and month."""
    date_count = initialize_year_month_dict(start_year, end_year)
    count_maintenance_by_year_and_month(available_maintenances, date_count)
    return date_count


def initialize_year_month_dict(start_year: int, end_year: int) -> dict:
    """Initializes a dictionary with years as keys and months as nested keys with 0 values."""
    return {year: {month: 0 for month in range(1, 13)} for year in range(start_year, end_year + 1)}


def count_maintenance_by_year_and_month(available_maintenances: list[Maintenance], date_count: dict):
    """Counts the maintenance requests per year and month."""
    for maintenance in available_maintenances:
        year = maintenance.scheduledDate.year
        month = maintenance.scheduledDate.month
        date_count[year][month] += 1