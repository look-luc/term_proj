import matplotlib.pyplot as plt
from matplotlib.transforms import Affine2D

def scatter_plot(data1x,data1y,data2x,data2y,title,data1_leg,data2_leg,save_title):
    plt.figure(figsize=(8, 7))
    rotation_degrees=90

    ax = plt.gca()

    plt.scatter(data1y,data1x,c="blue",marker="x",label=data1_leg)
    plt.scatter(data2y,data2x,c="red",marker="o",label=data2_leg)

    ax.invert_xaxis()
    ax.invert_yaxis()

    ax.xaxis.tick_top()
    ax.xaxis.set_label_position('top')

    ax.yaxis.tick_right()
    ax.yaxis.set_label_position('right')

    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    ax.spines['top'].set_visible(True)
    ax.spines['left'].set_visible(True)

    plt.xlabel("F2")
    plt.ylabel("F1")
    plt.title(f"{title} (Casual vs Clear)")
    plt.legend()
    plt.savefig(f"{save_title}.png")

def main_plot(
        data,
        title_eng:str,
        title_fr:str,
        title_combine_freclr:str,
        title_combine_engclr:str,
        data1_leg:str,
        data2_leg:str,
        save_title_eng:str,
        save_title_fr:str,
        save_title_frengcas_freclear:str,
        save_title_frengcas_engclear:str,
):
    engl_cas_F1 = [d["F1"] for d in data if "Engl_casual_speach" in d["filename"]]
    engl_cas_F2 = [d["F2"] for d in data if "Engl_casual_speach" in d["filename"]]

    engl_clr_F1 = [d["F1"] for d in data if "Engl_clear_speach" in d["filename"]]
    engl_clr_F2 = [d["F2"] for d in data if "Engl_clear_speach" in d["filename"]]

    scatter_plot(
        engl_cas_F1,
        engl_cas_F2,
        engl_clr_F1,
        engl_clr_F2,
        title=title_eng,
        data1_leg="eng "+data1_leg,
        data2_leg="eng "+data2_leg,
        save_title=save_title_eng
    )

    fr_cas_F1 = [d["F1"] for d in data if "French_casual_speech" in d["filename"]]
    fr_cas_F2 = [d["F2"] for d in data if "French_casual_speech" in d["filename"]]

    fr_clr_F1 = [d["F1"] for d in data if "French_clear_speech" in d["filename"]]
    fr_clr_F2 = [d["F2"] for d in data if "French_clear_speech" in d["filename"]]

    scatter_plot(
        fr_cas_F1,
        fr_cas_F2,
        fr_clr_F1,
        fr_clr_F2,
        title=title_fr,
        data1_leg="French "+data1_leg,
        data2_leg="French "+data2_leg,
        save_title=save_title_fr
    )

    scatter_plot(
        fr_cas_F1+engl_cas_F1,
        fr_cas_F2+engl_cas_F2,
        fr_clr_F1,
        fr_clr_F2,
        title=title_combine_freclr,
        data1_leg="Casual vowels (eng + fre)",
        data2_leg="French clear vowels",
        save_title=save_title_frengcas_freclear
    )

    scatter_plot(
        fr_cas_F1+engl_cas_F1,
        fr_cas_F2+engl_cas_F2,
        engl_clr_F1,
        engl_clr_F2,
        title=title_combine_engclr,
        data1_leg="Casual vowels (eng + fre)",
        data2_leg="English clear vowels",
        save_title=save_title_frengcas_engclear
    )
    return 0