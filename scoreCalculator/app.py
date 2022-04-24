import pandas as pd


MODULES = {
    'asd': {'cof': 3, 'module': ['TD', 'TP']},
    'ao': {'cof': 3, 'module': ['TD', 'TP']},
    'si': {'cof': 3, 'module': ['TD', 'TP']},
    'lm': {'cof': 2, 'module': ['TD']},
    'mn': {'cof': 2, 'module': ['TP']},
    'tg': {'cof': 2, 'module': ['TD']},
    'eng': {'cof': 1, 'module': []},
}


def correct_data(df, col_names=None):
    if col_names in df.columns:
        df.drop(columns=col_names, inplace=True)

    df.dropna(axis=0, inplace=True, how='all')  # remove unavailable rows
    df.dropna(axis=1, inplace=True, how='all')  # remove unavailable cols

    # fill the neccessiry gaps
    df['Prénom'].fillna('', inplace=True)
    df['Nom'].fillna('', inplace=True)
    df.fillna(0, inplace=True)

    # merge Nom & Prenom column togother
    df['Nom'] = df[['Nom', 'Prénom']].agg(' '.join, axis=1)
    df.drop(columns='Prénom', inplace=True)


def calculate_score(df, name):
    module = MODULES[name]['module']

    # We don't need to calculate the score for English cause it only has exam
    if len(module) == 0:
        return

    # This module contain TD and TP
    if len(module) == 2:
        td_note = (df['TD'] + df['TP']) / 2
        df[f'{name}_note'] = (td_note*0.4) + (df['Examen']*0.6)
        df.drop(columns=['TD', 'TP', 'Examen'], inplace=True)
        return

    # This module contain only TD or TP
    df[f'{name}_note'] = (df['Examen']*0.6) + (df[module[0]]*0.4)
    df.drop(columns=[module[0], 'Examen'], inplace=True)


def calculate_final_score(notes):
    asd = notes['asd_note']*MODULES['asd']['cof']
    tg = notes['tg_note']*MODULES['tg']['cof']
    lm = notes['lm_note'] * MODULES['lm']['cof']
    ao = notes['ao_note'] * MODULES['ao']['cof']
    mn = notes['mn_note'] * MODULES['mn']['cof']
    si = notes['si_note'] * MODULES['si']['cof']
    eng = notes['eng_note'] * MODULES['eng']['cof']

    # Remove unccessery columns
    notes.drop(columns=['asd_note', 'tg_note', 'lm_note', 'ao_note',
               'mn_note', 'si_note', 'eng_note'], inplace=True)

    notes['note_final'] = round(sum([asd, tg, lm, ao, mn, si, eng]) / 16, 2)
    notes.sort_values(by=['note_final'], inplace=True, ascending=False)
    notes.reset_index(inplace=True, drop=True)
    # Default indexes start from 0
    notes.index += 1


def save_to_excel(df, file_name, sheet_name):
    # Save the contents to an excel sheet file
    with pd.ExcelWriter(file_name, engine='xlsxwriter') as file:
        df.to_excel(file, sheet_name=sheet_name)
        worksheet = file.sheets[sheet_name]
        # Change the width of columns
        worksheet.set_column(1, 1, 30)
        worksheet.set_column(2, 2, 30)


def main():
    modules_names = ['asd', 'tg', 'lm', 'ao', 'mn', 'si', 'eng']

    # Load all data
    [asd, tg, lm, ao, mn, si, eng] = [pd.read_excel(
        f'assets/{module}.xlsx') for module in modules_names]

    # unwanted columns names in the AO file
    ao.drop(columns=['Hadji', 'TD Bada', 'TP Djezzar',
            'TD Abdelaziz'], inplace=True)
    eng.rename(columns={'Unnamed: 3': 'eng_note'}, inplace=True)

    # Prepare the data to work with
    # then calculate score for each module
    for idx, df in enumerate([asd, tg, lm, ao, mn, si, eng]):
        correct_data(df, col_names='N')
        calculate_score(df, modules_names[idx])

    notes = pd.merge(tg, lm).merge(ao).merge(
        mn).merge(si).merge(eng).merge(asd)

    calculate_final_score(notes)
    save_to_excel(notes, 'notes final.xlsx', 'Notes')


if __name__ == '__main__':
    main()
