import os
import unittest
import tempfile
from typing import List, Dict

from nanobot_abi_skill.skill import AutonomousBusinessIntelligenceSkill

class TestAutonomousBusinessIntelligenceSkill(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for insights
        self.test_insights_dir = tempfile.mkdtemp()
        
        # Initialize skill with test insights directory
        self.skill = AutonomousBusinessIntelligenceSkill(
            insights_dir=self.test_insights_dir,
            log_level=None  # Disable logging for cleaner test output
        )
    
    def mock_web_search(self, query: str, count: int = 3) -> List[Dict[str, str]]:
        """
        Mock web search function for testing
        
        :param query: Search query
        :param count: Number of results to return
        :return: List of mock search results
        """
        return [
            {
                'title': f'Test Result for {query} {i}',
                'url': f'https://example.com/{query.replace(" ", "-")}-{i}',
                'snippet': f'This is a mock snippet for {query} result {i}'
            } for i in range(count)
        ]
    
    def mock_message(self, content: str, media: List[str] = None):
        """
        Mock message function for testing
        
        :param content: Message content
        :param media: List of media files
        """
        # In test, we'll just store the message details
        self.last_message_content = content
        self.last_message_media = media
    
    def test_generate_insights_default_topics(self):
        """
        Test generating insights with default topics
        """
        insights = self.skill.generate_insights(
            web_search_fn=self.mock_web_search,
            message_fn=self.mock_message
        )
        
        # Verify insights were generated
        self.assertTrue(len(insights) > 0)
        
        # Check that insight files exist
        for insight_path in insights:
            self.assertTrue(os.path.exists(insight_path))
            with open(insight_path, 'r') as f:
                content = f.read()
                self.assertTrue(len(content) > 100)  # Ensure meaningful content
    
    def test_generate_insights_custom_topics(self):
        """
        Test generating insights with custom topics
        """
        custom_topics = [
            "AI in Healthcare",
            "Blockchain Technology Trends"
        ]
        
        insights = self.skill.generate_insights(
            topics=custom_topics,
            web_search_fn=self.mock_web_search,
            message_fn=self.mock_message
        )
        
        # Verify insights were generated for custom topics
        self.assertEqual(len(insights), len(custom_topics))
        
        # Check that insight files exist
        for insight_path in insights:
            self.assertTrue(os.path.exists(insight_path))
            with open(insight_path, 'r') as f:
                content = f.read()
                self.assertTrue(len(content) > 100)  # Ensure meaningful content
    
    def test_generate_insights_empty_topics(self):
        """
        Test generating insights with empty topics list
        """
        insights = self.skill.generate_insights(
            topics=[],
            web_search_fn=self.mock_web_search,
            message_fn=self.mock_message
        )
        
        # Verify default topics are used when empty list is provided
        self.assertTrue(len(insights) > 0)
    
    def test_generate_insights_none_topics(self):
        """
        Test generating insights with None topics
        """
        insights = self.skill.generate_insights(
            topics=None,
            web_search_fn=self.mock_web_search,
            message_fn=self.mock_message
        )
        
        # Verify default topics are used
        self.assertTrue(len(insights) > 0)

if __name__ == '__main__':
    unittest.main()