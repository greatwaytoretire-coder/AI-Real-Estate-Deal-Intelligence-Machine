from datetime import datetime, timezone
from typing import List, Dict, Any


class LearningMemory:
    """
    Persistent adaptive memory store.

    Stores learned investment signals
    that influence future decisions.
    """


    def __init__(self):

        self.memories: List[Dict[str, Any]] = []



    def store(
        self,
        memory: Dict[str, Any],
    ):

        memory["created_at"] = datetime.now(
            timezone.utc
        )

        self.memories.append(memory)

        return memory



    def get_all(self):

        return self.memories



    def count(self):

        return len(self.memories)



    def successful_patterns(self):

        return [

            memory

            for memory in self.memories

            if memory.get(
                "outcome"
            )
            ==
            "SUCCESS"

        ]
    