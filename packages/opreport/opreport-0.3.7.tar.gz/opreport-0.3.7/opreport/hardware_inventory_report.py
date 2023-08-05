import opreport.helpers as helpers
import opreport.objects as objects
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import  matplotlib.dates as mdates
import os
import math
import re
import xlsxwriter

ALL_COLUMNS = {
    "id": "Resource ID",

}

DEFAULT_FIELD_LIST = [
    'client.name',
    'name',
    'resourceType',
    'make',
    'model',
    'ipAddress',
    'osName',
    'serialNumber'
]

DEFAULT_HEADERS = {
    'client.name': 'Customer Name',
    'id': 'ID',
    'name': 'name',
    'resourceType': 'Resource Type',
    'make': 'Make',
    'model': 'Model',
    'ipAddress': 'IP Address',
    'osName': 'OS',
    'serialNumber': 'Serial Number'
}

def getfields(openv, tenants, extrafields):
    df = []
    for tenant in tenants:
        queryString = 'type:DEVICE'
        resources = objects.get_objects(openv, 'resources', tenant=tenant['uniqueId'], queryString=queryString)
        if len(resources)==0:
            continue
        if extrafields:
            resource_detail = objects.get_object(openv, 'resource', resources[0]['id'], tenant=tenant['uniqueId'])
            resources[0] = {**resources[0], **resource_detail}
        df = pd.DataFrame(pd.json_normalize(resources))
        for column in df.columns:
            try:
                df = df.drop([f'generalInfo.{column}'], axis=1)
            except:
                pass
        df.columns = df.columns.str.replace('generalInfo.', '', regex=False)
        break        
    retval =  df.columns.values
    retval.sort()
    return retval

def get_cpu_count(cpus):
    if cpus == 'nan':
        numcpus = ''
    else:
        numcpus = len(eval(cpus))
        if numcpus == 0:
            numcpus = ''
    return numcpus

def report(openv, tenants, includefields, extrafields, format, queryString, outdir, logo):
    for tenant in tenants:
        print("Tenant is " + tenant['uniqueId'] + " - " + tenant['name'])

        #
        # Get resources
        #

        if includefields is None:
            includefields = DEFAULT_FIELD_LIST
        if queryString is None:
            queryString = 'type:DEVICE'
        resources = objects.get_objects(openv, 'resources', tenant=tenant['uniqueId'], queryString=queryString)
        resources_extra = []
        if extrafields:
            for ridx, resource in enumerate(resources):
                print(f'  Getting extra field details for {resource["name"]}')
                resource_detail = objects.get_object(openv, 'resource', resource['id'], tenant=tenant['uniqueId'])
                resources[ridx] = {**resources[ridx], **resource_detail}
                resources_extra.append(resource_detail)


        #
        # INITIALIZE PDF DOC
        #

        if format == 'pdf' :
            pw = max(len(includefields)*40, 216) # min of 8.5 in, but expands based on # columns
            ph = 279 # 11 in.
            pdf = helpers.PDF_STD_HEADER_FOOTER(tenant, "Hardware Inventory Report", None, None, None, None, logo, 'P', 'mm', (pw,ph))
            pdf.alias_nb_pages()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()



        df = pd.DataFrame(pd.json_normalize(resources))
        for column in df.columns:
            try:
                df = df.drop([f'generalInfo.{column}'], axis=1)
            except:
                pass
        df.columns = df.columns.str.replace('generalInfo.', '', regex=False)


        repdir = f'{outdir}{os.sep}{tenant["name"]}'
        if not os.path.exists(repdir):
            os.makedirs(repdir)
        if format == 'pdf' :
            if len(df) > 0:
                pdf.set_font('Helvetica', 'B', 11)
                pdf.cell(w=pdf.epw, txt=f'Hardware Inventory Details', align='L', ln=1)
                pdf.ln(5)

                pdf.set_fill_color(224, 102, 54)
                pdf.set_text_color(255,255,255)
                pdf.set_font('Helvetica', 'B', 9)
                line_height = pdf.font_size * 4
                col_width = pdf.epw / len(includefields) # distribute content evenly as baseline
                for colidx,column in enumerate(includefields):
                    border = 'TB'
                    ln = 3
                    if colidx == 0:
                        border = 'LTB'
                    elif colidx == len(includefields)-1:
                        border = 'TBR'
                        ln = 1
                    pdf.multi_cell(col_width, line_height, column, border=border, ln=ln, max_line_height=pdf.font_size, fill=True, align='C')

                pdf.set_text_color(0,0,0)
                pdf.set_font('Helvetica', '', 7)
                line_height = pdf.font_size * 2
                iter = df.iterrows()
                try:
                    while True:
                        nextrec = next(iter)
                        idx = nextrec[0]
                        rec = nextrec[1]
                        if idx%2 == 0:
                            pdf.set_fill_color(252, 245, 233)
                        else:
                            pdf.set_fill_color(249, 234, 213)

                        numrowsmax = int(math.ceil(max([pdf.get_string_width(str(rec[column]))/col_width for column in includefields if not pd.isna(rec[column])])))
                        this_line_height = line_height*numrowsmax
                        for colidx, column in enumerate(includefields):
                            border = 'TB'
                            ln = 3
                            if colidx == 0:
                                border = 'LTB'
                            elif colidx == len(includefields)-1:
                                border = 'TBR'
                                ln = 1
                            colval = rec[column]
                            if pd.isna(colval):
                                colval = ""
                            else:
                                colval = str(colval)
                            if column == 'osName':
                                colval = re.sub(r' [.\d]+ Build.*','', colval)
                            pdf.multi_cell(col_width, this_line_height, colval, border=border, ln=ln, max_line_height=pdf.font_size, fill=True, align='C')
                except StopIteration:
                    pass   
            else:
                pdf.ln(60)
                pdf.cell(w=pdf.epw, txt="No Devices found for this client.", align='C')

            pdf_file = "hardware_inventory_report.pdf"
            pdf.output(f'{repdir}{os.sep}{pdf_file}')

        elif format == 'excel':
            dfout = pd.DataFrame(columns=includefields)
            if len(df) > 0:
                for cidx,column in enumerate(includefields):
                    if column in df.columns:
                        if column == 'cpus':
                            cpudf = pd.json_normalize(pd.json_normalize(df['cpus'])[0])
                            if 'processorName' in cpudf.columns:
                                dfout['cpus'] = cpudf['processorName']
                            else:
                                dfout['cpus'] = ''
                            if 'numberOfCores' in cpudf.columns:
                                dfout.insert(cidx+1, 'cpus.cores', cpudf['numberOfCores'])
                            else:
                                dfout.insert(cidx+1, 'cpus.cores', '')
                            dfout.insert(cidx+1, 'cpus.count', df['cpus'].astype(str).apply(get_cpu_count))

                        else:
                            dfout[column] = df[column]
            filename = "hardware_inventory_report.xlsx"
            writer = pd.ExcelWriter(f'{repdir}{os.sep}{filename}', engine="xlsxwriter")
            dfout.to_excel(writer, index=False, sheet_name='Hardware Inventory')
            workbook  = writer.book
            worksheet = writer.sheets['Hardware Inventory']
            for i, col in enumerate(dfout.columns):
                column_len = max(min(max(dfout[col].astype(str).str.len().max(), len(col) + 2),100),20)
                if pd.isna(column_len):
                    column_len = 20
                worksheet.set_column(i, i, column_len)
            writer.save()




if __name__ == "__main__":
    # execute only if run as a script
    report() 