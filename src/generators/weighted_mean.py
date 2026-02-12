"""
Weighted Mean Generator - UPDATED WITH UNITS
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
    """Generate weighted mean questions with proper unit formatting"""
    
    # Type A: Percentage of Total
    PERCENTAGE_CONTEXTS = [
        {
            "id": "course_grades",
            "template": "{name} is calculating their final grade in {course}. The grading breakdown is shown below.",
            "uses": ["name", "course"],
            "categories": ["Homework", "Quizzes", "Midterm", "Project", "Final Exam"],
            "typical_weights": [0.10, 0.20, 0.25, 0.20, 0.25],
            "unit": "%",
            "unit_display": "points"
        },
        {
            "id": "portfolio_evaluation",
            "template": "{name} is evaluating candidates for a position at {business}. The evaluation criteria are shown below.",
            "uses": ["name", "business"],
            "categories": ["Experience", "Education", "Interview", "References", "Skills Test"],
            "typical_weights": [0.30, 0.20, 0.25, 0.10, 0.15],
            "unit": "points",
            "unit_display": "points"
        },
        {
            "id": "art_competition",
            "template": "{name} entered a competition with scores in different categories.",
            "uses": ["name"],
            "categories": ["Originality", "Design", "Colour", "Technique"],
            "typical_weights": [0.35, 0.40, 0.25, 0.00],
            "unit": "points",
            "unit_display": "points"
        }
    ]
    
    # Type B: Repeating Items
    FREQUENCY_CONTEXTS = [
        {
            "id": "server_tips",
            "template": "{name} works as a server and received tips during one shift.",
            "uses": ["name"],
            "value_range": (5, 15),
            "frequencies_range": (2, 6),
            "unit": "$",
            "unit_position": "prefix"
        },
        {
            "id": "weekly_hours",
            "template": "{name} tracked the number of days worked per week over a year.",
            "uses": ["name"],
            "value_range": (1, 7),
            "frequencies_range": (2, 14),
            "unit": "days",
            "unit_position": "suffix"
        },
        {
            "id": "item_prices",
            "template": "{name} sells crafts at markets. The prices and quantities sold are shown below.",
            "uses": ["name"],
            "value_range": (10, 50),
            "frequencies_range": (3, 12),
            "unit": "$",
            "unit_position": "prefix"
        }
    ]
    
    def __init__(self, data_manager: DataManager):
        self.data = data_manager
        self.calc = StatisticsCalculator()
    
    def generate_question(self, difficulty: int = 2, question_type: str = "percentage") -> Question:
        """Generate weighted mean question with proper units"""
        if question_type == "percentage":
            return self._generate_percentage_question(difficulty)
        else:
            return self._generate_frequency_question(difficulty)
    
    def _generate_percentage_question(self, difficulty: int) -> Question:
        """Generate Type A: Percentage of total (e.g., course grades)"""
        
        context_template = random.choice(self.PERCENTAGE_CONTEXTS)
        context_str = self._populate_context(context_template)
        
        num_categories = 3 if difficulty <= 2 else (4 if difficulty <= 3 else 5)
        categories = context_template["categories"][:num_categories]
        
        weights = self._generate_weights(num_categories, difficulty)
        scores = self._generate_scores(num_categories, difficulty)
        
        weighted_mean = self.calc.calculate_weighted_mean(scores, weights)
        
        table_str = self._format_percentage_table(categories, scores, weights)
        
        question_text = f"""{context_str}

{table_str}

