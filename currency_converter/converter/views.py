import requests
from django.shortcuts import render

API_KEY = "f57280e028dd75f5d25cbfec"  # Replace with a valid API key
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest"

def get_exchange_rate(from_currency, to_currency):
    url = f"{BASE_URL}/{from_currency}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return None

    try:
        data = response.json()
        return data["conversion_rates"].get(to_currency, None)
    except requests.exceptions.JSONDecodeError:
        return None

def currency_converter(request):
    if request.method == "POST":
        from_currency = request.POST.get("from_currency").upper()
        to_currency = request.POST.get("to_currency").upper()
        amount = request.POST.get("amount")

        try:
            amount = float(amount)
            exchange_rate = get_exchange_rate(from_currency, to_currency)
            
            if exchange_rate:
                converted_amount = amount * exchange_rate
                return render(request, "index.html", {
                    "converted_amount": f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}",
                    "from_currency": from_currency,
                    "to_currency": to_currency,
                    "amount": amount
                })
            else:
                error = "Invalid currency codes. Please try again."
        except ValueError:
            error = "Invalid amount entered."

        return render(request, "index.html", {"error": error})

    return render(request, "index.html")
