day_string = ["Luni", "Marti", "Miercuri", "Joi", "Vineri"]
hour_string = ["8:00",
               "9:00",
               "10:00",
               "11:00",
               "12:00",
               "13:00",
               "14:00",
               "15:00",
               "16:00",
               "17:00",
               "18:00",
               "19:00",
               "20:00"]


def print_page_data(days, hours, classes):
    print('---------------------------------Rows')
    print('Luni:      ', days[0])
    print('Marti:     ', days[1])
    print('Miercuri:  ', days[2])
    print('Joi:       ', days[3])
    print('Vineri:    ', days[4])
    print('------------------------------Columns')
    print('8:  ', hours[0])
    print('9:  ', hours[1])
    print('10: ', hours[2])
    print('11: ', hours[3])
    print('12: ', hours[4])
    print('13: ', hours[5])
    print('14: ', hours[6])
    print('15: ', hours[7])
    print('16: ', hours[8])
    print('17: ', hours[9])
    print('18: ', hours[10])
    print('19: ', hours[11])
    print('------------------------------Cells')

    for index, cl in enumerate(classes):
        if cl[0] == 0:
            print('new Day')
        print(index, cl)
