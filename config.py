#import lightgbm as lgb
#from sklearn.ensemble import GradientBoostingClassifier
#from sklearn.ensemble import RandomForestClassifier
from catboost import CatBoostClassifier
#from xgboost.sklearn import XGBClassifier




MODEL = 'CatBoostClassifier'
TARGET = 'WNB'

#Cols that are used to idenfity predictions for the flask application.
PREDICT_ID_FLASK = 'UR_NUMBER','OUTPATIENT_NUMBER','CURRENT_BOOKED_DATE'
#The cols the model needed during training. can be extracted from models/ModelFeatures.csv
FLASK_COLS = 'OUTPATIENT_NUMBER','UR_NUMBER','CURRENT_BOOKED_DATE','APPOINTMENT_CODE', 'WNB_RATE', 'ORTH_WNB_RATE', 'OUTCOME_OF_LAST_APPT', 'TFC', 'DESCRIPTION', 'WAITING_LETTER_DATE', 'WAITING_DATE_BOOKING_MADE', 'WAITING_REFERRAL_DATE', 'DAYS_SINCE_LAST_OP_CONTACT', 'DAYS_SINCE_LAST_ORTH_CONTACT', 'ORTH_Att_last_4weeks', 'ORTH_Att_last_12mth', 'ORTH_WNB_last_4weeks', 'ORTH_WNB_last_12weeks', 'ORTH_WNB_last_12mth', 'ORTH_PatCan_last_12mth', 'ORTH_HospCan_last_12weeks', 'ORTH_HospCan_last_12mth', 'OUT_ATT_last_4weeks', 'OUT_ATT_last_12mth', 'OUT_WNB_last_12mth', 'OUT_PatCan_last_4weeks', 'OUT_PatCan_last_12weeks', 'OUT_PatCan_last_12mth', 'OUT_HospCan_last_12mth', 'REFERRAL_SOURCE_BOOKING', 'SLR_SPEC', 'AGE', 'DISTANCE_FROM_APPT', 'LEAD_CARE_PROFESSIONAL', 'APPOINTMENT_TYPE', 'GENDER', 'HOUR_OF_DAY', 'MONTH', 'IMD', 'DAY_OF_WEEK'
#FlaskModelPath
FLASK_MODEL_PATH = 'models/'+MODEL+'.pkl'