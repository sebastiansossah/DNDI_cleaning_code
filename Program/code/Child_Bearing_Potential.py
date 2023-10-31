
from datetime import datetime
from revision_fechas import revision_fecha
from log_writer import log_writer
import warnings
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows

warnings.filterwarnings('ignore')

def child_bearing_potential(df_root, path_excel_writer):
    '''
    Esta funcion tiene como finalidad la revision de cada uno de los puntos 
    del edit check para el formulario de Child Bearing Potential
    '''

    df= df_root[df_root['name']=='Child Bearing Potential']
    lista_sujetos = df['Participante'].unique()
    df = df[['name', 'Visit', 'activityState', 'Participante', 'Estado del Participante', 'Campo', 'Valor', 'FormFieldInstance Id']]
    df['Value_id'] = df['Valor'].astype(str) + '|' + df['FormFieldInstance Id'].astype(str)

    df_visit_date = df_root[df_root['name']=='Date of visit']
    df_visit_date = df_visit_date[['Visit','Participante', 'Campo', 'Valor']]
    df_visit_date = df_visit_date[df_visit_date['Campo']=='Visit Date']
    df_visit_date = df_visit_date[['Visit','Participante','Valor']]
    df_visit_date = df_visit_date.rename(columns={'Participante':'Subject'})

    df_demographic = df_root[df_root['name']=='Demographics']
    df_demographic = df_demographic[['Visit','Participante', 'Campo', 'Valor']]
    df_demographic = df_demographic[df_demographic['Campo']=='Gender']
    df_demographic = df_demographic[['Visit','Participante','Valor']]
    df_demographic = df_demographic.rename(columns={'Participante':'Subject', 'Valor':'Genero'})

    df_demographic_age = df_root[df_root['name']=='Demographics']
    df_demographic_age = df_demographic_age[['Visit','Participante', 'Campo', 'Valor']]
    df_demographic_age = df_demographic_age[df_demographic_age['Campo']=='Birth Year']
    df_demographic_age = df_demographic_age[['Visit','Participante','Valor']]
    df_demographic_age = df_demographic_age.rename(columns={'Participante':'Subject', 'Valor':'Birth_year'})

    lista_revision = []
    lista_logs = ['Child Bearing Potential']


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
            pru = pru.merge(df_demographic, on=['Subject', 'Visit'], how='left')
            pru = pru.merge(df_demographic_age, on=['Subject', 'Visit'], how='left')

            for index, row in pru.iterrows():
                status = row['status']
                if status == 'DATA_ENTRY_COMPLETE':

                    try:
                        subject = row['Subject']
                    except Exception as e:
                        subject = ''

                    try:
                        visit = row['Visit']
                    except Exception as e:
                        visit = ''

                    try:
                        fecha_visita = row['Valor']
                    except Exception as e:
                        fecha_visita = ''

                    try:
                        genero = row['Genero']
                    except Exception as e:
                        genero = ''

                    try:
                        birth_year = row['Birth_year']
                    except Exception as e:
                        birth_year = ''
