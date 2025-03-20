import streamlit as st

from data.dbconnect import get_dataframe_from_query


@st.cache_data
def eshows_custes(day1, day2):
  return get_dataframe_from_query(f"""
SELECT 
    C.NAME AS 'Loja',
    DATE_FORMAT(P.DATA_INICIO, '%d/%m/%Y') AS 'Data Evento',
    SUM(P.VALOR_BRUTO) AS 'Valor Gasto'
  FROM T_PROPOSTAS P
  LEFT JOIN T_COMPANIES C ON P.FK_CONTRANTE = C.ID
    WHERE (C.FK_GRUPO = '124')
	  AND C.ID IN ('797','1504','261','846')
    AND P.FK_STATUS_PROPOSTA IS NOT NULL
    AND P.FK_STATUS_PROPOSTA NOT IN ('102')
    AND P.DATA_INICIO >= '{day1}'
    AND P.DATA_INICIO <= '{day2}'                                  
  GROUP BY YEAR(P.DATA_INICIO), MONTH(P.DATA_INICIO), DAY(P.DATA_INICIO), C.ID
  ORDER BY YEAR(P.DATA_INICIO), MONTH(P.DATA_INICIO), DAY(P.DATA_INICIO)
  """)


@st.cache_data
def eshows_proposals(day1, day2):
  return get_dataframe_from_query(f"""
SELECT 
    C.NAME AS 'Loja',
    P.ID AS 'ID Proposta',
    DATE_FORMAT(P.DATA_INICIO, '%d/%m/%Y') AS 'Data Evento',
		TIME_FORMAT(P.DATA_INICIO, '%H:%i') AS 'Horário',    
    A.NOME AS 'Artista',
    P.VALOR_BRUTO AS 'Valor Bruto'
  FROM T_PROPOSTAS P
    LEFT JOIN T_COMPANIES C ON P.FK_CONTRANTE = C.ID
    LEFT JOIN T_ATRACOES A ON A.ID = P.FK_CONTRATADO
  WHERE (C.FK_GRUPO = '124')
  AND C.ID IN ('797','1504','261','846')
	AND P.FK_STATUS_PROPOSTA IS NOT NULL
	AND P.FK_STATUS_PROPOSTA NOT IN ('102')
  AND P.DATA_INICIO >= '{day1}'
  AND P.DATA_INICIO <= '{day2}'  
  ORDER BY YEAR(P.DATA_INICIO), MONTH(P.DATA_INICIO), DAY(P.DATA_INICIO), C.ID
  """)   