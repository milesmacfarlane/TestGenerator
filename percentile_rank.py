"""
Percentile Rank Generator
Generates questions for outcome 12E5.S.2
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from question_models import Question, QuestionType, AnswerFormat
from statistics_calculator import StatisticsCalculator
from data_manager import DataManager


class PercentileRankGenerator:
    """
    Generate percentile rank questions
    
    Provincial Exam Patterns:
    - Question 37 (1 mark): Conceptual understanding
    - Question 38 (2 marks): Calculate PR using formula
    
    Formula: PR = (b/n) × 100
    """
    
    CALCULATION_CONTEXTS = [
        {
            "id": "credit_scores",
            "template": "Financial institutions use credit scores to decide whether people qualify for loans. Below is a list of credit scores for people applying for a bank loan.",
            "value_range": (600, 850),
            "dataset_size": 20
        },
        {
            "id": "test_scores",
            "template": "{name} teaches a class of {n} students. The test scores are shown below.",
            "uses": ["name"],
            "value_range": (50, 100),
            "dataset_size": (15, 25)
        },
        {
            "id": "property_values",
            "template": "A real estate agent compiled home prices in {city}. The prices (in thousands) are shown below.",
            "uses": ["city"],
            "value_range": (200, 800),
            "dataset_size": 20
        },
        {
            "id": "produce_weights",
            "template": "{name} is a farmer who grows produce. The weights (in grams) of items from new plants are shown below.",
            "uses": ["name"],
            "value_range": (90, 180),
            "dataset_size": (12, 18)
        }
    ]
    
    CONCEPTUAL_CONTEXTS = [
        {
            "id": "entrance_exam",
            "template": "{name} must write an entrance exam to enter university. A minimum grade of {min_grade}% is required for acceptance.",
            "uses": ["name"]
        },
        {
            "id": "job_ranking",
            "template": "A company ranks job applicants based on their interview scores. The top {top_percent}% of candidates move to the next round.",
            "uses": []
        }
    ]
    
    def __init__(self, data_manager: DataManager):
        self.data = data_manager
        self.calc = StatisticsCalculator()
    
    def generate_question(self, difficulty: int = 2, question_type: str = "calculation") -> Question:
        """
        Generate percentile rank question
        
        Args:
            difficulty: 1-5
            question_type: "calculation" or "conceptual"
        """
        if question_type == "calculation":
            return self._generate_calculation_question(difficulty)
        else:
            return self._generate_conceptual_question(difficulty)
    
    def _generate_calculation_question(self, difficulty: int) -> Question:
        """
        Generate calculation question (2 marks)
        Provincial Exam Question 38 pattern
        """
        # Select context
        context_template = random.choice(self.CALCULATION_CONTEXTS)
        
        # Generate dataset
        if isinstance(context_template["dataset_size"], tuple):
            n = random.randint(*context_template["dataset_size"])
        else:
            n = context_template["dataset_size"]
        
        value_min, value_max = context_template["value_range"]
        
        # Generate sorted dataset
        dataset = sorted([random.randint(value_min, value_max) for _ in range(n)])
        
        # Select target value (not highest or lowest)
        target_index = random.randint(int(n * 0.3), int(n * 0.8))
        target_value = dataset[target_index]
        
        # Calculate b and PR
        b = sum(1 for x in dataset if x < target_value)
        pr = self.calc.percentile_rank(target_value, dataset)
        
        # Format context
        context_str = self._populate_context(context_template, n)
        
        # Format dataset (display as table for readability)
        dataset_str = self._format_dataset(dataset, context_template["id"])
        
        # Build question
        question_text = f"""{context_str}

{dataset_str}

