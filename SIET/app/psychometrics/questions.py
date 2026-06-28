"""
Psychometrics module for SIET.
Contains RED-TIC questionnaire data and scoring utilities.
Based on scientific literature for technostress assessment.
"""

from typing import List, Dict


class REDTICQuestions:
    """
    RED-TIC questionnaire questions based on scientific literature.
    Measures four dimensions of technostress.
    """
    
    @staticmethod
    def get_questions() -> List[Dict]:
        """
        Get all RED-TIC questionnaire questions.
        
        Returns:
            List of question dictionaries with id, text, dimension, reverse_scored, order
        """
        return [
            # Fatiga Tecnológica (Technological Fatigue)
            {
                'id': 1,
                'question_text': 'Me siento cansado/a después de usar tecnología digital.',
                'dimension': 'fatiga_tecnologica',
                'reverse_scored': False,
                'order': 1
            },
            {
                'id': 2,
                'question_text': 'El uso prolongado de dispositivos me produce agotamiento mental.',
                'dimension': 'fatiga_tecnologica',
                'reverse_scored': False,
                'order': 2
            },
            {
                'id': 3,
                'question_text': 'Necesito descansos frecuentes cuando uso tecnología.',
                'dimension': 'fatiga_tecnologica',
                'reverse_scored': False,
                'order': 3
            },
            {
                'id': 4,
                'question_text': 'Me siento energizado/a al usar nuevas tecnologías.',
                'dimension': 'fatiga_tecnologica',
                'reverse_scored': True,
                'order': 4
            },
            {
                'id': 5,
                'question_text': 'El tiempo frente a la pantalla me deja sin energía.',
                'dimension': 'fatiga_tecnologica',
                'reverse_scored': False,
                'order': 5
            },
            
            # Ansiedad Tecnológica (Technological Anxiety)
            {
                'id': 6,
                'question_text': 'Me siento nervioso/a cuando la tecnología no funciona correctamente.',
                'dimension': 'ansiedad_tecnologica',
                'reverse_scored': False,
                'order': 6
            },
            {
                'id': 7,
                'question_text': 'Me preocupa no poder aprender a usar nuevas tecnologías.',
                'dimension': 'ansiedad_tecnologica',
                'reverse_scored': False,
                'order': 7
            },
            {
                'id': 8,
                'question_text': 'Siento ansiedad cuando tengo que usar tecnología unfamiliar.',
                'dimension': 'ansiedad_tecnologica',
                'reverse_scored': False,
                'order': 8
            },
            {
                'id': 9,
                'question_text': 'Me siento tranquilo/a al explorar nuevas aplicaciones.',
                'dimension': 'ansiedad_tecnologica',
                'reverse_scored': True,
                'order': 9
            },
            {
                'id': 10,
                'question_text': 'Evito usar tecnología por miedo a cometer errores.',
                'dimension': 'ansiedad_tecnologica',
                'reverse_scored': False,
                'order': 10
            },
            
            # Escepticismo Tecnológico (Technological Skepticism)
            {
                'id': 11,
                'question_text': 'Dudo de los beneficios reales de las nuevas tecnologías.',
                'dimension': 'escepticismo',
                'reverse_scored': False,
                'order': 11
            },
            {
                'id': 12,
                'question_text': 'Creo que la tecnología complica más que simplifica.',
                'dimension': 'escepticismo',
                'reverse_scored': False,
                'order': 12
            },
            {
                'id': 13,
                'question_text': 'Pienso que las herramientas digitales son sobrevaloradas.',
                'dimension': 'escepticismo',
                'reverse_scored': False,
                'order': 13
            },
            {
                'id': 14,
                'question_text': 'Confío en que la tecnología mejora mi productividad.',
                'dimension': 'escepticismo',
                'reverse_scored': True,
                'order': 14
            },
            {
                'id': 15,
                'question_text': 'Cuestiono la necesidad de tantas aplicaciones y dispositivos.',
                'dimension': 'escepticismo',
                'reverse_scored': False,
                'order': 15
            },
            
            # Ineficacia Tecnológica (Technological Inefficacy)
            {
                'id': 16,
                'question_text': 'Me siento incompetente al usar tecnología avanzada.',
                'dimension': 'ineficacia',
                'reverse_scored': False,
                'order': 16
            },
            {
                'id': 17,
                'question_text': 'Tardo más que otras personas en aprender a usar nuevos programas.',
                'dimension': 'ineficacia',
                'reverse_scored': False,
                'order': 17
            },
            {
                'id': 18,
                'question_text': 'Necesito ayuda frecuentemente para resolver problemas tecnológicos.',
                'dimension': 'ineficacia',
                'reverse_scored': False,
                'order': 18
            },
            {
                'id': 19,
                'question_text': 'Me siento capaz de dominar cualquier herramienta digital.',
                'dimension': 'ineficacia',
                'reverse_scored': True,
                'order': 19
            },
            {
                'id': 20,
                'question_text': 'Evito tareas que requieren habilidades tecnológicas complejas.',
                'dimension': 'ineficacia',
                'reverse_scored': False,
                'order': 20
            }
        ]
    
    @staticmethod
    def get_questions_by_dimension(dimension: str) -> List[Dict]:
        """
        Get questions filtered by dimension.
        
        Args:
            dimension: Dimension name (fatiga_tecnologica, ansiedad_tecnologica, escepticismo, ineficacia)
            
        Returns:
            List of question dictionaries for the specified dimension
        """
        questions = REDTICQuestions.get_questions()
        return [q for q in questions if q['dimension'] == dimension]
    
    @staticmethod
    def get_dimensions() -> List[str]:
        """
        Get list of all RED-TIC dimensions.
        
        Returns:
            List of dimension names
        """
        return ['fatiga_tecnologica', 'ansiedad_tecnologica', 'escepticismo', 'ineficacia']


class CRTQuestions:
    """
    Cognitive Reflection Test questions.
    Based on Frederick (2005) - measures ability to override intuitive responses.
    """
    
    @staticmethod
    def get_questions() -> List[Dict]:
        """
        Get CRT questions with correct answers.
        
        Returns:
            List of question dictionaries with question, options, correct_answer
        """
        return [
            {
                'id': 1,
                'question': 'Un bate y una pelota cuestan $1.10 en total. El bate cuesta $1.00 más que la pelota. ¿Cuánto cuesta la pelota?',
                'options': ['$0.10', '$0.05', '$0.15'],
                'correct_answer': '$0.05',
                'intuitive_answer': '$0.10'
            },
            {
                'id': 2,
                'question': 'Si 5 máquinas tardan 5 minutos en hacer 5 artículos, ¿cuánto tiempo tardarían 100 máquinas en hacer 100 artículos?',
                'options': ['100 minutos', '5 minutos', '50 minutos'],
                'correct_answer': '5 minutos',
                'intuitive_answer': '100 minutos'
            },
            {
                'id': 3,
                'question': 'En un lago hay un parche de nenúfares. Cada día, el parche duplica su tamaño. Si tarda 48 días en cubrir todo el lago, ¿cuánto tarda en cubrir la mitad del lago?',
                'options': ['24 días', '47 días', '46 días'],
                'correct_answer': '47 días',
                'intuitive_answer': '24 días'
            }
        ]
