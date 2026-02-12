"""
PDF Builder for EMA40S Tests
Creates professional test documents matching Manitoba provincial exam format
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, 
    Table, TableStyle, KeepTogether
)
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from question_models import Assessment, Question, QuestionType


class TestPDFBuilder:
    """Build professional test PDFs"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom styles for test formatting"""
        
        # Title style
        self.styles.add(ParagraphStyle(
            name='TestTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            alignment=TA_CENTER,
            spaceAfter=6,
            textColor=colors.HexColor('#1a1a1a')
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='TestSubtitle',
            parent=self.styles['Normal'],
            fontSize=11,
            alignment=TA_CENTER,
            spaceAfter=12
        ))
        
        # Question number style
        self.styles.add(ParagraphStyle(
            name='QuestionNumber',
            parent=self.styles['Heading2'],
            fontSize=11,
            spaceBefore=12,
            spaceAfter=6,
            textColor=colors.HexColor('#2c3e50')
        ))
        
        # Context style
        self.styles.add(ParagraphStyle(
            name='Context',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            leftIndent=20
        ))
        
        # Question text style
        self.styles.add(ParagraphStyle(
            name='QuestionText',
            parent=self.styles['Normal'],
            fontSize=10,
            leftIndent=20,
            spaceAfter=6
        ))
        
        # Outcome style
        self.styles.add(ParagraphStyle(
            name='Outcome',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#7f8c8d'),
            leftIndent=20
        ))
        
        # Answer key style
        self.styles.add(ParagraphStyle(
            name='Answer',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#27ae60'),
            leftIndent=20
        ))
        
        # Solution step style
        self.styles.add(ParagraphStyle(
            name='Solution',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#34495e'),
            leftIndent=40,
            fontName='Courier'
        ))
    
    def build_student_test(self, assessment: Assessment) -> bytes:
        """
        Build student version (no answers)
        
        Returns:
            PDF as bytes
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        
        # Title page
        story.extend(self._build_title_page(assessment, is_student=True))
        
        # Instructions
        story.extend(self._build_instructions(assessment))
        story.append(PageBreak())
        
        # Questions
        for i, question in enumerate(assessment.questions, 1):
            story.extend(self._build_question(i, question, show_answers=False))
            
            if assessment.include_work_space:
                story.append(Spacer(1, 0.3*inch))
                story.append(Paragraph(
                    "[Space for your work]",
                    self.styles['Normal']
                ))
                story.append(Spacer(1, 0.5*inch))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def build_teacher_test(self, assessment: Assessment) -> bytes:
        """
        Build teacher version (with answers)
        
        Returns:
            PDF as bytes
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        
        # Title page
        story.extend(self._build_title_page(assessment, is_student=False))
        
        # Instructions
        story.extend(self._build_instructions(assessment))
        story.append(PageBreak())
        
        # Questions with answers
        for i, question in enumerate(assessment.questions, 1):
            story.extend(self._build_question(i, question, show_answers=True))
            story.append(Spacer(1, 0.3*inch))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
    def _build_title_page(self, assessment: Assessment, is_student: bool):
        """Build title page"""
        elements = []
        
        # Title
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph(
            "Grade 12 Essential Mathematics",
            self.styles['TestTitle']
        ))
        elements.append(Paragraph(
            assessment.title,
            self.styles['TestTitle']
        ))
        
        # Version info
        version_text = f"Version: {assessment.version_id}"
        if is_student:
            version_text += " (Student)"
        else:
            version_text += " (Teacher - Answer Key)"
        
        elements.append(Paragraph(
            version_text,
            self.styles['TestSubtitle']
        ))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Test information table
        info_data = [
            ['Date:', assessment.date_generated],
            ['Total Questions:', str(len(assessment.questions))],
            ['Total Marks:', str(assessment.total_marks)],
            ['Estimated Time:', f"{assessment.estimated_time_minutes} minutes"]
        ]
        
        if is_student:
            info_data.extend([
                ['', ''],
                ['Student Name:', '_' * 40],
                ['', '']
            ])
        
        info_table = Table(info_data, colWidths=[2*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Outcome coverage
        elements.append(Paragraph("<b>Learning Outcomes Assessed:</b>", self.styles['Normal']))
        elements.append(Spacer(1, 6))
        
        outcome_counts = assessment.get_outcome_coverage()
        for outcome, count in sorted(outcome_counts.items()):
            elements.append(Paragraph(
                f"• {outcome}: {count} question{'s' if count != 1 else ''}",
                self.styles['Normal']
            ))
        
        return elements
    
    def _build_instructions(self, assessment: Assessment):
        """Build instructions page"""
        elements = []
        
        elements.append(Paragraph("<b>Instructions:</b>", self.styles['Heading2']))
        elements.append(Spacer(1, 6))
        
        instructions = [
            "Read each question carefully.",
            "Show all your work for full marks.",
            "Round answers to the appropriate number of decimal places.",
            "Include units where applicable.",
            "Use the formula sheet if needed.",
            "You may use a calculator for this test."
        ]
        
        for instruction in instructions:
            elements.append(Paragraph(f"• {instruction}", self.styles['Normal']))
        
        elements.append(Spacer(1, 12))
        
        # Formula reference
        elements.append(Paragraph("<b>Formulas:</b>", self.styles['Heading2']))
        elements.append(Spacer(1, 6))
        
        formulas = [
            "Mean: <i>x̄ = (sum of values) ÷ (number of values)</i>",
            "Percentile Rank: <i>PR = (b/n) × 100</i>",
            "  where b = number of scores below the given score",
            "  and n = total number of scores"
        ]
        
        for formula in formulas:
            elements.append(Paragraph(formula, self.styles['Normal']))
        
        return elements
    
    def _build_question(self, num: int, question: Question, show_answers: bool):
        """Build a single question"""
        elements = []
        
        # Question number and marks
        header = f"Question {num}. {question.get_marks_display()}"
        if show_answers and question.outcomes:
            header += f" [{question.get_outcomes_display()}]"
        
        elements.append(Paragraph(header, self.styles['QuestionNumber']))
        
        # Context
        if question.context:
            elements.append(Paragraph(
                f"<i>{question.context}</i>",
                self.styles['Context']
            ))
        
        # Question text (preserve formatting)
        question_lines = question.question_text.split('\n')
        for line in question_lines:
            if line.strip():
                elements.append(Paragraph(line, self.styles['QuestionText']))
            else:
                elements.append(Spacer(1, 6))
        
        # Answer key (teacher version only)
        if show_answers:
            elements.append(Spacer(1, 12))
            elements.append(Paragraph(
                "<b>ANSWER KEY:</b>",
                self.styles['Answer']
            ))
            
            # Multi-part answers
            if question.parts:
                for part in question.parts:
                    answer_text = f"<b>{part.letter})</b> {part.answer}"
                    elements.append(Paragraph(answer_text, self.styles['Answer']))
            else:
                # Single answer
                answer_text = f"<b>Answer:</b> {question.answer}"
                elements.append(Paragraph(answer_text, self.styles['Answer']))
            
            # Solution steps
            if question.solution_steps:
                elements.append(Spacer(1, 6))
                elements.append(Paragraph(
                    "<b>Solution:</b>",
                    self.styles['Answer']
                ))
                for step in question.solution_steps:
                    elements.append(Paragraph(
                        step,
                        self.styles['Solution']
                    ))
        
        return elements


# Test function
if __name__ == "__main__":
    print("PDF Builder loaded successfully")
    print("Use build_student_test() or build_teacher_test() with an Assessment object")
