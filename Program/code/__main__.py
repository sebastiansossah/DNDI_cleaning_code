import pandas as pd
import os
from datetime import datetime

# Importing forms from screening visit--------------------------------------------------------------------------------
from Date_of_visit import date_of_visit
from Informed_Consent import informed_consent_revision
from Demographics import demographic
from Child_Bearing_Potential import child_bearing_potential
from History_of_cutaneous_leishmaniasis import history_of_cutaneous_leishmaniasis
from Eligibility import eligibility
from Medical_Or_Surgical_History import Medical_or_surgical_history
from Vein_assessment import vein_assesment
from Urinary_Drug_Screen import urinary_drug_screen
from Pregnancy_Test import pregnancy_test 
from Clinical_Laboratory_Test_Hematology import clinical_laboratory_test_hematology
from Clinical_Laboratory_Test_Clinical_Chemistry import clinical_laboratory_test_clinical_chemistry
from Clinical_Laboratory_Test_Coagulation import clinical_laboratory_test_coagulation
from Immunoassay import immunoassay
from Urinalysis import urinalysis
from Urine_Microscopic_Examination import urine_microscopic_examination
from Virology import virology
from Lesion_Measurement import lesion_measurement
from Physical_Examination import physical_examination
from Vital_Signs import vital_signs
from Lead_ECG import lead_ECG

# Importing forms from D-1 ---------------------------------------------------------------------------------------
from Covid_19_testing import covid_19_testing
from Alcohol_screen import alcohol_screen
from Clinical_Laboratory_Test_Clinical_Chemistry_D_1 import clinical_laboratory_test_clinical_chemistry_D_1
from Interleukin_6 import interleukin_6
from Titration_Of_Auto_Antibodies import titration_of_auto_antibodies

# Importing forms from D1 ---------------------------------------------------------------------------------------
from Injection_Site_Examination import injection_site_examination
from PBMC_isolate import PBMC_isolate
from Pharmacokinetic_blood_sampling import Pharmacokinetic_blood_sampling
from pharmacodynamic_blood_sampling import pharmacodynamic_blood_sampling
from mRNA_Markers import mRNA_markers

# importing forms from unscheduled --------------------------------------------------------------------------------
from Administration_CpG_ODN import adminsitration_CpG_ODN
from Miltefosine_administration import miltefosine_administration
from Prior_concomitant_medications import prior_concomitant_medication
from Prior_concomitant_procedures import prior_concomitant_procedures
from Events_Medication_procedure_study_treatment import ev_med_proce_treatment
from end_of_study import end_of_study
from Adverse_events import adverse_events

###########################################################################################################
#---------------------------------------------------------------------------------------------------------#


