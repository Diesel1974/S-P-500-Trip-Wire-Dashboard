import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from reddit_scraper import RedditStockSentimentScraper
import json
import os

class RedditSentimentGUI:
    """
    GUI application for Reddit Stock Market Sentiment Scraper.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Reddit Stock Market Sentiment Analyzer")
        self.root.geometry("1000x800")
        self.root.minsize(800, 600)

        # Initialize scraper
        self.scraper = RedditStockSentimentScraper()

        # Configuration file for storing credentials
        self.config_file = "reddit_config.json"

        # Create UI
        self.create_widgets()

        # Load saved credentials if available
        self.load_credentials()

    def create_widgets(self):
        """Create all GUI widgets."""

        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)

        # Title
        title_label = ttk.Label(
            main_frame,
            text="Reddit Stock Market Sentiment Analyzer",
            font=('Helvetica', 18, 'bold')
        )
        title_label.grid(row=0, column=0, pady=10, sticky=tk.W)

        # Subtitle
        subtitle_label = ttk.Label(
            main_frame,
            text="Scrapes Reddit for stock market sentiment and analyzes trends",
            font=('Helvetica', 10)
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 20), sticky=tk.W)

        # API Credentials Frame
        cred_frame = ttk.LabelFrame(main_frame, text="Reddit API Credentials", padding="10")
        cred_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        cred_frame.columnconfigure(1, weight=1)

        # Client ID
        ttk.Label(cred_frame, text="Client ID:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.client_id_entry = ttk.Entry(cred_frame, width=50)
        self.client_id_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # Client Secret
        ttk.Label(cred_frame, text="Client Secret:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.client_secret_entry = ttk.Entry(cred_frame, width=50, show="*")
        self.client_secret_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        # User Agent
        ttk.Label(cred_frame, text="User Agent:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.user_agent_entry = ttk.Entry(cred_frame, width=50)
        self.user_agent_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        self.user_agent_entry.insert(0, "StockSentimentScraper/1.0")

        # Save credentials checkbox
        self.save_creds_var = tk.BooleanVar(value=True)
        save_creds_check = ttk.Checkbutton(
            cred_frame,
            text="Save credentials (stored locally)",
            variable=self.save_creds_var
        )
        save_creds_check.grid(row=3, column=1, sticky=tk.W, pady=5)

        # Help button for getting API credentials
        help_btn = ttk.Button(
            cred_frame,
            text="How to get API credentials?",
            command=self.show_api_help
        )
        help_btn.grid(row=3, column=0, sticky=tk.W, pady=5)

        # Control Frame
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)

        # Posts per subreddit
        ttk.Label(control_frame, text="Posts per subreddit:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.posts_spinbox = ttk.Spinbox(control_frame, from_=10, to=100, width=10)
        self.posts_spinbox.set(25)
        self.posts_spinbox.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)

        # Analyze button
        self.analyze_btn = ttk.Button(
            control_frame,
            text="Start Analysis",
            command=self.start_analysis,
            style='Accent.TButton'
        )
        self.analyze_btn.grid(row=0, column=2, padx=20, pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(control_frame, mode='indeterminate', length=200)
        self.progress.grid(row=0, column=3, padx=10, pady=5)

        # Status label
        self.status_label = ttk.Label(control_frame, text="Ready", foreground="green")
        self.status_label.grid(row=0, column=4, padx=10, pady=5)

        # Results Frame
        results_frame = ttk.LabelFrame(main_frame, text="Analysis Results", padding="10")
        results_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

        # Text widget for results
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            width=80,
            height=25,
            font=('Courier', 10)
        )
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Button frame at bottom
        button_frame = ttk.Frame(results_frame)
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        # Clear button
        clear_btn = ttk.Button(
            button_frame,
            text="Clear Results",
            command=self.clear_results
        )
        clear_btn.grid(row=0, column=0, padx=5)

        # Export button
        export_btn = ttk.Button(
            button_frame,
            text="Export Results",
            command=self.export_results
        )
        export_btn.grid(row=0, column=1, padx=5)

    def show_api_help(self):
        """Show help dialog for getting Reddit API credentials."""
        help_text = """
How to get Reddit API Credentials:

1. Go to https://www.reddit.com/prefs/apps
2. Log in with your Reddit account
3. Scroll to the bottom and click "create another app..."
4. Fill in the form:
   - Name: Choose any name (e.g., "Stock Sentiment Scraper")
   - Select "script" as the app type
   - Description: Optional
   - About URL: Optional
   - Redirect URI: http://localhost:8080
