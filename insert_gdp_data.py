__author__ = 'Shiven'
import xlrd
import os
import pymongo


def read_gdp_data():
    book = xlrd.open_workbook(os.path.dirname(__file__) + '/resources/GDPData.xlsx')
    print book.nsheets
    print book.sheet_names()

    db = connect_mongo()
    posts = db.gdp

    sheet = book.sheet_by_index(0)
    print sheet.name, sheet.nrows, sheet.ncols

    print sheet.row_values(0)

    for cell_pos in range(1, 7):
        document = {}
        cell_data = sheet.cell(0, cell_pos)
        country = cell_data.value
        document["country"] = country
        gdp_map = {}
        document["gdp"] = gdp_map

        for row_pos in range(1, 65):
            row_data_year = sheet.cell(row_pos, 0)
            row_data_gdp = sheet.cell(row_pos, cell_pos)
            gdp_map[str(int(row_data_year.value))] = int(row_data_gdp.value)

        posts.insert(document)
    print document


def connect_mongo():
    client = pymongo.MongoClient('localhost', 27017)
    db = client.f1db
    return db


if __name__ == "__main__":
    read_gdp_data()
