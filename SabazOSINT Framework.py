# SabazOSINT: A Social Media and OSINT Framework
# Coded By: Mr. Sabaz Ali Khan, Pakistani Ethical Hacker
# Purpose: Ethical open-source intelligence gathering for publicly available data
# Warning: Use this tool responsibly and in compliance with all applicable laws and platform terms of service.

import tweepy
import instaloader
from googlesearch import search
import holehe
import logging
import sys
import json
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='sabazosint.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SabazOSINT:
    def __init__(self, twitter_api_key=None, twitter_api_secret=None, 
                 twitter_access_token=None, twitter_access_secret=None):
        """Initialize the SabazOSINT framework."""
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing SabazOSINT Framework by Mr. Sabaz Ali Khan")
        
        # Twitter/X API setup
        if all([twitter_api_key, twitter_api_secret, twitter_access_token, twitter_access_secret]):
            try:
                self.twitter_client = tweepy.Client(
                    consumer_key=twitter_api_key,
                    consumer_secret=twitter_api_secret,
                    access_token=twitter_access_token,
                    access_token_secret=twitter_access_secret
                )
                self.logger.info("Twitter/X API initialized successfully")
            except Exception as e:
                self.logger.error(f"Twitter/X API initialization failed: {e}")
                self.twitter_client = None
        else:
            self.twitter_client = None
            self.logger.warning("Twitter/X API credentials not provided")

        # Instagram setup
        self.instagram_loader = instaloader.Instaloader()
        self.logger.info("Instagram loader initialized")

    def twitter_search(self, username=None, query=None, max_results=10):
        """Search Twitter/X for user info or posts."""
        if not self.twitter_client:
            self.logger.error("Twitter/X API not initialized")
            return {"error": "Twitter/X API not initialized"}

        result = {"username": username, "query": query, "data": []}
        try:
            if username:
                user = self.twitter_client.get_user(username=username)
                if user.data:
                    result["data"].append({
                        "id": user.data.id,
                        "name": user.data.name,
                        "username": user.data.username,
                        "description": user.data.description,
                        "public_metrics": user.data.public_metrics
                    })
                    self.logger.info(f"Retrieved Twitter/X user data for {username}")

            if query:
                tweets = self.twitter_client.search_recent_tweets(
                    query=query, max_results=max_results, tweet_fields=["created_at", "public_metrics"]
                )
                if tweets.data:
                    for tweet in tweets.data:
                        result["data"].append({
                            "id": tweet.id,
                            "text": tweet.text,
                            "created_at": str(tweet.created_at),
                            "public_metrics": tweet.public_metrics
                        })
                    self.logger.info(f"Retrieved {len(tweets.data)} tweets for query: {query}")

        except Exception as e:
            self.logger.error(f"Twitter/X search failed: {e}")
            result["error"] = str(e)

        return result

    def instagram_profile(self, username):
        """Gather public Instagram profile data."""
        result = {"username": username, "data": {}}
        try:
            profile = instaloader.Profile.from_username(self.instagram_loader.context, username)
            result["data"] = {
                "username": profile.username,
                "full_name": profile.full_name,
                "biography": profile.biography,
                "followers": profile.followers,
                "following": profile.followees,
                "posts": profile.mediacount,
                "is_private": profile.is_private
            }
            self.logger.info(f"Retrieved Instagram profile data for {username}")
        except Exception as e:
            self.logger.error(f"Instagram profile retrieval failed: {e}")
            result["error"] = str(e)

        return result

    def web_search(self, query, num_results=10):
        """Perform a Google web search for OSINT."""
        result = {"query": query, "data": []}
        try:
            for url in search(query, num_results=num_results):
                result["data"].append({"url": url})
            self.logger.info(f"Retrieved {len(result['data'])} web results for query: {query}")
        except Exception as e:
            self.logger.error(f"Web search failed: {e}")
            result["error"] = str(e)

        return result

    def email_osint(self, email):
        """Check email-related OSINT data using holehe."""
        result = {"email": email, "data": []}
        try:
            from holehe.core import get_modules
            modules = get_modules()
            for module in modules:
                try:
                    out = module(email)
                    if out.get("exists"):
                        result["data"].append({
                            "platform": out.get("name"),
                            "exists": out.get("exists"),
                            "additional_info": out.get("other")
                        })
                except Exception as e:
                    self.logger.warning(f"Module {module.__name__} failed for {email}: {e}")
            self.logger.info(f"Retrieved email OSINT for {email}")
        except Exception as e:
            self.logger.error(f"Email OSINT failed: {e}")
            result["error"] = str(e)

        return result

    def save_results(self, data, filename_prefix="osint_result"):
        """Save results to a JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            self.logger.info(f"Results saved to {filename}")
            return {"status": "success", "filename": filename}
        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")
            return {"status": "error", "message": str(e)}

def main():
    print("SabazOSINT Framework by Mr. Sabaz Ali Khan, Pakistani Ethical Hacker")
    print("WARNING: Use this tool ethically and legally. Respect privacy and platform terms.")
    
    # Example usage
    osint = SabazOSINT(
        twitter_api_key="YOUR_API_KEY",
        twitter_api_secret="YOUR_API_SECRET",
        twitter_access_token="YOUR_ACCESS_TOKEN",
        twitter_access_secret="YOUR_ACCESS_SECRET"
    )

    # Twitter/X search
    twitter_result = osint.twitter_search(username="example_user", query="OSINT", max_results=5)
    osint.save_results(twitter_result, "twitter_osint")

    # Instagram profile
    instagram_result = osint.instagram_profile("example_user")
    osint.save_results(instagram_result, "instagram_osint")

    # Web search
    web_result = osint.web_search("OSINT tools")
    osint.save_results(web_result, "web_osint")

    # Email OSINT
    email_result = osint.email_osint("example@email.com")
    osint.save_results(email_result, "email_osint")

if __name__ == "__main__":
    main()