# main.py
from utils.extract import extract_data

def main():
    print("🔍 Memulai proses ETL...")
    extract_data()
    print("✅ Proses ETL selesai dengan sukses!")

if __name__ == "__main__":
    main()
