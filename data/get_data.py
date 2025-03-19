import pandas as pd

def initialize_data(id):
    # Dicionário com dados de entrada
    data = {
        "eshowsProposals" : pd.DataFrame(),
        "eshowsCustes" : pd.DataFrame(),
        "fabricaInvoicingCouvent" : pd.DataFrame(),
        "id": id,
    }

    return data