if __name__ == '__main__':

    script_directory = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
    relative_folder_path = "data"
    folder_path = os.path.join(script_directory.replace('\code', ''), relative_folder_path)
    file = os.listdir(folder_path)
    path = f"{folder_path}\{file[0]}"
    current_date = datetime.now().strftime("%Y%m%d")
    
    df_root = pd.read_excel(path)
    df_root.rename(columns = {'Instancia':'FormFieldInstance Id'}, inplace = True)
    df_root = df_root[(df_root['activityState']== 'DATA_VERIFIED') | (df_root['activityState']== 'DATA_ENTRY_COMPLETE')]
    df_root = df_root[(df_root['QueryState']!= 'OPEN')]
    df_root = df_root[(df_root['TypeQuery']!= 'QUERY')]
    print(df_root.shape)
    path_excel_writer = r"C:\Users\sebastian sossa\Documents\integraIT\projects_integrait\DNDI\Program\output\DNDi_cleaning_yyyymmdd.xlsx".replace('yyyymmdd', current_date)
    log_file = r"C:\Users\sebastian sossa\Documents\integraIT\projects_integrait\DNDI\Program\output\DNDi_log_yyyymmdd.txt".replace('yyyymmdd', current_date)
    
    df_csv_final_output  = pd.DataFrame()
    df_excel_initializer = pd.DataFrame()
    
    excel_file_path_initializer = f"{script_directory.replace('code', '')}output\DNDi_cleaning_{current_date}.xlsx"
    df_excel_initializer.to_excel(excel_file_path_initializer, index=False)


    with open(f"{script_directory.replace('code', '')}output\DNDi_log_{current_date}.txt", 'w') as file:
        file.write("")

    # --------------------- Screening visit --------------------------------------38

    date_of_visit = date_of_visit(df_root, path_excel_writer)
    informed_consent_revision= informed_consent_revision(df_root, path_excel_writer)
    demographic = demographic(df_root, path_excel_writer)
    child_bearing_potential = child_bearing_potential(df_root, path_excel_writer)
    history_of_cutaneous_leishmaniasis = history_of_cutaneous_leishmaniasis(df_root, path_excel_writer)
    eligibility = eligibility(df_root, path_excel_writer)
    Medical_or_surgical_history = Medical_or_surgical_history(df_root, path_excel_writer)
    vein_assesment = vein_assesment(df_root, path_excel_writer)
    urinary_drug_screen = urinary_drug_screen(df_root, path_excel_writer)
    pregnancy_test = pregnancy_test(df_root, path_excel_writer)
    clinical_laboratory_test_hematology = clinical_laboratory_test_hematology(df_root, path_excel_writer)
    clinical_laboratory_test_clinical_chemistry = clinical_laboratory_test_clinical_chemistry(df_root, path_excel_writer)
    clinical_laboratory_test_coagulation = clinical_laboratory_test_coagulation(df_root, path_excel_writer)
    immunoassay = immunoassay(df_root, path_excel_writer)
    urinalysis = urinalysis(df_root, path_excel_writer)
    urine_microscopic_examination = urine_microscopic_examination(df_root, path_excel_writer)
    virology = virology(df_root, path_excel_writer)
    lesion_measurement = lesion_measurement(df_root, path_excel_writer)
    physical_examination = physical_examination(df_root, path_excel_writer)
    vital_signs = vital_signs(df_root, path_excel_writer)
    lead_ECG = lead_ECG(df_root, path_excel_writer)

    # --------------------- D-1 --------------------------------------
    covid_19_testing = covid_19_testing(df_root, path_excel_writer)
    alcohol_screen = alcohol_screen(df_root, path_excel_writer)
    clinical_laboratory_test_clinical_chemistry_D_1 = clinical_laboratory_test_clinical_chemistry_D_1(df_root, path_excel_writer)
    interleukin_6 = interleukin_6(df_root, path_excel_writer)
    titration_of_auto_antibodies = titration_of_auto_antibodies(df_root, path_excel_writer)

    # --------------------- D1 --------------------------------------
    injection_site_examination = injection_site_examination(df_root, path_excel_writer)
    PBMC_isolate = PBMC_isolate(df_root, path_excel_writer)
    Pharmacokinetic_blood_sampling = Pharmacokinetic_blood_sampling(df_root, path_excel_writer)
    pharmacodynamic_blood_sampling = pharmacodynamic_blood_sampling(df_root, path_excel_writer)
    mRNA_markers = mRNA_markers(df_root, path_excel_writer)

    # --------------------- unscheduled --------------------------------------
    adminsitration_CpG_ODN = adminsitration_CpG_ODN(df_root, path_excel_writer)
    miltefosine_administration = miltefosine_administration(df_root, path_excel_writer)
    prior_concomitant_medication = prior_concomitant_medication(df_root, path_excel_writer)
    prior_concomitant_procedures = prior_concomitant_procedures(df_root, path_excel_writer)
    ev_med_proce_treatment = ev_med_proce_treatment(df_root, path_excel_writer)
    end_of_study = end_of_study(df_root, path_excel_writer)
    adverse_events = adverse_events(df_root, path_excel_writer)

#-------------------------------------------------------------------------------------------


list_variables_union = [date_of_visit,
informed_consent_revision,
demographic,
child_bearing_potential,
history_of_cutaneous_leishmaniasis,
eligibility,
Medical_or_surgical_history,
vein_assesment,
urinary_drug_screen,
pregnancy_test ,
clinical_laboratory_test_hematology,
clinical_laboratory_test_clinical_chemistry,
clinical_laboratory_test_coagulation,
immunoassay,
urinalysis,
urine_microscopic_examination,
virology,
lesion_measurement,
physical_examination,
vital_signs,
lead_ECG,
covid_19_testing,
alcohol_screen,
clinical_laboratory_test_clinical_chemistry_D_1,
interleukin_6,
titration_of_auto_antibodies,
injection_site_examination,
PBMC_isolate,
Pharmacokinetic_blood_sampling,
pharmacodynamic_blood_sampling,
mRNA_markers,
adminsitration_CpG_ODN,
miltefosine_administration,
prior_concomitant_medication,
prior_concomitant_procedures,
ev_med_proce_treatment,
end_of_study,
adverse_events]

for variable in list_variables_union:

    df_csv_final_output = pd.concat([df_csv_final_output, variable], ignore_index=True)

df_csv_final_output = df_csv_final_output.rename(columns={'Form Field Instance ID': 'FormFieldInstance_id', 'Standard Error Message': 'comment'})
df_csv_final_output = df_csv_final_output.replace({'"': ''}, regex=True)
df_csv_final_output = df_csv_final_output.reset_index().rename(columns={'index': 'id'})

df_csv_final_output.to_csv(r'C:\Users\sebastian sossa\Documents\integraIT\projects_integrait\DNDI\Program\output\DNDi_querys_yyyymmdd.csv'.replace('yyyymmdd', current_date), index=False, sep=';')

