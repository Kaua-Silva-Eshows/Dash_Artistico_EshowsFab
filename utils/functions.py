import streamlit as st
import streamlit.components.v1 as components

def function_format_number(num):
  try:
    num = float(num)
    return f"{num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
  except (ValueError, TypeError):
    return num

def function_format_columns_number(df, numeric_columns):
  for col in numeric_columns:
    if col in df.columns:
      df[col] = df[col].apply(function_format_number)
  return df

def function_copy_dataframe_as_tsv(df):
    # Converte o DataFrame para uma string TSV
    df_tsv = df.to_csv(index=False, sep='\t')
    
    # Gera código HTML e JavaScript para copiar o conteúdo para a área de transferência
    components.html(
        f"""
        <style>
            .custom-button {{
                background-color: #1e1e1e; /* Cor de fundo escura */
                color: #ffffff; /* Cor do texto claro */
                border: 1px solid #333333; /* Cor da borda escura */
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                display: inline-block;
                text-align: center;
                text-decoration: none;
                transition: background-color 0.3s ease, color 0.3s ease;
            }}
            .custom-button:hover {{
                background-color: #333333; /* Cor de fundo escura ao passar o mouse */
                color: #e0e0e0; /* Cor do texto ao passar o mouse */
            }}
        </style>
        <textarea id="clipboard-textarea" style="position: absolute; left: -10000px;">{df_tsv}</textarea>
        <button class="custom-button" onclick="document.getElementById('clipboard-textarea').select(); document.execCommand('copy'); alert('DataFrame copiado para a área de transferência como TSV!');">Copiar DataFrame</button>
        """,
        height=100
    )

def function_rename_stores(df_eshows, df_fabrica=None):
    rename_df_eshows = {
        'Jacaré ': 'Jacaré',
        'Bar Brahma': 'Bar Brahma',
        'Bar dos Arcos - Salão Dourado': 'Arcos',
        'Bar Brahma Granja': 'Granja'
    }
    
    rename_df_fabrica = {
        'Jacaré ': 'Jacaré',
        'Bar Brahma - Centro': 'Bar Brahma',
        'Arcos': 'Arcos',
        'Bar Brahma - Granja': 'Granja'
    }
    
    df_eshows['Loja'] = df_eshows['Loja'].replace(rename_df_eshows)

    if df_fabrica is not None:
        df_fabrica['Loja'] = df_fabrica['Loja'].replace(rename_df_fabrica)
        return df_eshows, df_fabrica
    
    return df_eshows

def funtion_calculate_percentage(new_value, old_value):
    if old_value == 0:  
        return float('nan'), 'gray', '–'

    percentage_difference = ((new_value - old_value) / abs(old_value)) * 100  
    
    if (old_value < 0 and new_value < old_value) or (old_value > 0 and new_value < old_value):
        percentage_color = 'red'
        arrow = '▼'
    else:
        percentage_color = 'green' 
        arrow = '▲'

    return percentage_difference, percentage_color, arrow