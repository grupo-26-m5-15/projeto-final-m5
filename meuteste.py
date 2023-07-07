import calendar
import datetime
from datetime import date

from dateutil.relativedelta import relativedelta


def devolution_date():
    end_date = date.today() + relativedelta(days=+15)
    name_day = calendar.day_name[datetime.datetime.strptime(
        str(end_date), '%Y-%m-%d').weekday()]

    if name_day == 'Saturday':
        end_date = date.today() + relativedelta(days=+17)

    if name_day == 'Sunday':
        end_date = date.today() + relativedelta(days=+16)
    return end_date


print(devolution_date())

# data_atual = date.today()


# def returnDate(plus_days=0):
#     return date.today() + relativedelta(days=+15 + plus_days)

# data_entrega = returnDate()

# data_devolucao = datetime.datetime.strptime(
#     str(data_entrega), '%Y-%m-%d').weekday()

# name_day = calendar.day_name[data_devolucao]

# if name_day == 'Saturday':
#     data_entrega = returnDate(2)

# if name_day == 'Sunday':
#     data_entrega = returnDate(1)

# print("data_entrega: ", data_entrega)
# print("entrega: ", entrega)
# print("name_day: ", name_day)
