import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from typing import Dict, List, Any, Optional
from datetime import datetime


class MongoDBClient:
    """
    MongoDB connection handler for PES.
    Uses MongoDB Atlas free tier.
    """

    def __init__(self):
        """Initialize MongoDB connection."""
        self.uri = os.getenv('MONGODB_URI') or os.getenv('MONGO_URI')
        if not self.uri:
            raise ValueError("MONGODB_URI environment variable not set. Please configure it in your deployment.")

        self.client = None
        self.db = None
        self.collection = None
        self._connect()

    def _connect(self):
        """Connect to MongoDB."""
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            # Verify connection
            self.client.admin.command('ping')
            self.db = self.client['pes_db']
            self.collection = self.db['scan_results']
            # Create indexes
            self.collection.create_index('created_at')
            self.collection.create_index('verdict')
            print("✓ MongoDB connected successfully")
        except ConnectionFailure as e:
            raise RuntimeError(f"Failed to connect to MongoDB: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"MongoDB authentication failed: {str(e)}")

    def insert_scan_result(self, result: Dict[str, Any]) -> bool:
        """
        Insert a scan result into MongoDB.

        Args:
            result (Dict[str, Any]): Scan result to store.

        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            self.collection.insert_one(result)
            return True
        except Exception as e:
            print(f"Error inserting scan result: {str(e)}")
            return False

    def query_history(self, domain: Optional[str] = None, verdict: Optional[str] = None,
                      limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Query scan history from MongoDB.

        Args:
            domain (Optional[str]): Filter by sender domain.
            verdict (Optional[str]): Filter by verdict (PHISHING/BENIGN).
            limit (int): Maximum results to return.
            offset (int): Number of results to skip.

        Returns:
            List[Dict[str, Any]]: Scan results.
        """
        try:
            query = {}
            if domain:
                query['sender_domain'] = domain
            if verdict:
                query['verdict'] = verdict

            results = list(
                self.collection.find(query)
                .sort('created_at', -1)
                .skip(offset)
                .limit(limit)
            )

            # Remove MongoDB internal _id for cleaner response
            for result in results:
                result.pop('_id', None)

            return results
        except Exception as e:
            print(f"Error querying history: {str(e)}")
            return []

    def close(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()