import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset from a local file
file_path = "transfers.csv"  # Adjust the path as necessary
data = pd.read_csv(file_path)

# Clean the data: Convert transfer_fee and market_value_in_eur to numeric, handling errors
data['transfer_fee'] = pd.to_numeric(data['transfer_fee'], errors='coerce')
data['market_value_in_eur'] = pd.to_numeric(data['market_value_in_eur'], errors='coerce')

# 1. Clubs with the most transfers
most_transfers_from = data['from_club_name'].value_counts().head(10)
most_transfers_to = data['to_club_name'].value_counts().head(10)

print("Top 10 clubs making transfers:")
print(most_transfers_from)
print("\nTop 10 clubs receiving transfers:")
print(most_transfers_to)

# 2. Relationship between market values and transfer fees
plt.figure(figsize=(10, 6))
plt.scatter(data['market_value_in_eur'], data['transfer_fee'], alpha=0.5)
plt.title('Market Value vs Transfer Fee')
plt.xlabel('Market Value (EUR)')
plt.ylabel('Transfer Fee (EUR)')
plt.xscale('log')
plt.yscale('log')
plt.grid(True)
plt.show()

# 3. Total transfer fees for each player
total_transfer_fees_per_player = data.groupby('player_name')['transfer_fee'].sum().reset_index()
total_transfer_fees_per_player = total_transfer_fees_per_player.sort_values(by='transfer_fee', ascending=False).head(10)

# Plotting total transfer fees per player
plt.figure(figsize=(12, 6))
plt.bar(total_transfer_fees_per_player['player_name'], total_transfer_fees_per_player['transfer_fee'], color='lightblue')
plt.title('Top 10 Players by Total Transfer Fees')
plt.xlabel('Player Name')
plt.ylabel('Total Transfer Fees (EUR)')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()

# 4. Calculate total transfer fees for each club
total_transfer_fees_from = data.groupby('from_club_name')['transfer_fee'].sum().reset_index()
total_transfer_fees_to = data.groupby('to_club_name')['transfer_fee'].sum().reset_index()

# Merge both totals into a single DataFrame for easier plotting
total_transfer_fees = pd.merge(total_transfer_fees_from, total_transfer_fees_to,
                                left_on='from_club_name', right_on='to_club_name', 
                                how='outer', suffixes=('_from', '_to'))

# Fill NaN values with 0
total_transfer_fees.fillna(0, inplace=True)

# Calculate total fees for each club
total_transfer_fees['total_fee'] = total_transfer_fees['transfer_fee_from'] + total_transfer_fees['transfer_fee_to']

# Sort by total fees
total_transfer_fees = total_transfer_fees.sort_values(by='total_fee', ascending=False).head(10)

# Plotting the total transfer fees per club
plt.figure(figsize=(12, 6))
plt.bar(total_transfer_fees['from_club_name'], total_transfer_fees['total_fee'], color='skyblue')
plt.title('Top 10 Clubs by Total Transfer Fees')
plt.xlabel('Club Name')
plt.ylabel('Total Transfer Fees (EUR)')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()

# 5. Average market value of players transferred for each club
avg_market_value_per_club = data.groupby('from_club_name')['market_value_in_eur'].mean().reset_index()
avg_market_value_per_club = avg_market_value_per_club.sort_values(by='market_value_in_eur', ascending=False).head(10)

# Plotting average market value per club
plt.figure(figsize=(12, 6))
plt.bar(avg_market_value_per_club['from_club_name'], avg_market_value_per_club['market_value_in_eur'], color='lightgreen')
plt.title('Top 10 Clubs by Average Market Value of Transferred Players')
plt.xlabel('Club Name')
plt.ylabel('Average Market Value (EUR)')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()

# 6. Pie chart for distribution of total transfer fees among top clubs
top_clubs_pie = total_transfer_fees.set_index('from_club_name')['total_fee']
plt.figure(figsize=(10, 8))
plt.pie(top_clubs_pie, labels=top_clubs_pie.index, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
plt.title('Distribution of Total Transfer Fees Among Top Clubs')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()