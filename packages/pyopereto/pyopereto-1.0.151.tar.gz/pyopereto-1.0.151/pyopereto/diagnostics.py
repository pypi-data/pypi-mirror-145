import os
import logging
from datetime import datetime
import tempfile
from pyopereto.client import OperetoClient
from optparse import OptionParser
import importlib

logger = logging.getLogger(__name__)
TEMP_DIR = tempfile.gettempdir()
HOME_DIR = os.path.expanduser("~")


def parse_options():
    usage = "%prog -s START_TIME -e END_TIME"

    parser = OptionParser(usage=usage)
    parser.add_option("-s", "--start", dest="start_time", help="start time in the datetime ISO format")
    parser.add_option("-e", "--end", dest="end_time", help="end time in the datetime ISO format")
    parser.add_option("-f", "--file", dest="output_file", help="optional output file name")
    (options, args) = parser.parse_args()
    if not options.start_time or not options.end_time:
        parser.error('Time range must be provided.')
    return (options, args)


def remove_file_if_exists(file):
    if os.path.exists(file):
        os.remove(file)

def run_diagnostics(start_date, end_date, output_file=None, test_results={}):

    if output_file is None:
        output_file=os.path.join(HOME_DIR, f'opereto-diagnostics-{str(start_date)}-{str(end_date)}.pdf')


    required_packages = ['matplotlib', 'pandas', 'numpy', 'pdfkit', 'PyPDF2']
    for package in required_packages:
        if not importlib.util.find_spec(package):
            raise Exception(f'Opereto diagnostics requires the following python packages {str(required_packages)}. In addition it requres the wkhtmltopdf executable. Please install them and then re-run this command.')

    import pdfkit
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.backends.backend_pdf

    def create_report(data={}):
        temp_files = []

        def create_temp_file():
            fd, path = tempfile.mkstemp()
            temp_files.append(path)
            return path

        try:
            remove_file_if_exists(output_file)
            title = data['title']
            main_title_flag=False
            if 'tables' in data:
                for table in data['tables']:
                    temp_file = create_temp_file()
                    main_title = ''
                    if not main_title_flag:
                        main_title = f'<h1>{title}</h1>'
                        main_title_flag=True
                    html_table = table['df'].to_html()
                    table_title = table['title']
                    body = f"""
                        <html><body>
                        {main_title}
                        <h2>{table_title}</h2>
                        <head>
                            <meta name="pdfkit-page-size" content="Legal"/>
                            <meta name="pdfkit-orientation" content="Landscape"/>
                            <style> 
                              table, th, td {{font-size:12pt; border:1px solid #333333; border-collapse:collapse; text-align:left;}}
                              th, td {{padding: 5px;}}
                            </style>
                        </head>
                        {html_table}
                        </body></html>"""
                    pdfkit.from_string(body, temp_file)

            if 'plots' in data:
                pdf_doc = matplotlib.backends.backend_pdf.PdfPages
                for plot in data['plots']:
                    temp_file = create_temp_file()
                    with pdf_doc(temp_file) as pdf:
                        fig, axs = plt.subplots(figsize=(8, 4))
                        axs.set_title(plot['title'])
                        axs.set_xlabel(plot.get('xlabel') or 'Time')
                        axs.set_ylabel(plot.get('ylabel') or 'Value')
                        axs.plot(plot['df']['value'])
                        plt.tight_layout()
                        pdf.savefig(fig)
                        plt.close()

            # Merge all PDFs
            import PyPDF2
            pdfWriter = PyPDF2.PdfFileWriter()
            pdfWriter.addMetadata({
                '/Author': 'Dror Russo',
                '/Title': 'Opereto Diagnostics',
                '/CreationDate': str(datetime.today())
            })

            for filename in temp_files:
                pdf_reader = PyPDF2.PdfFileReader(filename)
                for page_num in range(pdf_reader.numPages):
                    page_obj = pdf_reader.getPage(page_num)
                    pdfWriter.addPage(page_obj)
            pdfOutputFile = open(output_file, 'wb')
            pdfWriter.write(pdfOutputFile)
            pdfOutputFile.close()

        finally:
            for filename in temp_files:
                remove_file_if_exists(filename)

    final_results = []
    client = OperetoClient()

    start_time = datetime.fromisoformat(str(start_date))
    end_time = datetime.fromisoformat(str(end_date))
    timedelta = end_time - start_time
    if timedelta.total_seconds() > 60 * 60 * 24:
        raise Exception('Time range must not exceed 24 hours')

    main_title = f'Opereto system diagnostics - from {start_date} to {end_date} - measure intervals: 1 minute.'
    print(main_title)

    start = 0
    size = 10000
    request_data = {'start': start, 'limit': size,
                    'filter': {'datetime_range': {'from': str(start_date), 'to': str(end_date)}}}
    res = client._call_rest_api('post', '/search/diagnostics', data=request_data, start=start, limit=size, error='Cannot fetch diagnostics data')
    all_diagnostics = res
    if res is not None:
        while len(res) == size:
            start = start + size
            request_data = {'start': start, 'limit': size,
                            'filter': {'datetime_range': {'from': str(start_date), 'to': str(end_date)}}}
            res = client._call_rest_api('post', '/search/diagnostics', limit=size, data=request_data,
                                        error='Cannot fetch diagnostics data')
            all_diagnostics += res

    if all_diagnostics:
        print(f'Total search entries found: {len(all_diagnostics)}\n')
        for entry in all_diagnostics:
            for kpi, kpivalue in entry['value'].items():
                if kpivalue is not None:
                    final_results.append({'kpi': kpi, 'time': np.datetime64(entry['orig_date']), 'value': int(kpivalue)})

        ## All KPI
        df = pd.DataFrame(final_results)

        def _get_kpi_table(prefix):
            try:
                kpi_final_table = df[df.kpi.str.startswith(tuple([prefix]))]
            except:
                kpi_final_table=None
            finally:
                return kpi_final_table

        data = {
            'title': main_title,
            'tables': [

            ],
            'plots': [

            ]
        }

        ## Opereto Benchmark test
        if test_results:
            final_test_results=[]
            for kpi, results in test_results['data'].items():
                for value in results['values']:
                    final_test_results.append({
                        'kpi': kpi,
                        'criteria': results['criteria'],
                        'status': results['status'].upper(),
                        'value': value
                    })

            final_status = test_results['status'].upper()
            test_results_df = pd.DataFrame(final_test_results)
            data['tables'].append(
                {
                    'df': test_results_df.groupby(['kpi', 'status', 'criteria']).describe().reset_index(level=['kpi', 'status', 'criteria']),
                    'title': f'API Response Times Benchmark Test [{final_status}]'
                }
            )

        ## API calls
        api_per_url = _get_kpi_table('REST')
        if api_per_url is not None:
            if not api_per_url.empty:
                api_per_url_grouped = api_per_url.groupby([pd.Grouper(key='time', freq='1min'), 'kpi']).sum()
                data['tables'].append(
                    {
                        'df': api_per_url_grouped['value'].round(2).groupby('kpi').describe().reset_index(level='kpi'),
                        'title': 'API calls per URL'
                    }
                )
                data['plots'].append(
                    {
                        'df': api_per_url.groupby([pd.Grouper(key='time', freq='1min')]).sum(),
                        'title': 'Total API Calls Over Time'
                    }
                )

        ## Processes
        processes_kpi = _get_kpi_table('PROCESSES')
        if processes_kpi is not None:
            if not processes_kpi.empty:
                processes_kpi_grouped = processes_kpi.groupby([pd.Grouper(key='time', freq='1min'), 'kpi']).mean()
                data['tables'].append(
                    {
                        'df': processes_kpi_grouped['value'].round(2).groupby('kpi').describe().reset_index(level='kpi'),
                        'title': 'Processes Usage'
                    }
                )
                data['plots'].append(
                    {
                        'df': processes_kpi.groupby([pd.Grouper(key='time', freq='1min')]).mean(),
                        'title': 'Process Execution'
                    }
                )

        ## Environments
        environments_kpi = _get_kpi_table('ENVIRONMENTS')
        if environments_kpi is not None:
            if not environments_kpi.empty:
                environments_kpi_grouped = environments_kpi.groupby([pd.Grouper(key='time', freq='1min'), 'kpi']).mean()
                data['tables'].append(
                    {
                        'df': environments_kpi_grouped['value'].round(2).groupby('kpi').describe().reset_index(level='kpi'),
                        'title': 'Environments Usage'
                    }
                )

        ## Agents
        agents_kpi = _get_kpi_table('AGENTS')
        if agents_kpi is not None:
            if not agents_kpi.empty:
                agents_kpi_grouped = agents_kpi.groupby([pd.Grouper(key='time', freq='1min'), 'kpi']).mean()
                data['tables'].append(
                    {
                        'df': agents_kpi_grouped['value'].round(2).groupby('kpi').describe().reset_index(level='kpi'),
                        'title': 'Agents Usage'
                    }
                )
                data['plots'].append(
                    {
                        'df': agents_kpi.groupby([pd.Grouper(key='time', freq='1min')]).mean(),
                        'title': 'Active Agents'
                    }
                )

        create_report(data)
        print(f'Generated diagnostics file: {output_file}')

    else:
        logger.error('No diagnostics data found for this time range')


if __name__ == "__main__":
    (options, args) = parse_options()
    run_diagnostics(str(options.start_time), str(options.end_time), options.output_file)
