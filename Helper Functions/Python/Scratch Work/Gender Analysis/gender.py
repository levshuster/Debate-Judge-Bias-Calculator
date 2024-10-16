import requests, zipfile, io, shutil
import pandas as pd
import os

class Genderizer:
    df: pd.DataFrame = None
    
    def __init__(self, path: str = "gender_compendium.csv"):
        if not os.path.exists(path):
            self.df = self.build_compendium()
        else:
            self.df = pd.read_csv(path)
    # If we don't have our compendium, build it from scratch
    def build_compendium(self) -> pd.DataFrame:
        # Download files:
        if os.path.exists("names"):
            shutil.rmtree("names")
        os.mkdir("names")
        source = "https://www.ssa.gov/oact/babynames/names.zip"
        req = requests.get(source, stream=True)
        z = zipfile.ZipFile(io.BytesIO(req.content))
        z.extractall("names")
        # Build and combine dataframes:
        dataframes = []
        for filename in os.listdir('names'):
            if not filename.endswith(".txt"):
                continue
            df = pd.read_csv("names/"+filename, header=None, names=["name", "sex", "count"])
            dataframes.append(df)
            # Concatenate and group:
            df = pd.concat(dataframes).groupby(["name", "sex"], as_index=False).sum()
            # Separate M/F columns:
            df = df.pivot(index='name', columns='sex', values='count').fillna(0)
            df.columns = ["F", "M"]
            df.reset_index(inplace=True)
            df = df[["name", "M", "F"]]
            df = df.astype({"M": int, "F": int})
            # Write to CSV and clean up
            df.to_csv("gender_compendium.csv", index=False)
            shutil.rmtree("names")
            return df

    # Get the gender of one or more names
    def gender(self, name: str | list[str]) -> dict[str, int] | dict[str, dict[str, int]]:
        # Check for multiple names:
        if isinstance(name, list):
            return self.genders(name)
        
        name = name.capitalize()
        row = self.df[self.df["name"] == name]
        # If the name is absent, get it from genderize.io
        if row.empty:
            return self.request_gender(name)
        m = int(row["M"].values[0])
        f = int(row["F"].values[0])
        # Conditional returns:
        if m == f:
            return {"gender": "U", "prob": 0.5, "count": m+f}
        gender = "M" if m > f else "F"
        prob = max(m, f) / (m+f)
        return {"gender": gender, "prob": prob, "count": m+f, "API": False}

    # Helper for multiple names
    def genders(self, names: list[str]) -> dict[str, dict[str, int]]:
        return {name: self.gender(name) for name in names}

    # Get the gender from genderize.io
    def request_gender(self, name: str) -> dict[str, int]:
        name = name.capitalize()
        url = f"https://api.genderize.io?name={name}"
        response = requests.get(url)
        data = response.json()
        if data["probability"] <= 0.5:
            return {"gender": "U", "prob": 0.5, "count": data["count"], "API": True}
        gender = "M" if data["gender"] == "male" else "F"
        return {"gender": gender, "prob": data["probability"], "count": data["count"], "API": True}
    
    
if __name__ == "__main__":
    g = Genderizer()
    print("---\nName: Mary")
    print(" ", g.gender("Mary"))
    names = ["John", "Alex", "Corin", "Borscht", "Cruella", "Compost"]
    print("---\nNames:", ", ".join(names))
    genders = g.gender(names)
    for name in genders.keys():
        print(f"  {name}: {genders[name]}")