5. Click "create app"
6. You'll see your credentials:
   - Client ID: Under the app name (short string)
   - Client Secret: Labeled as "secret"
7. Copy these values into the fields above

Note: Keep your credentials secure and don't share them!
        """
        messagebox.showinfo("Reddit API Credentials Help", help_text)

    def load_credentials(self):
        """Load saved credentials from config file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.client_id_entry.insert(0, config.get('client_id', ''))
                    self.client_secret_entry.insert(0, config.get('client_secret', ''))
                    self.user_agent_entry.delete(0, tk.END)
                    self.user_agent_entry.insert(0, config.get('user_agent', 'StockSentimentScraper/1.0'))
            except Exception as e:
                print(f"Error loading credentials: {e}")

    def save_credentials(self):
        """Save credentials to config file."""
        if self.save_creds_var.get():
            config = {
                'client_id': self.client_id_entry.get(),
                'client_secret': self.client_secret_entry.get(),
                'user_agent': self.user_agent_entry.get()
            }
            try:
                with open(self.config_file, 'w') as f:
                    json.dump(config, f)
            except Exception as e:
                print(f"Error saving credentials: {e}")

    def clear_results(self):
        """Clear the results text widget."""
        self.results_text.delete(1.0, tk.END)

    def export_results(self):
        """Export results to a text file."""
        results = self.results_text.get(1.0, tk.END)
        if not results.strip():
            messagebox.showwarning("No Results", "There are no results to export.")
            return

        from tkinter import filedialog
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile=f"reddit_sentiment_analysis_{self.get_timestamp()}.txt"
        )

        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(results)
                messagebox.showinfo("Success", f"Results exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export results: {str(e)}")

    def get_timestamp(self):
        """Get current timestamp string."""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def validate_credentials(self):
        """Validate that credentials are entered."""
        if not self.client_id_entry.get():
            messagebox.showerror("Missing Credentials", "Please enter Client ID")
            return False
        if not self.client_secret_entry.get():
            messagebox.showerror("Missing Credentials", "Please enter Client Secret")
            return False
        if not self.user_agent_entry.get():
            messagebox.showerror("Missing Credentials", "Please enter User Agent")
            return False
        return True

    def start_analysis(self):
        """Start the analysis in a separate thread."""
        if not self.validate_credentials():
            return

        # Save credentials if checkbox is checked
        self.save_credentials()

        # Disable button and start progress
        self.analyze_btn.config(state='disabled')
        self.progress.start(10)
        self.status_label.config(text="Analyzing...", foreground="blue")
        self.clear_results()

        # Run analysis in separate thread to prevent GUI freezing
        analysis_thread = threading.Thread(target=self.run_analysis)
        analysis_thread.daemon = True
        analysis_thread.start()

    def run_analysis(self):
        """Run the actual analysis (called in separate thread)."""
        try:
            # Initialize Reddit client
            success, message = self.scraper.initialize_reddit_client(
                client_id=self.client_id_entry.get(),
                client_secret=self.client_secret_entry.get(),
                user_agent=self.user_agent_entry.get()
            )

            if not success:
                self.update_results(f"Error: {message}", error=True)
                return

            # Get posts per subreddit value
            posts_per_sub = int(self.posts_spinbox.get())

            # Scrape subreddits
            self.update_results("Starting to scrape Reddit...\n")
            posts = self.scraper.scrape_all_subreddits(post_limit_per_sub=posts_per_sub)

            # Generate summary
            self.update_results(f"\nScraped {len(posts)} total posts. Generating summary...\n\n")
            summary = self.scraper.generate_summary(posts)

            # Display results
            self.update_results(summary)

        except Exception as e:
            self.update_results(f"Error during analysis: {str(e)}", error=True)

        finally:
            # Re-enable button and stop progress
            self.root.after(0, self.analysis_complete)

    def update_results(self, text, error=False):
        """Update the results text widget (thread-safe)."""
        def update():
            if error:
                self.results_text.insert(tk.END, text, 'error')
                self.results_text.tag_config('error', foreground='red')
            else:
                self.results_text.insert(tk.END, text)
            self.results_text.see(tk.END)

        self.root.after(0, update)

    def analysis_complete(self):
        """Called when analysis is complete."""
        self.analyze_btn.config(state='normal')
        self.progress.stop()
        self.status_label.config(text="Analysis Complete", foreground="green")


def main():
    """Main entry point for the application."""
    root = tk.Tk()

    # Set a nice theme if available
    style = ttk.Style()
    try:
        style.theme_use('clam')
    except:
        pass

    # Create and run the application
    app = RedditSentimentGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
