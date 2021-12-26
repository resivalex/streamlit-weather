import streamlit as st


st.set_page_config(page_title='Weather')


def main():
    st.write('ClickHouse port: ' + str(st.secrets['clickhouse_port']))


if __name__ == "__main__":
    main()
