import pandas as pd


def read_files_as_string(xlsx_file, csv_file):
    # Read xlsx file into a pandas DataFrame
    df_xlsx = pd.read_excel(xlsx_file, dtype=str)

    # Read csv file into a pandas DataFrame
    df_csv = pd.read_csv(csv_file, dtype=str, on_bad_lines='skip')    
    
    return df_xlsx, df_csv

def check_oids(df_xlsx, df_csv):
    
    OIDs = df_csv.loc[:, 'OID']
    print(OIDs)
    ids_present = 0
    for index, row in df_xlsx.iterrows():
        oid = row['OID']
        if (df_csv['OID'].eq(oid)).any():
            ids_present += 1
        else:
            print( oid)
    print(ids_present)
    
def check_values(df_xlsx, df_csv):
    for index, row in df_xlsx.iterrows():
        val = row['ICE1LDV Innenanzeiger']
        if (df_csv['OID'].eq(val)).any():
            ids_present += 1
        else:
            print(df_csv.loc[index,:])
                
    


if __name__ == "__main__":
    xlsx_file_path = "SNMP_OIDs_Innenanzeiger.xlsx"
    csv_file_path = "ICE-L_AA_SNMP_Output_172.17.44.97_2023-08-02_10.04.09.csv"
    
    df_xlsx, df_csv = read_files_as_string(xlsx_file_path, csv_file_path)
    
    check_oids(df_xlsx, df_csv)
    check_values(df_xlsx, df_csv)
