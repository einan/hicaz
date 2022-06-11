import os
import csv


fi_lst = os.listdir("csv/")
print(len(fi_lst))

ALL_CONTENT = []
cnt = 1
for fi in fi_lst:
    with open('csv/'+fi, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            # ['zümrüt', 'Bu renkte olan', 'gerçek', 'Zümrüt çayırlar.']
            term = row[0]
            defini = row[1]
            type = row[2]
            txt = row[3].lower()
            if type in 'mecaz':
                #if len(txt) > 40:
                f_in = open('csv/'+fi, newline='', encoding='utf-8')
                reader_in = csv.reader(f_in)
                for row_in in reader_in:
                    #print(f"{fi} -- {f_in}")
                    if row_in[0] == term and row_in[2] == 'gerçek':
                        print(f"ter: {term} - type: {type} - defini: {defini} - txt: {txt}")
                        txt_tmp = txt.replace(term, "[MASK]")
                        print(txt_tmp)
                        print(f"ter: {row_in[0]} - type: {row_in[2]} - defini: {row_in[1]} - txt: {row_in[3]}")
                        txt_real_tmp = row_in[3].lower().replace(term, "[MASK]")
                        print(txt_real_tmp)
                        row = [fi, term, type, defini, txt, txt_tmp, fi, row_in[0], row_in[2], row_in[1], row_in[3], txt_real_tmp]
                        ALL_CONTENT.append(row)
                        print(40 * "*")
                        cnt += 1
                        break
print(cnt)


with open("mecaz_degerlendirme.csv", "w", newline="", encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';', quotechar='"')
    headers = ['fi','terim_mecaz','tipi_mecaz','tanim_mecaz','cumle_mecaz','cumle_mecaz_mask','fi','terim_gercek','tipi_gercek','tanim_gercek','cumle_gercek','cumle_gercek_mask']
    writer.writerow(headers)
    for row in ALL_CONTENT:
        writer.writerow(row)



import matplotlib.pyplot as plt
import pandas as pd

df_experiments = pd.read_csv('mecaz_degerlendirme.csv', sep=';')
print(df_experiments.shape)
df_experiments.drop_duplicates(keep=False,inplace=True)
print(df_experiments.shape)
ALL_CONTENT = []
cnt = 1
for ind, row in df_experiments.iterrows():
    if 'MASK' in row["cumle_mecaz_mask"] and 'MASK' in row["cumle_gercek_mask"]:
        print(ind, row["terim_mecaz"], row["cumle_mecaz_mask"], row["cumle_gercek_mask"])
        ALL_CONTENT.append(row)
        cnt += 1
print(cnt)

with open("mecaz_degerlendirme_son.csv", "w", newline="", encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, delimiter=';', quotechar='"')
    headers = ['fi','terim_mecaz','tipi_mecaz','tanim_mecaz','cumle_mecaz','cumle_mecaz_mask','fi','terim_gercek','tipi_gercek','tanim_gercek','cumle_gercek','cumle_gercek_mask']
    writer.writerow(headers)
    for row in ALL_CONTENT:
        writer.writerow(row)
