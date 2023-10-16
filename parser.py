import pandas as pd
import argparse


def menu():
    """Just the menu

    Returns:
        class: all the arguments provided by user
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--keg_file", required=True, help="keg file to \
                        extract info")
    args = parser.parse_args()

    return args

def keg_to_tsv(filek):
    '''
    This parser extracts info from file .keg and transforms it in a TSV file with 
    columns:
        KO - KO number;
        Group - B hierarchy - the most general classification;
        General Classification - C hierarchy;
        Description - D hierarchy - a specific description of protein related to KO.

    Input:
        filek - file format .keg
        
    Output:
        tsv table
    '''
    data = {}
    blabel = None
    clabel = None
    blabel = None
    dlabel = None

# Reading file and extrating info
    with open(filek, 'r') as file:
        lines_after_5 = file.readlines()[5:]
        
        for line in lines_after_5:
            linha = line.split()

            if linha[0] == 'B' and len(linha) > 1:
                blabel = ' '.join(linha[2:])
                data[blabel] = {}

            elif linha[0] == 'C':
                clabel = ' '.join(linha[2:-1])
                data[blabel][clabel] = {}
                

            elif linha[0] == 'D':
                if linha[1] not in data:
                    dlabel = linha[1]
                    data[blabel][clabel][dlabel] = ' '.join(linha[2:])

    # Convert dictionary to DataFrame
    df = pd.DataFrame([(k1, k2, k3, v3) for k1, v1 in data.items() for k2, v2 
                       in v1.items() for k3, v3 in v2.items()],
                    columns=['Group','General Classification', 'KO','Description'])

    # Grouping values by "KO" and "Group" and joining other columns
    dfgroupped = df.groupby(['KO', 'Group'], as_index=False).agg({
        'General Classification': ' | '.join, 'Description': ' | '.join})

    # Saving DataFrame as TSV
    dfgroupped.to_csv('mapp_K03.tsv', sep='\t', index=False)

def main():
    options = menu()
    keg_to_tsv(options.keg_file)

if __name__ == "__main__":
    main()
