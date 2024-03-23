meal_cost = input("Enter the cost of the meal: ")
tip = float(meal_cost) * 0.15
tax = float(meal_cost) * 0.21

total = (float(meal_cost) + float(tip) + float(tax))

total = round(total, 3)
tax = round(tax, 3)
tip = round(tip, 3)

print("Tax: " + str(tax) + ", Tip: " + str(tip) + ", Total: " + str(total))