"""
Generate the HTML report for the Shape Data Engineering Challenge.
"""

from reports.html_report import HtmlReport
from data.generate_analysis import generate_analysis


def get_html_content():
    """Get the HTML content for the report."""
    print()
    print("=" * 50)
    print("Generating analysis...")
    print("=" * 50)
    results = generate_analysis()
    
    print()
    print("=" * 50)
    print("Generating HTML report...")
    print("=" * 50)
    report = HtmlReport(results)
    html_content = report.generate()
    
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
