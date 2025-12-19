"""HTML report implementation using Template Method pattern."""

from datetime import datetime

import pandas as pd


class HtmlReport():
    """HTML report generator for failure analysis results."""

    def __init__(self, analysis: dict):
        self.analysis = analysis

    def generate(self) -> str:
        """Generate the HTML report."""
        return f"""
            {self._generate_header()}
            {self._generate_introduction()}
            {self._generate_analysis()}
            {self._generate_footer()}
        """
    
    def _generate_header(self) -> str:
        """Generate the HTML header with styles."""
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Shape Data Engineering Challenge - Answers</title>
            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }
                
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 20px;
                    min-height: 100vh;
                }
                
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 10px;
                    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                    padding: 40px;
                }
                
                /* Navigation Styles */
                .nav-tabs {
                    display: flex;
                    gap: 10px;
                    margin-bottom: 30px;
                    border-bottom: 2px solid #e0e0e0;
                    padding-bottom: 0;
                }
                
                .nav-tab {
                    padding: 12px 24px;
                    background: #f8f9fa;
                    border: none;
                    border-top-left-radius: 8px;
                    border-top-right-radius: 8px;
                    cursor: pointer;
                    font-size: 1em;
                    font-weight: 500;
                    color: #666;
                    transition: all 0.3s ease;
                    border-bottom: 3px solid transparent;
                }
                
                .nav-tab:hover {
                    background: #e9ecef;
                    color: #667eea;
                }
                
                .nav-tab.active {
                    background: white;
                    color: #667eea;
                    border-bottom-color: #667eea;
                }
                
                /* Page Content */
                .page {
                    display: none;
                }
                
                .page.active {
                    display: block;
                }
                
                h1 {
                    color: #667eea;
                    margin-bottom: 10px;
                    font-size: 2.5em;
                    text-align: center;
                }
                
                .subtitle {
                    text-align: center;
                    color: #666;
                    margin-bottom: 40px;
                    font-size: 1.1em;
                }
                
                /* Introduction Page Styles */
                .intro-section {
                    margin: 30px 0;
                    padding: 25px;
                    background: #f8f9fa;
                    border-left: 5px solid #667eea;
                    border-radius: 5px;
                }
                
                .intro-section h2 {
                    color: #667eea;
                    margin-bottom: 15px;
                    font-size: 1.5em;
                }
                
                .intro-section p {
                    margin-bottom: 15px;
                    color: #555;
                }
                
                .intro-section ul,
                .intro-section ol {
                    margin-left: 20px;
                    margin-bottom: 15px;
                    color: #555;
                }
                
                .intro-section li {
                    margin-bottom: 8px;
                }
                
                .tool-card {
                    background: white;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 15px 0;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }
                
                .tool-card h3 {
                    color: #764ba2;
                    margin-bottom: 10px;
                    font-size: 1.2em;
                }
                
                .tool-card p {
                    color: #666;
                    margin-bottom: 5px;
                }
                
                .code-snippet {
                    background: #2d2d2d;
                    color: #f8f8f2;
                    padding: 15px;
                    border-radius: 5px;
                    font-family: 'Courier New', monospace;
                    font-size: 0.9em;
                    overflow-x: auto;
                    margin: 10px 0;
                }
                
                /* Analysis Report Styles */
                .question {
                    margin: 40px 0;
                    padding: 25px;
                    background: #f8f9fa;
                    border-left: 5px solid #667eea;
                    border-radius: 5px;
                }
                
                .question h2 {
                    color: #667eea;
                    margin-bottom: 15px;
                    font-size: 1.5em;
                }
                
                .answer {
                    margin-top: 20px;
                    padding: 20px;
                    background: white;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                }
                
                .answer-numbers-container {
                    display: flex;
                    gap: 20px;
                    margin-bottom: 15px;
                }
                
                .answer-number-box {
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                }
                
                .answer-number {
                    font-size: 2em;
                    font-weight: bold;
                    color: #764ba2;
                    text-align: center;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border-radius: 5px;
                    margin-bottom: 10px;
                }
                
                .answer-number-label {
                    text-align: center;
                    color: #666;
                    font-size: 0.9em;
                    padding: 0 10px;
                }
                
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 15px;
                    font-size: 0.95em;
                }
                
                th {
                    background: #667eea;
                    color: white;
                    padding: 12px;
                    text-align: left;
                    font-weight: 600;
                }
                
                td {
                    padding: 10px 12px;
                    border-bottom: 1px solid #e0e0e0;
                }
                
                tr:hover {
                    background: #f5f5f5;
                }
                
                .footer {
                    margin-top: 50px;
                    padding-top: 20px;
                    border-top: 2px solid #e0e0e0;
                    text-align: center;
                    color: #666;
                    font-size: 0.9em;
                }
                
                @media (max-width: 768px) {
                    .container {
                        padding: 20px;
                    }
                    
                    h1 {
                        font-size: 2em;
                    }
                    
                    .nav-tabs {
                        flex-direction: column;
                    }
                    
                    .nav-tab {
                        border-radius: 5px;
                        border-bottom: none;
                        border-left: 3px solid transparent;
                    }
                    
                    .nav-tab.active {
                        border-left-color: #667eea;
                    }
                    
                    .answer-numbers-container {
                        flex-direction: column;
                    }
                    
                    table {
                        font-size: 0.85em;
                    }
                    
                    th, td {
                        padding: 8px;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Shape Data Engineering Challenge</h1>
                <p class="subtitle">FPSO Equipment Failure Analysis</p>
                
                <!-- Navigation Tabs -->
                <div class="nav-tabs">
                    <button class="nav-tab active" onclick="showPage('intro')">Introduction</button>
                    <button class="nav-tab" onclick="showPage('analysis')">Analysis Report</button>
                </div>
    """
    
    def _generate_introduction(self) -> str:
        """Generate the introduction section."""
        return """
        <!-- Introduction Page -->
        <div id="intro-page" class="page active">
            <div class="intro-section">
                <h2>Project Overview</h2>
                <p>
                    This project presents an analysis of FPSO (Floating Production Storage and Offloading) 
                    equipment failure data. The analysis focuses on understanding failure patterns, identifying 
                    critical equipment, and ranking sensors by failure frequency to support predictive maintenance 
                    strategies.
                </p>
            </div>
            
            <div class="intro-section">
                <h2>Tools and Technologies</h2>
                <p>The following tools and technologies were used in this project:</p>
                
                <div class="tool-card">
                    <h3>🐍 Python</h3>
                    <p><strong>Version:</strong> Python 3.10.12</p>
                    <p><strong>Usage:</strong> Core programming language for data processing, analysis, and report generation.</p>
                    <p><strong>Why Python:</strong> Python provides excellent libraries for data manipulation, 
                    statistical analysis, and automation, and it is a simple language, making it ideal for data engineering tasks.</p>
                </div>
                
                <div class="tool-card">
                    <h3>📊 Pandas</h3>
                    <p><strong>Version:</strong> 2.3.3</p>
                    <p><strong>Usage:</strong> Primary library for data manipulation and analysis.</p>
                    <p><strong>Why Pandas:</strong> Pandas is a powerful library for data manipulation and analysis, and it is a simple library to use.</p>
                    <p><strong>Key Features Used:</strong></p>
                    <ul>
                        <li>DataFrame operations for merging and joining datasets</li>
                        <li>GroupBy operations for aggregating failure data</li>
                        <li>Data filtering and transformation</li>
                        <li>HTML table generation for report visualization</li>
                    </ul>
                </div>
                
                <div class="tool-card">
                    <h3>🔍 Regular Expressions (re)</h3>
                    <p><strong>Usage:</strong> Parsing structured log files with complex format patterns.</p>
                    <p><strong>Why Regular Expressions:</strong> The log files contain structured text data that 
                    requires pattern matching to extract timestamp, status, sensor ID, temperature, and vibration 
                    values efficiently.</p>
                    <div class="code-snippet">
                        import re<br>
                        # Pattern matching for log file parsing<br>
                        regex = re.compile(r"^\[(\d{4}[-/]\d{1,2}[-/]\d{1,2}...)\]\t(\w+)\tsensor\[(\d+)\]:\t...")
                    </div>
                </div>
                
                <div class="tool-card">
                    <h3>📁 File Processing</h3>
                    <p><strong>Usage:</strong> Handling compressed archives and text file processing.</p>
                    <ul>
                        <li>Extracting TAR.GZ archives containing log files</li>
                        <li>Reading and parsing large text log files</li>
                        <li>Processing JSON and CSV data files</li>
                    </ul>
                </div>
                
                <div class="tool-card">
                    <h3>🌐 HTML/CSS/JavaScript</h3>
                    <p><strong>Usage:</strong> Creating an interactive, multi-page report.</p>
                    <ul>
                        <li>HTML5 for semantic structure</li>
                        <li>CSS3 for modern styling and responsive design</li>
                        <li>JavaScript for page navigation and interactivity</li>
                        <li>Gradient backgrounds and card-based layouts</li>
                    </ul>
                </div>
            </div>

            <div class="intro-section">
                <h2>Scalability and Performance</h2>
                <p><strong>Execution log:</strong></p>
                <div class="code-snippet">
                    Sat Dec 13 20:36:15 -03 2025<br>
                    Performing failure analysis...<br>
                    Loading data...<br>
                    Processing data...<br>
                    Answering question 1...<br>
                    Answering question 2...<br>
                    Answering question 3...<br>
                    Answering question 4...<br>
                    Generating HTML report...<br>
                    HTML report generated successfully: matheus_braganca_teste_shape.html<br>
                    Sat Dec 13 20:36:28 -03 2025<br>
                </div>
                <p>Using the Pandas library, which is a powerful easy-to-use library for data manipulation and analysis but is not the most performant, the report is running well, taking 13 seconds to be generated.</p>
                <p>This is a simple report, so performance is not a major concern, but for a production environment and large datasets, it would be necessary to use more performant tools and technologies, preferably parallel processing, like Spark, DuckDB or Trino.</p>
            </div>
            
            <div class="intro-section">
                <h2>Data Sources</h2>
                <p>The analysis uses three main data sources:</p>
                <ul>
                    <li><strong>equipment.json:</strong> Contains equipment metadata including equipment IDs, names, and group assignments</li>
                    <li><strong>equipment_sensors.csv:</strong> Maps equipment to their associated sensors</li>
                    <li><strong>equipment_failure_sensors.txt:</strong> Log file containing sensor readings with timestamps, status (ERROR/WARNING), temperature, and vibration values</li>
                </ul>
            </div>
            
            <div class="intro-section">
                <h2>Methodology</h2>
                <p>The analysis follows these steps:</p>
                <ol>
                    <li><strong>Data Extraction:</strong> Extract and parse log files from compressed archives</li>
                    <li><strong>Data Integration:</strong> Merge equipment, sensor, and failure data using pandas operations</li>
                    <li><strong>Data Filtering:</strong> Filter records to focus on ERROR status entries</li>
                    <li><strong>Aggregation:</strong> Perform group-by operations to calculate failure counts and averages</li>
                    <li><strong>Ranking:</strong> Rank equipment and sensors by failure frequency</li>
                    <li><strong>Visualization:</strong> Generate HTML tables and formatted reports</li>
                </ol>
            </div>
            
            <div class="intro-section">
                <h2>Key Analysis Questions</h2>
                <p>This report addresses four main questions that were answered in the Analysis Report section:</p>
                <ol>
                    <li>How many equipment failures happened?</li>
                    <li>Which piece of equipment had most failures?</li>
                    <li>What is the average amount of failures per asset across equipment groups?</li>
                    <li>For each asset, which sensors present the most number of failures?</li>
                </ol>
            </div>
        </div>
    """

    def _generate_footer(self) -> str:
        """Generate the report footer."""
        timestamp = datetime.now().strftime('%B %d, %Y, at %I:%M:%S %p')
        return f"""
                <div class="footer">
                    <p>Generated by: Matheus Bragança</p>
                    <p>Generated on: {timestamp}</p>
                </div>
            </div>
        
                <script>
                    function showPage(pageId) {{
                        // Hide all pages
                        document.querySelectorAll('.page').forEach(page => {{
                            page.classList.remove('active');
                        }});
                        
                        // Remove active class from all tabs
                        document.querySelectorAll('.nav-tab').forEach(tab => {{
                            tab.classList.remove('active');
                        }});
                        
                        // Show selected page
                        document.getElementById(pageId + '-page').classList.add('active');
                        
                        // Add active class to clicked tab
                        event.target.classList.add('active');
                    }}
                </script>
        </body>
        </html>
    """
    
    def _generate_analysis(self) -> str:
        """Generate the analysis section with all questions."""
        q1_html = self._format_question_1(self.analysis["q1_result"])
        q2_html = self._format_question_2(self.analysis["q2_result"])
        q3_html = self._format_question_3(self.analysis["q3_result"])
        q4_html = self._format_question_4(self.analysis["q4_result"])
        
        return f"""
        <!-- Analysis Report Page -->
            <div id="analysis-page" class="page">
                {q1_html}
                {q2_html}
                {q3_html}
                {q4_html}
            </div>
        """
    
    def _format_question_1(self, q1_result: dict) -> str:
        """Format failure count results."""
        total = q1_result["v1"]
        unique = q1_result["v2"]
        return f"""<!-- Question 1 -->
            <div class="question">
                <h2>1. How many equipment failures happened?</h2>
                <div class="answer">
                    <div class="answer-numbers-container">
                        <div class="answer-number-box">
                            <div class="answer-number">{total:,}</div>
                            <div class="answer-number-label">Total failures</div>
                        </div>
                        <div class="answer-number-box">
                            <div class="answer-number">{unique:,}</div>
                            <div class="answer-number-label">Total equipment failures<br>(unique events per equipment and timestamp)</div>
                        </div>
                    </div>
                </div>
            </div>"""
    
    def _format_question_2(self, q2_result: pd.DataFrame) -> str:
        """Format equipment ranking results."""
        top_equipment = q2_result.iloc[0]
        return f"""<!-- Question 2 -->
            <div class="question">
                <h2>2. Which piece of equipment had most failures?</h2>
                <div class="answer">
                    {q2_result.to_html(index=False, classes='', table_id='q2-table', escape=False)}
                    <p style="margin-top: 15px; color: #666;">
                        <strong>Equipment with most failures:</strong> {top_equipment['equipment_name']} (ID: {top_equipment['equipment_id']}) 
                        with {top_equipment['failures']:,} failures.
                    </p>
                </div>
            </div>"""
    
    def _format_question_3(self, q3_result: pd.DataFrame) -> str:
        """Format group statistics results."""
        return f"""<!-- Question 3 -->
            <div class="question">
                <h2>3. Find the average amount of failures per asset across equipment groups, ordered by the total number of failures in ascending order.</h2>
                <div class="answer">
                    {q3_result.to_html(index=False, classes='', table_id='q3-table', escape=False)}
                </div>
            </div>"""
    
    def _format_question_4(self, q4_result: pd.DataFrame) -> str:
        """Format sensor ranking results."""
        return f"""<!-- Question 4 -->
            <div class="question">
                <h2>4. For each asset, rank the sensors which present the most number of failures, and also include the equipment group in the output.</h2>
                <div class="answer">
                    {q4_result.to_html(index=False, classes='', table_id='q4-table', escape=False)}
                    <p style="margin-top: 15px; color: #666;">
                        <em>Showing the top 3 sensors with most failures for each equipment.</em>
                    </p>
                </div>
            </div>"""
