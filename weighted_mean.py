"""
Weighted Mean Generator
Generates questions for outcome 12E5.S.1 (weighted means)
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from question_models import Question, QuestionType, AnswerFormat
from statistics_calculator import StatisticsCalculator
from data_manager import DataManager


class WeightedMeanGenerator:
    """
    Generate weighted mean questions
    
    Provincial Exam: 2-3 marks
    Student Booklet: Lesson 3A and 3B
    
    Two types:
    - Type A: Percentage of total (course grades)
    - Type B: Repeating items (frequency data)
    """
    
    # Type A: Percentage of Total
    PERCENTAGE_CONTEXTS = [
        {
            "id": "course_grades",
            "template": "{name} is calculating their final grade in {course}. The grading breakdown is shown below.",
            "uses": ["name", "course"],
            "categories": ["Homework", "Quizzes", "Midterm", "Project", "Final Exam"],
            "typical_weights": [0.10, 0.20, 0.25, 0.20, 0.25]
        },
        {
            "id": "portfolio_evaluation",
            "template": "{name} is evaluating candidates for a position at {business}. The evaluation criteria are shown below.",
            "uses": ["name", "business"],
            "categories": ["Experience", "Education", "Interview", "References", "Skills Test"],
            "typical_weights": [0.30, 0.20, 0.25, 0.10, 0.15]
        },
        {
            "id": "art_competition",
            "template": "{name} entered a competition with scores in different categories.",
            "uses": ["name"],
            "categories": ["Originality", "Design", "Colour", "Technique"],
            "typical_weights": [0.35, 0.40, 0.25, 0.00]  # 3 categories
        }
    ]
    
    # Type B: Repeating Items
    FREQUENCY_CONTEXTS = [
        {
            "id": "server_tips",
            "template": "{name} works as a server and received tips during one shift.",
            "uses": ["name"],
            "value_range": (5, 15),
            "frequencies_range": (2, 6)
        },
        {
            "id": "weekly_hours",
            "template": "{name} tracked the number of days worked per week over a year.",
            "uses": ["name"],
            "value_range": (1, 7),
            "frequencies_range": (2, 14)
        },
        {
            "id": "item_prices",
            "template": "{name} sells crafts at markets. The prices and quantities sold are shown below.",
            "uses": ["name"],
            "value_range": (10, 50),
            "frequencies_range": (3, 12)
        }
    ]
    
    def __init__(self, data_manager: DataManager):
        self.data = data_manager
        self.calc = StatisticsCalculator()
    
    def generate_question(self, difficulty: int = 2, question_type: str = "percentage") -> Question:
        """
        Generate weighted mean question
        
        Args:
            difficulty: 1-5
            question_type: "percentage" or "frequency"
        """
        if question_type == "percentage":
            return self._generate_percentage_question(difficulty)
        else:
            return self._generate_frequency_question(difficulty)
    
    def _generate_percentage_question(self, difficulty: int) -> Question:
        """Generate Type A: Percentage of total (e.g., course grades)"""
        
        # Select context
        context_template = random.choice(self.PERCENTAGE_CONTEXTS)
        context_str = self._populate_context(context_template)
        
        # Generate categories and weights
        num_categories = 3 if difficulty <= 2 else (4 if difficulty <= 3 else 5)
        categories = context_template["categories"][:num_categories]
        
        # Generate weights that sum to 1.0
        weights = self._generate_weights(num_categories, difficulty)
        
        # Generate scores
        scores = self._generate_scores(num_categories, difficulty)
        
        # Calculate weighted mean
        weighted_mean = self.calc.calculate_weighted_mean(scores, weights)
        
        # Build table
        table_str = self._format_percentage_table(categories, scores, weights)
        
        # Build question
        question_text = f"""{context_str}

{table_str}

Calculate the final score using a weighted mean."""
        
        # Build solution
        solution_steps = []
        for i, (cat, score, weight) in enumerate(zip(categories, scores, weights)):
            weighted_value = score * weight
            solution_steps.append(f"{weight:.0%} × {score} = {weighted_value:.2f}")
        solution_steps.append(f"Total: {weighted_mean:.2f}")
        
        return Question(
            id="",
            unit="Statistics",
            outcomes=["12E5.S.1"],
            question_type=QuestionType.CALCULATION,
            difficulty=difficulty,
            total_marks=2,
            mark_breakdown={"process": 1.0, "answer": 1.0},
            context=context_str,
            question_text=question_text,
            given_data={
                "categories": categories,
                "scores": scores,
                "weights": weights,
                "context_template": context_template["id"]
            },
            answer=round(weighted_mean, 2),
            answer_format=AnswerFormat.NUMERIC,
            solution_steps=solution_steps,
            context_template_id=context_template["id"],
            requires_calculator=True
        )
    
    def _generate_frequency_question(self, difficulty: int) -> Question:
        """Generate Type B: Repeating items (frequency data)"""
        
        # Select context
        context_template = random.choice(self.FREQUENCY_CONTEXTS)
        context_str = self._populate_context(context_template)
        
        # Generate values and frequencies
        num_items = 4 if difficulty <= 2 else (5 if difficulty <= 3 else 6)
        
        value_min, value_max = context_template["value_range"]
        freq_min, freq_max = context_template["frequencies_range"]
        
        # Generate unique values
        values = sorted(random.sample(range(value_min, value_max + 1), num_items))
        
        # Generate frequencies
        frequencies = [random.randint(freq_min, freq_max) for _ in range(num_items)]
        
        # Calculate weighted mean
        weighted_mean = self.calc.calculate_weighted_mean_frequency(values, frequencies)
        
        # Format data
        data_str = self._format_frequency_data(values, frequencies, context_template["id"])
        
        # Build question
        question_text = f"""{context_str}

