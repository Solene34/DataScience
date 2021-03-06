import pandas as pandas
import re


def split_row(df,col,nameFile):
    stopwords = open(r"visualisation/data/stopwords.txt")
    stop = stopwords.readline()
    stopwords.close()
    print(stop)
    #On met tout en minuscule
    df[col] = df[col].str.lower()

    #Split chaque String de chaque ligne, ce qui va créer des tableaux de string
    #On supprime les lignes étant des stop words ou étant des nombres
    df[col] = df[col].str.split("\ |\:|\!|\?|\-|\"|\(|\)|\[|\]|\<|\>|\@|\&|\/|\,|\=|\.|\#|\n|\t|\'")
    df[col] = df[col].apply(lambda x: [item for item in x if item not in stop and len(item) > 2 and not bool(re.search("[0-9]+", item))])

    #On va l'exploser, donc ajouter pour chaque string dans
    #les listes une nouvelle ligne avec juste un string
    df = df.explode(col)

    #On va mettre 1 pour chaque mot
    df["count"] = 1

    #On regroupe chaque mot, et on additionne leur count
    #On aura donc le nombre d'occurences de chaque mot
    grouped_df = df.groupby([col]).count()

    #On trie par ordre décroissant
    grouped_df = grouped_df.sort_values(by=["count"], ascending=False)
    grouped_df = grouped_df.query('count>=200')
    grouped_df.to_csv(nameFile)
    print(grouped_df)

    #On regarde combien on a de catégories
    print(len(grouped_df))
    print(type(grouped_df))

if __name__ == '__main__':
    df = pandas.read_csv("visualisation/data/formatted_data.csv", low_memory=False, header=0)
    df1 = df[['Subject']].dropna()
    print(df1)
    split_row(df1, 'Subject', "visualisation/data/map_reduced_subject.csv")