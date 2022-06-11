from transformers import AutoTokenizer, AutoModel
from transformers import pipeline
import pandas as pd
import csv

#pipe = pipeline('fill-mask', model = model, tokenizer=tokenizer, topk=10)
pipe = pipeline('fill-mask', model = "dbmdz/electra-base-turkish-mc4-cased-generator", tokenizer="dbmdz/electra-base-turkish-mc4-cased-generator")

df_experiments = pd.read_csv('mecaz_degerlendirme_temiz_son.csv', sep=';')
print(df_experiments.shape)

def decide_metap(score1, score2):
    pred_str1 = ""
    pred_str2 = ""
    if score1 > score2:
        pred_str1 = "real"
        pred_str2 = "metap"
    else:
        pred_str1 = "metap"
        pred_str2 = "real"
    return pred_str1, pred_str2

ALL_CONTENT = []
for index, row in df_experiments.iterrows():
    #if 'MASK' in row["cumle_mecaz_mask"] and 'MASK' in row["cumle_gercek_mask"]:
    print(row["terim_mecaz"], row["cumle_mecaz_mask"], row["cumle_gercek_mask"])
    term_lst = [row["terim_mecaz"]]

    #results = pipe('Kolundaki [MASK] künye, okuduğu kâğıdın üzerine sürtünüyor.', targets= ['altın', 'siyah', 'bir', 'sarı'])
    results = pipe(row["cumle_mecaz_mask"], targets= term_lst)
    #for i in range(len(results)):
    score1 = 0
    score2 = 0

    if len(results) > 1:
        print(f"{results[0][0]['token_str']} -- mecaz score: {results[0][0]['score']}")
        score2 = results[0][0]['score']
    else:
        print(f"{results[0]['token_str']} -- mecaz score: {results[0]['score']}")
        score2 = results[0]['score']


    results_gercek = pipe(row["cumle_gercek_mask"], targets= term_lst)
    print(len(results_gercek))
    print(results_gercek)
    #for i in range(len(results)):
    if len(results_gercek) > 1:
        print(f"{results_gercek[0][0]['token_str']} -- gercek score: {results_gercek[0][0]['score']}")
        score1 = results_gercek[0][0]['score']
    else:
        print(f"{results_gercek[0]['token_str']} -- gercek score: {results_gercek[0]['score']}")
        score1 = results_gercek[0]['score']

    pred_str1, pred_str2 = decide_metap(float(score1), float(score2))
    row = [row["terim_mecaz"], row["tanim_mecaz"], row["cumle_mecaz"], row["cumle_mecaz_mask"], row["tipi_mecaz"], pred_str2, row["terim_gercek"], row["tipi_gercek"], pred_str1, row["tanim_gercek"], row["cumle_gercek"], row["cumle_gercek_mask"]]
    ALL_CONTENT.append(row)


with open("mecaz_degerlendirme_electra_base_turkish_sonuclar.csv", "w", newline="", encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';', quotechar='"')
    headers = ['terim_mecaz','tanim_mecaz','cumle_mecaz','cumle_mecaz_mask','tipi_mecaz','tahmin_mecaz','terim_gercek','tipi_gercek','tahmin_gercek','tanim_gercek','cumle_gercek','cumle_gercek_mask']
    writer.writerow(headers)
    for row in ALL_CONTENT:
        writer.writerow(row)