{data_str}

Calculate the mean."""
        
        # Build solution
        total_value = sum(v * f for v, f in zip(values, frequencies))
        total_count = sum(frequencies)
        
        solution_steps = [
            "Weighted sum: " + " + ".join([f"({v} × {f})" for v, f in zip(values, frequencies)]),
            f"= {total_value}",
            f"Total items: {total_count}",
            f"Mean: {total_value} ÷ {total_count} = {weighted_mean:.2f}"
        ]
        
        return Question(
            id="",
            unit="Statistics",
            outcomes=["12E5.S.1"],
            question_type=QuestionType.CALCULATION,
            difficulty=difficulty,
            total_marks=2,
            mark_breakdown={"process": 1.0, "answer": 1.0},
            context=context_str,
            question_text=question_text,
            given_data={
                "values": values,
                "frequencies": frequencies,
                "context_template": context_template["id"]
            },
            answer=round(weighted_mean, 2),
            answer_format=AnswerFormat.NUMERIC,
            solution_steps=solution_steps,
            context_template_id=context_template["id"],
            requires_calculator=True
        )
    
    def _generate_weights(self, num_categories: int, difficulty: int) -> list:
        """Generate weights that sum to 1.0"""
        if difficulty <= 2:
            # Easy: nice percentages (10%, 20%, 25%, etc.)
            nice_values = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40]
            weights = []
            remaining = 1.0
            
            for i in range(num_categories - 1):
                max_weight = min(remaining - 0.1 * (num_categories - i - 1), 0.40)
                available = [w for w in nice_values if w <= max_weight]
                if available:
                    weight = random.choice(available)
                else:
                    weight = round(remaining / (num_categories - i), 2)
                weights.append(weight)
                remaining -= weight
            
            weights.append(round(remaining, 2))
            return weights
        else:
            # Harder: random weights
            weights = [random.random() for _ in range(num_categories)]
            total = sum(weights)
            weights = [round(w / total, 2) for w in weights]
            
            # Adjust to ensure sum is exactly 1.0
            diff = 1.0 - sum(weights)
            weights[0] += diff
            
            return weights
    
    def _generate_scores(self, num_categories: int, difficulty: int) -> list:
        """Generate scores for each category"""
        if difficulty <= 2:
            # Easy: scores out of 100
            return [random.randint(60, 100) for _ in range(num_categories)]
        elif difficulty <= 3:
            # Medium: varied scores
            return [random.randint(50, 100) for _ in range(num_categories)]
        else:
            # Hard: scores with decimals
            return [round(random.uniform(50, 100), 1) for _ in range(num_categories)]
    
    def _format_percentage_table(self, categories: list, scores: list, weights: list) -> str:
        """Format table for percentage-based weighted mean"""
        lines = ["Category | Score | Weight"]
        lines.append("---------|-------|-------")
        
        for cat, score, weight in zip(categories, scores, weights):
            lines.append(f"{cat} | {score} | {weight:.0%}")
        
        return "\n".join(lines)
    
    def _format_frequency_data(self, values: list, frequencies: list, context_id: str) -> str:
        """Format frequency data"""
        if "tips" in context_id:
            lines = []
            for val, freq in zip(values, frequencies):
                plural = "tips" if freq != 1 else "tip"
                lines.append(f"{freq} {plural} of ${val:.2f}")
            return "\n".join(lines)
        elif "hours" in context_id or "days" in context_id:
            lines = []
            for val, freq in zip(values, frequencies):
                plural = "weeks" if freq != 1 else "week"
                days = "days" if val != 1 else "day"
                lines.append(f"{freq} {plural} working {val} {days}")
            return "\n".join(lines)
        else:
            lines = []
            for val, freq in zip(values, frequencies):
                lines.append(f"{freq} items at ${val:.2f} each")
            return "\n".join(lines)
    
    def _populate_context(self, template: dict) -> str:
        """Populate context template"""
        context = template["template"]
        uses = template["uses"]
        
        replacements = {}
        
        if "name" in uses:
            name_data = self.data.get_name(with_title=True)
            replacements["{name}"] = name_data["full_name"]
        
        if "course" in uses:
            replacements["{course}"] = self.data.get_course()
        
        if "business" in uses:
            replacements["{business}"] = self.data.get_business()
        
        for key, value in replacements.items():
            context = context.replace(key, value)
        
        return context
