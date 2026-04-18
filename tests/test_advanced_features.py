import unittest
from typing import List, Dict, Any

from nanobot_abi_skill.advanced_features import TopicClusterer

class TestTopicClusterer(unittest.TestCase):
    def setUp(self):
        """
        Set up test data for topic clustering
        """
        self.sample_insights = [
            {
                'title': 'AI in Healthcare Diagnostics',
                'content': 'Machine learning algorithms improving medical diagnosis accuracy',
                'tags': ['AI', 'Healthcare', 'Machine Learning']
            },
            {
                'title': 'AI Transforming Medical Imaging',
                'content': 'Deep learning models detecting diseases from medical scans',
                'tags': ['AI', 'Healthcare', 'Deep Learning']
            },
            {
                'title': 'Blockchain in Financial Services',
                'content': 'Decentralized finance applications revolutionizing banking',
                'tags': ['Blockchain', 'Finance', 'Decentralization']
            },
            {
                'title': 'Cryptocurrency and Blockchain Technology',
                'content': 'Exploring the impact of blockchain on digital currencies',
                'tags': ['Blockchain', 'Cryptocurrency', 'Finance']
            }
        ]
    
    def test_cluster_by_tags(self):
        """
        Test clustering insights by tags
        """
        clusterer = TopicClusterer()
        clusters = clusterer.cluster_by_tags(self.sample_insights)
        
        # Verify cluster creation
        self.assertIsNotNone(clusters)
        self.assertTrue(len(clusters) > 0)
        
        # Check specific clusters
        healthcare_cluster = next(
            (cluster for cluster in clusters if any('Healthcare' in insight['tags'] for insight in cluster['insights'])), 
            None
        )
        blockchain_cluster = next(
            (cluster for cluster in clusters if any('Blockchain' in insight['tags'] for insight in cluster['insights'])), 
            None
        )
        
        # Validate Healthcare cluster
        self.assertIsNotNone(healthcare_cluster)
        self.assertTrue(any('Healthcare' in insight['tags'] for insight in healthcare_cluster['insights']))
        
        # Validate Blockchain cluster
        self.assertIsNotNone(blockchain_cluster)
        self.assertTrue(any('Blockchain' in insight['tags'] for insight in blockchain_cluster['insights']))
    
    def test_generate_cluster_summary(self):
        """
        Test generating summary for a cluster
        """
        clusterer = TopicClusterer()
        clusters = clusterer.cluster_by_tags(self.sample_insights)
        
        # Select a cluster for summary generation
        healthcare_cluster = next(
            (cluster for cluster in clusters if any('Healthcare' in insight['tags'] for insight in cluster['insights'])), 
            None
        )
        
        # Generate summary
        summary = clusterer.generate_cluster_summary(healthcare_cluster)
        
        # Validate summary
        self.assertIsNotNone(summary)
        self.assertTrue(len(summary) > 10)  # Ensure some meaningful content
        self.assertTrue('Healthcare' in summary or 'AI' in summary)
    
    def test_similarity_scoring(self):
        """
        Test calculating similarity between insights
        """
        clusterer = TopicClusterer()
        
        # Test similarity between two healthcare insights
        healthcare_insights = [
            insight for insight in self.sample_insights if 'Healthcare' in insight['tags']
        ]
        
        similarity_score = clusterer.calculate_similarity(
            healthcare_insights[0], 
            healthcare_insights[1]
        )
        
        # Validate similarity score
        self.assertIsNotNone(similarity_score)
        self.assertTrue(0 <= similarity_score <= 1)
        self.assertGreater(similarity_score, 0.5)  # High similarity expected
    
    def test_edge_cases(self):
        """
        Test edge cases for topic clustering
        """
        clusterer = TopicClusterer()
        
        # Test empty insights list
        empty_clusters = clusterer.cluster_by_tags([])
        self.assertEqual(len(empty_clusters), 0)
        
        # Test insights with no common tags
        unique_insights = [
            {
                'title': 'Unique Insight 1',
                'content': 'Some unique content',
                'tags': ['Unique1']
            },
            {
                'title': 'Unique Insight 2',
                'content': 'Another unique content',
                'tags': ['Unique2']
            }
        ]
        
        unique_clusters = clusterer.cluster_by_tags(unique_insights)
        self.assertEqual(len(unique_clusters), 2)  # Each insight forms its own cluster

if __name__ == '__main__':
    unittest.main()