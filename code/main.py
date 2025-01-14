import data_processing as dp

# get annotations data
annotations = dp.get_annotations()

# .pcapng files list
capture_files = []
for value in annotations:
    capture_files.append(value[0])

# Combines P1 and P2 data from all the .pcapng files. Each member is a Player object
Player_Data = []
# parse capture files
for capture_file in capture_files:
    print(f"Processing {capture_file}")
    Player_Data.append(dp.parse_capture_file(capture_file)) # From a single .pcapng file, append both Player1 and Player2 data To a list
    print(f"{capture_file} is done")
#     # aici faci vectorul mare de trasaturi care va fi trimis catre model. la vectoru asta contribuie fiecare capture file

# X - matricea ce contine datele
# Y - matricea ce contine addnotarile (label-urile) - clasele
# OUT - matricea ce contine ceea ce a prezis modelul
#X_train, Y_train - pentru antrenare
# X_val, Y_val - pentru validare
# OUT_train OUT_val - ceea ce a prezis modelul boss, pentru antrenare si validare


# dataset = capture_files
# random.seed()
# random.shuffle(dataset)

# 80 / 20 dataset split
# train_idx = round(len(dataset) * 0.8)
# dataset_train = dataset[0:train_idx]
# dataset_val = dataset[train_idx:]

# DIN PACHETE TREBUIE SA EXTRAGI TRASATURI BOSS
# TRE SA VEZI MAI INTAI CARE SUNT TRASATURILE SI APOI CUM LE EXTRAGI DIN TRAFIC
# AI DE PLM AGAIN