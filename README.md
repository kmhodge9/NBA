# NBA Game Log Scraper

![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Automated-success.svg)

An automated Python scraper that fetches NBA player game logs from the NBA Stats API, filters for the most recent games, and exports the data to CSV format.

## 🏀 Features

- **Automated Data Collection**: Scrapes NBA player game logs using the official NBA Stats API
- **Most Recent Games**: Automatically filters data to show only the latest game date
- **Alphabetical Sorting**: Players sorted A-Z for easy lookup
- **GitHub Actions Integration**: Runs daily to keep data fresh
- **Retry Logic**: Built-in error handling and exponential backoff for reliability
- **CSV Export**: Clean, structured data ready for analysis

## 📊 Data Output

The scraper generates CSV files containing:
- Player names
- Game dates
- Team matchups
- Statistics (points, rebounds, assists, etc.)
- All sorted alphabetically by player name
- Filtered to the most recent game date only

**Sample Output:**
```
PLAYER_NAME,GAME_DATE,MATCHUP,PTS,REB,AST,MIN,...
Aaron Gordon,2026-01-03,DEN vs. LAL,18,7,4,35,...
Alperen Sengun,2026-01-03,HOU @ MIA,22,11,6,38,...
Anthony Davis,2026-01-03,LAL @ DEN,31,14,3,42,...
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Local Installation

1. **Clone the repository:**
```bash
git clone https://github.com/cgpropz/Nba_Project_25.git
cd Nba_Project_25
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the scraper:**
```bash
python scrape_nba.py
```

4. **Check the output:**
The script will create a CSV file named `nba_most_recent_games_YYYYMMDD_HHMMSS.csv`

## 🤖 Automated Workflow

This project uses GitHub Actions to automatically scrape data daily.

### How It Works

1. **Scheduled Runs**: Executes daily at 9:00 AM UTC (4:00 AM EST)
2. **Manual Triggers**: Can be run on-demand via GitHub Actions interface
3. **Auto-Commit**: Successfully scraped data is automatically committed back to the repository

### Running Manually

1. Go to the **Actions** tab in this repository
2. Select **"Scrape NBA Game Logs"** workflow
3. Click **"Run workflow"**
4. Select the branch (usually `main`)
5. Click the green **"Run workflow"** button

### Workflow Status

Check the latest run status in the [Actions tab](../../actions).

## 📁 Project Structure

```
Nba_Project_25/
├── .github/
│   └── workflows/
│       └── scrape_nba.yml          # GitHub Actions workflow
├── scrape_nba.py                    # Main scraper script
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
└── *.csv                           # Generated game log files
```

## 🛠️ Technical Details

### Dependencies

- **pandas**: Data manipulation and CSV export
- **requests**: HTTP requests to NBA Stats API

### API Endpoint

The scraper uses the NBA Stats API endpoint:
```
https://stats.nba.com/stats/playergamelogs
```

### Key Functions

- `make_request_with_retry()`: Handles API requests with exponential backoff
- `get_player_game_logs()`: Fetches all player game logs for a season
- `filter_and_sort_data()`: Filters for most recent date and sorts alphabetically

## ⚙️ Configuration

### Change Season

Edit `scrape_nba.py` line 102:
```python
seasons_to_try = ['2025-26', '2024-25']  # Add or modify seasons
```

### Adjust Schedule

Edit `.github/workflows/scrape_nba.yml` line 5:
```yaml
cron: '0 9 * * *'  # Format: minute hour day month weekday
```

**Examples:**
- `'0 */6 * * *'` - Every 6 hours
- `'0 0 * * *'` - Daily at midnight UTC
- `'0 12 * * 1-5'` - Weekdays at noon UTC

### Modify Retry Behavior

In `scrape_nba.py`, adjust parameters in `make_request_with_retry()`:
```python
max_retries=5,        # Number of retry attempts
backoff_factor=2      # Exponential backoff multiplier
```

## 🔧 Troubleshooting

### Common Issues

**1. 403 Forbidden Error**
- **Cause**: NBA.com may block certain IPs (especially cloud providers)
- **Solution**: The script includes retry logic and proper headers to minimize this

**2. Empty Data**
- **Cause**: Season hasn't started or no games on recent date
- **Solution**: Script automatically tries previous season (2024-25)

**3. GitHub Actions Fails**
- **Cause**: API rate limiting or network issues
- **Solution**: Check workflow logs, increase retry delays, or run manually

**4. Timeout Errors**
- **Cause**: Slow API response
- **Solution**: Script has 30-second timeout with automatic retries

### Debug Mode

For more detailed logging, run locally and check console output:
```bash
python scrape_nba.py
```

## 📈 Use Cases

- **Fantasy Basketball**: Track daily player performance
- **Data Analysis**: Build datasets for statistical modeling
- **Sports Analytics**: Analyze player trends and patterns
- **Machine Learning**: Training data for prediction models
- **Personal Projects**: Custom NBA dashboards and visualizations

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Ideas for Contribution

- Add support for playoff game logs
- Include advanced stats (PER, TS%, etc.)
- Create data visualization scripts
- Add database storage option
- Implement notification system for workflow failures

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This project uses the unofficial NBA Stats API. The API is subject to change without notice. This scraper is for educational and personal use only. Please respect NBA.com's terms of service and rate limits.

## 🔗 Resources

- [NBA Stats Website](https://www.nba.com/stats)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 📧 Contact

**Project Creator**: [@cgpropz](https://github.com/cgpropz)

**Repository**: [Nba_Project_25](https://github.com/cgpropz/Nba_Project_25)

---

⭐ If you find this project useful, please consider giving it a star!

**Last Updated**: January 2026
