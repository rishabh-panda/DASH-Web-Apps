import pandas as pd
import pyodbc

# Import spreadsheet
data = pd.read_excel('datasheet.xlsx')   
df = pd.DataFrame(data)
df = df.fillna(value=0)

# Connect to SQL Server
cnxn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};",
    "SERVER=;",
    "DATABASE=;",
    "Trusted_Connection=yes;",
    "UID=;",
    "PWD=;",
)

cnxn_str = ";".join(cnxn_str)
cnxn = pyodbc.connect(cnxn_str)
cursor = cnxn.cursor()

# Create Table
cursor.execute('''
        CREATE TABLE buyer_input_dash (
            supplier nvarchar(100),
            supplier_id nvarchar(20),
            category nvarchar(30),
            buying_area nvarchar(50),
            RAG_status nvarchar(10),
            multiplication_factor int,
            investment_offered int,
            realisable_investment int,
            COGS int,
            volume int,
            sales int,
            PPA int,
            PPA_percentage float
            )
               ''')

# Insert DataFrame to Table
for row in df.itertuples():
    cursor.execute('''
                INSERT INTO buyer_input_dash (
                                         supplier,
                                         supplier_id,
                                         category,
                                         buying_area,
                                         RAG_status,
                                         multiplication_factor,
                                         investment_offered,
                                         realisable_investment,
                                         COGS,
                                         volume,
                                         sales,
                                         PPA,
                                         PPA_percentage
                                         )
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''',
                row.supplier, 
                row.supplier_id,
                row.category,
                row.buying_area,
                row.RAG_status,
                row.multiplication_factor,
                row.investment_offered,
                row.realisable_investment,
                row.COGS,
                row.volume,
                row.sales,
                row.PPA,
                row.PPA_percentage,
                )
cnxn.commit()
