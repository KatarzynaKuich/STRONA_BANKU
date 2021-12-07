
import requests
import csv
from flask import Flask, render_template, request

app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
rates = data[0].get('rates')
date = [data[0].get(x) for x in ['table', 'no', 'tradingDate', "effectiveDate"]]

# get codes for currency
codes = []
for code in rates:
    codes.append(code.get("code"))

# save csv_file
with open('rates.csv', 'w') as csv_file:
    fieldnames = ['currency', 'code', 'bid', 'ask']
    writer = csv.DictWriter(csv_file, delimiter=';', fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rates)

             
@app.route("/", methods =["GET", "POST"])
def message():
   wynik= None
   if request.method == "POST":
        print("We recieved POST")
        amount =request.form['amount']

        # find ask value for code
        for rate in rates:
            if rate['code'] == request.form['codes']:
                wynik=f"{amount} {request.form['codes']} * {rate['ask']} ={(round((float((rate['ask'])) * float(amount)), 2)):,.2f} PLN"

   return render_template("form.html",codes=codes, date=date,result=wynik)

if __name__ == "__main__":
    app.run(debug=True)
