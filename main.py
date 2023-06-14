import json
import os
import re
import shutil

import pandas as pd
import pdfkit
import requests

from html_format import report_template
from summary_data import summaries


class Report:
    def __init__(self, start_time, end_time, batch_name=None, academy_module=None):
        self.start_time = start_time
        self.end_time = end_time
        self.academy_modules = [academy_module] if academy_module is not None else None
        self.batch_names = [batch_name] if batch_name is not None else None

        self.session_id = "4ffc9fbd-f567-45d3-9ae5-08bd2729d507"
        self.url = "https://metabase.interviewbit.com/api/card/7465/query"

    def generate_payload(self):
        parameters = [
            {
                "type": "date/single",
                "value": self.start_time,
                "target": ["variable", ["template-tag", "start_time"]],
                "id": "1106e160-8917-ff9b-a2b9-eb1b18b00245"
            },
            {
                "type": "date/single",
                "value": self.end_time,
                "target": ["variable", ["template-tag", "end_time"]],
                "id": "dc9ee437-3bb7-a49e-c00a-a8ff60ec0147"
            },
            #     {
            #         "type":"category",
            #         "value":["Bipin Kalra"],
            #         "target":["variable",["template-tag","instructor_name"]],
            #         "id":"2a311680-60f3-aa07-c46b-33fb3219f815"
            #     },
        ]

        if self.batch_names is not None:
            parameters.append(
                {
                    "type": "string/=",
                    "value": self.batch_names,
                    "target": ["dimension", ["template-tag", "super_batches"]],
                    "id": "0fd0313c-6a6a-529f-3e52-0e20b4d98a2c"
                }
            )

        if self.academy_modules is not None:
            parameters.append(
                {
                    "type": "string/=",
                    "value": self.academy_modules,
                    "target": ["dimension", ["template-tag", "academy_modules"]],
                    "id": "7f769207-4116-ae70-ce71-94ee6ef80b0a"
                },
            )

        payload = {"ignore_cache": False, "collection_preview": False, "parameters": parameters}
        return json.dumps(payload)

    def make_connection(self):
        payload = self.generate_payload()
        headers = {"Content-Type": "application/json", 'X-Metabase-Session': self.session_id}
        response = requests.post(self.url, headers=headers, data=payload)
        return response

    def get_data(self):
        response = self.make_connection()
        if response.status_code not in [200, 202]:
            raise Exception("Connection Error")

        data = response.json()['data']
        column_metadata = data['results_metadata']['columns']
        column_names = [item['display_name'] for item in column_metadata]
        report_df = pd.DataFrame(data['rows'], columns=column_names)
        report_df['class_time'] = pd.to_datetime(report_df['class_time'])

        report_df['summary'] = ""
        classes = report_df['class_title'].unique().tolist()
        for class_ in classes:
            summary = summaries.get(class_.strip(), "")
            if summary != "":
                content = summary.strip().split("\n")[0] + "<br><br>"

                points = summary.strip().split("\n")[1:]
                points = ["<li>" + point.strip()[3:] + "</li>" for point in points]
                points = "<ul class='summ_points'>" + "".join(points) + "</ul>"

                content += points
                content = re.sub(r'\n', '<br>', content)
                content = re.sub(r'    ', '&nbsp;&nbsp;&nbsp;&nbsp;', content)
                report_df.loc[report_df['class_title'] == class_, 'summary'] = content

        return report_df

    def generate_report(self):
        data = self.get_data()
        batch_names = data['batch_names'].unique().tolist()
        academy_module = data.iloc[0]['module_name']
        print(f"Batches found: {batch_names}")

        dir_path = f"{academy_module} ({self.start_time} to {self.end_time})"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        else:
            print(f"Directory {dir_path} is already present, this process will delete the already existing materials "
                  f"inside this directory")
            shutil.rmtree(dir_path)
            os.makedirs(dir_path)

        for batch_name in batch_names:
            df = data[data['batch_names'] == batch_name]
            records = df[['class_title', 'meeting_link', 'summary']].to_dict('records')

            html_code = report_template.format(module_name=academy_module,
                                               batch_name=batch_name,
                                               class_data=records)

            report_path = os.path.join(dir_path, batch_name + ".pdf")
            pdfkit.from_string(html_code, report_path)

            # html_file_path = batch_name + ".html"
            # with open(html_file_path, 'w', encoding='utf-8') as file:
            #     file.write(html_code)

        print("Successful, all pages for respective batches are generated and stored")


if __name__ == "__main__":
    # Usage: For single batch
    report = Report(
        start_time="2023-05-12",
        end_time="2023-05-31",
        batch_name="DSML Feb23 Beginner Mon 2",
        academy_module="Beginner Python 1"
    )
    report.generate_report()

    # Usage: For all batches within a module
    report = Report(
        start_time="2023-05-12",
        end_time="2023-05-31",
        academy_module="Beginner Python 1"
    )
    report.generate_report()
