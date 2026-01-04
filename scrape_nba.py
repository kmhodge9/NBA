import pandas as pd
import requests
import time
from datetime import datetime
import sys

# Enhanced headers to mimic real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.nba.com/',
    'Origin': 'https://www.nba.com',
    'Connection': 'keep-alive',
    'x-nba-stats-origin': 'stats',
    'x-nba-stats-token': 'true',
}

def make_request_with_retry(url, params, max_retries=5, backoff_factor=2):
    """Make request with exponential backoff retry logic"""
    
    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}...")
            
            # Add delay between attempts (except first)
            if attempt > 0:
                wait_time = backoff_factor ** attempt
                print(f"Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            
            response = requests.get(
                url, 
                headers=headers, 
                params=params,
                timeout=30  # 30 second timeout
            )
            
            # Check if successful
            response.raise_for_status()
            
            # Verify we got JSON back
            data = response.json()
            
            # Check if data structure is valid
            if 'resultSets' in data and len(data['resultSets']) > 0:
                print("✓ Successfully retrieved data")
                return data
            else:
                print("⚠ Response missing expected data structure")
                continue
                
        except requests.exceptions.Timeout:
            print(f"✗ Timeout on attempt {attempt + 1}")
        except requests.exceptions.HTTPError as e:
            print(f"✗ HTTP Error on attempt {attempt + 1}: {e.response.status_code}")
            if e.response.status_code == 403:
                print("  (403 Forbidden - may be blocked)")
            elif e.response.status_code == 429:
                print("  (429 Too Many Requests - rate limited)")
                time.sleep(10)  # Extra wait for rate limiting
        except requests.exceptions.RequestException as e:
            print(f"✗ Request error on attempt {attempt + 1}: {str(e)}")
        except ValueError:
            print(f"✗ Invalid JSON response on attempt {attempt + 1}")
        
        if attempt < max_retries - 1:
            print("Retrying...")
    
    print(f"\n✗ Failed after {max_retries} attempts")
    return None

def get_player_game_logs(season='2025-26', season_type='Regular Season'):
    """Get game logs for all players with retry logic"""
    
    print(f"\nFetching game logs for {season} {season_type}...")
    print("-" * 60)
    
    url = 'https://stats.nba.com/stats/playergamelogs'
    params = {
        'Season': season,
        'SeasonType': season_type,
        'DateFrom': '',
        'DateTo': '',
        'LeagueID': '00',  # NBA league ID
    }
    
    data = make_request_with_retry(url, params)
    
    if data is None:
        return pd.DataFrame()  # Return empty dataframe on failure
    
    try:
        headers_list = data['resultSets'][0]['headers']
        rows = data['resultSets'][0]['rowSet']
        df = pd.DataFrame(rows, columns=headers_list)
        return df
    except (KeyError, IndexError) as e:
        print(f"Error parsing response data: {e}")
        return pd.DataFrame()

def filter_and_sort_data(df):
    """Filter by most recent game date and sort by player name A-Z"""
    
    if df.empty:
        return df
    
    # Convert GAME_DATE to datetime
    df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'])
    
    # Find most recent date
    most_recent_date = df['GAME_DATE'].max()
    print(f"\nMost recent game date: {most_recent_date.strftime('%Y-%m-%d')}")
    
    # Filter and sort
    filtered_df = df[df['GAME_DATE'] == most_recent_date].copy()
    filtered_df = filtered_df.sort_values('PLAYER_NAME', ascending=True)
    filtered_df = filtered_df.reset_index(drop=True)
    
    print(f"Games on most recent date: {len(filtered_df)}")
    print(f"Unique players: {filtered_df['PLAYER_NAME'].nunique()}")
    
    return filtered_df

def main():
    print("=" * 60)
    print("NBA Game Log Scraper (GitHub Actions Compatible)")
    print("=" * 60)
    
    # Try current season first
    seasons_to_try = ['2025-26', '2024-25']
    game_logs_df = pd.DataFrame()
    
    for season in seasons_to_try:
        game_logs_df = get_player_game_logs(season=season)
        
        if not game_logs_df.empty:
            print(f"\n✓ Successfully retrieved data for {season}")
            break
        else:
            print(f"\n✗ No data available for {season}")
            if season != seasons_to_try[-1]:
                print(f"Trying {seasons_to_try[seasons_to_try.index(season) + 1]}...")
    
    if game_logs_df.empty:
        print("\n" + "=" * 60)
        print("ERROR: Could not retrieve any data")
        print("=" * 60)
        print("\nPossible issues:")
        print("1. GitHub Actions IP may be blocked by NBA.com")
        print("2. API endpoint may be down")
        print("3. Season data not yet available")
        print("\nConsider using alternative data sources or proxies")
        sys.exit(1)  # Exit with error code for GitHub Actions
    
    print(f"\nTotal entries: {len(game_logs_df)}")
    print(f"Unique players: {game_logs_df['PLAYER_NAME'].nunique()}")
    
    # Filter and sort
    print("\n" + "-" * 60)
    print("Processing data...")
    print("-" * 60)
    filtered_df = filter_and_sort_data(game_logs_df)
    
    if filtered_df.empty:
        print("ERROR: No data after filtering")
        sys.exit(1)
    
    # Save to CSV
    output_file = f'nba_most_recent_games_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    filtered_df.to_csv(output_file, index=False)
    
    print("\n" + "=" * 60)
    print(f"✓ SUCCESS: Data saved to {output_file}")
    print(f"✓ Total players: {len(filtered_df)}")
    print(f"✓ Sorted A-Z by player name")
    print("=" * 60)
    
    # Display sample
    print("\n--- SAMPLE: First 10 Players ---")
    sample_cols = ['PLAYER_NAME', 'GAME_DATE', 'MATCHUP', 'PTS', 'REB', 'AST']
    available_cols = [col for col in sample_cols if col in filtered_df.columns]
    print(filtered_df[available_cols].head(10).to_string(index=False))

if __name__ == "__main__":
    main()
```


