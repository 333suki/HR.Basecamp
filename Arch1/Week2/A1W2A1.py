input_date = input("Input date: ")

months_31 = [1, 3, 5, 7, 9]
months_30 = [4, 6, 8, 10, 11]

date_array = input_date.split("-")

if len(date_array) == 3 and len(date_array[0]) == 4 and len(date_array[1]) == 2 and len(date_array[2]) == 2:
    year = int(date_array[0])
    month = int(date_array[1])
    day = int(date_array[2])

    if month in months_30 and day == 30:
        month = month + 1 # month
        day = 1
    elif month in months_30 and day < 30:
        day = day + 1 # add +1 to day

    elif month in months_31 and day == 31:
        month = month + 1 # maand
        day = 1
    elif month in months_31 and day < 31:
        day = day + 1

    elif month == 2 and day == 28:
        month = month + 1
        day = 1
    elif month == 2 and day < 28:
        day = day + 1

    elif month == 12 and day == 31:
        year = year + 1 # jaar
        month = 1
        day = 1


    print(f"Next date: {year:04d}-{month:02d}-{day:02d}")

else:
    print("Input format ERROR. Correct Format: YYYY-MM-DD")
