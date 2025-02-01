import pandas as pd
from django.http import HttpResponse


class Json:

    @staticmethod
    def to_excel(json_data):
        df = pd.DataFrame(json_data)

        styled_df = df.style.set_properties(
            subset=df.columns, **{"text-align": "center"}
        ).set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("text-align", "center"),
                        ("font-weight", "bold"),
                    ],
                }
            ]
        )

        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = 'attachment; filename="data.xlsx"'

        styled_df.to_excel(response, index=False, engine="openpyxl")

        return response
