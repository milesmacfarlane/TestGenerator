"""
Percentile Rank Generator - UPDATED WITH PROPER FORMATTING
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
    """Generate percentile rank questions with proper answer formatting"""
    
    CALCULATION_CONTEXTS = [
        {
            "id": "credit_scores",
            "template": "Financial institutions use credit scores to decide whether people qualify for loans. Below is a list of credit scores for people applying for a bank loan.",
            "value_range": (600, 850),
            "dataset_size": 20,
            "unit": "",
            "value_name": "score"
        },
        {
            "id": "test_scores",
            "template": "{name} teaches a class of {n} students. The test scores are shown below.",
            "uses": ["name"],
            "value_range": (50, 100),
            "dataset_size": (15, 25),
            "unit": "%",
            "value_name": "score"
        },
        {
            "id": "property_values",
            "template": "A real estate agent compiled home prices in {city}. The prices (in thousands of dollars) are shown below.",
            "uses": ["city"],
            "value_range": (200, 800),
            "dataset_size": 20,
            "unit": "k",  # Thousands
            "value_name": "price"
        },
        {
            "id": "produce_weights",
            "template": "{name} is a farmer who grows produce. The weights (in grams) of items from new plants are shown below.",
            "uses": ["name"],
            "value_range": (90, 180),
            "dataset_size": (12, 18),
            "unit": "g",
            "value_name": "weight"
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
        """Generate percentile rank question with proper formatting"""
        if question_type == "calculation":
            return self._generate_calculation_question(difficulty)
        else:
            return self._generate_conceptual_question(difficulty)
    
    def _generate_calculation_question(self, difficulty: int) -> Question:
        """Generate calculation question with proper answer formatting"""
        
        context_template = random.choice(self.CALCULATION_CONTEXTS)
        
        if isinstance(context_template["dataset_size"], tuple):
            n = random.randint(*context_template["dataset_size"])
        else:
            n = context_template["dataset_size"]
        
        value_min, value_max = context_template["value_range"]
        dataset = sorted([random.randint(value_min, value_max) for _ in range(n)])
        
        target_index = random.randint(int(n * 0.3), int(n * 0.8))
        target_value = dataset[target_index]
        
        b = sum(1 for x in dataset if x < target_value)
        pr = self.calc.percentile_rank(target_value, dataset)
        
        context_str = self._populate_context(context_template, n)
        dataset_str = self._format_dataset(dataset, context_template)
        
        # Format target value with unit if applicable
        unit = context_template.get("unit", "")
        if unit == "k":
            target_display = f"${target_value}k"
        elif unit == "g":
            target_display = f"{target_value}g"
        elif unit == "%":
            target_display = f"{target_value}%"
        else:
            target_display = str(target_value)
        
        question_text = f"""{context_str}

{dataset_str}

Calculate the percentile rank for a {context_template['value_name']} of {target_display}."""
        
        # Format answer properly - Provincial exam accepts multiple formats
        pr_int = int(pr)
        formatted_answer = f"{pr_int}th percentile (or P{pr_int} or {pr_int})"
        
        # Build solution
        solution_steps = [
            f"b = {b} (number of scores below {target_display})",
            f"n = {n} (total number of scores)",
            f"PR = (b/n) × 100",
            f"PR = ({b}/{n}) × 100",
            f"PR = {pr:.1f}",
            f"Answer: {pr_int}th percentile (or P{pr_int} or {pr_int})"
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
                "n": n,
                "unit": unit
            },
            answer=formatted_answer,
            answer_format=AnswerFormat.TEXT,
            solution_steps=solution_steps,
            context_template_id=context_template["id"],
            requires_calculator=True
        )
    
    def _generate_conceptual_question(self, difficulty: int) -> Question:
        """Generate conceptual question"""
        
        context_template = random.choice(self.CONCEPTUAL_CONTEXTS)
        
        if context_template["id"] == "entrance_exam":
            name = self.data.get_name(with_title=True)
            min_grade = random.choice([70, 75, 80])
            
            last_year_pr = random.randint(60, min_grade - 5)
            this_year_pr = random.randint(last_year_pr + 5, 95)
            
            context = context_template["template"].format(
                name=name["full_name"],
                min_grade=min_grade
            )
            
            question_text = f"""{context}

Last year their mark was in the {last_year_pr}th percentile. They were not accepted.
This year their mark is in the {this_year_pr}th percentile.

Justify why it cannot be determined if they will be accepted this year."""
            
            answer = f"It cannot be determined because percentile rank only indicates their position relative to other test-takers, not their actual grade. A higher percentile does not guarantee the minimum grade of {min_grade}% is achieved."
            
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
            given_data={"context_template": context_template["id"]},
            answer=answer,
            answer_format=AnswerFormat.TEXT,
            solution_steps=solution_steps,
            context_template_id=context_template["id"],
            requires_calculator=False
        )
    
    def _format_dataset(self, dataset: list, context_template: dict) -> str:
        """Format dataset for display with units"""
        chunk_size = 5
        chunks = [dataset[i:i+chunk_size] for i in range(0, len(dataset), chunk_size)]
        
        unit = context_template.get("unit", "")
        context_id = context_template["id"]
        
        if unit == "g":
            # Add 'g' for grams
            formatted_chunks = [", ".join([f"{x}g" for x in chunk]) for chunk in chunks]
        elif unit == "k":
            # Add '$' and 'k' for thousands
            formatted_chunks = [", ".join([f"${x}k" for x in chunk]) for chunk in chunks]
        elif unit == "%":
            # Add '%' for percentages
            formatted_chunks = [", ".join([f"{x}%" for x in chunk]) for chunk in chunks]
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
