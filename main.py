import pandas as pd
import stat_calculation
import plot

def getdata(filepath: str) -> list[dict]:
    if filepath == "":
        return []
    else:
        df = pd.read_csv(filepath, encoding='latin-1')
        values = df.to_dict(orient='records')
        for d in values:
            if "ï»¿filename" in d:
                d["filename"] = d.pop("ï»¿filename")
        return values

def main():
    luc_data = getdata("./Luc data/data.csv")
    stat_calculation.main_stat(
        luc_data,
        "Luc"
    )
    plot.main_plot(
        luc_data,
        "Luc english",
        "Luc french",
        "Luc french & english vs French",
        "Luc french & english vs English",
        "casual",
        "clear",
        "luc_english",
        "luc_french",
        "Luc_fre_eng_cas_fre_clr",
        "Luc_fre_eng_cas_eng_clr",
    )

    father_data = getdata("./Father data/data.csv")
    stat_calculation.main_stat(
        father_data,
        "Stephan"
    )
    plot.main_plot(
        father_data,
        "Stephan english",
        "Stephan french",
        "Stephan French & English vs French",
        "Stephan french & english vs English",
        "casual",
        "clear",
        "Stephan_english",
        "Stephan_french",
        "Stephan_fre_eng_cas_fre_clr",
        "Stephan_fre_eng_cas_eng_clr",
    )

    megan_data = getdata("./Megan data/data.csv")
    stat_calculation.main_stat(megan_data,"Megan")
    plot.main_plot(
        megan_data,
        "Megan english",
        "Megan french",
        "Megan French & English vs French",
        "Megan french & english vs English",
        "casual",
        "clear",
        "Megan_english",
        "Megan_french",
        "Megan_fre_eng_cas_fre_clr",
        "Megan_fre_eng_cas_eng_clr",
    )
    return 0

if __name__ == "__main__":
    main()