import json
def update_hyperlink():
    try:
        letter = input("Enter your letter: ")
        with open("reference.json", "r") as f:
            data = json.load(f)
            if letter in data:
                hyperlink = input("Enter a new hyperlink: ")
                data[letter] = hyperlink
                with open("reference.json", "w") as f:
                    json.dump(data, f)
                print("hyperlink updated successfully.")
            else:
                print("letter not found.")
    except Exception as e:
        print("An error occurred while updating the hyperlink:", e)

