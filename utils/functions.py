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
            .custom-copy-btn {{
                background: linear-gradient(90deg, #FFB131 0%, #FF7F50 50%, #A52A2A 100%);
                color: #fff;
                border: none;
                padding: 12px 28px 12px 18px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                display: inline-flex;
                align-items: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.10);
                transition: background 0.3s, color 0.3s;
                position: relative;
                gap: 8px;
            }}
            .custom-copy-btn:hover {{
                background: linear-gradient(90deg, #8B0000 0%, #FF7F50 50%, #FFB131 100%);
                color: #222;
            }}
            .copy-icon {{
                width: 20px;
                height: 20px;
                vertical-align: middle;
                fill: currentColor;
            }}
        </style>
        <textarea id="clipboard-textarea" style="position: absolute; left: -10000px;">{df_tsv}</textarea>
        <button class="custom-copy-btn" id="copy-btn" onclick="copyDF()">
            <svg class='copy-icon' viewBox='0 0 24 24'><path d='M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z'/></svg>
            <span id="copy-btn-text">Copiar DataFrame</span>
        </button>
        <script>
        function copyDF() {{
            var textarea = document.getElementById('clipboard-textarea');
            textarea.select();
            document.execCommand('copy');
            var btn = document.getElementById('copy-btn');
            var btnText = document.getElementById('copy-btn-text');
            btnText.innerText = 'Copiado!';
            btn.style.background = 'linear-gradient(90deg, #4BB543 0%, #43e97b 100%)';
            setTimeout(function() {{
                btnText.innerText = 'Copiar DataFrame';
                btn.style.background = 'linear-gradient(90deg, #A52A2A 0%, #FF7F50 50%, #FFB131 100%)';
            }}, 1500);
        }}
        </script>
        """,
        height=110
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