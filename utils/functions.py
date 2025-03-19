import streamlit as st

def format_brazilian(num):
  try:
    num = float(num)
    return f"{num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
  except (ValueError, TypeError):
    return num

def format_columns_brazilian(df, numeric_columns):
  for col in numeric_columns:
    if col in df.columns:
      df[col] = df[col].apply(format_brazilian)
  return df

def component_fix_tab_echarts():
    streamlit_style = """
    <style>
    iframe[title="streamlit_echarts.st_echarts"]{ height: 450px; width: 750px;} 
   </style>
    """

    return st.markdown(streamlit_style, unsafe_allow_html=True)    

def component_effect_underline():
    st.markdown("""
    <style>
        .full-width-line-white {
            width: 100%;
            border-bottom: 1px solid #ffffff;
            margin-bottom: 0.5em;
        }
        .full-width-line-black {
            width: 100%;
            border-bottom: 1px solid #000000;
            margin-bottom: 0.5em;
        }
    </style>
    """, unsafe_allow_html=True)