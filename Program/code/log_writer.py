
def log_writer(list_log):
    '''
    Esta funcion tiene como funcion principal, escribir el reporte de todos los errores  que se presentan
    '''

    path_log_txt  = r"C:\Users\sebastian sossa\Documents\integraIT\projects_integrait\DNDI\Program\output\log.txt"

    opener = open(path_log_txt, 'a+')

    contador = 0
    for item in list_log:
        if contador == 0:
            separator = '----------------------------------------------------------'
            separator_2 = '-----------------------------'
            opener.write(separator)
            opener.write('\n')
            opener.write(item)
            opener.write('\n')
            opener.write(separator_2)
            opener.write('\n')
        
        else:
            opener.write(item)
            opener.write('\n')
        contador +=1
    
    opener.close()


