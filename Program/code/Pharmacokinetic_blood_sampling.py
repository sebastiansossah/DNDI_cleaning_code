import numpy as np
import math
import pandas as pd
from datetime import datetime
from revision_fechas import revision_fecha
import warnings
from log_writer import log_writer
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
warnings.filterwarnings('ignore')

def Pharmacokinetic_blood_sampling(df_root, path_excel_writer):
    '''
    Esta funcion tiene como finalidad la revision de cada uno de los puntos 
    del edit check para el formulario de Pharmacokinetic Blood Sampling (PK)
    '''

    df= df_root[df_root['name']== 'Pharmacokinetic Blood Sampling (PK)']
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

    df_visit_done = df_root[df_root['name']=='Date of visit']
    df_visit_done = df_visit_done[['Visit','Participante', 'Campo', 'Valor', 'FormFieldInstance Id']]
    df_visit_done = df_visit_done[df_visit_done['Campo']=='Was the visit performed?']
    df_visit_done['Valor_completo'] = df_visit_done['Valor'].astype(str) + '|' + df_visit_done['FormFieldInstance Id'].astype(str)
    df_visit_done = df_visit_done[['Visit','Participante','Valor_completo']]
    df_visit_done = df_visit_done.rename(columns={'Participante':'Subject', 'Valor_completo':'was_DV_performed'})

    lista_logs = ['Pharmacokinetic Blood Sampling (PK)']
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
            pru = pru.merge(df_visit_done, on=['Subject', 'Visit'], how='left')

            for index, row in pru.iterrows():
                status = row['status']
                subject = row['Subject']
                visit = row['Visit']

                date_of_visit = row['Date_of_visit']
                date_inform_consent = row['Informed_consent_date']
                end_study_date = row['end_study_date']

                was_DV_performed = row['was_DV_performed']
                was_DV_performed_pure = was_DV_performed.split('|')[0]
                was_DV_performed_form_field_instance = was_DV_performed.split('|')[1]
   
                if status == 'DATA_ENTRY_COMPLETE':
                    try:
                        Was_any_pharmacokinetic_blood_sample_collected = row["Was any pharmacokinetic blood sample collected?"]
                        Was_any_pharmacokinetic_blood_sample_collected_pure = Was_any_pharmacokinetic_blood_sample_collected.split('|')[0]
                        Was_any_pharmacokinetic_blood_sample_collected_form_field_instance = Was_any_pharmacokinetic_blood_sample_collected.split('|')[1]
                    except Exception as e:
                        Was_any_pharmacokinetic_blood_sample_collected_pure = math.nan
                        Was_any_pharmacokinetic_blood_sample_collected_form_field_instance = 'This field doesnt have any data'

                    # try:
                    #     Provide_the_reason = row["Provide the reason"]
                    # except Exception as e:
                    #     pass 

                    try:
                        Date_of_blood_sample_collected = row["Date of blood sample collected"]
                        Date_of_blood_sample_collected_pure = Date_of_blood_sample_collected.split('|')[0]
                        Date_of_blood_sample_collected_form_field_instance = Date_of_blood_sample_collected.split('|')[1]
                    except Exception as e:
                        Date_of_blood_sample_collected_pure = ''
                        Date_of_blood_sample_collected_form_field_instance = 'This field doesnt have any data'

                    # try:
                    #     Pre_dose = row["Pre dose"]
                    # except Exception as e:
                    #     pass 
                    # try:
                    #     Pre_dose_Reason_not_done = row["Pre dose, Reason not done"]
                    # except Exception as e:
                    #     pass 

                    # try:
                    #     min_05_post_dose = row["05-min post dose"]
                    # except Exception as e:
                    #     pass 
                    # try:
                    #     min_05_post_dose_Reason_not_done = row["05-min post dose, Reason not done"]
                    # except Exception as e:
                    #     pass 

                    # try:
                    #     min_10_post_dose = row["10-min post dose"]
                    # except Exception as e:
                    #     pass 

                    # try:
                    #     min_10_post_dose_Reason_not_done = row["10-min post dose, Reason not done"]
                    # except Exception as e:
                    #     pass 
                    # try:
                    #     min_15_post_dose = row["15-min post dose"]
                    # except Exception as e:
                    #     pass 
                    # try:
                    #     min_15_post_dose_Reason_not_done = row["15-min post dose, Reason not done"]
                    # except Exception as e:
                    #     pass 
                    # try:
                    #     min_20_post_dose = row["20-min post dose"]
                    # except Exception as e:
                    #     pass 
                    # try:
                    #     min_20_post_dose_Reason_not_done = row["20-min post dose, Reason not done"]
                    # except Exception as e:
                    #     pass 
                    # try:
                    #     min_25_post_dose = row["25-min post dose"]
                    # except Exception as e:
                    #     pass 
                    # try:
                    #     min_25_post_dose_Reason_not_done = row["25 min post dose, Reason not done"]
                    # except Exception as e:
                    #     pass 
                    # try:
                    #     min_30_post_dose = row["30-min post dose"]
                    # except Exception as e:
                    #     pass 
                    # try:
                    #     min_30_post_dose_Reason_not_done = row["30-min post dose, Reason not done"]
                    # except Exception as e:
                    #     pass 
                    # try:
                    #     min_45_post_dose = row["45-min post dose"]
                    # except Exception as e:
                    #     pass 
                    # try:
                    #     min_45_post_dose_Reason_not_done = row["45-min post dose, Reason not done"]
                    # except Exception as e:
                    #     pass 
                    # try:
                    #     min_60_post_dose = row["60-min post dose"]
                    # except Exception as e:
                    #     pass 
                    # try:
                    #     min_60_post_dose_Reason_not_done = row["60-min post dose, Reason not done"]
                    # except Exception as e:
                    #     pass 
                    # try:
                    #     min_75_post_dose = row["75-min post dose"]
                    # except Exception as e:
                    #     pass 
                    # try:
                    #     min_75_post_dose_Reason_not_done = row["75-min post dose, Reason not done"]
                    # except Exception as e:
                    #     pass 

                    # --------------------------------------------------------------------------------------------------------------
                    # Revision GE0070
                    if float(was_DV_performed_pure) !=  1.0:
                        error = [subject, visit, 'Visit Pages', was_DV_performed_form_field_instance , 'This Form will be disabled because the visit was not done', was_DV_performed_pure, 'GE0070']
                        lista_revision.append(error)

                    try:
                        # Primera  revision general de formato de fecha ->GE0020
                        f = revision_fecha(Date_of_blood_sample_collected_pure)
                        if f == None:
                            pass
                        else:
                            error = [subject, visit, 'Date of blood sample collected', Date_of_blood_sample_collected_form_field_instance,\
                                     f , Date_of_blood_sample_collected_pure, 'GE0020']
                            lista_revision.append(error)     
                    except Exception as e:
                        lista_logs.append(f'Revision GE0020 --> {e} - Subject: {subject},  Visit: {visit} ')

                    # Revision PK0010
                    try:
                        date_format = '%d-%b-%Y'
                        date_of_test_f = datetime.strptime(Date_of_blood_sample_collected_pure, date_format)
                        date_of_visit_f = datetime.strptime(date_of_visit, date_format)

                        if date_of_test_f != date_of_visit_f:
                            error = [subject, visit, 'Date of blood sample collected', Date_of_blood_sample_collected_form_field_instance ,\
                                     'The date should be the same as the visit date in the "Date of Visit" form' , f'{Date_of_blood_sample_collected_pure} - {date_of_visit}', 'PK0010']
                            lista_revision.append(error)
                        else:
                            pass

                    except Exception as e:
                        lista_logs.append(f'Revision PK0010--> {e} - Subject: {subject},  Visit: {visit} ')

                    # Revision PK0030
                    try:
                        date_format = '%d-%b-%Y'
                        date_of_test_f = datetime.strptime(Date_of_blood_sample_collected_pure, date_format)
                        date_inform_consent_f = datetime.strptime(date_inform_consent, date_format)

                        if date_of_test_f < date_inform_consent_f:
                            error = [subject, visit, 'Date of blood sample collected', Date_of_blood_sample_collected_form_field_instance ,\
                                      'The date of sample collected cant be before the informed consent date', f'{Date_of_blood_sample_collected_pure} - {date_inform_consent}', 'PK0030']
                            lista_revision.append(error)
                        else:
                            pass
                    except Exception as e:
                        lista_logs.append(f'Revision PK0030--> {e} - Subject: {subject},  Visit: {visit} ')

                    # Revision -> PK0040
                    try:
                        if datetime.strptime(str(Date_of_blood_sample_collected_pure), '%d-%b-%Y') >= datetime.strptime(str(end_study_date), '%d-%b-%Y'):
                            pass
                        else: 
                            error = [subject, visit, 'Date of blood sample collected', Date_of_blood_sample_collected_form_field_instance,\
                                     'Date of blood sample collected must be before the End of study/Early withdrawal date. ', Date_of_blood_sample_collected_pure, 'PK0040']
                            lista_revision.append(error)
                    except Exception as e:
                        lista_logs.append(f'Revision PK0040 --> {e} - Subject: {subject},  Visit: {visit}  ')


                    lista_validacion = [
                            'Pre dose',
                            '05-min post dose',
                            '10-min post dose',
                            '15-min post dose',
                            '20-min post dose',
                            '25-min post dose',
                            '30-min post dose',
                            '45-min post dose',
                            '60-min post dose',
                            '75-min post dose',
                    ]

                    cuenta_validar = 0

                    for validador_raw in lista_validacion:
                        try: 
                            validador = row[validador_raw].split('|')[0]
                        except:
                            validador = math.nan
       
                        if math.isnan(float(validador)) or float(validador) == 0.0 or validador == '' or validador == '-' or float(validador) == np.nan:
                            pass
                        else:
                            cuenta_validar +=1

                    
                    # Revision PK0050
                    try:
                        if float(Was_any_pharmacokinetic_blood_sample_collected_pure) == 1.0:
                            if cuenta_validar == 0:
                                error = [subject, visit, 'Was blood sample collected?', Was_any_pharmacokinetic_blood_sample_collected_form_field_instance ,\
                                        'If the sample was collected, not all sections can be "not done"', Was_any_pharmacokinetic_blood_sample_collected_pure, 'PK0050']
                                lista_revision.append(error)
                    except Exception as e:
                        lista_logs.append(f'Revision PK0050--> {e} - Subject: {subject},  Visit: {visit} ')
                    

    excel_writer = load_workbook(path_excel_writer)
    column_names = ['Subject', 'Visit', 'Field', 'Form Field Instance ID' ,'Standard Error Message', 'Value', 'Check Number']
    Pharmacokinetic_blood_sampling_output = pd.DataFrame(lista_revision, columns=column_names)
    
    sheet = excel_writer.create_sheet("Pharmacokinetic BS(PK)")

    for row in dataframe_to_rows(Pharmacokinetic_blood_sampling_output, index=False, header=True):
        sheet.append(row)

    excel_writer.save(path_excel_writer)
    log_writer(lista_logs)

    return Pharmacokinetic_blood_sampling_output[['Form Field Instance ID' ,'Standard Error Message']].replace({',': '', ';': ''}, regex=True)

if __name__ == '__main__':
    path_excel = r"C:\Users\sebastian sossa\Documents\integraIT\projects_integrait\DNDI\Program\output\prueba.xlsx"
    df_root = pd.read_excel(r'C:\Users\sebastian sossa\Documents\integraIT\projects_integrait\DNDI\data\newDNDI_v2.xlsx')
    Pharmacokinetic_blood_sampling(df_root, path_excel ) 