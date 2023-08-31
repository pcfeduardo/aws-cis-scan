import pandas as pd

class ExcelReportGenerator:

    def __init__(self, vuln_data, report_file):
        self.vuln_data = vuln_data
        self.report_file = report_file

    def generate(self):
        with pd.ExcelWriter(self.report_file) as writer:
            self._generate_general_sheet(writer)
            self._generate_total_sheet(writer)
            self._generate_total_by_service_sheet(writer)
            self._generate_all_sheet(writer)

    def _generate_general_sheet(self, writer):
        data = self.vuln_data['GENERAL']
        if data:
            pd.DataFrame(data).to_excel(writer, sheet_name='GENERAL', index=False)

    def _generate_total_sheet(self, writer):
        total_df = pd.DataFrame(self.vuln_data['TOTAL'])
        total_df['Total'] = total_df.sum(axis=1)
        total_df.to_excel(writer, sheet_name='TOTAL', index=False)

    def _generate_total_by_service_sheet(self, writer):
        df = pd.DataFrame(self.vuln_data['TOTAL_BY_SERVICE'])
        pivot_table = df.pivot_table(index='Service', columns='Severity', aggfunc=len, fill_value=0)
        pivot_table['Total'] = pivot_table.sum(axis=1)
        sum_row = pd.DataFrame(pivot_table.sum(axis=0)).transpose()
        sum_row.index = ['Total']
        pivot_table = pd.concat([pivot_table, sum_row])
        pivot_table.to_excel(writer, sheet_name='TOTAL_BY_SERVICE')

    def _generate_all_sheet(self, writer):
        pd.DataFrame(self.vuln_data['ALL']).to_excel(writer, sheet_name='ALL', index=False)
