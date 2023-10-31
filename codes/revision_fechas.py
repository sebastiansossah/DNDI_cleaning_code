
def revision_fecha(fecha):

    months = [
    'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
    'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC', 'UNK'
    ]

    months_dict = {
    1: 'JAN',
    2: 'FEB',
    3: 'MAR',
    4: 'APR',
    5: 'MAY',
    6: 'JUN',
    7: 'JUL',
    8: 'AUG',
    9: 'SEP',
    10: 'OCT',
    11: 'NOV',
    12: 'DEC'
    }


    if str(fecha) == 'nan' or fecha == float('nan'):
        return 'Value is not a valid date'
    else:
        divided = str(fecha).split('-')
        ultimo  = divided
                
        if len(divided) != 3:
            
            division_interna = fecha.split('/')
            if  len(division_interna) == 3:

                new = division_interna
                if division_interna[1] not in months:
                    
                    if str(division_interna[1]).upper() in months:
                        pass
                    
                    elif isinstance(division_interna[1], int) == True or isinstance(division_interna[1], float):
                        if int(str(division_interna[1]).replace('0','')) in months_dict.keys():
                            new[1] =  months_dict[int(str(division_interna[1]).replace('0',''))]
                            pass
                        
                        else: 
                            new = 'Value is not a valid date'

                if len(division_interna[2]) != 4:
                    if division_interna[0] == 'UNK':
                        pass
                    else:            
                        new =  'Value is not a valid date'


                if len(division_interna[0]) !=2:
                    if division_interna[0] == 'UNK':
                            pass

                    elif len(str(division_interna[0]))==1:
                        new[0] = '0' + str(division_interna[0])

                    else:
                        new = 'Value is not a valid date'


                return f'SEC - In order to comply with the correct date format, the date will be changed to {"-".join(new)}'

    #------------------------------------------
            else:
                return 'Value is not a valid date'
        
        if divided[1] not in months:
            

            if divided[1].upper() in months:
                ultimo[1] =  divided[1].upper()

            elif isinstance(divided[1], int) == True or isinstance(divided[1], float): 
                if int(str(divided[1]).replace('0','')) in months_dict.keys():
                    ultimo[1] =  months_dict[int(str(divided[1]).replace('0',''))]

                else:
                    ultimo =  'Value is not a valid date'


        if len(divided[2]) != 4:
            if divided[0] == 'UNK':
                pass
            else:
                ultimo =  'Value is not a valid date'


        if len(divided[0]) !=2:
            if divided[0] == 'UNK':
                pass

            elif len(str(divided[0]))==1:
                ultimo[0] = '0' + str(divided[0])

            else:
                ultimo=  'Value is not a valid date'
        
        if "-".join(ultimo) != fecha:
            return f'SEC - In order to comply with the correct date format, the date will be changed to {"-".join(ultimo)}'
        else:
            return None

if __name__ == '__main__':
    prueba1 = '08-JUN-2023'
    prueba2 = '8-05-2022'
    prueba3 = '08/JUN/2023'

    print(revision_fecha(prueba1))
    print(revision_fecha(prueba2))
    print(revision_fecha(prueba3))