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

includefields = [1,2,3,4,5,6,7]

def report(openv, tenants, queryString, outdir, logo):
    for tenant in tenants:
        print("Tenant is " + tenant['uniqueId'] + " - " + tenant['name'])

        #
        # Initialize pdf doc and header/footer
        #
        pw = max(len(includefields)*40, 216) # min of 8.5 in, but expands based on # columns
        ph = 279 # 11 in.
        pdf = helpers.PDF_STD_HEADER_FOOTER(tenant, "Software Inventory Report", None, None, None, None, logo, 'P', 'mm', (pw,ph))
        pdf.alias_nb_pages()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        #
        # Get resources
        #

        if queryString is None:
            queryString = 'agentInstalled:true'
        resources = objects.get_objects(openv, 'resources', tenant=tenant['uniqueId'], queryString=queryString)

        for ridx,resource in enumerate(resources):
            apps = objects.get_object(openv, 'discoveredApps', resource['id'], tenant['uniqueId'])
            services = objects.get_object(openv, 'discoveredServices', resource['id'], tenant['uniqueId'])
            df_apps = pd.DataFrame(pd.json_normalize(apps))
            df_services = pd.DataFrame(pd.json_normalize(services))


            #
            # Add the apps pdf table
            #
            if ridx > 0:
                pdf.add_page()
            pdf.set_font('Helvetica', 'B', 11)
            pdf.cell(w=pdf.epw, txt=f'Installed applications for {resource["name"]}', align='L', ln=1)
            pdf.ln(5)
            if len(df_apps) > 0:
                for fld in ['installedDate', 'createdDate', 'modifiedDate']:
                    if fld in df_apps:
                        df_apps[fld] = pd.to_datetime(df_apps[fld]).dt.strftime('%Y-%m-%d')
                    else:
                        df_apps[fld] = '-'
                df_apps.fillna('-', axis=1, inplace=True)
                df_apps.replace(r'^\s*$', '-', regex=True, inplace=True)
                helpers.pdf_table_from_df(pdf, df_apps, df_apps.columns)
            else:
                pdf.ln(10)
                pdf.cell(w=pdf.epw, txt="No installed applications discovered for this device.", align='C', ln=1)

            #
            # Add the services pdf table
            #
            pdf.add_page()
            pdf.set_font('Helvetica', 'B', 11)
            pdf.cell(w=pdf.epw, txt=f'Installed services for {resource["name"]}', align='L', ln=1)
            pdf.ln(5)
            if len(df_services) > 0:
                #for fld in ['installedDate', 'createdDate', 'modifiedDate']:
                #    df_services[fld] = pd.to_datetime(df_services[fld]).dt.strftime('%Y-%m-%d')
                df_services.fillna('-', axis=1, inplace=True)
                df_services.replace(r'^\s*$', '-', regex=True, inplace=True)
                helpers.pdf_table_from_df(pdf, df_services, df_services.columns)
            else:
                pdf.ln(10)
                pdf.cell(w=pdf.epw, txt="No installed services discovered for this device.", align='C', ln=1)


        #
        # Prep the output directory
        #
        repdir = f'{outdir}{os.sep}{tenant["name"]}'
        if not os.path.exists(repdir):
            os.makedirs(repdir)

        #
        # Write the pdf file
        #
        pdf_file = "software_inventory_report.pdf"
        pdf.output(f'{repdir}{os.sep}{pdf_file}')


if __name__ == "__main__":
    # execute only if run as a script
    report() 