Calculate the percentile rank for a score of {target_value}."""
        
        # Build solution
        solution_steps = [
            f"b = {b} (number of scores below {target_value})",
            f"n = {n} (total number of scores)",
            f"PR = (b/n) × 100",
            f"PR = ({b}/{n}) × 100",
            f"PR = {pr:.0f}",
            f"Therefore, {target_value} is at the {pr:.0f}th percentile"
        ]
        
        return Question(
            id="",
            unit="Statistics",
            outcomes=["12E5.S.2"],
            question_type=QuestionType.CALCULATION,
            difficulty=difficulty,
            total_marks=2,
            mark_breakdown={"formula_substitution": 1.0, "answer": 1.0},
            context=context_str,
            question_text=question_text,
            given_data={
                "dataset": dataset,
                "target_value": target_value,
                "b": b,
                "n": n
            },
            answer=int(pr),
            answer_format=AnswerFormat.NUMERIC,
            solution_steps=solution_steps,
            context_template_id=context_template["id"],
            requires_calculator=True
        )
    
    def _generate_conceptual_question(self, difficulty: int) -> Question:
        """
        Generate conceptual question (1 mark)
        Provincial Exam Question 37 pattern
        """
        context_template = random.choice(self.CONCEPTUAL_CONTEXTS)
        
        # Generate scenario
        if context_template["id"] == "entrance_exam":
            name = self.data.get_name(with_title=True)
            min_grade = random.choice([70, 75, 80])
            
            # Last year: below required percentile, not accepted
            last_year_pr = random.randint(60, min_grade - 5)
            # This year: higher percentile
            this_year_pr = random.randint(last_year_pr + 5, 95)
            
            context = context_template["template"].format(
                name=name["full_name"],
                min_grade=min_grade
            )
            
            question_text = f"""{context}

Last year their mark was in the {last_year_pr}th percentile. They were not accepted.
This year their mark is in the {this_year_pr}th percentile.

Justify why it cannot be determined if they will be accepted this year."""
            
            answer = "It cannot be determined because percentile rank only indicates their position relative to other test-takers, not their actual grade. A higher percentile does not guarantee the minimum grade of {min_grade}% is achieved."
            
        else:  # job_ranking
            top_percent = random.choice([10, 15, 20, 25])
            
            context = context_template["template"].format(top_percent=top_percent)
            
            candidate_pr = random.randint(75, 90)
            
            question_text = f"""{context}

A candidate scored in the {candidate_pr}th percentile.

Explain whether this candidate will move to the next round."""
            
            if candidate_pr >= (100 - top_percent):
                answer = f"Yes, the candidate will move forward. The {candidate_pr}th percentile means {100 - candidate_pr}% scored higher, so they are in the top {100 - candidate_pr}% which is better than the required top {top_percent}%."
            else:
                answer = f"No, the candidate will not move forward. The {candidate_pr}th percentile means {100 - candidate_pr}% scored higher, which is more than the top {top_percent}% requirement."
        
        solution_steps = [
            "Key concept: Percentile rank indicates relative position, not actual score",
            f"Answer: {answer}"
        ]
        
        return Question(
            id="",
            unit="Statistics",
            outcomes=["12E5.S.2"],
            question_type=QuestionType.JUSTIFICATION,
            difficulty=difficulty,
            total_marks=1,
            mark_breakdown={"reasoning": 1.0},
            context=context,
            question_text=question_text,
            given_data={
                "context_template": context_template["id"]
            },
            answer=answer,
            answer_format=AnswerFormat.TEXT,
            solution_steps=solution_steps,
            context_template_id=context_template["id"],
            requires_calculator=False
        )
    
    def _format_dataset(self, dataset: list, context_id: str) -> str:
        """Format dataset for display"""
        # Show in rows for readability
        chunk_size = 5
        chunks = [dataset[i:i+chunk_size] for i in range(0, len(dataset), chunk_size)]
        
        if "credit" in context_id or "property" in context_id:
            # No extra formatting needed
            formatted_chunks = [", ".join(map(str, chunk)) for chunk in chunks]
        elif "produce" in context_id:
            # Add 'g' for grams
            formatted_chunks = [", ".join([f"{x}g" for x in chunk]) for chunk in chunks]
        else:
            # Regular numbers
            formatted_chunks = [", ".join(map(str, chunk)) for chunk in chunks]
        
        return "\n".join(formatted_chunks)
    
    def _populate_context(self, template: dict, n: int = None) -> str:
        """Populate context template"""
        context = template["template"]
        uses = template.get("uses", [])
        
        replacements = {}
        
        if "name" in uses:
            name_data = self.data.get_name(with_title=True)
            replacements["{name}"] = name_data["full_name"]
        
        if "city" in uses:
            place = self.data.get_place_cdn()
            replacements["{city}"] = place["city"]
        
        if "{n}" in context:
            replacements["{n}"] = str(n)
        
        for key, value in replacements.items():
            context = context.replace(key, value)
        
        return context
