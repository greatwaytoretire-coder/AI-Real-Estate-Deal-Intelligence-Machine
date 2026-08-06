from typing import List


class PatternDetector:
    """
    Detects investment patterns from completed learning records.

    Sprint 4 Part 3:
    - Reads LearningRecord objects
    - Identifies repeatable deal patterns
    - Produces confidence scoring
    """


    def analyze(
        self,
        learning_records: List,
    ):

        patterns = []


        if not learning_records:

            return {

                "patterns": [],

                "confidence": 0,

            }



        categories = [

            record.category

            for record in learning_records

        ]



        lessons = [

            record.lesson

            for record in learning_records

        ]



        #
        # Detect successful acquisition patterns
        #

        if "SUCCESSFUL_ACQUISITION" in categories:

            patterns.append(

                "Successful acquisitions are producing repeatable positive signals."

            )



        #
        # Detect high profit patterns
        #

        if "HIGH_PROFIT_DEAL" in categories:

            patterns.append(

                "High profit opportunities should receive increased priority scoring."

            )



        #
        # Detect buyer demand patterns
        #

        if "BUYER_MATCH" in categories:

            patterns.append(

                "Strong buyer matches indicate improved disposition probability."

            )



        #
        # Generic learning fallback
        #

        if not patterns and lessons:

            patterns.append(

                "Additional deal history is required to identify stronger investment patterns."

            )



        confidence = min(

            len(learning_records) * 10,

            100,

        )



        return {

            "patterns":

                patterns,


            "confidence":

                confidence,

        }