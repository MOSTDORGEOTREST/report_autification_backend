import datetime

# Текущая дата
current_date = datetime.date.today()

# Заданная дата в прошлом
past_date = datetime.date(2024, 3, 1)

# Вычисление числа месяцев между датами
months_diff = (current_date.year - past_date.year) * 12 + current_date.month - past_date.month

# Вывод результата
print(f"Число месяцев от {past_date} до {current_date}: {months_diff}")