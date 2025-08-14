import pandas as pd
from sqlalchemy import create_engine, text

from utilities.database_uri import get_database_uri


def setup_drive_database():
    engine = create_engine(get_database_uri())

    for cat in ("academic_calendar", "important_files", "staff_list", "term_overview", "timetable"):
        with engine.connect() as conn:
            if cat == "important_files":
                df_dict = {"grade": ["KG", "EL", "JH", "SH", "ALL"], "url": [None, None, None, None, None]}
            elif cat == "staff_list":
                df_dict = {"grade": ["ALL"], "url": [None]}
            else:
                df_dict = {"grade": ["KG", "EL", "JH", "SH"], "url": [None, None, None, None]}
            df = pd.DataFrame(df_dict)
            
            table_exists = engine.dialect.has_table(conn, cat)
            if table_exists:
                row_count = conn.execute(text(f"SELECT COUNT(*) FROM {cat}")).scalar()
                if row_count > 0:
                    print(f"Table '{cat}' already has data! Aborting.")
                    continue

            # If table hasn't existed, or table has zero rows
            success_rows = df.to_sql(cat, con=engine, if_exists="append", index=False)
            if success_rows and success_rows > 0:
                print('setup_drive_database() SUCCESS')


def run_drive_data_pipeline():
    setup_drive_database()


if __name__ == "__main__":
    run_drive_data_pipeline()
