import csv
import os
import argparse

""" Ce code a été écrit avec l'aide de ChatGPT """


class file_csv():

    def write_csv(self, file, name, quantity, price, category):
        """
        - PRE:
            - 'file' est une chaîne de caractères correspondant au nom du fichier cible.
            - 'name', 'quantity', 'price', 'category' sont des valeurs valides à ajouter dans le CSV.
        - POST:
            - Ajoute une ligne avec les données spécifiées au fichier CSV indiqué.
            - Crée le fichier s'il n'existe pas.
        - RAISE:
            - IOError si une erreur d'écriture survient.
        """
        
        directory = 'CSV'

        if not os.path.exists(directory):
            os.mkdir(directory)

        try:
            with open(f'{directory}/{file}',
                      'a', encoding='utf-8') as CSV_file:
                CSV_file.write(f'{name},{quantity},{price},{category}\n')

        except IOError:
            print('ErreurIO')

    def print_csv(self, path):
        """
        - PRE:
            - 'path' est un chemin valide vers un fichier CSV existant.
        - POST:
            - Affiche chaque ligne du fichier CSV au format:
              line {i} : name = {name}, quantity = {quantity}, price = {price}, category = {category}.
        - RAISE:
            - FileNotFoundError si le fichier spécifié n'existe pas.
        """

        with open(path, 'r') as CSV_file:
            reader = csv.reader(CSV_file)
            i = 0

            for line in reader:
                i += 1
                print(f'line {i} : name = {line[0]}, quantity = {line[1]},'
                    + f'price = {line[2]}, category = {line[3]}.')

    def merge_csv(self, directory, directory_output, file_output):
        """
        - PRE:
            - 'directory' est un chemin valide vers un répertoire contenant des fichiers CSV.
            - 'file_output' est un chemin valide pour le fichier de sortie.
        - POST:
            - Fusionne tous les fichiers CSV du répertoire dans un seul fichier.
            - Crée un fichier CSV de sortie avec les données fusionnées.
        - RAISE:
            - FileNotFoundError si le répertoire source ou le fichier de sortie est introuvable.
            - FileNotFoundError si aucun fichier CSV n'est trouvé dans le répertoire.
            - IOError si une erreur survient lors de la lecture ou l'écriture des fichiers.
        """

        # Vérifie si le dossier existe
        if not os.path.exists(directory):
            raise FileNotFoundError('Le dossier n\'exitste pas')

        if not os.path.exists(directory_output):
            os.mkdir(directory_output)
            print(f'the {directory_output} directory as been created')

        # Liste pour stocker les fichiers CSV
        file_csv = [f for f in os.listdir(directory) if f.endswith('.csv')]

        # Vérifie s'il y a des fichiers CSV à fusionner
        if not file_csv:
            raise FileNotFoundError('Aucun CSV dans le dossier')

        else:
            with open(f'{directory_output}/{file_output}',
                      'w', newline='', encoding='utf-8') as output:
                output.write('name,quantity,price,category\n')
                for file in file_csv:
                    file_path = os.path.join(directory, file)
                    with open(file_path, 'r', encoding='utf-8') as entree:
                        reader = csv.reader(entree)
                        writer = csv.writer(output)
                        writer.writerow(next(reader))

                        # Écrire les lignes du fichier courant
                        for line in reader:
                            writer.writerow(line)

            print(f"Fusion terminée. Fichier créé : {file_output}")

    def write_option(self):
        """
        - PRE:
            - L'utilisateur fournit une chaîne de caractères sous le format: file,name,quantity,price,category.
        - POST:
            - Ajoute les données au fichier spécifié.
            - Redemande une entrée si le format est incorrect.
        - RAISE:
            - ValueError si le format de l'entrée est incorrect.
        """

        write_input = input('what do you want to write ? : ')

        if write_input == 'exit':
            exit()

        list_input = write_input.split(',')
        if len(list_input) < 5:
            print('Please enter enough argument (5)\n')
            self.write_option()

        else:
            self.write_csv(list_input[0], list_input[1],
                           list_input[2], list_input[3], list_input[4])

    def sort_csv(self, directory_input, file_input):
        """
        - PRE:
            - 'file_input' est un chemin valide vers un fichier CSV existant.
            - L'utilisateur fournit une colonne valide pour le tri: name, quantity, price, category.
        - POST:
            - Trie le fichier CSV selon la colonne spécifiée.
            - Affiche les données triées.
            - Offre la possibilité de sauvegarder les données triées.
        - RAISE:
            - FileNotFoundError si le fichier ou le répertoire n'existe pas.
            - ValueError si la colonne spécifiée pour le tri est invalide.
        """

        sort_column = input('name quantity price category\n'
                            + 'On what do you want to sort ? : ')

        if sort_column == 'exit':
            exit()

        elif (sort_column != 'name' and sort_column != 'quantity'
                and sort_column != 'price' and sort_column != 'category'):
            print('Please enter an existinge column : '
                  + 'name quantity price category\n')
            self.sort_csv('merged_csv/merge.csv')

        else:
            if not os.path.exists(directory_input):
                raise FileNotFoundError('There is nothing to sort on')

            with open(f'{directory_input}/{file_input}',
                      'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                lignes = list(reader)  # Charger toutes les lignes
                # Trier les lignes en fonction de la colonne
                if sort_column == 'price' or sort_column == 'quantity':
                    sorted_lines = sorted(lignes, key=lambda x:
                                          float(x[sort_column]))
                else:
                    sorted_lines = sorted(lignes, key=lambda x: x[sort_column])
                for i in sorted_lines:
                    print(f"name = {i['name']}, quantity = {i['quantity']},"
                          + f" price = {i['price']}, "
                          + f"category = {i['category']}.")

                save = input('Do you want to save that sorted list ? : ')
                if (save == 'y' or save == 'Y'
                            or save == 'yes' or save == 'Yes'
                            or save == 'YES'):

                    file_output = input('What will be the name of '
                                        + 'the file ? : ')
                    directory = 'sorted_csv'
                    if not os.path.exists(directory):
                        os.mkdir(directory)
                        print(f'The {directory} directory as been c')

                    with open(f'{directory}/{file_output}.csv',
                              'w', newline='', encoding='utf-8') as file:
                        writer = csv.DictWriter(file,
                                                fieldnames=reader.fieldnames)
                        writer.writeheader()  # Écrire l'en-tête
                        writer.writerows(sorted_lines)

    def what_to_do(self):
        """
        - PRE:
            - L'utilisateur exécute le script avec un argument valide: write, read, merge, sort.
        - POST:
            - Exécute l'action demandée en fonction de l'argument fourni.
            - Guide l'utilisateur pour les actions interactives.
        - RAISE:
            - ValueError si l'argument fourni est invalide ou manquant.
        """

        parser = argparse.ArgumentParser(description="A script to read, write, merge and sort CSV files.")
        parser.add_argument("action", choices=["write", "read", "merge", "sort"], help="Action à effectuer", nargs="?")
        args = parser.parse_args()

        if not args.action:
            print("Plase enter a valid option ['write', 'read', 'merge', 'sort']")

        elif args.action == 'write':
            self.write_option()

        elif args.action == 'merge':
            self.merge_csv('CSV', 'merged_csv', 'merge.csv')

        elif args.action == 'read':
            read = input('Which file do you want to read ? : ')

            try:
                self.print_csv(read)

            except FileNotFoundError:
                print('The file that you typed does not exist')
                self.what_to_do()

        elif args.action == 'sort':
            self.sort_csv('merged_csv', 'merge.csv')


if __name__ == '__main__':

    test = file_csv()
    test.what_to_do()
