from datetime import datetime
from revision_fechas import revision_fecha, date_format
from log_writer import log_writer
import warnings
import pandas as pd

from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

warnings.filterwarnings('ignore')

def Medical_or_surgical_history(df_root, path_excel_writer):
    '''
    Esta funcion tiene como finalidad la revision de cada uno de los puntos 
    del edit check para el formulario de Medical Or Surgical History (other than Leishmaniasis)
    '''

    df= df_root[df_root['name']== 'Medical Or Surgical History (other than Leishmaniasis)']
    lista_sujetos = df['Participante'].unique()
    df = df[['name', 'Visit', 'activityState', 'Participante', 'Estado del Participante', 'Campo', 'Valor', 'FormFieldInstance Id']]
    df['Value_id'] = df['Valor'].astype(str) + '|' + df['FormFieldInstance Id'].astype(str)

    df_demographic_age = df_root[df_root['name']=='Demographics']
    df_demographic_age = df_demographic_age[['Visit','Participante', 'Campo', 'Valor']]
    df_demographic_age = df_demographic_age[df_demographic_age['Campo']=='Birth Year']
    df_demographic_age = df_demographic_age[['Visit','Participante','Valor']]
    df_demographic_age = df_demographic_age.rename(columns={'Participante':'Subject', 'Valor':'Birth_Year'})

    lista_revision = []
    lista_logs = ['Medical Or Surgical History (other than Leishmaniasis)']

    # fecha_inicio = datetime.strptime('19-06-2023', "%d-%m-%Y")
    # fecha_fin =  datetime.strptime('31-10-2023', "%d-%m-%Y")

    for sujeto in lista_sujetos:
        sujeto_principal = df[df['Participante']==sujeto]

        lista_comprobacion_overlap = []

        for visita in sujeto_principal.Visit.unique():
            pru_1 = sujeto_principal[sujeto_principal['Visit']==visita]
            pru = pru_1
            pru = pru[['Campo', 'Value_id']].T
            new_columns = pru.iloc[0]
            pru = pru[1:].set_axis(new_columns, axis=1)
            pru['Subject'] = sujeto
            pru['Visit'] = visita
            pru['status'] = pru_1['activityState'].unique()
            pru = pru.merge(df_demographic_age, on=['Subject', 'Visit'], how='left')

            for index, row in pru.iterrows():

                status = row['status']
                if status == 'DATA_ENTRY_COMPLETE':
                
                    subject = row['Subject']
                    visit = row['Visit']
                    demographic_year = row['Birth_Year']

                    try:
                        any_relevant_medical = row['Are there any relevant medical history or surgical history ?']
                        any_relevant_medical_pure = any_relevant_medical.split('|')[0]
                        any_relevant_medical_form_field_instance = any_relevant_medical.split('|')[1]
                    except:
                        any_relevant_medical_pure = ''
                        any_relevant_medical_form_field_instance = 'This field doesnt have any data'
                    
                    try:
                        medical_surgical = row['Medical/Surgical History/Current Condition']
                        medical_surgical_pure = medical_surgical.split('|')[0]
                        medical_surgical_form_field_instance = medical_surgical.split('|')[1]
                    except Exception as e:
                        medical_surgical_pure = ''
                        medical_surgical_form_field_instance = 'This field doesnt have any data'

                    try:
                        onset_date = row['Onset Date/First Diagnosis/Surgery']
                        onset_date_pure = onset_date.split('|')[0]
                        onset_date_form_field_instance = onset_date.split('|')[1]
                    except Exception as e:
                        onset_date_pure = ''
                        onset_date_form_field_instance = 'This field doesnt have any data'

                    try:
                        end_date = row['End Date']
                        end_date_pure = end_date.split('|')[0]
                        end_date_form_field_instance = end_date.split('|')[1]
                    except Exception as e:
                        end_date_pure = ''
                        end_date_form_field_instance = 'This field doesnt have any data'

                    # condition_ongoing = ''
                    # severity = ''
                    # frequency = ''
                    # currently_treated = ''
                    
                    # --------------------------------------------------------------------------------------

                    try:
                        # Primera  revision general de formato de fecha ->GE0020
                        f = revision_fecha(onset_date_pure)
                        if f == None:
                            pass
                        else:
                            error = [subject, visit, 'Onset Date/First Diagnosis/Surgery', onset_date_form_field_instance ,f , onset_date_pure, 'GE0020']
                            lista_revision.append(error)     

                    except Exception as e:
                        lista_logs.append(f'Revision GE0020 --> {e}')

                    try:
                        # Primera  revision general de formato de fecha ->GE0020
                        f = revision_fecha(end_date_pure)
                        if f == None:
                            pass
                        else:
                            error = [subject, visit, 'End Date', end_date_form_field_instance ,f , end_date_pure, 'GE0020']
                            lista_revision.append(error)     

                    except Exception as e:
                        lista_logs.append(f'Revision GE0020 --> {e}')

                    # Revision  MS0010
                    try:
                        if float(any_relevant_medical_pure) == 1.0:
                            if type(medical_surgical_pure) == pd.Series:
                                print('revision MS0010 revisar medical or surgical')
                                pass
                            elif medical_surgical_pure != '' :
                                pass
                            else:
                                error = [subject, visit, 'Are there any relevant medical history or surgical history?', any_relevant_medical_form_field_instance,\
                                         'If the answer is Yes, at least one section of Medical or Surgical History Detail should be added' , any_relevant_medical_pure, 'MS0010']
                                lista_revision.append(error) 
                    except Exception as e:
                        lista_logs.append(f'Revision MS0020 --> {e}')

                    # Revision  MS0020
                    try:
                        if float(any_relevant_medical_pure) == 0.0:
                            if type(medical_surgical_pure) != pd.Series:
                                print('revision MS0020 revisar medical or surgical')
                                pass
                            elif medical_surgical_pure == '':
                                pass
                            else:
                                error = [subject, visit, 'Are there any relevant medical history or surgical history?', any_relevant_medical_form_field_instance,\
                                         'If the answer is No, No sections of Medical or Surgical History Detail should be added' , any_relevant_medical, 'MS0020']
                                lista_revision.append(error)
                    except Exception as e:
                        lista_logs.append(f'Revision MS0020 --> {e}')
                    
                    try:
                        if float(any_relevant_medical_pure) == 1.0:
                            # Revision  MS0040
                            try:
                                date_format = '%d-%b-%Y'
                                onset_date_f = datetime.strptime(onset_date_pure, date_format)
                                end_date_f = datetime.strptime(end_date_pure, date_format)

                                if onset_date_f > end_date_f:
                                    error = [subject, visit, 'End Date', end_date_form_field_instance ,\
                                        'End date must be after Onset Date/First Diagnosis/Surgery.' , end_date_pure, 'MS0040']
                                    lista_revision.append(error)
                                else:
                                    pass
                            except Exception as e:
                                lista_logs.append(f'Revision MS0040 --> {e}')

                            # Revision MS0050
                            try: 
                                if type(onset_date_pure) == pd.Series:
                                    print('revision MS0050 revisar medical or surgical')
                                    for date in onset_date_pure:
                                        onset_date_year = str(date).split('-')[2]
                                        if int(onset_date_year) < int(demographic_year):
                                            error = [subject, visit, 'Onset Date/First Diagnosis/Surgery'  ,'The year and month of  Onset Date/First taken must be equal or after the month and year of birth in DEMOGRAPHIC Diagnosis/Surgery.' , onset_date_year, 'MS0050']
                                            lista_revision.append(error)
                                else:
                                    onset_date_year = str(onset_date_pure).split('-')[2]
                                    if int(onset_date_year) < int(demographic_year):
                                        error = [subject, visit, 'Onset Date/First Diagnosis/Surgery', onset_date_form_field_instance , \
                                                 'The year and month of  Onset Date/First taken must be equal or after the month and year of birth in DEMOGRAPHIC Diagnosis/Surgery.' , onset_date_year, 'MS0050']
                                        lista_revision.append(error)
                            except Exception as e:
                                lista_logs.append(f'Revision MS0050 --> {e}')
                            
                            # Revision MS0060
                            try:
                                medical_date_history = (medical_surgical_pure, onset_date_pure, end_date_pure)

                                if medical_date_history in lista_comprobacion_overlap:
                                        error = [subject, visit, 'Medical/Surgical History/ Current Condition', medical_surgical_form_field_instance , \
                                                 'The Medica/Surgical History/ Current Condition shuold not be enter twice if the dates overlap2' , medical_surgical_pure, 'MS0060']
                                        lista_revision.append(error)
                                else:
                                    lista_comprobacion_overlap.append(medical_date_history)
                            except Exception as e:
                                lista_logs.append(f'Revision MS0060 --> {e}')

                            # Revision MS070
                            try:
                                if medical_surgical_pure != '':
                                    print('hacer la revision MS070')
                            except:
                                pass
        
                    except Exception as e:
                        lista_logs.append(f'Revision desde MS0040 hasta MS0060 --> {e}')
                    


    excel_writer = load_workbook(path_excel_writer)
    column_names = ['Subject', 'Visit', 'Field', 'Form Field Instance ID' ,'Standard Error Message', 'Value', 'Check Number']
    medical_surgical_output = pd.DataFrame(lista_revision, columns=column_names)
 
    sheet = excel_writer.create_sheet("Medical Or Surgical History")

    for row in dataframe_to_rows(medical_surgical_output, index=False, header=True):
        sheet.append(row)

    excel_writer.save(path_excel_writer)
    log_writer(lista_logs)

    return medical_surgical_output[['Form Field Instance ID' ,'Standard Error Message']].replace({',': '', ';': ''}, regex=True)

if __name__ == '__main__':
    path_excel = r"C:\Users\sebastian sossa\Documents\integraIT\projects_integrait\DNDI\Program\output\prueba.xlsx"
    df_root = pd.read_excel(r"C:\Users\sebastian sossa\Documents\integraIT\projects_integrait\DNDI\data\newDNDI.xlsx")
    Medical_or_surgical_history(df_root, path_excel ) 