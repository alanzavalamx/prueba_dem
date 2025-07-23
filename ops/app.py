# app.py
import pandas as pd
from sqlalchemy import create_engine

def main():
    engine = create_engine(
        "mysql+pymysql://PalaceAdmin:Str0ngSecurePAssw0rd@mysql-db:3306/relationships_db"
    )

    df = (
        pd.read_excel("Matriz_de_adyacencia_data_team.xlsx")
        .iloc[1:, 2:]
        .reset_index()
        .rename(columns={"index": "person_a"})
    )

    df = df.melt(id_vars=["person_a"], var_name="person_b", value_name="relationship")
    df = df[df["relationship"] > 0].reset_index(drop=True)
    df["date_created"] = pd.Timestamp.now()

    df.to_sql(
        name="person_relationship",
        con=engine,
        if_exists="append",
        index=False,
    )

    print(f"Table 'person_relationship' updated with {len(df)} records.")

if __name__ == "__main__":
    main()
