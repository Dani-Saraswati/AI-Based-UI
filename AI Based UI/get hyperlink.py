import json
def get_hyperlink(letter):
    try:
        with open("reference.json", "r") as f:
            data = json.load(f)
            if letter in data:
                return data[letter]
            else:
                return None
    except Exception as e:
        print("An error occurred while getting the hyperlink:", e)
        return None


