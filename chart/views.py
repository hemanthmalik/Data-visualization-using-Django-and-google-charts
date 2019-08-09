from django.http import HttpResponse
from django.shortcuts import render
import json

def home(request):
    jsonHandle = open(r'C:\Users\HemantMalik\djangopractice\assignment\chart\chart\json\jsondata.json', encoding="utf8").read()
    jsonData = json.loads(jsonHandle)
    tableData = []
    count = 0
    for i in jsonData:
        tableData.append(["<a href = '" + (i['url'])+ "'>" + i["title"] + "</a>", i["topic"], str(i["start_year"]), i["sector"], i["region"], i["pestle"]])
    countries = {}
    sectors = {}
    countryCount = 1
    sectorCount = 1
    for i in jsonData:
        if i["country"] not in countries and i["country"] != "":
            countries[i["country"]] = countryCount
            countryCount += 1
        if i["sector"] not in sectors and i["sector"] != "":
            sectors[i["sector"]] = sectorCount
            sectorCount += 1
    
    heading = ["Country"] + [i for i in sectors]



    chartList = [[None for i in range(sectorCount)] for j in range(countryCount-1)]
    chartList.insert(0, heading)

    for key, value in countries.items():
        chartList[value][0] = key

    for i in jsonData:
        if i["country"] != "" and i["sector"] != "" and type(i["intensity"]) == int:
            if chartList[countries[i["country"]]][sectors[i["sector"]]] is None:
                chartList[countries[i["country"]]][sectors[i["sector"]]] = i["intensity"]
            else:
                if chartList[countries[i["country"]]][sectors[i["sector"]]] < i["intensity"]:
                    chartList[countries[i["country"]]][sectors[i["sector"]]] = i["intensity"]
    sectorList = [i for i in sectors]
    chartList = json.dumps(chartList[1:])

    return render(request, "index.html", {"jsonData": chartList, "tableData": tableData, "sectors": sectorList})
