import csv

moved_cities = ["浜松市中区", "浜松市東区", "浜松市西区", "浜松市南区", "浜松市北区", "浜松市浜北区"]

zipcode_file_path = 'KEN_ALL.CSV'
with open(zipcode_file_path, mode='r', encoding='cp932') as file:
    csv_reader = csv.DictReader(file)
    zipcodes = [row for row in csv_reader]
zipcodes_dict = {zipcode['郵便番号']: zipcode for zipcode in zipcodes}

address_file_path = 'addresses.csv'
with open(address_file_path, mode='r', encoding='cp932') as file:
    csv_reader = csv.DictReader(file)
    addresses = [row for row in csv_reader]

results = []
for address in addresses:
    # print(address)
    zipcode = zipcodes_dict.get(address['自宅郵便番号'])
    result = address.copy()

    matched_moved_city = next(filter(lambda city: city in address["自宅住所"], moved_cities), None)
    if not zipcode or not matched_moved_city:
        results.append(result)
        continue
    
    updated_address = result["自宅住所"].replace(matched_moved_city, zipcode["市区町村名"], 1)
    print(f"変更前 -> {result["自宅住所"]}")
    print(f"変更後 -> {updated_address}\n")

    result["自宅住所"] = updated_address
    results.append(result)

with open('updated_addresses.csv', mode='w', encoding='cp932', newline='') as file:
    fieldnames = results[0].keys()
    csv_writer = csv.DictWriter(file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    csv_writer.writeheader()
    csv_writer.writerows(results)