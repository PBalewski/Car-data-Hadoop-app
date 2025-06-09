from flask import Flask, request, render_template
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

app = Flask(__name__)

# Initialize Spark session
spark = SparkSession.builder.appName("CarsDataApp").getOrCreate()

# Load dataset
DATA_PATH = "hdfs://hadoop-master:9000/cars/CarsData.csv"
df = spark.read.csv(DATA_PATH, header=True, inferSchema=True)
df.cache()

@app.route('/', methods=['GET', 'POST'])
def index():
    from math import ceil

    # 1. Get user view
    view = request.values.get('view', '')
    label, xcol, ycol = '', '', ''

    if view == "brand_price":
        xcol, ycol = "Manufacturer", "price"
        label = "Average Price by Brand"
    elif view == "brand_mileage":
        xcol, ycol = "Manufacturer", "mileage"
        label = "Average Mileage by Brand"
    elif view == "brand_mpg":
        xcol, ycol = "Manufacturer", "mpg"
        label = "Average MPG by Brand"
    elif view == "fuel_price":
        xcol, ycol = "fuelType", "price"
        label = "Average Price by Fuel Type"
    elif view == "transmission_price":
        xcol, ycol = "transmission", "price"
        label = "Average Price by Transmission Type"

    data, filtered_rows = [], []
    x_values, y_min, y_max = [], None, None
    best_car = None

    if xcol and ycol:
        x_values = df.select(xcol).distinct().rdd.flatMap(lambda x: x).collect()
        y_min = df.agg({ycol: "min"}).first()[0]
        y_max = df.agg({ycol: "max"}).first()[0]

        selected_x = request.args.getlist("x_filter") or x_values
        try:
            y_min = float(request.args.get("y_min")) if request.args.get("y_min") else y_min
        except ValueError:
            y_min = y_min

        try:
            y_max = float(request.args.get("y_max")) if request.args.get("y_max") else y_max
        except ValueError:
            y_max = y_max

        # Pagination params
        per_page = 100
        page = int(request.args.get("page", 1))

        # Filtered dataframe
        df_filtered = df.filter(
            (col(xcol).isin(selected_x)) &
            (col(ycol) >= y_min) &
            (col(ycol) <= y_max)
        )

        # Grouped result
        grouped = df.groupBy(xcol).avg(ycol).orderBy(f"avg({ycol})", ascending=False)
        grouped = grouped.toPandas()
        grouped.columns = [xcol, ycol]
        data = list(grouped.itertuples(index=False, name=None))

        # Raw filtered rows
        all_filtered = df_filtered.select("*").limit(10000).toPandas().to_dict(orient="records")
        total_records = len(all_filtered)
        total_pages = ceil(total_records / per_page)

        start = (page - 1) * per_page
        end = start + per_page
        filtered_rows = all_filtered[start:end]
        
        # easiest recommendation logic: best car by highest mpg
        if not df_filtered.rdd.isEmpty() and "mpg" in df_filtered.columns:
            df_best = df_filtered.orderBy(col("mpg").desc_nulls_last())
            best_car_row = df_best.limit(1).toPandas().to_dict(orient="records")
            best_car = best_car_row[0] if best_car_row else None
    else:
        page = 1
        per_page = 100
        total_pages = 1

        
    return render_template("index.html",
        view=view,
        xcol=xcol,
        ycol=ycol,
        x_values=x_values,
        y_min=y_min,
        y_max=y_max,
        data=data,
        label=label,
        filtered_rows=filtered_rows,
        page=page,
        per_page=per_page,
        total_pages=total_pages,
        best_car=best_car,
        request=request
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)