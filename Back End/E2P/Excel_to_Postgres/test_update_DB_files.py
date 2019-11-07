import dropbox
import os

def update_dropbox_files(file_names,scope):
    dbx = dropbox.Dropbox('4cNxccGIm1AAAAAAAAAA3qfnUsYdNwJkWWgxYub2WTOtpZKIrMnMtH1VUdu0-aTt')
    # FUND_DATA_FILES = ['BELS Research Consumer.xlsx', 'BELS Research Financials.xlsx',  'BELS Research Healthcare.xlsx', 'BELS Research Industrials.xlsx', 'BELS Research REIT.xlsx', 'BELS Research Technology.xlsx']
    # ALL_FILES = FUND_DATA_FILES + ['Reconciliation to PLR.xlsx']

    if scope == 'fund_data':
        for fn in file_names:
            print("Downloading: ",fn)
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'Excel_files',fn)
            dbx.files_download_to_file(path, '/' + fn)
    elif scope == 'positions':
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)),'Excel_files',fn)
        fn = 'Reconciliation to PLR.xlsx'
        dbx.files_download_to_file(path, '/' + fn)
