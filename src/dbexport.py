import xlsxwriter

import dbdata
from os.path import exists


def export():
    workbook = xlsxwriter.Workbook('export.xlsx')
    header_cell_format = workbook.add_format({'bold': True, 'border': True, 'bg_color': '#C6EFCE'})
    for n in range(0, 7):
        if n == 0:
            worksheet = workbook.add_worksheet("uid")
            worksheet.write(0, 0, "uid", header_cell_format)
            worksheet.write(0, 1, "VF_ID", header_cell_format)
            data = dbdata.get_all_data_of_uid()
        elif n == 1:
            worksheet = workbook.add_worksheet("name")
            worksheet.write(0, 0, "uid", header_cell_format)
            worksheet.write(0, 1, "Vorname", header_cell_format)
            worksheet.write(0, 2, "Nachname", header_cell_format)
            data = dbdata.get_all_data_of_name()
        elif n == 2:
            worksheet = workbook.add_worksheet("getr")
            worksheet.write(0, 0, "Getränke ID", header_cell_format)
            worksheet.write(0, 1, "Name", header_cell_format)
            worksheet.write(0, 2, "Kosten", header_cell_format)
            data = dbdata.get_all_data_of_getr()
        elif n == 3:
            worksheet = workbook.add_worksheet("ess")
            worksheet.write(0, 0, "EID", header_cell_format)
            worksheet.write(0, 1, "EPreis", header_cell_format)
            worksheet.write(0, 2, "E Datum", header_cell_format)
            data = dbdata.get_all_data_of_ess()
        elif n == 4:
            worksheet = workbook.add_worksheet("persget")
            worksheet.write(0, 0, "UID", header_cell_format)
            worksheet.write(0, 1, "Getränke ID", header_cell_format)
            worksheet.write(0, 2, "Zähler", header_cell_format)
            data = dbdata.get_all_data_of_persget()
        elif n == 5:

            worksheet = workbook.add_worksheet("persess")
            worksheet.write(0, 0, "UID", header_cell_format)
            worksheet.write(0, 1, "Essens ID", header_cell_format)
            worksheet.write(0, 2, "Zähler", header_cell_format)
            data = dbdata.get_all_data_of_persess()
        elif n == 6:
            worksheet = workbook.add_worksheet("stay")
            worksheet.write(0, 0, "UID", header_cell_format)
            worksheet.write(0, 1, "Start", header_cell_format)
            worksheet.write(0, 2, "Ende", header_cell_format)
            worksheet.write(0, 3, "Zähler", header_cell_format)
            data = dbdata.get_all_data_of_stay()
        body_cell_format = workbook.add_format({'border': True})

        for i in data:
            for a in i:
                worksheet.write(data.index(i)+1, i.index(a), a, body_cell_format)
        print(str(worksheet.get_name() + ' rows written successfully to ' + workbook.filename))
    workbook.close()
    if exists("export.xlsx"):
        return "Exported successfully"
    else:
        return "Export failed"
