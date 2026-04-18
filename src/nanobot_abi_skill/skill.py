import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
from typing import List, Optional, Dict, Any

class AutonomousBusinessIntelligenceSkill:
    def __init__(
        self, 
        insights_dir: Optional[str] = None, 
        log_dir: Optional[str] = None,
        log_level: int = logging.INFO,
        max_log_size_bytes: int = 1 * 1024 * 1024,  # 1 MB
        backup_count: int = 5  # Number of backup log files to keep
    ):
        """
        Initialize the Autonomous Business Intelligence Skill
        
        :param insights_dir: Directory to store generated insights
        :param log_dir: Directory to store log files
        :param log_level: Logging level
        :param max_log_size_bytes: Maximum size of log file before rotation
        :param backup_count: Number of backup log files to keep
        """
        # Determine log directory
        self.log_dir = log_dir or os.path.join(
            os.path.dirname(__file__), '..', 'logs'
        )
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Configure logging with log rotation
        log_file_path = os.path.join(self.log_dir, 'abi_skill.log')
        
        # Create a rotating file handler
        file_handler = RotatingFileHandler(
            log_file_path, 
            maxBytes=max_log_size_bytes,  # 1 MB per log file
            backupCount=backup_count  # Keep 5 backup files
        )
        
        # Create console handler
        console_handler = logging.StreamHandler()
        
        # Set log formatting
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Configure logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)
        
        # Clear any existing handlers to prevent duplicate logging
        self.logger.handlers.clear()
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
        # Configure insights directory
        self.insights_dir = insights_dir or os.path.join(
            os.path.dirname(__file__), '..', 'insights'
        )
        os.makedirs(self.insights_dir, exist_ok=True)

    def _validate_topics(self, topics: Optional[List[str]]) -> List[str]:
        """
        Validate and prepare topics for insight generation
        
        :param topics: List of topics to validate
        :return: Validated list of topics
        """
        # If topics is None or an empty list, return default topics
        if not topics:
            return [
                "AI business transformation trends 2026",
                "Enterprise AI strategy and implementation",
                "Future of work with artificial intelligence"
            ]
        
        return [
            topic for topic in topics 
            if topic and isinstance(topic, str)
        ]

    def generate_insights(
        self, 
        topics: Optional[List[str]] = None, 
        web_search_fn: Optional[Any] = None, 
        message_fn: Optional[Any] = None
    ) -> List[str]:
        """
        Generate business intelligence insights
        
        :param topics: Optional list of topics
        :param web_search_fn: Optional web search function (for dependency injection)
        :param message_fn: Optional message function (for dependency injection)
        :return: List of generated insight file paths
        """
        # Log the start of insight generation
        self.logger.info("Starting insight generation process")
        
        # Validate and prepare topics
        validated_topics = self._validate_topics(topics)
        
        # Validate search and message functions
        if web_search_fn is None:
            try:
                from nanobot.tools import web_search
            except ImportError:
                self.logger.error("Web search function not available")
                return []
        else:
            web_search = web_search_fn
        
        if message_fn is None:
            try:
                from nanobot.tools import message
            except ImportError:
                self.logger.error("Message function not available")
                return []
        else:
            message = message_fn

        # Generate insights
        generated_insights = []
        
        for topic in validated_topics:
            try:
                # Perform web search
                search_results = web_search(query=topic, count=3)
                
                # Generate insight filename
                insight_filename = (
                    f"{datetime.now().strftime('%Y%m%d')}_"
                    f"{topic.replace(' ', '_')[:50]}_insights.md"
                )
                insight_path = os.path.join(self.insights_dir, insight_filename)
                
                # Write insights to file
                with open(insight_path, 'w', encoding='utf-8') as f:
                    f.write(f"# Strategic Insights: {topic}\n\n")
                    f.write(f"## Generated on: {datetime.now().isoformat()}\n\n")
                    
                    # Add research sources
                    f.write("## Research Sources:\n")
                    for result in search_results:
                        f.write(f"- [{result['title']}]({result['url']})\n")
                    
                    f.write("\n## Key Insights:\n")
                    
                    # Add snippets as insights
                    for result in search_results:
                        f.write(f"### {result['title']}\n")
                        f.write(f"{result['snippet']}\n\n")
                
                generated_insights.append(insight_path)
                self.logger.info(f"Successfully generated insights for topic: {topic}")
            
            except Exception as topic_error:
                self.logger.error(f"Failed to generate insights for topic '{topic}': {topic_error}")
        
        # Deliver insights via message
        if generated_insights:
            try:
                message(
                    content="🔍 Strategic Business Intelligence Insights\n\n"
                            "I've generated the latest strategic insights for you:",
                    media=generated_insights
                )
                self.logger.info(f"Delivered {len(generated_insights)} insight reports")
            except Exception as delivery_error:
                self.logger.error(f"Failed to deliver insights: {delivery_error}")
        
        # Log the completion of insight generation
        self.logger.info("Insight generation process completed")
        
        return generated_insights

def main(topics: Optional[List[str]] = None):
    """
    Main function for direct skill invocation
    
    :param topics: Optional list of topics
    """
    skill = AutonomousBusinessIntelligenceSkill()
    skill.generate_insights(topics)