# --------------------------------------------------------------------------

                    try:
                        date_of_start_condom = row['Date of start of systematic use of condom']
                        date_of_start_condom_pure = date_of_start_condom.split('|')[0]
                        date_of_start_condom_form_field_instance = date_of_start_condom.split('|')[1]
                    except:
                        date_of_start_condom_pure = ''
                        date_of_start_condom_form_field_instance = 'This field doesnt have any data'
                
                    try:
                        date_start_contraceptive = row['Date of start of contraceptive method']
                        date_start_contraceptive_pure = date_start_contraceptive.split('|')[0]
                        date_start_contraceptive_form_field_instance = date_start_contraceptive.split('|')[1]
                    except:
                        date_start_contraceptive_pure = ''
                        date_start_contraceptive_form_field_instance = 'This field doesnt have any data'

                    try:
                        last_mestruation_year = row['Year of Last Menstruation']
                        last_mestruation_year_pure = last_mestruation_year.split('|')[0]
                        last_mestruation_year_form_field_instance = last_mestruation_year.split('|')[1]
                    except:
                        last_mestruation_year_pure = ''
                        last_mestruation_year_form_field_instance = 'This field doesnt have any data'

                    try:
                        participant_postmenopausical = row['Is the participant postmenopausal?']
                        participant_postmenopausical_pure = participant_postmenopausical.split('|')[0]
                        participant_postmenopausical_form_field_instance = participant_postmenopausical.split('|')[1]
                    except:
                        participant_postmenopausical_pure = ''
                        participant_postmenopausical_form_field_instance = 'This field doesnt have any data'

                    try:
                        last_mestruation_month = row['Month of Last Menstruation']
                        last_mestruation_month_pure = last_mestruation_month.split('|')[0]
                        last_mestruation_month_form_field_instance = last_mestruation_month.split('|')[1]
                    except:
                        last_mestruation_month_pure = ''
                        last_mestruation_month_form_field_instance = 'This field doesnt have any data'

                    try:
                        fsh_available = row['Is the FSH test result available and ≥ 40 IU/L?']
                        fsh_available_pure = fsh_available.split('|')[0]
                        fsh_available_form_field_instance = fsh_available.split('|')[1]
                    except:
                        fsh_available_pure = ''
                        fsh_available_form_field_instance = 'This field doesnt have any data'
                    
                    try:
                        contraception = row['Contraception of non post-menopausal woman']
                        contraception_pure = contraception.split('|')[0]
                        contraception_form_field_instance = contraception.split('|')[1]
                    except:
                        contraception_pure = ''
                        contraception_form_field_instance = 'This field doesnt have any data'

                    try:
                        use_combined_hormonal = row['Use of combined (estrogen and progestogen-containing) hormonal contraception. associated with inhibition of ovulation']
                        use_combined_hormonal_pure = use_combined_hormonal.split('|')[0]
                        use_combined_hormonal_form_field_instance = use_combined_hormonal.split('|')[1]
                    except:
                        use_combined_hormonal_pure = ''
                        use_combined_hormonal_form_field_instance = 'This field doesnt have any data'
                    
                    try:
                        progeston_hormonal = row['Use of progestogen-only hormonal contraception']
                        progeston_hormonal_pure = progeston_hormonal.split('|')[0]
                        progeston_hormonal_form_field_instance = progeston_hormonal.split('|')[1]
                    except:
                        progeston_hormonal_pure = ''
                        progeston_hormonal_form_field_instance = 'This field doesnt have any data'

                    # ----------------------------------------------


                    # Revision para CB0010
                    if float(genero) == 1.0:
                        try:
                            
                            if str(participant_postmenopausical_pure) != '' or  participant_postmenopausical_pure != float('nan') or str(participant_postmenopausical_pure) != 'N/A':
                                error = [subject, visit, 'Form Child Bearing Potential', participant_postmenopausical_form_field_instance ,'If Subjects Gender is "Male" in DEMOGRAPHIC, form should be left empty' , \
                                         participant_postmenopausical_pure, 'CB0010']
                                lista_revision.append(error)
                        except Exception as e:
                            pass
                      
                        try:
                            if str(last_mestruation_month_pure) != '' or  last_mestruation_month_pure != float('nan') or str(last_mestruation_month_pure) != 'N/A':
                                error = [subject, visit, 'Form Child Bearing Potential', last_mestruation_month_form_field_instance,  \
                                         'If Subjects Gender is "Male" in DEMOGRAPHIC, form should be left empty' , last_mestruation_month_pure, 'CB0010']
                                lista_revision.append(error)
                        except Exception as e:
                            pass

                        try:
                            if str(last_mestruation_year_pure) != '' or  last_mestruation_year_pure != float('nan') or str(last_mestruation_year_pure) != 'N/A':
                                error = [subject, visit,'Form Child Bearing Potential', last_mestruation_year_form_field_instance, \
                                         'If Subjects Gender is "Male" in DEMOGRAPHIC, form should be left empty' , last_mestruation_year_pure, 'CB0010']
                                lista_revision.append(error)
                        except Exception as e:
                            pass

                        try:
                            if str(fsh_available_pure) != '' or  fsh_available_pure != float('nan') or str(fsh_available_pure) != 'N/A':
                                error = [subject, visit,'Form Child Bearing Potential', fsh_available_form_field_instance, \
                                         'If Subjects Gender is "Male" in DEMOGRAPHIC, form should be left empty' , fsh_available_pure, 'CB0010']
                                lista_revision.append(error)
                        except Exception as e:
                            pass

                        try:
                            if str(contraception_pure) != '' or  contraception_pure != float('nan') or str(contraception_pure) != 'N/A':
                                error = [subject, visit, 'Form Child Bearing Potential', contraception_form_field_instance, \
                                         'If Subjects Gender is "Male" in DEMOGRAPHIC, form should be left empty', contraception_pure, 'CB0010']
                                lista_revision.append(error)
                        except Exception as e: 
                            pass

                        try:
                            if str(use_combined_hormonal_pure) != '' or  use_combined_hormonal_pure != float('nan') or str(use_combined_hormonal_pure) != 'N/A':
                                error = [subject, visit, 'Form Child Bearing Potential', use_combined_hormonal_form_field_instance, \
                                         'If Subjects Gender is "Male" in DEMOGRAPHIC, form should be left empty' , use_combined_hormonal_pure, 'CB0010']
                                lista_revision.append(error)
                        except Exception as e:
                            pass

                        try:
                            if str(progeston_hormonal_pure) != '' or  progeston_hormonal_pure != float('nan') or str(progeston_hormonal_pure) != 'N/A':
                                error = [subject, visit,'Form Child Bearing Potential', progeston_hormonal_form_field_instance ,\
                                         'If Subjects Gender is "Male" in DEMOGRAPHIC, form should be left empty' , progeston_hormonal_pure, 'CB0010']
                                lista_revision.append(error)
                        except Exception as e:
                            pass

                        try:
                            if str(date_start_contraceptive_pure) != '' or  date_start_contraceptive_pure != float('nan') or str(date_start_contraceptive_pure) != 'N/A':
                                error = [subject, visit,'Form Child Bearing Potential', date_start_contraceptive_form_field_instance ,\
                                         'If Subjects Gender is "Male" in DEMOGRAPHIC, form should be left empty' , date_start_contraceptive_pure, 'CB0010']
                                lista_revision.append(error)
                        except Exception as e:
                            pass

                        try:
                            if str(date_of_start_condom_pure) != '' or  date_of_start_condom_pure != float('nan') or str(date_of_start_condom_pure) != 'N/A':
                                error = [subject, visit, 'Form Child Bearing Potential', date_of_start_condom_form_field_instance, \
                                         'If Subjects Gender is "Male" in DEMOGRAPHIC, form should be left empty' , date_of_start_condom_pure, 'CB0010']
                                lista_revision.append(error)
                        except Exception as e:
                            pass    
                    else:
