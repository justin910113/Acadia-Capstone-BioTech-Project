import pandas as pd
from openai import OpenAI
from pydantic import BaseModel
import o3studio.settings

o3studio.settings.init_dev()

class KPIMetric(BaseModel):
    search_metric: str
    metric_name: str
    metric_type: str
    metric_unit: str
    time_period: str
    metric_value: str
    explanation: str


def extract_kpi(search_metric, search_chunks):

    # Construct LLM prompt
    llm_prompt = f"""
you are an data entry operator. using ONLY the data provided in [data], extract the metrics requested in [metrics] using the format provided in [format]. Return ONLY data that is provided in [data] to not make assumptions or make up data.

If there are multiple matches you should return all of them. Return all variations of the metric, for example different time periods, different metrics (both the amount and growth numbers), different regions, etc.

if you are unable to find the metric, return an empty list.

[data]

{" ".join(search_chunks)}

[metrics]
{search_metric}

[format]
{' | '.join(KPIMetric.model_fields)}

metric_name: states the name of the kpi to extracted. this should be as comprehensive as possible and take into account any hierarchical structure in a table or so where the name is split across different lines or grouped together.
metric_type: describes the type of metric, for example: growth_yoy for year over year growth, growth_qoq for quarter over quarter sequential growth, currency for dollar or other currency amounts, amount for a count or other numeric amount
metric_unit: extract the units for the table, for example m for millions, $m for $ in millions, % for percentage. Note that this information is often contained in the header or footer of the table.  
time_period: describes the time period of the metric, for example: 2024Q1 for the first quarter of 2024, FY2024 for the year 2024, FYQ1 for the first quarter when year is not given 
metric_value: the value of the metric, for example: 9% for 9 percent growth, 1000000 for 1 million dollars, 1000000000 for 1 billion amount
explanation: extract commentary about this number, for example why it has changed. this might be contained in a footnote to the table.

example:
{search_metric} | global room nights Europe | growth_yoy | % | 2024Q1 | 9% | due to higher retail pricing, partially offset by a higher mix of subscribers to wholesale offerings
{search_metric} | global room nights Americs | growth_yoy | % | 2024Q1 | 9% | Null
{search_metric} | global room nights Europe | growth_yoy | % | 2023Q1 | 9% | Null
{search_metric} | global room nights Americs | growth_yoy | % | 2023Q1 | 9% | Null
{search_metric} | Average Daily Rate Europe | currency | $ | 2024Q1 | $7.18 | due to higher retail pricing, partially offset by a higher mix of subscribers to wholesale offerings
{search_metric} | Average Daily Rate Americs | currency | $ | 2024Q1 | $7.18 | Null
{search_metric} | Average Daily Rate Europe | currency | $ | 2023Q1 | $7.18 | Null
{search_metric} | Average Daily Rate Americs | currency | $ | 2023Q1 | $7.18 | Null

extract all values the best you can do with the information provided. Fill with "Null" when one of the fields cannot be extracted. 

return only the data in a pipe delimited string and nothing else.

=> output:
"""

    # Initialize OpenAI client
    client = OpenAI(api_key=o3studio.settings.creds['openai'])

    # Make API call
    # completion = client.beta.chat.completions.parse(
    completion = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "Extract the KPI metric information from the provided text."},
            {"role": "user", "content": llm_prompt},
        ],
        temperature=0
        # response_format=KPIMetric,
    )

    # Get the parsed result
    result = completion.choices[0].message.content.strip()
    
    # Split the result into lines and create DataFrame
    lines = [line.strip() for line in result.split('\n') if line.strip()]
    df_metrics = pd.DataFrame([line.split('|') for line in lines], 
                            columns=list(KPIMetric.model_fields))

    return df_metrics




