"""
Generate the HTML report for the Shape Data Engineering Challenge.
"""

from datetime import datetime
import pandas as pd
from data.log_data import get_log_dataframe


def get_html_content():
    """Get the HTML content for the report."""
    # Load data
    print("Loading data...")
    equipment = pd.read_json("data/equipment.json")
    equipment_sensors = pd.read_csv("data/equipment_sensors.csv")
    equipment_failure_sensors = get_log_dataframe("data/extracted/equipment_failure_sensors/equpment_failure_sensors.txt")

    # Create combined dataset
    print("Processing data...")
    equipment_failures = (
        equipment
        .merge(equipment_sensors, on="equipment_id", how="left")
        .merge(equipment_failure_sensors, on="sensor_id", how="left")
        .drop_duplicates()
    )

    equipment_failures = equipment_failures[equipment_failures["status"] == "ERROR"]
    equipment_failures.rename(columns={"name": "equipment_name", "group_name": "equipment_group"}, inplace=True)

    # Question 1: How many equipment failures happened?
    print("Answering question 1...")
    q1_resultv1 = equipment_failures \
        .shape[0]

    q1_resultv2 = equipment_failures \
        .drop_duplicates(subset=["equipment_id", "timestamp"]) \
        .shape[0]

    # Question 2: Which piece of equipment had most failures?
    print("Answering question 2...")
    q2_result = equipment_failures \
        .drop_duplicates(subset=["equipment_id", "timestamp"]) \
        .groupby(["equipment_id", "equipment_name"]).size().rename("failures") \
        .sort_values(ascending=False) \
        .reset_index()

    q2_result["percentage"] = round(q2_result["failures"] / q2_result["failures"].sum() * 100, 2)
    q2_result["percentage"] = q2_result["percentage"].astype(str) + "%"

    # Question 3: Average failures per asset across equipment groups
    print("Answering question 3...")
    q3_result = equipment_failures \
        .groupby(["equipment_group", "equipment_id"])["timestamp"].nunique().rename("failures") \
        .reset_index()

    q3_result = q3_result \
        .groupby("equipment_group").agg(
            equipment_list=("equipment_id", lambda x: sorted(list(x))),
            avg_failures=("failures", "mean"),
            total_failures=("failures", "sum")
        ).sort_values(by="total_failures", ascending=True) \
        .reset_index()

    q3_result["percentage"] = round(q3_result["total_failures"] / q3_result["total_failures"].sum() * 100, 2)
    q3_result["percentage"] = q3_result["percentage"].astype(str) + "%"

    # Question 4: Rank sensors by failures per asset
    print("Answering question 4...")
    q4_result = equipment_failures \
        .groupby(["equipment_id", "equipment_name", "equipment_group", "sensor_id"]).size().rename("failures") \
        .reset_index() \
        .sort_values(by=["equipment_id", "failures"], ascending=[True, False]) \
        .groupby("equipment_id").head(3)

    # Generate HTML
    print("Generating HTML...")

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Shape Data Engineering Challenge - Answers</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                min-height: 100vh;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                padding: 40px;
            }}
            
            h1 {{
                color: #667eea;
                margin-bottom: 10px;
                font-size: 2.5em;
                text-align: center;
            }}
            
            .subtitle {{
                text-align: center;
                color: #666;
                margin-bottom: 40px;
                font-size: 1.1em;
            }}
            
            .question {{
                margin: 40px 0;
                padding: 25px;
                background: #f8f9fa;
                border-left: 5px solid #667eea;
                border-radius: 5px;
            }}
            
            .question h2 {{
                color: #667eea;
                margin-bottom: 15px;
                font-size: 1.5em;
            }}
            
            .answer {{
                margin-top: 20px;
                padding: 20px;
                background: white;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            
            .answer-numbers-container {{
                display: flex;
                gap: 20px;
                margin-bottom: 15px;
            }}
            
            .answer-number-box {{
                flex: 1;
                display: flex;
                flex-direction: column;
            }}
            
            .answer-number {{
                font-size: 2em;
                font-weight: bold;
                color: #764ba2;
                text-align: center;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border-radius: 5px;
                margin-bottom: 10px;
            }}
            
            .answer-number-label {{
                text-align: center;
                color: #666;
                font-size: 0.9em;
                padding: 0 10px;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
                font-size: 0.95em;
            }}
            
            th {{
                background: #667eea;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: 600;
            }}
            
            td {{
                padding: 10px 12px;
                border-bottom: 1px solid #e0e0e0;
            }}
            
            tr:hover {{
                background: #f5f5f5;
            }}
            
            .footer {{
                margin-top: 50px;
                padding-top: 20px;
                border-top: 2px solid #e0e0e0;
                text-align: center;
                color: #666;
                font-size: 0.9em;
            }}
            
            @media (max-width: 768px) {{
                .container {{
                    padding: 20px;
                }}
                
                h1 {{
                    font-size: 2em;
                }}
                
                .answer-numbers-container {{
                    flex-direction: column;
                }}
                
                table {{
                    font-size: 0.85em;
                }}
                
                th, td {{
                    padding: 8px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Shape Data Engineering Challenge</h1>
            <p class="subtitle">FPSO Equipment Failure Analysis</p>
            
            <!-- Question 1 -->
            <div class="question">
                <h2>1. How many equipment failures happened?</h2>
                <div class="answer">
                    <div class="answer-numbers-container">
                        <div class="answer-number-box">
                            <div class="answer-number">{q1_resultv1:,}</div>
                            <div class="answer-number-label">Total failures</div>
                        </div>
                        <div class="answer-number-box">
                            <div class="answer-number">{q1_resultv2:,}</div>
                            <div class="answer-number-label">Total equipment failures<br>(unique events per equipment and timestamp)</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Question 2 -->
            <div class="question">
                <h2>2. Which piece of equipment had most failures?</h2>
                <div class="answer">
                    {q2_result.to_html(index=False, classes='', table_id='q2-table', escape=False)}
                    <p style="margin-top: 15px; color: #666;">
                        <strong>Equipment with most failures:</strong> {q2_result.iloc[0]['equipment_name']} (ID: {q2_result.iloc[0]['equipment_id']}) 
                        with {q2_result.iloc[0]['failures']:,} failures.
                    </p>
                </div>
            </div>
            
            <!-- Question 3 -->
            <div class="question">
                <h2>3. Find the average amount of failures per asset across equipment groups, ordered by the total number of failures in ascending order.</h2>
                <div class="answer">
                    {q3_result.to_html(index=False, classes='', table_id='q3-table', escape=False)}
                </div>
            </div>
            
            <!-- Question 4 -->
            <div class="question">
                <h2>4. For each asset, rank the sensors which present the most number of failures, and also include the equipment group in the output.</h2>
                <div class="answer">
                    {q4_result.to_html(index=False, classes='', table_id='q4-table', escape=False)}
                    <p style="margin-top: 15px; color: #666;">
                        <em>Showing the top 3 sensors with most failures for each equipment.</em>
                    </p>
                </div>
            </div>
            
            <div class="footer">
                <p>Shape Data Engineering Challenge - Analysis Report</p>
                <p>Generated by: Matheus Bragança</p>
                <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </div>
    </body>
    </html>
    """

    return html_content


def generate_html_report(output_file: str) -> None:
    """Generate the HTML report."""
    try:
        html_content = get_html_content()
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"HTML report generated successfully: {output_file}")
    except Exception as e:
        print(f"Error generating HTML report: {e}")
        raise


if __name__ == "__main__":
    generate_html_report("matheus_braganca_teste_shape.html")
