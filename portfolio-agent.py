# portfolio-agent.py

"""
Portfolio Agent

An autonomous portfolio management system that includes the following features:

1. Repository Scanning Class
2. Portfolio Analyzer
3. Issue Creation System
4. Dashboard/Report Generator
"""

import os
import requests
import json

class RepositoryScanner:
    """
    A class to scan GitHub repositories and read their metadata.
    """
    def __init__(self, username):
        self.username = username
        self.base_url = 'https://api.github.com/users/' + username + '/repos'

    def get_repositories(self):
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()  # Raises an error for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f'Error retrieving repositories: {e}')
            return []

class PortfolioAnalyzer:
    """
    A class to categorize projects into tiers based on predefined metrics.
    """
    def analyze_projects(self, repos):
        tiers = {'High': [], 'Medium': [], 'Low': []}
        for repo in repos:
            stars = repo.get('stargazers_count', 0)
            if stars > 100:
                tiers['High'].append(repo['name'])
            elif stars > 50:
                tiers['Medium'].append(repo['name'])
            else:
                tiers['Low'].append(repo['name'])
        return tiers

class IssueCreator:
    """
    A class to auto-generate GitHub issues for problems encountered in repositories.
    """
    def __init__(self, repo_name, token):
        self.repo_name = repo_name
        self.token = token

    def create_issue(self, title, body):
        url = f'https://api.github.com/repos/{self.repo_name}/issues'
        headers = {'Authorization': f'token {self.token}'}
        issue = {'title': title, 'body': body}
        try:
            response = requests.post(url, json=issue, headers=headers)
            response.raise_for_status()
            print('Issue created:', response.json()['url'])
        except requests.exceptions.RequestException as e:
            print(f'Error creating issue: {e}')

class DashboardGenerator:
    """
    A class to generate dashboard/reports based on the analyzed portfolio.
    """
    def generate_report(self, tiers):
        report = "Portfolio Report:\n"
        for tier, projects in tiers.items():
            report += f'{tier} Projects: {', '.join(projects)}\n'
        return report

if __name__ == '__main__':
    username = 'OsamaMoftah' # GitHub username
    # You need to put your GitHub token here
    token = '<your_github_token>'

    scanner = RepositoryScanner(username)
    repos = scanner.get_repositories()

    analyzer = PortfolioAnalyzer()
    tiers = analyzer.analyze_projects(repos)

    dashboard = DashboardGenerator()
    report = dashboard.generate_report(tiers)
    print(report)
    
    # Example of issue creation
    # issue_creator = IssueCreator('OsamaMoftah/portfolio-agent', token)
    # issue_creator.create_issue('Sample Issue Title', 'Issue body content here.');