Calculate the final score using a weighted mean."""
        
        # Format answer with unit
        unit_display = context_template.get("unit_display", "points")
        formatted_answer = f"{weighted_mean:.2f} {unit_display}"
        
        # Build solution with units
        solution_steps = []
        for cat, score, weight in zip(categories, scores, weights):
            weighted_value = score * weight
            solution_steps.append(f"{weight:.0%} × {score} = {weighted_value:.2f}")
        solution_steps.append(f"Total: {weighted_mean:.2f} {unit_display}")
        
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
                "context_template": context_template["id"],
                "unit": unit_display
            },
            answer=formatted_answer,  # Answer includes unit
            answer_format=AnswerFormat.NUMERIC_WITH_UNIT,
            solution_steps=solution_steps,
            context_template_id=context_template["id"],
            requires_calculator=True
        )
    
    def _generate_frequency_question(self, difficulty: int) -> Question:
        """Generate Type B: Repeating items (frequency data) with units"""
        
        context_template = random.choice(self.FREQUENCY_CONTEXTS)
        context_str = self._populate_context(context_template)
        
        num_items = 4 if difficulty <= 2 else (5 if difficulty <= 3 else 6)
        
        value_min, value_max = context_template["value_range"]
        freq_min, freq_max = context_template["frequencies_range"]
        
        values = sorted(random.sample(range(value_min, value_max + 1), num_items))
        frequencies = [random.randint(freq_min, freq_max) for _ in range(num_items)]
        
        weighted_mean = self.calc.calculate_weighted_mean_frequency(values, frequencies)
        
        data_str = self._format_frequency_data(values, frequencies, context_template)
        
        question_text = f"""{context_str}

{data_str}

Calculate the mean."""
        
        # Format answer with unit
        unit = context_template.get("unit", "")
        unit_position = context_template.get("unit_position", "suffix")
        
        if unit_position == "prefix":
            formatted_answer = f"{unit}{weighted_mean:.2f}"
        else:
            formatted_answer = f"{weighted_mean:.2f} {unit}"
        
        # Build solution with units
        total_value = sum(v * f for v, f in zip(values, frequencies))
        total_count = sum(frequencies)
        
        solution_steps = [
            "Weighted sum: " + " + ".join([f"({v} × {f})" for v, f in zip(values, frequencies)]),
            f"= {total_value}",
            f"Total items: {total_count}",
            f"Mean: {total_value} ÷ {total_count} = {formatted_answer}"
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
                "context_template": context_template["id"],
                "unit": unit,
                "unit_position": unit_position
            },
            answer=formatted_answer,  # Answer includes unit
            answer_format=AnswerFormat.NUMERIC_WITH_UNIT,
            solution_steps=solution_steps,
            context_template_id=context_template["id"],
            requires_calculator=True
        )
    
    def _generate_weights(self, num_categories: int, difficulty: int) -> list:
        """Generate weights that sum to 1.0"""
        if difficulty <= 2:
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
            weights = [random.random() for _ in range(num_categories)]
            total = sum(weights)
            weights = [round(w / total, 2) for w in weights]
            diff = 1.0 - sum(weights)
            weights[0] += diff
            return weights
    
    def _generate_scores(self, num_categories: int, difficulty: int) -> list:
        """Generate scores for each category"""
        if difficulty <= 2:
            return [random.randint(60, 100) for _ in range(num_categories)]
        elif difficulty <= 3:
            return [random.randint(50, 100) for _ in range(num_categories)]
        else:
            return [round(random.uniform(50, 100), 1) for _ in range(num_categories)]
    
    def _format_percentage_table(self, categories: list, scores: list, weights: list) -> str:
        """Format table for percentage-based weighted mean"""
        lines = ["Category | Score | Weight"]
        lines.append("---------|-------|-------")
        
        for cat, score, weight in zip(categories, scores, weights):
            lines.append(f"{cat} | {score} | {weight:.0%}")
        
        return "\n".join(lines)
    
    def _format_frequency_data(self, values: list, frequencies: list, context_template: dict) -> str:
        """Format frequency data with proper units"""
        context_id = context_template["id"]
        unit = context_template.get("unit", "")
        unit_position = context_template.get("unit_position", "suffix")
        
        lines = []
        
        if "tips" in context_id or "prices" in context_id:
            # Money format
            for val, freq in zip(values, frequencies):
                plural = "tips" if freq != 1 else "tip"
                if "prices" in context_id:
                    plural = "items" if freq != 1 else "item"
                lines.append(f"{freq} {plural} of ${val:.2f}")
        
        elif "hours" in context_id or "days" in context_id:
            # Days/hours format
            for val, freq in zip(values, frequencies):
                plural = "weeks" if freq != 1 else "week"
                days = "days" if val != 1 else "day"
                lines.append(f"{freq} {plural} working {val} {days}")
        
        else:
            # Generic format with units
            for val, freq in zip(values, frequencies):
                if unit_position == "prefix":
                    lines.append(f"{freq} items at {unit}{val}")
                else:
                    lines.append(f"{freq} items at {val} {unit}")
        
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
