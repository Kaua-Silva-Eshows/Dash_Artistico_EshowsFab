import pandas as pd
import streamlit as st
from data.querys_eshows import *
from data.querys_fabrica import *
from menu.page import Page
from utils.components import *
from utils.functions import *
from datetime import date, datetime

def BuildArtisticAccompaniment(fabricaInvoicingCouvent, eshowsCustes, eshowsProposals):
    
    st.write('## Lucro Por Loja')

    row = st.columns([3,2])

    with row[0]: 
        merged_df = fabricaInvoicingCouvent.merge(eshowsCustes, on='Data Evento', how='outer')
        merged_df.fillna(0, inplace=True)
        merged_df['Lucro'] = merged_df['Valor Liquido'] - merged_df['Valor Gasto']
        total_profit = merged_df['Lucro'].sum()
        total_profit = f"{total_profit:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        merged_df['Loja'] = merged_df['Loja'].replace(["0", 0], "")
        merged_df = format_columns_brazilian(merged_df, ['Valor Bruto', 'Desconto', 'Valor Liquido', 'Valor Gasto', 'Lucro'])

        row2_1 = st.columns(5)
        tile = row2_1[2].container(border=True)    
        tile.write(f"<p style='text-align: center; font-size: 12px;'>Lucro Total:</br><span style='font-size: 18px;'>{total_profit}</span></p>", unsafe_allow_html=True)
    
        filtered_copy, count = component_plotDataframe(merged_df, "Lucro Geral")

    with row[1]:
        # Converta a coluna 'DATA EVENTO' para datetime (se necessário)
        eshowsProposals = format_columns_brazilian(eshowsProposals, ['Valor Bruto'])
        filtered_copy, count = component_plotDataframe(eshowsProposals, "Propostas", height=496)

class ArtisticAccompaniment(Page):
    def render(self):
        self.data = {}
        self.data['fabricaInvoicingCouvent'] = fabrica_invoicing_couvent()
        self.data['eshowsCustes'] = eshows_custes()
        self.data['eshowsProposals'] = eshows_proposals()


        BuildArtisticAccompaniment(self.data['fabricaInvoicingCouvent'], 
                  self.data['eshowsCustes'], 
                  self.data['eshowsProposals'])
