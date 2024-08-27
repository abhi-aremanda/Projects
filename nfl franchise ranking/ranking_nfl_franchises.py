import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

def load_data(file_path):
    return pd.read_excel(file_path)

def calculate_scores(df, weights):
    df['Score'] = 0
    for metric, weight in weights.items():
        df['Score'] += df[metric] * weight
    
    df['Score per Time'] = df['Score'] / df['Tot yrs']
    return df

def get_top_bottom_teams(df, metric, top_n=5):
    df_sorted = df.sort_values(by=metric, ascending=False)
    top_teams = df_sorted.head(top_n)
    bottom_teams = df_sorted.tail(top_n)
    return top_teams, bottom_teams

def add_image(ax, img_path, xy, zoom=0.3):
    img = plt.imread(img_path)
    imagebox = OffsetImage(img, zoom=zoom)
    ab = AnnotationBbox(imagebox, xy, frameon=False)
    ax.add_artist(ab)

def plot_teams(ax, teams, image_paths, metric, color, is_top=True, total_teams=32):
    for i, (index, row) in enumerate(teams.iterrows()):
        if is_top:
            rank_str = f"{i + 1}."
        else:
            rank_str = f"{total_teams - len(teams) + i + 1}."

        team_name = row['Tm']
        score = f"{row[metric]:.2f}"

        ax.text(0.2, 1 - i * 0.15, rank_str, fontsize=12, fontweight='bold', va='center')
        ax.text(0.3, 1 - i * 0.15, team_name, fontsize=12, va='center')
        ax.text(0.85, 1 - i * 0.15, score, fontsize=12, color=color, va='center')

        if team_name in image_paths:
            add_image(ax, image_paths[team_name], (0.1, 1 - i * 0.15))

    ax.axis('off')


def main():
    file_path = "analytics/NFL franchise rankings.xlsx"
    weights = {
        'W-L%': 7,
        'W plyf': 3,      
        'L plyf': -1,    
        'Non sb chmp': 15,       
        'SBwl': 23,
        'SBwl app' : 12,
        'Conf': 10,
        'Div': 3,
        'Yr plyf': 2
    }
    
    image_paths = {
    
    'Arizona Cardinals':"analytics/nfl logos/CARDS.png",
    'Atlanta Falcons' : "analytics/nfl logos/atl.png",
    'Baltimore Ravens':"analytics/nfl logos/bmore.png",
    'Buffalo Bills':"analytics/nfl logos/buffalobills.png",
    'Carolina Panthers' : "analytics/nfl logos/car.png",
    'Chicago Bears' : "analytics/nfl logos/dabears.png",
    'Cincinnati Bengals' : "analytics/nfl logos/bengals.png",
    'Cleveland Browns' : "analytics/nfl logos/browns.png",
    'Dallas Cowboys' : "analytics/nfl logos/dal.png",
    'Denver Broncos' : "analytics/nfl logos/denver.png",
    'Detroit Lions' : "analytics/nfl logos/det.png",
    'Green Bay Packers' : "analytics/nfl logos/gbp.png",
    'Houston Texans' : "analytics/nfl logos/htx.png",
    'Indianapolis Colts' : "analytics/nfl logos/colts.png",
    'Jacksonville Jaguars': "analytics/nfl logos/jags.png",
    'Kansas City Chiefs': "analytics/nfl logos/kc.png",
    'Las Vegas Raiders' : "analytics/nfl logos/lv.png",
    'Los Angeles Chargers': "analytics/nfl logos/lachargers.png",
    'Los Angeles Rams' : "analytics/nfl logos/larams.png",
    'Miami Dolphins': "analytics/nfl logos/miamidolphins.png",
    'Minnesota Vikings' : "analytics/nfl logos/min.png",
    'New England Patriots' : "analytics/nfl logos/min.png",
    "New Orleans Saints" : "analytics/nfl logos/NO.png",
    "New York Giants" : "analytics/nfl logos/nyg.png",
    "New York Jets" : "analytics/nfl logos/nyjets.png",
    "Philadelphia Eagles" : "analytics/nfl logos/phil.png",
    'Pittsburgh Steelers' : "analytics/nfl logos/pittsburgh.png",
    'San Francisco 49ers' : "analytics/nfl logos/sf49.png",
    'Seattle Seahawks' : "analytics/nfl logos/seahW.png",
    'Tampa Bay Buccaneers' : "analytics/nfl logos/tamp.png",
    'Tennessee Titans' : "analytics/nfl logos/tennesee.png",
    'Washington Commanders':"analytics/nfl logos/wash.png"
}

    df = load_data(file_path)
    df = calculate_scores(df, weights)
    
    # Sort and print the full lists of teams by Score and Score per Time
    df_sorted_by_score = df.sort_values(by='Score', ascending=False)
    df_sorted_by_score_per_time = df.sort_values(by='Score per Time', ascending=False)

    print("Full list sorted by Score:")
    print(df_sorted_by_score[['Tm', 'Score']])
    
    print("\nFull list sorted by Score per Time:")
    print(df_sorted_by_score_per_time[['Tm', 'Score per Time']])
    
    # Get top and bottom teams
    top_5_score, bottom_5_score = get_top_bottom_teams(df, 'Score')
    top_5_score_per_time, bottom_5_score_per_time = get_top_bottom_teams(df, 'Score per Time')
    
    # Plot top 5 by Score
    fig, ax = plt.subplots(figsize=(5, 5))
    plot_teams(ax, top_5_score, image_paths, 'Score', 'Green')
    plt.show()

    # Plot top 5 by Score per Season
    fig, ax = plt.subplots(figsize=(5, 5))
    plot_teams(ax, top_5_score_per_time, image_paths, 'Score per Time', 'Green')
    plt.show()
    
    # Plot bottom 5 by Score
    fig, ax = plt.subplots(figsize=(5, 5))
    plot_teams(ax, bottom_5_score, image_paths, 'Score', 'Red', is_top=False)
    plt.show()

    # Plot bottom 5 by Score per Season
    fig, ax = plt.subplots(figsize=(5, 5))
    plot_teams(ax, bottom_5_score_per_time, image_paths, 'Score per Time', 'Red', is_top=False)
    plt.show()

if __name__ == "__main__":
    main()
