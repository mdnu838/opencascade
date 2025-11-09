"""
Rule-based task classifier for determining query types.
"""

import re
from typing import Tuple

from .task_types import TaskType
from ..utils.logging import setup_logger


logger = setup_logger(__name__)


class TaskClassifier:
    """Rule-based classifier for identifying task types from queries."""
    
    def __init__(self):
        """Initialize the classifier with pattern rules."""
        # Code-related patterns
        self.code_patterns = [
            r'\b(function|class|method|variable|implement|code|program|script)\b',
            r'\b(python|javascript|java|c\+\+|rust|go|typescript)\b',
            r'\b(debug|fix|refactor|optimize)\b',
            r'(```|`)',  # Code blocks
            r'\b(algorithm|data structure|api)\b',
        ]
        
        # Embeddings/search patterns
        self.embeddings_patterns = [
            r'\b(embed|embedding|vector|similarity)\b',
            r'\b(search|find similar|semantic search)\b',
            r'\b(index|retrieve|lookup)\b',
        ]
        
        # Compile patterns for efficiency
        self.code_regex = re.compile('|'.join(self.code_patterns), re.IGNORECASE)
        self.embeddings_regex = re.compile('|'.join(self.embeddings_patterns), re.IGNORECASE)
    
    def classify(self, query: str) -> Tuple[TaskType, float]:
        """Classify a query into a task type.
        
        Args:
            query: Input query to classify
            
        Returns:
            Tuple of (TaskType, confidence_score)
        """
        query_lower = query.lower()
        
        # Check for embeddings
        if self.embeddings_regex.search(query):
            logger.info("Classified as EMBEDDINGS task")
            return TaskType.EMBEDDINGS, 0.9
        
        # Check for code
        code_matches = len(self.code_regex.findall(query))
        if code_matches > 0:
            confidence = min(0.9, 0.6 + (code_matches * 0.1))
            logger.info(f"Classified as CODE task (confidence: {confidence})")
            return TaskType.CODE, confidence
        
        # Default to chat
        logger.info("Classified as CHAT task (default)")
        return TaskType.CHAT, 0.7
    
    def classify_batch(self, queries: list[str]) -> list[Tuple[TaskType, float]]:
        """Classify multiple queries at once.
        
        Args:
            queries: List of queries to classify
            
        Returns:
            List of (TaskType, confidence) tuples
        """
        return [self.classify(query) for query in queries]
