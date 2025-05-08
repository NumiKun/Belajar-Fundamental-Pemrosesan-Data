from sqlalchemy import text, create_engine, select, Table, MetaData, update, delete
 
DATABASE_URL = 'postgresql+psycopg2://surya:surya2003@localhost:5432/companydb'
engine = create_engine(DATABASE_URL)
 
metadata= MetaData()
 
user_table = Table(
    "users",
    metadata,
    autoload_with=engine
)
 
with engine.connect() as connection:
    try:
        # select_statement = text("SELECT * FROM users;") # Gunakan ini jika ingin menggunakan text()
        select_statement = select(user_table)
        result = connection.execute(select_statement)
 
        for row in result:
            print(row)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")