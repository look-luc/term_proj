import pandas as pd
from scipy import stats
import numpy as np
from scipy.stats import f

def meansd(data,data_name:str):
    temp = {"type": f"{data_name}", "mean": sum(data) / len(data), "stand dev": np.std(data)}
    return temp

def formants(data_lang,storage:list,data_name:str,vowel:str):
    F1 = [float(d["F1"]) for d in data_lang if d.get("vowel") == vowel]
    F2 = [float(d["F2"]) for d in data_lang if d.get("vowel") == vowel]

    storage.append(meansd(F1, f"{data_name} F1"))
    storage.append(meansd(F2, f"{data_name} F2"))
    return storage

def f_stat(cas,clr,who,lang):
    var_cas = np.var(cas, ddof=1)
    dof_cas = len(cas) - 1
    var_clr = np.var(clr, ddof=1)
    dof_clr = len(clr) - 1
    if who != "Stephan":
        if lang == "en":
            f_statistic = var_clr / var_cas
            p_value = 2 * min(f.cdf(f_statistic, dof_clr, dof_cas), 1 - f.cdf(f_statistic, dof_clr, dof_cas))
        else:
            f_statistic = var_cas / var_clr
            p_value = 2 * min(f.cdf(f_statistic, dof_cas, dof_clr), 1 - f.cdf(f_statistic, dof_cas, dof_clr))
    else:
        if lang == "fr":
            f_statistic = var_clr / var_cas
            p_value = 2 * min(f.cdf(f_statistic, dof_cas, dof_clr), 1 - f.cdf(f_statistic, dof_cas, dof_clr))
        else:
            f_statistic = var_cas / var_clr
            p_value = 2 * min(f.cdf(f_statistic, dof_clr, dof_cas), 1 - f.cdf(f_statistic, dof_clr, dof_cas))
    return f_statistic,p_value

def f_test_equal_variances(data_cas, data_clr, vowel: str, lang: str, who:str, data_name_cas:str,data_name_clr:str,):
    cas_f1 = np.array([float(d["F1"]) for d in data_cas if d["vowel"].strip() == vowel])
    clr_f1 = np.array([float(d["F1"]) for d in data_clr if d["vowel"].strip() == vowel])
    f_f1_statistic, p_f1_value = f_stat(cas_f1, clr_f1, who, lang)

    cas_f2 = np.array([float(d["F2"]) for d in data_cas if d["vowel"].strip() == vowel])
    clr_f2 = np.array([float(d["F2"]) for d in data_clr if d["vowel"].strip() == vowel])
    f_f2_statistic, p_f2_value = f_stat(cas_f2, clr_f2, who, lang)

    temp_stor = [
        {
            "name": f"{data_name_cas} {vowel} and {data_name_clr} {vowel} F1",
            "f-score": round(f_f1_statistic, 3),
            "p-value": round(p_f1_value, 3),
            "p value < 5%": str(p_f1_value < (5 / 100)),
            "DoF": (len(clr_f1)+len(cas_f1)) - 1
        },
        {
            "name": f"{data_name_cas} {vowel} and {data_name_clr} {vowel} F2",
            "f-score": round(f_f2_statistic, 3),
            "p-value": round(p_f2_value, 3),
            "p value < 5%": p_f2_value < (5 / 100),
            "DoF": (len(clr_f2) + len(cas_f2)) - 1
        }
    ]
    return temp_stor

def f_scores(
        data_cas,
        data_clr,
        storage:list,
        vowels:list,
        data_name_cas:str,
        data_name_clr:str,
        lang:str,
        who:str
):
    for vowel in vowels:
        storage.extend(
            f_test_equal_variances(
                data_cas,
                data_clr,
                vowel.strip(),
                lang,
                who,
                data_name_cas,
                data_name_clr
            )
        )
    return storage

def t_test(data_eng: list, data_fr: list, storage: object, data_name_eng: str, data_name_fr: str, who: str):
    temp_stor = {}
    t,p = stats.ttest_ind(data_eng,data_fr)
    temp_stor["name"] = f"{who}: {data_name_eng} and {data_name_fr} f1+f2"
    temp_stor["t test"] = round(t,3)
    temp_stor["p test"] = round(p,3)
    temp_stor["p value < 5%"] = p < (5/100)
    temp_stor["DoF"] = (len(data_eng)+len(data_fr))-1
    storage.append(temp_stor)
    return storage

