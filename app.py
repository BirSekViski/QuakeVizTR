from flask import Flask, render_template
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64


app = Flask(__name__)


@app.route('/')
def index():
    data = pd.read_csv('dataset.csv')
    return render_template(
    'index.html',
    title='180315008 Midterm Charts',
    data=data,
    top8_histogram=top8_histogram(data),
    earthquake_per_year_histogram = earthquake_per_year_histogram(data),
    scatter_plot=scatter_plot(data)
    )

def top8_histogram(data):
    city_counts = data['city'].value_counts()
    top_cities = city_counts.head(8)
    other_count = city_counts[8:].sum()
    other_series = pd.Series([other_count], index=['Other'])
    city_counts = pd.concat([top_cities, other_series])

    plt.bar(city_counts.index, city_counts.values)
    plt.title('City Occurrences')
    plt.xlabel('City')
    plt.ylabel('Count')
    plt.xticks(rotation=90)

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)

    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

    return f"data:image/png;base64,{img_base64}"


def earthquake_per_year_histogram(data):
    data['date_time'] = pd.to_datetime(data['date_time'], format='%d.%m.%Y %H:%M:%S')
    data['year'] = data['date_time'].dt.year
    eq_per_year = data.groupby('year')['magnitude'].count()

    plt.bar(eq_per_year.index, eq_per_year.values)
    plt.title('Earthquakes per Year')
    plt.xlabel('Year')
    plt.ylabel('Count')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    image_base64 = base64.b64encode(img.getvalue()).decode()

    return f"data:image/png;base64,{image_base64}"

def scatter_plot(data):
    data['date_time'] = pd.to_datetime(data['date_time'], format='%d.%m.%Y %H:%M:%S')
    dates = data['date_time'].values.astype(np.int64) // 10**6

    plt.scatter(dates, data['magnitude'], s=data['magnitude']*10)
    plt.title('Magnitude vs Date')
    plt.xlabel('Date')
    plt.ylabel('Magnitude')

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format='png')
    img_bytes.seek(0)

    img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')

    return f"data:image/png;base64,{img_base64}"





if __name__ == '__main__':
    app.run()

