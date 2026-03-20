import gzip
import pathlib
import geoip2.database
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

def format_bytes(n: int) -> str:
    """Converts a byte count to a human-readable string."""
    for unit in ('B', 'KB', 'MB', 'GB', 'TB'):
        if n < 1024:
            return f"{n:.2f} {unit}"
        n /= 1024
    return f"{n:.2f} PB"


def _iter_log_lines(log_dir: str, filename_glob: str):
    """Yields lines from all matching log files in a directory, handling .gz transparently."""
    files = sorted(pathlib.Path(log_dir).glob(filename_glob))
    if not files:
        print(f"Warning: No files matching '{filename_glob}' found in '{log_dir}'.")
    for path in files:
        try:
            if path.suffix == '.gz':
                with gzip.open(path, 'rt', errors='replace') as f:
                    yield from f
            else:
                with open(path, 'r', errors='replace') as f:
                    yield from f
        except OSError as e:
            print(f"Warning: Could not read '{path}': {e}")


def extract_ips(log_dir: str, filter_path: str, filename_glob: str = 'access.log*') -> list[dict]:
    """Parses all matching log files in log_dir and returns records with IP and bytes transferred."""
    records = []
    for line in _iter_log_lines(log_dir, filename_glob):
        if filter_path in line:
            parts = line.split()
            if parts:
                try:
                    bytes_sent = int(parts[9])
                except (IndexError, ValueError):
                    bytes_sent = 0
                records.append({'ip': parts[0], 'bytes': bytes_sent})
    return records

def get_geolocation_data(ips: list[str], db_path: str) -> pd.DataFrame:
    """Resolves IPs to (lat, lon) using the MaxMind database."""
    locations = []
    try:
        with geoip2.database.Reader(db_path) as reader:
            for ip in ips:
                try:
                    record = reader.city(ip)
                    # Note: Shapely/GeoPandas use (Longitude, Latitude) order
                    locations.append({
                        'ip': ip,
                        'lon': record.location.longitude,
                        'lat': record.location.latitude,
                        'country': record.country.name or 'Unknown'
                    })
                except (geoip2.errors.AddressNotFoundError, ValueError):
                    continue
    except FileNotFoundError:
        print(f"Error: Database '{db_path}' not found.")
    
    return pd.DataFrame(locations)

def print_summary(records: list[dict], df: pd.DataFrame, focus_country: str) -> None:
    """Prints summary statistics to the console."""
    raw_ips = [r['ip'] for r in records]
    unique_ips = set(raw_ips)

    print("Summary Statistics")
    print(f"Total connections matched: {len(records)}")
    print(f"Unique IPs: {len(unique_ips)}")

    if records:
        records_df = pd.DataFrame(records)
        bytes_values = records_df['bytes']
        total_bytes = int(bytes_values.sum())
        avg_bytes = bytes_values.mean()
        print(f"Total bytes transferred: {format_bytes(total_bytes)}")
        print(f"Average bytes per connection: {format_bytes(avg_bytes)}")
        print(f"Min / Max bytes: {format_bytes(int(bytes_values.min()))} / {format_bytes(int(bytes_values.max()))}")

        print("Top 5 clients by bytes transferred:")
        top_clients = (
            records_df.groupby('ip')['bytes']
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )
        for ip, b in top_clients.items():
            print(f"  {ip}: {format_bytes(int(b))}")

    if not df.empty:
        country_counts = (
            df.groupby('country')['ip']
            .nunique()
            .sort_values(ascending=False)
        )
        print(f"IPs resolved to location: {country_counts.sum()}")
        print("Top 5 countries by unique IP count:")
        for country, count in country_counts.head(5).items():
            print(f"  {country}: {count}")

        if records:
            merged = records_df.merge(df[['ip', 'country']].drop_duplicates(), on='ip', how='inner')
            country_bytes = (
                merged.groupby('country')['bytes']
                .sum()
                .sort_values(ascending=False)
            )
            print("Top 5 countries by bytes transferred:")
            for country, b in country_bytes.head(5).items():
                print(f"  {country}: {format_bytes(int(b))}")

            focus_ips = merged[merged['country'] == focus_country]
            if not focus_ips.empty:
                focus_top = (
                    focus_ips.groupby('ip')['bytes']
                    .sum()
                    .sort_values(ascending=False)
                    .head(5)
                )
                print(f"Top 5 {focus_country} IPs by bytes transferred:")
                for ip, b in focus_top.items():
                    print(f"  {ip}: {format_bytes(int(b))}")
            else:
                print(f"No {focus_country} IPs resolved to location.")
    else:
        print("IPs resolved to location: 0")


def plot_map(df: pd.DataFrame, output_file: str) -> None:
    """Plots the coordinates on a world map."""
    if df.empty:
        print("No valid location data to plot.")
        return

    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(
        df, 
        geometry=gpd.points_from_xy(df.lon, df.lat)
    )

    # Load base map
    world = gpd.read_file("https://naciscdn.org/naturalearth/10m/cultural/ne_10m_admin_0_countries.zip")

    # Setup plot
    fig, ax = plt.subplots(figsize=(15, 10))
    world.plot(ax=ax, color='#e0e0e0', edgecolor='white')
    gdf.plot(ax=ax, color='red', markersize=15, alpha=0.5)

    plt.axis('off')
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    print(f"Map saved successfully: {output_file}")

if __name__ == "__main__":
    LOG_DIR = 'nginx'
    DB_PATH = 'GeoLite2-City.mmdb'
    SEARCH_PATH = '/yUNshbl1fOXngs4JRBkrJIFU'
    OUTPUT_IMAGE = 'ip_map.png'
    FOCUS_COUNTRY = 'Russia'

    print("Parsing log files...")
    ip_list = extract_ips(LOG_DIR, SEARCH_PATH)
    
    if ip_list:
        print(f"Resolving {len(ip_list)} IPs...")
        location_data = get_geolocation_data([r['ip'] for r in ip_list], DB_PATH)
        print_summary(ip_list, location_data, FOCUS_COUNTRY)
        plot_map(location_data, OUTPUT_IMAGE)
    else:
        print("No matching connections found.")