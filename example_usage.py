# Example Usage of Claude AI for Analyzing Penetration Test Results

from claude_analyzer import ClaudeAnalyzer

# Initialize the analyzer with the path to the test results
analyzer = ClaudeAnalyzer("path/to/test_results.json")

# Analyze vulnerabilities
vulnerabilities = analyzer.analyze_vulnerabilities()

# Print out the detected vulnerabilities
print("Detected Vulnerabilities:")
for vulnerability in vulnerabilities:
    print(f"- {vulnerability['description']} (Severity: {vulnerability['severity']})")

# Generate a security report
report = analyzer.generate_security_report()

# Print out the security report
print("\nSecurity Report:")
print(report)