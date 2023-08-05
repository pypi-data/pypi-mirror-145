# Ivanov
##=====================
##TL; DR:
### All sh*t in one place!
##=====================

a
##Example:
from ivanov import SASMA
sas = SASMA(user='polibius', password = 'megaboss')
df_from_sas = sas.read_dataset(tablename='table1', libname='MYLIB')
sas.write_dataset(df=df, tablename='table2', libname='MYLIB')
sas.endsas()
