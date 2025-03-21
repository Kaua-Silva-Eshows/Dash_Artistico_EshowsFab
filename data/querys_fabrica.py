import streamlit as st
from data.dbconnect import get_dataframe_from_query


@st.cache_data
def fabrica_invoicing_couvent(day1, day2):
  return get_dataframe_from_query(f""" 
SELECT
    TE.NOME_FANTASIA AS 'Loja',
    DATE_FORMAT(IV.EVENT_DATE, '%d/%m/%Y') AS 'Data Evento',
    SUM(IV.UNIT_VALUE * IV.COUNT) AS 'Valor Bruto',
    SUM(IV.DISCOUNT_VALUE) AS Desconto,
    SUM((IV.UNIT_VALUE * IV.COUNT) - IV.DISCOUNT_VALUE) AS 'Valor Liquido'
  FROM T_ITENS_VENDIDOS IV
  LEFT JOIN T_ITENS_VENDIDOS_CADASTROS ICV ON IV.PRODUCT_ID = ICV.ID_ZIGPAY
  LEFT JOIN T_ITENS_VENDIDOS_CATEGORIAS ICV2 ON ICV.FK_CATEGORIA = ICV2.ID
  LEFT JOIN T_ITENS_VENDIDOS_TIPOS IVT ON ICV.FK_TIPO = IVT.ID
  LEFT JOIN T_EMPRESAS TE ON IV.LOJA_ID = TE.ID_ZIGPAY
  WHERE ICV2.DESCRICAO = 'Couvert'
	AND TE.ID IN ('122','105','148','114')
  AND IV.EVENT_DATE >= '{day1}'
  AND IV.EVENT_DATE <= '{day2}'
  GROUP BY IV.EVENT_DATE
  ORDER BY YEAR(IV.EVENT_DATE), MONTH(IV.EVENT_DATE), DAY(IV.EVENT_DATE)

  """, use_fabrica=True)