def main_stat(data, who):
    stat_mean_sd = []
    stat_f_p = []

    engl_cas = [d for d in data if "Engl_casual_speach" in d["filename"]]
    vowel_en_cas = set([d["vowel"].strip() for d in engl_cas])
    engl_cas_stor = []

    engl_clr = [d for d in data if "Engl_clear_speach" in d["filename"]]
    vowel_en_clr = set([d["vowel"].strip() for d in engl_clr])
    engl_clr_stor = []

    fren_cas = [d for d in data if "French_casual_speech" in d["filename"]]
    vowel_fr_cas = set([d["vowel"].strip() for d in fren_cas])
    fren_cas_stor = []
    
    fren_clr = [d for d in data if "French_clear_speech" in d["filename"]]
    vowel_fr_clr = set([d["vowel"].strip() for d in fren_clr])
    fren_clr_stor = []

    engl_V = sorted(set(vowel_en_cas).union(set(vowel_en_clr)))
    fren_V = sorted(set(vowel_fr_cas).union(set(vowel_fr_clr)))
    for v_eng, v_fr in zip(engl_V,fren_V):
        if(who == "Megan"):
            print(v_eng, v_fr)
        engl_cas_stor = formants(engl_cas, engl_cas_stor, f"English casual {str(v_eng).strip()}", str(v_eng).strip())
        engl_clr_stor = formants(engl_clr, engl_clr_stor, f"English clear {str(v_eng).strip()}", str(v_eng).strip())
        fren_cas_stor = formants(fren_cas, fren_cas_stor, f"French Casual {str(v_fr).strip()}", str(v_fr).strip())
        fren_clr_stor = formants(fren_clr, fren_clr_stor, f"French clear {str(v_fr).strip()}", str(v_fr).strip())

    stat_mean_sd.extend(engl_cas_stor)
    stat_mean_sd.extend(engl_clr_stor)
    stat_mean_sd.extend(fren_cas_stor)
    stat_mean_sd.extend(fren_clr_stor)

    engl = []
    fren = []

    eng_cas = [d for d in data if "Engl_casual_speach" in d["filename"]]
    eng_clr = [d for d in data if "Engl_clear_speach" in d["filename"]]

    fre_cas = [d for d in data if "French_casual_speech" in d["filename"]]
    fre_clr = [d for d in data if "French_clear_speech" in d["filename"]]

    eng = [eng_cas,eng_clr]
    fre = [fre_cas,fre_clr]


    engl = f_scores(
        eng[0],
        eng[1],
        engl,
        list(engl_V),
        who + " English casual",
        who + " English clear",
        "en",
        who
    )
    fren = f_scores(
        fre[0],
        fre[1],
        fren,
        list(fren_V),
        who + " French casual",
        who + " French clear",
        "fr",
        who
    )
    stat_f_p.extend(engl)
    stat_f_p.extend(fren)

    eng_cas_f1 = [d["F1"] for d in data if "Engl_casual_speach" in d["filename"]]
    eng_clr_f1 = [d["F1"] for d in data if "Engl_clear_speach" in d["filename"]]

    eng_cas_f2 = [d["F2"] for d in data if "Engl_casual_speach" in d["filename"]]
    eng_clr_f2 = [d["F2"] for d in data if "Engl_clear_speach" in d["filename"]]

    fr_cas_f1 = [d["F1"] for d in data if "French_casual_speech" in d["filename"]]
    fr_clr_f1 = [d["F1"] for d in data if "French_clear_speech" in d["filename"]]

    fr_cas_f2 = [d["F2"] for d in data if "French_casual_speech" in d["filename"]]
    fr_clr_f2 = [d["F2"] for d in data if "French_clear_speech" in d["filename"]]

    eng_diff = []
    fr_diff = []
    for casual, clear in zip(eng_cas_f1,eng_clr_f1):
        eng_diff.append(clear - casual)
    for casual, clear in zip(eng_cas_f2,eng_clr_f2):
        eng_diff.append(clear - casual)
    for casual, clear in zip(fr_cas_f1,fr_clr_f1):
        fr_diff.append(clear - casual)
    for casual, clear in zip(fr_cas_f2,fr_clr_f2):
        fr_diff.append(clear - casual)

    diff_formants = [fr_diff,eng_diff]
    t_test_list = []
    t_test_list = t_test(diff_formants[0],diff_formants[1],t_test_list,"English","French",who)

    t_df = pd.DataFrame(t_test_list)
    t_df.to_csv(who+"_t_test.csv",index=False)
    f_df = pd.DataFrame(stat_f_p)
    f_df.to_csv(who+'_f_test.csv',index=False)
    mean_df = pd.DataFrame(stat_mean_sd)
    mean_df.to_csv(who+'_mean_sd.csv',index=False)
    return 0