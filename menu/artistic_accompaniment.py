from matplotlib.dates import relativedelta
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
    row1 = st.columns(6)
    global day_ArtisticAccompaniment1, day_ArtisticAccompaniment2

    with row1[2]:
        day_ArtisticAccompaniment1 = st.date_input('Data Inicio:', value=date(datetime.today().year, datetime.today().month, 1) - relativedelta(months=1), format='DD/MM/YYYY', key='day_ArtisticAccompaniment1') 
    with row1[3]:
        day_ArtisticAccompaniment2 = st.date_input('Data Final:', value=date(datetime.today().year, datetime.today().month, 1) - relativedelta(days=1), format='DD/MM/YYYY', key='day_ArtisticAccompaniment2')

    row = st.columns([3,2])
    with row[0]: 
        fabricaInvoicingCouvent = fabrica_invoicing_couvent(day_ArtisticAccompaniment1, day_ArtisticAccompaniment2)
        eshowsCustes = eshows_custes(day_ArtisticAccompaniment1, day_ArtisticAccompaniment2)
        merged_df = fabricaInvoicingCouvent.merge(eshowsCustes, on='Data Evento', how='outer')
        merged_df.fillna(0, inplace=True)
        merged_df['Lucro'] = merged_df['Valor Liquido'] - merged_df['Valor Gasto']

        merged_df['Data Evento'] = pd.to_datetime(merged_df['Data Evento'], dayfirst=True)  # Certifica que é datetime
        merged_df = merged_df.sort_values(by='Data Evento', ascending=True)
        merged_df['Data Evento'] = merged_df['Data Evento'].dt.strftime('%d/%m/%Y')

        total_profit = merged_df['Lucro'].sum()
        total_profit = f"{total_profit:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        merged_df['Loja'] = merged_df['Loja'].replace(["0", 0], "")
        merged_df = function_format_columns_number(merged_df, ['Valor Bruto', 'Desconto', 'Valor Liquido', 'Valor Gasto', 'Lucro'])

        row2_1 = st.columns(5)
        tile = row2_1[2].container(border=True)    
        tile.write(f"<p style='text-align: center; font-size: 12px;'>Lucro Total Periodo:</br><span style='font-size: 18px;'>{total_profit}</span></p>", unsafe_allow_html=True)
    
        filtered_copy, count = component_plotDataframe(merged_df, "Lucro Geral")

    with row[1]:
        eshowsProposals = eshows_proposals(day_ArtisticAccompaniment1, day_ArtisticAccompaniment2)
        eshowsProposals = function_format_columns_number(eshowsProposals, ['Valor Bruto'])
        filtered_copy, count = component_plotDataframe(eshowsProposals, "Propostas", height=496)

class ArtisticAccompaniment(Page):
    def render(self):
        self.data = {}
        day_ArtisticAccompaniment1 = date(datetime.today().year, datetime.today().month, 1) - relativedelta(months=1)
        day_ArtisticAccompaniment2 = date(datetime.today().year, datetime.today().month, 1) - relativedelta(days=1)
        self.data['fabricaInvoicingCouvent'] = fabrica_invoicing_couvent(day_ArtisticAccompaniment1, day_ArtisticAccompaniment2)
        self.data['eshowsCustes'] = eshows_custes(day_ArtisticAccompaniment1, day_ArtisticAccompaniment2)
        self.data['eshowsProposals'] = eshows_proposals(day_ArtisticAccompaniment1, day_ArtisticAccompaniment2)

        BuildArtisticAccompaniment(self.data['fabricaInvoicingCouvent'], 
                  self.data['eshowsCustes'], 
                  self.data['eshowsProposals'])
