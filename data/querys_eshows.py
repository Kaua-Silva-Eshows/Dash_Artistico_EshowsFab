import streamlit as st

from data.dbconnect import get_dataframe_from_query


@st.cache_data
def eshows_custes():
  return get_dataframe_from_query("""
SELECT 
    DATE_FORMAT(P.DATA_INICIO, '%d/%m/%Y') AS 'Data Evento',
    SUM(P.VALOR_BRUTO) AS 'Valor Gasto'
  FROM T_PROPOSTAS P
  LEFT JOIN T_COMPANIES C ON P.FK_CONTRANTE = C.ID
  WHERE C.ID = '1504'
    AND P.FK_STATUS_PROPOSTA IS NOT NULL
    AND P.FK_STATUS_PROPOSTA NOT IN ('102')
  GROUP BY YEAR(P.DATA_INICIO), MONTH(P.DATA_INICIO), DAY(P.DATA_INICIO)
  ORDER BY YEAR(P.DATA_INICIO), MONTH(P.DATA_INICIO), DAY(P.DATA_INICIO)
  """)


@st.cache_data
def eshows_proposals():
  return get_dataframe_from_query(f"""
SELECT 
    P.ID AS 'ID Proposta',
    DATE_FORMAT(P.DATA_INICIO, '%d/%m/%Y') AS 'Data Evento',
		TIME_FORMAT(P.DATA_INICIO, '%H:%i') AS 'Horário',    
    A.NOME AS 'Artista',
    P.VALOR_BRUTO AS 'Valor Bruto'
  FROM T_PROPOSTAS P
    LEFT JOIN T_COMPANIES C ON P.FK_CONTRANTE = C.ID
    LEFT JOIN T_ATRACOES A ON A.ID = P.FK_CONTRATADO
  WHERE C.ID = '1504'
	AND P.FK_STATUS_PROPOSTA IS NOT NULL
	AND P.FK_STATUS_PROPOSTA NOT IN ('102')
  """)   