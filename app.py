from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load dataset (make sure meals.csv has 'recipe_details' column)
df = pd.read_csv("meals.csv")

def generate_full_day_plan(calories_limit, diet_type):
    categories = ["breakfast", "lunch", "dinner", "snack"]
    plan = {}
    total_calories = 0
    
    for cat in categories:
        # Strict filtering: exact match for vegetarian / non-vegetarian
        filtered = df[
            (df['category'].str.lower() == cat.lower()) &
            (df['type'].str.lower() == diet_type.lower())
        ]
        
        if not filtered.empty:
            meal = filtered.sample(1).iloc[0]
            plan[cat] = meal.to_dict()
            total_calories += meal['calories']
    
    return plan, total_calories

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            calories_limit = int(request.form.get("calories"))
        except (TypeError, ValueError):
            calories_limit = 2000  # default if user input is invalid
        
        diet_type = request.form.get("diet_type")  # vegetarian / non-vegetarian
        
        plan, total_calories = generate_full_day_plan(calories_limit, diet_type)
        return render_template(
            "index.html",
            plan=plan,
            calories=calories_limit,
            total_calories=total_calories,
            diet_type=diet_type
        )
    
    return render_template("index.html", plan=None)

if __name__ == "__main__":
    app.run(debug=True)