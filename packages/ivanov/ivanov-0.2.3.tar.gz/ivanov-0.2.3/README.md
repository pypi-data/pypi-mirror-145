# Ivanov
##=====================
### All sh*t in one place!
##===================== 

a
##Example:
sas = SASMA(user='sas', password='pass')
df_from_sas = sas.read_dataset(tablename='AAA', libname='CPC_AD')
print(df_from_sas.head())
sas.write_dataset(df=df_from_sas, libname='WORK', tablename='IVANOV')
sas.endsas()


sas = SASCS(user='srvSASCSPROD_LOAD', password='pass')
df_from_sas = sas.read_dataset(tablename='ENTITY_MASTER', libname='dabt_sub')
print(df_from_sas.head())
sas.write_dataset(df=df_from_sas, libname='WORK', tablename='IVANOV')
sas.endsas()
