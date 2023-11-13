import numpy as np
import pandas as pd
from datetime import datetime
from revision_fechas import revision_fecha
import warnings
from log_writer import log_writer
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
warnings.filterwarnings('ignore')

def PBMC_isolate(df_root, path_excel_writer):
    '''
    Esta funcion tiene como finalidad la revision de cada uno de los puntos 
    del edit check para el formulario de PBMC Isolate
    '''

    df= df_root[df_root['name']== 'PBMC Isolate']
    lista_sujetos = df['Participante'].unique()
    df = df[['name', 'Visit', 'activityState', 'Participante', 'Estado del Participante', 'Campo', 'Valor', 'FormFieldInstance Id']]
    df['Value_id'] = df['Valor'].astype(str) + '|' + df['FormFieldInstance Id'].astype(str)

    df_visit_date = df_root[df_root['name']=='Date of visit']
    df_visit_date = df_visit_date[['Visit','Participante', 'Campo', 'Valor']]
    df_visit_date = df_visit_date[df_visit_date['Campo']=='Visit Date']
    df_visit_date = df_visit_date[['Visit','Participante','Valor']]
    df_visit_date = df_visit_date.rename(columns={'Participante':'Subject', 'Valor': 'Date_of_visit'})

    df_informed = df_root[df_root['name']=='Informed Consent']
    df_informed = df_informed[['Visit','Participante', 'Campo', 'Valor']]
    df_informed = df_informed[df_informed['Campo']=='Informed consent signature date']
    df_informed = df_informed[['Visit','Participante','Valor']]
    df_informed = df_informed.rename(columns={'Participante':'Subject', 'Valor':'Informed_consent_date'})

    df_end_study_general = df_root[df_root['name']== 'End of Study Treatment (Miltefosine)']
    df_end_study_general = df_end_study_general[['Visit','Participante', 'Campo', 'Valor', 'Variable' ]]
    df_end_study_general = df_end_study_general[df_end_study_general['Variable'] == 'DSDAT']
    df_end_study_general = df_end_study_general[['Participante', 'Valor']]
    df_end_study_general = df_end_study_general.rename(columns={'Participante':'Subject', 'Valor':'end_study_date'})

    lista_logs = ['PBMC Isolate']
    lista_revision = []

    # fecha_inicio = datetime.strptime('19-06-2023', "%d-%m-%Y")
    # fecha_fin =  datetime.strptime('31-10-2023', "%d-%m-%Y")

    for sujeto in lista_sujetos:
        sujeto_principal = df[df['Participante']==sujeto]

        for visita in sujeto_principal.Visit.unique():
            pru_1 = sujeto_principal[sujeto_principal['Visit']==visita]
            pru = pru_1
            pru = pru[['Campo', 'Value_id']].T
            new_columns = pru.iloc[0]
            pru = pru[1:].set_axis(new_columns, axis=1)
            pru['Subject'] = sujeto
            pru['Visit'] = visita
            pru['status'] = pru_1['activityState'].unique()
            pru = pru.merge(df_visit_date, on=['Subject', 'Visit'], how='left')
            pru = pru.merge(df_informed, on=['Subject', 'Visit'], how='left')
            pru = pru.merge(df_end_study_general, on=['Subject'], how='left')

            for index, row in pru.iterrows():
                status = row['status']
                subject = row['Subject']
                visit = row['Visit']

                date_of_visit = row['Date_of_visit']
                date_inform_consent = row['Informed_consent_date']
                end_study_date = row['end_study_date']

                if status == 'DATA_ENTRY_COMPLETE':

                    try:
                        was_sample_collected = row['Was the sample collected to investigate immunological marker in PBMCs?']
                        was_sample_collected_pure = was_sample_collected.split('|')[0]
                        was_sample_collected_form_field_instance = was_sample_collected.split('|')[1]
                    except Exception as e:
                        was_sample_collected_pure = ''
                        was_sample_collected_form_field_instance = 'This field doesnt have any data'

                    try:
                        provide_reason = row['Provide the reason']
                        provide_reason_pure = provide_reason.split('|')[0]
                        provide_reason_form_field_instance = provide_reason.split('|')[1]
                    except Exception as e:
                        provide_reason_pure = ''
                        provide_reason_form_field_instance = 'This field doesnt have any data'

                    try:
                        date_sample_collected = row['Date of the sample collected']
                        date_sample_collected_pure = date_sample_collected.split('|')[0]
                        date_sample_collected_form_field_instance = date_sample_collected.split('|')[1]
                    except Exception as e:
                        date_sample_collected_pure = ''
                        date_sample_collected_form_field_instance = 'This field doesnt have any data'

                    # --------------------------------------------------------------------------
                    try:
                        # Primera  revision general de formato de fecha ->GE0020
                        f = revision_fecha(date_sample_collected_pure)
                        if f == None:
                            pass
                        else:
                            error = [subject, visit, 'Date of the sample collected', date_sample_collected_form_field_instance,\
                                     f , date_sample_collected_pure, 'GE0020']
                            lista_revision.append(error)     

                    except Exception as e:
                        lista_logs.append(f'Revision GE0020 --> {e} - Subject: {subject},  Visit: {visit} ')

                    # Revision PB0010
                    try:
                        date_format = '%d-%b-%Y'
                        date_of_test_f = datetime.strptime(date_sample_collected_pure, date_format)
                        date_of_visit_f = datetime.strptime(date_of_visit, date_format)

                        if date_of_test_f != date_of_visit_f:
                            error = [subject, visit, 'Date of the sample collected', date_sample_collected_form_field_instance ,\
                                     'The date should be the same as the visit date in the "Date of Visit" Form' , f'{date_sample_collected_pure} - {date_of_visit}', 'PB0010']
                            lista_revision.append(error)
                        else:
                            pass

                    except Exception as e:
                        lista_logs.append(f'Revision PB0010--> {e} - Subject: {subject},  Visit: {visit} ')

                    # Revision PB0030
                    try:
                        date_format = '%d-%b-%Y'
                        date_of_test_f = datetime.strptime(date_sample_collected_pure, date_format)
                        date_inform_consent_f = datetime.strptime(date_inform_consent, date_format)

                        if date_of_test_f < date_inform_consent_f:
                            error = [subject, visit, 'Date of the sample collected', date_sample_collected_form_field_instance ,\
                                      'The date/time of sample collected cant be before the informed consent date/time', f'{date_sample_collected_pure} - {date_inform_consent}', 'PB0030']
                            lista_revision.append(error)
                        else:
                            pass
                    except Exception as e:
                        lista_logs.append(f'Revision PB0030--> {e} - Subject: {subject},  Visit: {visit} ')

                    # Revision -> PB0040
                    try:
                        if datetime.strptime(str(date_sample_collected_pure), '%d-%b-%Y') >= datetime.strptime(str(end_study_date), '%d-%b-%Y'):
                            pass
                        else: 
                            error = [subject, visit, 'Date of the sample collected', date_sample_collected_form_field_instance ,\
                                     'Date of the sample collected must be before the End of study/Early withdrawal date. ', date_sample_collected_pure, 'PB0040']
                            lista_revision.append(error)
                    except Exception as e:
                        lista_logs.append(f'Revision PB0040 --> {e} - Subject: {subject},  Visit: {visit}  ')

    excel_writer = load_workbook(path_excel_writer)
    column_names = ['Subject', 'Visit', 'Field', 'Form Field Instance ID' ,'Standard Error Message', 'Value', 'Check Number']
    PBMC_isolate_output = pd.DataFrame(lista_revision, columns=column_names)
    
    sheet = excel_writer.create_sheet("PBMC Isolate")

    for row in dataframe_to_rows(PBMC_isolate_output, index=False, header=True):
        sheet.append(row)

    excel_writer.save(path_excel_writer)
    log_writer(lista_logs)

    return PBMC_isolate_output[['Form Field Instance ID' ,'Standard Error Message']].replace({',': '', ';': ''}, regex=True)

if __name__ == '__main__':
    path_excel = r"C:\Users\sebastian sossa\Documents\integraIT\projects_integrait\DNDI\Program\output\prueba.xlsx"
    df_root = pd.read_excel(r'C:\Users\sebastian sossa\Documents\integraIT\projects_integrait\DNDI\data\newDNDI_v2.xlsx')
    PBMC_isolate(df_root, path_excel ) 