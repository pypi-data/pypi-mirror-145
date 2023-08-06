from melaxtool.melaxapi import MelaxClient
import json

if __name__ == '__main__':
    import os

    # copy your key  to set env below
    # os.environ[
    # 'MELAX_TECH_KEY'] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIxIiwidXJsIjoiaHR0cDovL2ludGVybmFsLWs4cy1kZWZhdWx0LXRlc3R3ZWJtLTU0MjRkNWQwYTktMTI1MDk5MDgyMi51cy1lYXN0LTIuZWxiLmFtYXpvbmF3cy5jb20ifQ.rqdwll8ZcpkxrfUvwSK1PePQ7mpqAvT_1zZG63gsWeU"

    os.environ[
        'MELAX_TECH_KEY'] = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIxIiwidXJsIjoiaHR0cHM6Ly9tZXJjdXJ5Lm1lbGF4dGVjaC5jb20ifQ.Nw7SipDks5Q_75xWpU-YT4qfZ-A2LHLb47XNSKnY3i8"

    input1 = """cancer is cancer"""

    input = """
        Progress Note Patient : XXXXX  y.o. MRN# XXXXXXXX Location: XXXXXXX Primary Service: XXXXXXX - Attending: XXXXXXX,* Admit Date: 
    XXXXXXX- Hospital Day: LOS: 7 days Subjective: The patient is unable to communicate due to his severe intellectual impairment, but per nursing, he had no acute events 
    overnight. He continues to gradually improve. He is tolerating continuous TFs well. No fever, shortness of breath, or nausea/vomiting.  Current Medications reviewed: yes 
    Objective: General Appearance: Pleasant, confused CM lying in bed in NAD HEENT: NCAT, EOMI, OC/OP clear Neck: Supple, trachea midline, no JVD or LAD Cardiovascular: RRR, S1/S2 
    heard, no m/r/g; 2+ pulses in BUE and BLE Respiratory: Coarse breath sounds bilaterally with diffuse wheezing, but gradually improving; equal expansion b/l; no increased WOB 
    Abdomen: Soft, non-tender, non-distended; normal BS; PEG tube in place; incision site is clean and dry Neurological: AAOx3; no focal neurological deficits Extremities: No 
    clubbing, cyanosis, or edema Vital signs for last 24 hours: Temp: [97.3 °F (36.3 °C)-98.2 °F (36.8 °C)] 98.1 °F (36.7 °C) Heart Rate: [83-100] 100 Resp: [18] 18 BP: 
    (92-131)/(63-85) 92/63 mmHg Intake/Output last 3 shifts: I/O last 3 completed shifts: In: 2555 [I.V.:1375; Other:100; NG/GT:530; IV Piggyback:550] Out: 300 [Emesis/NG 
    output:300] Results: Lab Results Component Value Date WBC 6.95 XXXXXXX HGB 11.9* XXXXXXX HCT 35.9*  MCV 85.3  PLT 203  Lab Results Component Value 
    Date NA 142  POTASSIUM 3.4*  CL 110*  CO2 28  BUN 7  CREATININE 0.5*  GLUCOSE 139*  CALCIUM 8.2*  PHOS 
    3.7  MG 1.9  Blood cx: NGTD Urine cx: NGTD Sputum cx: mixed upper respiratory flora Assessment: Xxxxxxx is a XXy/o CM w/ a h/o autism, severe intellectual 
    disability, schizoaffective disorder, seizure disorder, and recurrent aspiration pneumonia who presented to the ED with complaints of fever, cough, and shortness of breath. He 
    was admitted to the ICU for aspiration pneumonia and acute respiratory failure and transferred to the floor on XXXXX with his respiratory failure improved. He underwent EGD on 
    xxxx with placement of a PEG tube.  Principal Problem: Aspiration pneumonia Active Problems: Seizure disorder Autism Severe intellectual disability Schizoaffective disorder 
    Swallowing impairment Hypokalemia G tube feedings Plan: Psych/Neuro: Intellectual Disability, Schizoaffective d/o, Seizure d/o: - At baseline - Continue valproate 1000mg IV BID 
    Resp: Hypoxic respiratory failure, aspiration PNA/HCAP ; - Stable on RA, weaned of O2 - Continue vancomycin, increase dose to 1500mg q12h (trough 13.1 on XXXX); continue 
    Primaxin (Day 8) - Blood and urine cx NGTD - Sputum cx: mixed upper respiratory flora - Continue chest PT q4h - Continue respiratory care protocol GI: - Strict NPO - Had swallow 
    study with fibro-optic endoscopic evaluation per Speech: strict NPO - GI placed PEG tube  during EGD - Nutrition is following, see recs below - Patient was started on 
    continuous TFs per Nutrition recs yesterday and is at goal (55mL/hr) - Switch to bolus feeds per Nutrition recs: 330mL Fibersource HN q6h w/ 65mL water flush before and after 
    feeds - Continue pantoprazole for stomach ulcer ppx Renal: Hypokalemia - K 3.4 on XXXX: replaced.  Heme: DVT ppx - Continue heparin The patient will complete his antibiotics 
    today, and he has been transitioned to bolus tube feeds. If he remains stable, he will be ready for discharge tomorrow, but he cannot return to the 
     over the long weekend, so he will likely be discharged Tuesday
    """

    # client = MelaxClient('/Users/lvjian/key.txt')

    client = MelaxClient()
    client.url = "http://127.0.0.1"
    print(client.url)

    #
    # response = client.invoke(input1, "tf-clinical-pipeline-container:v1.0.0")
    # print(response)

    # clinical
    response = client.invoke(input1, "Comprehensive Clinical Information:v1.0")
    response.getAllSentence()

    response = client.visualization(input, "Comprehensive Clinical Information:v1.0")

    # print(len(response.getAllSentence()))

    # print(len(response.getAllSentence()))
