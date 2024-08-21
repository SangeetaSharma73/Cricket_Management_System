import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
import pygame
from random import randint, choice

# Initialize Pygame for sound
pygame.mixer.init()

# Main Cricket Game Class
class CricketGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Cricket Player Management & Scoring System")
        self.root.geometry("400x400")  # Width x Height of the main window
        self.root.resizable(False,False)
        
        # Player DataFrame
        self.players = pd.DataFrame(columns=[
            "Name", "Type", "Runs", "Wickets", "Strike Rate", "Economy Rate", 
            "Fielding Position", "Catches", "Run-outs", "Stumpings"
        ])

        # Create GUI
        self.create_widgets()

    def create_widgets(self):
        # Player Entry Fields
        tk.Label(self.root, text="Player Name:", width=15, anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.player_name = tk.Entry(self.root, width=30)
        self.player_name.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(self.root, text="Player Type:", width=15, anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.player_type = ttk.Combobox(self.root, values=["Batsman", "Bowler", "All-Rounder", "Wicket-Keeper"], width=28)
        self.player_type.grid(row=1, column=1, padx=10, pady=5)

        tk.Button(self.root, text="Add Player", command=self.add_player, width=15).grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Display Players Button
        tk.Button(self.root, text="View Players", command=self.show_players, width=15).grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Simulate Match Button
        tk.Button(self.root, text="Simulate Match", command=self.simulate_match, width=15).grid(row=4, column=1, padx=10, pady=10, sticky="w")

        # Comparison Button
        tk.Button(self.root, text="Compare Players", command=self.compare_players, width=15).grid(row=5, column=1, padx=10, pady=10, sticky="w")

        # Exit Button
        tk.Button(self.root, text="Exit", command=self.root.quit, width=15).grid(row=6, column=1, padx=10, pady=10, sticky="w")

    def add_player(self):
        self.play_sound("StockTune.mp3")
        name = self.player_name.get()
        p_type = self.player_type.get()

        if name and p_type:
            # Random attributes for demo purposes
            runs = randint(0, 5000)
            wickets = randint(0, 200)
            strike_rate = round(randint(60, 150), 2)
            economy_rate = round(randint(3, 10), 2)
            fielding_pos = choice(["Slip", "Mid-On", "Square Leg", "Fine Leg", "Wicket Keeper"])
            catches = randint(0, 50)
            run_outs = randint(0, 20)
            stumpings = randint(0, 30) if p_type == "Wicket-Keeper" else 0
            
            # Add player data to DataFrame
            player_data = pd.DataFrame([{
                "Name": name, "Type": p_type, "Runs": runs, "Wickets": wickets, 
                "Strike Rate": strike_rate, "Economy Rate": economy_rate, 
                "Fielding Position": fielding_pos, "Catches": catches, 
                "Run-outs": run_outs, "Stumpings": stumpings
            }])
            self.players = pd.concat([self.players, player_data], ignore_index=True)
            
            messagebox.showinfo("Success", f"Player {name} added!")
            

    def show_players(self):
        if not self.players.empty:
            top = tk.Toplevel(self.root)
            top.title("Player List")
            top.geometry("600x400")  # Set width and height for the player list window
            cols = list(self.players.columns)
            tree = ttk.Treeview(top, columns=cols, show='headings')
            for col in cols:
                tree.heading(col, text=col)
                tree.grid(row=0, column=0)

            for index, row in self.players.iterrows():
                tree.insert("", "end", values=list(row))
        else:
            messagebox.showinfo("No Players", "No players added yet!")

    def simulate_match(self):
        if len(self.players) > 1:
            # Sample two players from the DataFrame
            sampled_players = self.players.sample(2)
            player1 = sampled_players.iloc[0]
            player2 = sampled_players.iloc[1]

            # Simulate match based on player statistics
            result = f"Simulating a match between {player1['Name']} and {player2['Name']}\n"
            result += f"{player1['Name']} scored {player1['Runs']} runs\n"
            result += f"{player2['Name']} scored {player2['Runs']} runs\n"
            
            if player1['Runs'] > player2['Runs']:
                result += f"{player1['Name']} wins!"
            elif player1['Runs'] < player2['Runs']:
                result += f"{player2['Name']} wins!"
            else:
                result += "It's a tie!"

            messagebox.showinfo("Match Result", result)
        else:
            messagebox.showinfo("Not Enough Players", "You need at least 2 players to simulate a match.")
        
    def compare_players(self):
        if len(self.players) > 1:
            # Sample 2 players and convert them into individual Series
            sample_players = self.players.sample(2)
            player1 = sample_players.iloc[0]
            player2 = sample_players.iloc[1]

            # Bar chart comparison
            fig, ax = plt.subplots()
            categories = ["Runs", "Wickets", "Catches", "Strike Rate", "Economy Rate"]
            player1_vals = [player1[c] for c in categories]
            player2_vals = [player2[c] for c in categories]

            ax.bar(categories, player1_vals, label=player1["Name"])
            ax.bar(categories, player2_vals, label=player2["Name"], alpha=0.7)
            ax.legend()

            plt.title("Player Comparison")
            plt.show()
        else:
            messagebox.showinfo("Not Enough Players", "You need at least 2 players to compare.")
        
    def play_sound(self, file):
        try:
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
        except pygame.error as e:
            messagebox.showerror("Error", f"Sound file error: {str(e)}")

# Main Tkinter Loop
if __name__ == "__main__":
    root = tk.Tk()
    app = CricketGame(root)
    root.mainloop()
