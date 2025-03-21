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

    num_months = (day_ArtisticAccompaniment2.year - day_ArtisticAccompaniment1.year) * 12 + (day_ArtisticAccompaniment2.month - day_ArtisticAccompaniment1.month) + 1

    day_ArtisticAccompaniment3 = day_ArtisticAccompaniment1 - relativedelta(months=num_months)
    day_ArtisticAccompaniment4 = day_ArtisticAccompaniment2 - relativedelta(months=num_months)

    last_day_of_the_month = (day_ArtisticAccompaniment2.replace(day=1) + relativedelta(months=1, days=-1)).day
    if day_ArtisticAccompaniment2.day == last_day_of_the_month:
        day_ArtisticAccompaniment4 = (day_ArtisticAccompaniment4.replace(day=1) + relativedelta(months=1, days=-1))

    row = st.columns([3,2])
    with row[0]: 
        fabricaInvoicingCouvent = fabrica_invoicing_couvent(day_ArtisticAccompaniment1, day_ArtisticAccompaniment2)
        eshowsCustes = eshows_custes(day_ArtisticAccompaniment1, day_ArtisticAccompaniment2)
        eshowsCustes, fabricaInvoicingCouvent = function_rename_stores(eshowsCustes, fabricaInvoicingCouvent)
        merged_df = fabricaInvoicingCouvent.merge(eshowsCustes, on=['Data Evento', 'Loja'],how='outer')        
        merged_df.fillna(0, inplace=True)
        merged_df['Resultado'] = merged_df['Valor Liquido'] - merged_df['Valor Gasto']
        merged_df['Data Evento'] = pd.to_datetime(merged_df['Data Evento'], dayfirst=True)  # Certifica que é datetime
        merged_df = merged_df.sort_values(by='Data Evento', ascending=True)
        merged_df['Data Evento'] = merged_df['Data Evento'].dt.strftime('%d/%m/%Y')
        merged_df['Loja'] = merged_df['Loja'].replace(["0", 0], "")


        fabricaInvoicingCouvent2 = fabrica_invoicing_couvent(day_ArtisticAccompaniment3, day_ArtisticAccompaniment4)
        eshowsCustes2 = eshows_custes(day_ArtisticAccompaniment3, day_ArtisticAccompaniment4)
        eshowsCustes2, fabricaInvoicingCouvent2 = function_rename_stores(eshowsCustes2, fabricaInvoicingCouvent2)
        merged_df2 = fabricaInvoicingCouvent2.merge(eshowsCustes2, on=['Data Evento', 'Loja'],how='outer')        
        merged_df2.fillna(0, inplace=True)
        merged_df2['Resultado'] = merged_df2['Valor Liquido'] - merged_df2['Valor Gasto']

        selected_stores = st.multiselect("Selecione a Loja", merged_df['Loja'].unique(), default=merged_df['Loja'].unique(), key='lojas_artistic_accompaniment')

        filtered_merged_df = merged_df[merged_df['Loja'].isin(selected_stores)]
        filtered_merged_df2 = merged_df2[merged_df2['Loja'].isin(selected_stores)]

        row2_1 = st.columns([2,1.5,2])

        tile = row2_1[1].container(border=True)    
        total_profit = filtered_merged_df['Resultado'].sum()
        total_profit2 = filtered_merged_df2['Resultado'].sum()
        percentage_difference, percentage_color, arrow = funtion_calculate_percentage(total_profit, total_profit2)
        total_profit = f"{total_profit:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        tile.write(f"<p style='text-align: center; font-size: 12px;'>Lucro Total Periodo:</br><span style='font-size: 18px;'>{total_profit}</span></br><span style='font-size: 10px; color: {percentage_color};'>{percentage_difference:.2f}% {arrow}</span></p>", unsafe_allow_html=True)
    
        filtered_merged_df = function_format_columns_number(filtered_merged_df, ['Valor Bruto', 'Desconto', 'Valor Liquido', 'Valor Gasto', 'Resultado'])
        filtered_copy, count = component_plotDataframe(filtered_merged_df, "Lucro Geral", height=420)
        function_copy_dataframe_as_tsv(filtered_copy)


    with row[1]:
        eshowsProposals = eshows_proposals(day_ArtisticAccompaniment1, day_ArtisticAccompaniment2)
        eshowsProposals = function_rename_stores(eshowsProposals)
        filter_eshowsProposals = eshowsProposals[eshowsProposals['Loja'].isin(selected_stores)]
        eshowsProposals = function_format_columns_number(filter_eshowsProposals, ['Valor Bruto'])
        filtered_copy, count = component_plotDataframe(filter_eshowsProposals, "Propostas", height=620)
        function_copy_dataframe_as_tsv(filtered_copy)

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