# --------------------------------------------- Revision de edit check-----------------------------------------------------------


                        # Revision para ->GE0020
                        try:
                            f = revision_fecha(date_of_start_condom_pure)
                            if f == None:
                                pass
                            else:
                                error = [subject, visit, 'Date of start of systematic use of condom', date_of_start_condom_form_field_instance ,f , date_of_start_condom_pure, 'GE0020']
                                lista_revision.append(error) 
                        except Exception as e:
                            lista_logs.append(f'Revision GE0020 --> {e}')
                        
                        # Revision para->GE0020
                        try:
                            f = revision_fecha(date_start_contraceptive_pure)
                            if f == None:
                                pass
                            else:
                                error = [subject, visit, 'Date of start of contraceptive method', date_start_contraceptive_form_field_instance ,f , date_start_contraceptive_pure, 'GE0020']
                                lista_revision.append(error) 
                        except Exception as e:
                            lista_logs.append(f'Revision GE0020 --> {e}')
                        
                        # Revision para CB0020
                        try:        
                            vist_date_year =  fecha_visita.split('-')[2]
                            amount_years = int(vist_date_year) - int(last_mestruation_year_pure)
                            if amount_years >= 1:
                                pass
                            else:
                                error = [subject, visit, 'Year of Last Menstruation', last_mestruation_year_form_field_instance,\
                                         'There should be more than a year difference between the visit date and the year of last menstruation' , last_mestruation_year_pure, 'CB0020']
                                lista_revision.append(error)
                        except Exception as e:
                            lista_logs.append(f'Revision CB0020 --> {e}')

                        # Revision para CB0030
                        try:                        
                            if int(last_mestruation_year_pure) <= 1968 or int(last_mestruation_year_pure) >= 2024:
                                pass
                            else:
                                error = [subject, visit, 'Year of Last Menstruation' , last_mestruation_year_form_field_instance ,'The year should be after 1968 and before 2024',\
                                          last_mestruation_year_pure, 'CB0030']
                                lista_revision.append(error)
                        except Exception as e:
                            lista_logs.append(f'Revision CB0030 --> {e}')

                        try:
                            # Revision para CB0140
                            if int(birth_year) < int(date_start_contraceptive_pure.split('-')[2]):
                                pass
                            else:
                                error = [subject, visit, 'Date of start of contraceptive method', date_start_contraceptive_form_field_instance, \
                                         'The contraceptive method date cant be before the birth date' , date_start_contraceptive_pure, 'CB0140']
                                lista_revision.append(error)
                        except Exception as e:
                            lista_logs.append(f'Revision CB0140 --> {e}')

                        # if float(contraception_pure) == 1.0:



    excel_writer = load_workbook(path_excel_writer)
    column_names =  ['Subject', 'Visit', 'Field', 'Form Field Instance ID' ,'Standard Error Message', 'Value', 'Check Number']
    child_bearing_potential_output = pd.DataFrame(lista_revision, columns=column_names)
 
    sheet = excel_writer.create_sheet("Child Bearing Potential")

    for row in dataframe_to_rows(child_bearing_potential_output, index=False, header=True):
        sheet.append(row)

    excel_writer.save(path_excel_writer)
    log_writer(lista_logs)

    return child_bearing_potential_output[['Form Field Instance ID' ,'Standard Error Message']].replace({',': '', ';': ''}, regex=True)

if __name__ == '__main__':
    path_excel = r"C:\Users\sebastian sossa\Documents\integraIT\projects_integrait\DNDI\Program\output\prueba.xlsx"
    df_root = pd.read_excel(r"C:\Users\sebastian sossa\Documents\integraIT\projects_integrait\DNDI\data\newDNDI.xlsx")
    child_bearing_potential(df_root, path_excel ) 