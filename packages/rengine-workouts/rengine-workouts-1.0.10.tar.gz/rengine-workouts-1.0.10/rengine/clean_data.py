import pandas as pd
import os




def clean_data():
    df = pd.read_excel(os.getcwd()+"\\rengine\\data\\exercises.xlsx", header=1)
    df = df.iloc[:,:-1]
    df["MaxReps"] = df.apply(lambda x: 1 if x["Endurance"] == 2 else 0,axis=1)
    return df


def test():
    df = clean_data()
    print(df.columns)
    print(df[df["Stength"]==1])

if __name__ == "__main__":
    test()



