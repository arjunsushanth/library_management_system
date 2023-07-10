import datetime


class Pricing:
    def calculate_price(borrowed_date, return_date):
        calculate_days = (return_date.date() -
                          borrowed_date.date()).days
        if calculate_days <= 7:
            fine = 5
        else:
            fine = 5 + (calculate_days - 7) * 10
        return fine