from module import *

region = str(input("Enter region (eg. pl/de/fr"))
save_to_file = str(input("Save to file? (y/n)"))
if save_to_file == "y":
    save_to_file = True
else:
    save_to_file = False

generator = ZalandoNewsletter()
newsletter_code = generator.generate_code(region, save_to_file)
print(f"Generated newsletter code: {newsletter_code}")