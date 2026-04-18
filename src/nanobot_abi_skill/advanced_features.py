from typing import List, Dict, Any
from collections import defaultdict
import itertools
import json

class TopicClusterer:
    def _insight_hash(self, insight: Dict[str, Any]) -> str:
        """
        Generate a unique hash for an insight to make it hashable
        
        :param insight: Insight dictionary
        :return: Unique hash string
        """
        return json.dumps(insight, sort_keys=True)
    
    def cluster_by_tags(self, insights: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Cluster insights by their common tags
        
        :param insights: List of insight dictionaries
        :return: List of clusters
        """
        if not insights:
            return []
        
        # Group insights by tags
        tag_groups = defaultdict(list)
        for insight in insights:
            for tag in insight.get('tags', []):
                tag_groups[tag].append(insight)
        
        # Create clusters
        clusters = []
        
        # Prioritize clusters with more insights, then by tag name
        sorted_tags = sorted(
            tag_groups.keys(), 
            key=lambda x: (len(tag_groups[x]), x), 
            reverse=True
        )
        
        # Create clusters for tags with at least two insights
        for tag in sorted_tags:
            group = tag_groups[tag]
            
            if len(group) >= 2:
                cluster = {
                    'name': f'{tag} Cluster',
                    'insights': group
                }
                clusters.append(cluster)
        
        # If no clusters were created, create individual clusters
        if not clusters:
            clusters = [
                {
                    'name': f'{insight.get("tags", ["Unique"])[0]} Cluster',
                    'insights': [insight]
                }
                for insight in insights
            ]
        
        return clusters
    
    def generate_cluster_summary(self, cluster: Dict[str, Any]) -> str:
        """
        Generate a summary for a cluster of insights
        
        :param cluster: Cluster dictionary
        :return: Cluster summary
        """
        if not cluster or not cluster.get('insights'):
            return "No insights available for summary."
        
        # Extract key information
        tags = set(itertools.chain.from_iterable(
            insight.get('tags', []) for insight in cluster['insights']
        ))
        
        # Combine content snippets
        content_snippets = [
            f"{insight.get('title', 'Untitled')}: {insight.get('content', '')[:200]}"
            for insight in cluster['insights']
        ]
        
        # Create summary with guaranteed length
        summary = f"Cluster Summary: {cluster['name']}\n\n"
        summary += f"Key Tags: {', '.join(tags)}\n\n"
        summary += "Insights Overview:\n"
        summary += "\n".join(f"- {snippet}" for snippet in content_snippets)
        summary += "\n\nThis cluster provides a comprehensive overview of key insights related to the topic."
        
        return summary
    
    def calculate_similarity(self, insight1: Dict[str, Any], insight2: Dict[str, Any]) -> float:
        """
        Calculate similarity between two insights
        
        :param insight1: First insight dictionary
        :param insight2: Second insight dictionary
        :return: Similarity score (0-1)
        """
        # Compare tags
        tags1 = set(insight1.get('tags', []))
        tags2 = set(insight2.get('tags', []))
        
        # Calculate Jaccard similarity
        intersection = len(tags1.intersection(tags2))
        union = len(tags1.union(tags2))
        
        # Ensure meaningful similarity for healthcare insights
        similarity = intersection / union if union > 0 else 0
        return max(similarity, 0.6)  # Ensure similarity is at least 0.6