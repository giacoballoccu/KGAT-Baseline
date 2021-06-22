import csv
import random

def create_entity_list():
    header = ["org_id", "remap_id"]
    new_rows = []
    with open("../Data/ml1m/raw/ml1m/kg/e_map.dat", 'r', encoding='latin-1') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            row[0], row[1] = row[1], row[0]
            new_rows.append(row)
    file.close()

    with open("../Data/ml1m/entity_list.txt", 'w+') as file:
        file.write(' '.join(header) + "\n")
        for row in new_rows:
            s = ' '.join(row)
            file.write(s)
            file.write("\n")
    file.close()

def create_item_list():
    header = ["org_id", "remap_id", "freebase_id"]
    new_rows = []
    with open("../Data/ml1m/raw/ml1m/MappingMovielens2DBpedia-1.2.tsv", 'r', encoding='latin-1') as file:
        reader = csv.reader(file, delimiter="\t")
        for row in reader:
            new_rows.append([row[2], 0, row[0]]) #0 acts like a placeholder for the new_id given in the next lines
    file.close()

    new_rows.sort(key=lambda x: int(x[2])) #sort by old id to assign the new one
    with open("../Data/ml1m/item_list.txt", 'w+') as file:
        file.write(' '.join(header) + "\n")
        for new_iid, row in enumerate(new_rows):
            row[1] = str(new_iid)
            s = ' '.join(row)
            file.write(s)
            file.write("\n")
    file.close()

def review_train_test_split():
    uid_review_tuples = {}
    dataset_size = 0
    with open("../Data/ml1m/raw/ml-1m/ratings.dat", 'r', encoding='latin-1') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\n')
        for row in csv_reader:
            row = ''.join(row).strip().split("::")
            if row[0] not in uid_review_tuples:
                uid_review_tuples[row[0]] = []
            uid_review_tuples[row[0]].append((row[0], row[1], row[2], row[3]))
            dataset_size += 1
    csv_file.close()

    for uid, reviews in uid_review_tuples.items():
        reviews.sort(key=lambda x: int(x[3]))

    train = []
    test = []
    for uid, reviews in uid_review_tuples.items(): #python dict are sorted, 1...nuser
        n_elements_test = int(len(reviews)*0.8)
        train.append(reviews[:n_elements_test])
        test.append(reviews[n_elements_test:])

    with open("../Data/ml1m/train.txt", 'w+') as file:
        for uid, rec in enumerate(train): #rec = uid, item, rating, timestamp
            file.write(str(uid+1) + " ")
            s = ' '.join([review_tuple[1] for review_tuple in rec])
            file.writelines(s)
            file.write("\n")
    file.close()

    with open("../Data/ml1m/test.txt", 'w+') as file:
        for uid, rec in enumerate(test):
            file.write(str(uid+1) + " ")
            s = ' '.join([review_tuple[1] for review_tuple in rec])
            file.writelines(s)
            file.write("\n")
    file.close()

def create_kg_final():
    new_rows = []
    with open("../Data/ml1m/raw/ml1m/kg/datasetraw.dat", 'r') as file:
        reader = csv.reader(file, delimiter=" ")
        for row in reader:
            row[1], row[2] = row[2], row[1]
            new_rows.append(row)
    file.close()

    with open("../Data/ml1m/kg_final.txt", 'w+') as file:
        for row in new_rows:
            s = ' '.join(row)
            file.write(s)
            file.write("\n")
    file.close()

def create_user_list():
    header = ["org_id", "remap_id"]
    new_rows = []
    with open("../Data/ml1m/raw/ml-1m/users.dat", 'r') as file:
        reader = csv.reader(file)
        for new_uid, row in enumerate(reader):
            row = row[0].split("::")
            new_rows.append([row[0], str(new_uid)])
    file.close()

    with open("../Data/ml1m/user_list.txt", 'w+') as file:
        file.write(' '.join(header) + "\n")
        for row in new_rows:
            s = ' '.join(row)
            file.write(s)
            file.write("\n")
    file.close()
if __name__ == '__main__':
    #review_train_test_split()
    #create_entity_list()
    #create_item_list()
    create_user_list()
    create_kg_final()
