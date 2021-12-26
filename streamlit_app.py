import streamlit as st
from clickhouse_driver import Client
import datetime
import pandas as pd


st.set_page_config(page_title='Погода')


def main():
    ch = Client(
        host=st.secrets['clickhouse_host'],
        port=st.secrets['clickhouse_port'],
        database=st.secrets['clickhouse_database'],
        user=st.secrets['clickhouse_user'],
        password=st.secrets['clickhouse_password']
    )
    (timestamp, weather_name, temperature, feels_like_temperature, wind_speed) = ch.execute('''
        select timestamp, weather_name, temperature, feels_like_temperature, wind_speed
        from weather_log
        order by timestamp desc
        limit 1
    ''')[0]
    current = pd.DataFrame(
        index=['Время', 'Описание', 'Температура', 'Ощущается как', 'Скорость ветра'],
        columns=['Значение'],
        data=[
            [datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')],
            [weather_name],
            [f'{temperature:.0f}°С'],
            [f'{feels_like_temperature:.0f}°С'],
            [f'{wind_speed}']
        ]
    )
    st.write('Последнее измерение')
    st.dataframe(current)
    history_df = pd.DataFrame(
        data=ch.execute('''
            select timestamp, weather_name, temperature, feels_like_temperature, wind_speed
            from (
                select
                    timestamp, weather_name, temperature, feels_like_temperature, wind_speed,
                    row_number() over (partition by timestamp) as row_num
                from weather_log
            )
            where row_num = 1
            order by timestamp
        '''),
        columns=['timestamp', 'weather_name', 'temperature', 'feels_like_temperature', 'wind_speed']
    )
    st.write('История изменения температуры')
    temperature_chart_df = pd.DataFrame(
        index=[datetime.datetime.fromtimestamp(timestamp) for timestamp in history_df['timestamp']],
        data={
            'Температура, °С': history_df['temperature'].tolist(),
            'Ощущается как, °С': history_df['feels_like_temperature'].tolist()
        }
    )
    st.line_chart(temperature_chart_df)
    st.write('История изменения скорости ветра')
    wind_chart_df = pd.DataFrame(
        index=[datetime.datetime.fromtimestamp(timestamp) for timestamp in history_df['timestamp']],
        data={
            'Скорость ветра, м/с': history_df['wind_speed'].tolist()
        }
    )
    st.line_chart(wind_chart_df)


if __name__ == "__main__":
    main()
