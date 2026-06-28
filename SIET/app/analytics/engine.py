"""
Analytical engine for SIET.
Implements rule-based classification and scoring algorithms.
No trained ML models - uses predefined thresholds from config.
"""

from typing import Dict, List, Optional, Tuple
from app.models import REDTICScore, StroopResult, NBackResult, DigitSpanResult, TrailMakingResult, CRTResult
from config import Config


class AnalyticalEngine:
    """
    Core analytical engine for processing evaluation results.
    Uses rule-based classification without trained ML models.
    """
    
    def __init__(self):
        """Initialize the analytical engine with configuration thresholds."""
        self.stress_thresholds = Config.STRESS_LEVELS
        self.redtic_dimensions = Config.REDTIC_THRESHOLDS
    
    def classify_stress_level(self, total_score: float) -> str:
        """
        Classify stress level based on total score using predefined thresholds.
        
        Args:
            total_score: Total RED-TIC score (0-100)
            
        Returns:
            Stress level classification: 'bajo', 'moderado', or 'alto'
        """
        for level, thresholds in self.stress_thresholds.items():
            if thresholds['min'] <= total_score <= thresholds['max']:
                return level
        return 'moderado'  # Default fallback
    
    def calculate_redtic_scores(
        self, 
        answers: Dict[int, int], 
        questions: List[Dict]
    ) -> Dict[str, float]:
        """
        Calculate RED-TIC dimension scores from answers.
        
        Args:
            answers: Dictionary mapping question_id to answer_value (1-5)
            questions: List of question dictionaries with id, dimension, reverse_scored
            
        Returns:
            Dictionary with scores for each dimension (0-100 scale)
        """
        dimension_scores = {
            'fatiga_tecnologica': [],
            'ansiedad_tecnologica': [],
            'escepticismo': [],
            'ineficacia': []
        }
        
        # Group answers by dimension
        for question in questions:
            q_id = question['id']
            dimension = question['dimension']
            reverse_scored = question.get('reverse_scored', False)
            
            if q_id in answers:
                score = answers[q_id]
                
                # Reverse scoring if needed (6 - score for 1-5 scale)
                if reverse_scored:
                    score = 6 - score
                
                dimension_scores[dimension].append(score)
        
        # Calculate average scores and normalize to 0-100
        normalized_scores = {}
        for dimension, scores in dimension_scores.items():
            if scores:
                avg_score = sum(scores) / len(scores)
                # Convert from 1-5 scale to 0-100 scale
                normalized_scores[dimension] = ((avg_score - 1) / 4) * 100
            else:
                normalized_scores[dimension] = 0.0
        
        # Calculate total score (average of all dimensions)
        total_score = sum(normalized_scores.values()) / len(normalized_scores) if normalized_scores else 0.0
        
        normalized_scores['total_score'] = total_score
        normalized_scores['stress_level'] = self.classify_stress_level(total_score)
        
        return normalized_scores
    
    def calculate_stroop_metrics(
        self, 
        trials: List[Dict]
    ) -> Dict[str, float]:
        """
        Calculate Stroop test metrics from trial data.
        
        Args:
            trials: List of trial dictionaries with reaction_time, correct, congruent
            
        Returns:
            Dictionary with Stroop metrics
        """
        if not trials:
            return {}
        
        congruent_correct = []
        incongruent_correct = []
        total_correct = 0
        total_errors = 0
        total_rt = 0
        
        for trial in trials:
            rt = trial.get('reaction_time_ms', 0)
            correct = trial.get('correct', False)
            congruent = trial.get('congruent', True)
            
            if correct:
                total_correct += 1
                total_rt += rt
                if congruent:
                    congruent_correct.append(rt)
                else:
                    incongruent_correct.append(rt)
            else:
                total_errors += 1
        
        # Calculate interference score (difference between incongruent and congruent RT)
        avg_congruent = sum(congruent_correct) / len(congruent_correct) if congruent_correct else 0
        avg_incongruent = sum(incongruent_correct) / len(incongruent_correct) if incongruent_correct else 0
        interference_score = avg_incongruent - avg_congruent if avg_congruent > 0 else 0
        
        return {
            'total_trials': len(trials),
            'correct_answers': total_correct,
            'errors': total_errors,
            'avg_reaction_time_ms': total_rt / total_correct if total_correct > 0 else 0,
            'interference_score': interference_score,
            'completion_rate': (total_correct / len(trials)) * 100 if trials else 0
        }
    
    def calculate_nback_metrics(
        self, 
        trials: List[Dict]
    ) -> Dict[str, float]:
        """
        Calculate N-Back test metrics from trial data.
        
        Args:
            trials: List of trial dictionaries with is_target, responded, response_time_ms, correct
            
        Returns:
            Dictionary with N-Back metrics including d-prime
        """
        if not trials:
            return {}
        
        hits = 0
        misses = 0
        false_alarms = 0
        correct_rejections = 0
        total_rt = 0
        hit_count = 0
        
        for trial in trials:
            is_target = trial.get('is_target', False)
            responded = trial.get('responded', False)
            rt = trial.get('response_time_ms', 0)
            
            if is_target:
                if responded:
                    hits += 1
                    total_rt += rt
                    hit_count += 1
                else:
                    misses += 1
            else:
                if responded:
                    false_alarms += 1
                else:
                    correct_rejections += 1
        
        # Calculate hit rate and false alarm rate
        total_targets = sum(1 for t in trials if t.get('is_target', False))
        total_non_targets = len(trials) - total_targets
        
        hit_rate = hits / total_targets if total_targets > 0 else 0
        fa_rate = false_alarms / total_non_targets if total_non_targets > 0 else 0
        
        # Calculate d-prime (signal detection theory)
        # Avoid division by zero and log(0)
        hit_rate_adj = max(0.01, min(0.99, hit_rate))
        fa_rate_adj = max(0.01, min(0.99, fa_rate))
        
        from math import sqrt, log
        try:
            z_hit = -sqrt(2) * self._erfc_inv(2 * hit_rate_adj)
            z_fa = -sqrt(2) * self._erfc_inv(2 * fa_rate_adj)
            d_prime = z_hit - z_fa
        except:
            d_prime = 0.0
        
        accuracy = (hits + correct_rejections) / len(trials) if trials else 0
        
        return {
            'total_trials': len(trials),
            'hits': hits,
            'misses': misses,
            'false_alarms': false_alarms,
            'correct_rejections': correct_rejections,
            'accuracy': accuracy * 100,
            'avg_reaction_time_ms': total_rt / hit_count if hit_count > 0 else 0,
            'd_prime': d_prime
        }
    
    def _erfc_inv(self, x: float) -> float:
        """Approximate inverse complementary error function."""
        # Simple approximation for d-prime calculation
        if x <= 0:
            return 3.0
        if x >= 2:
            return -3.0
        if x == 1:
            return 0.0
        
        # Approximation using rational functions
        if x < 1:
            t = -log(x * (2 - x))
            return (0.147 * t ** 0.5 * log(t)) if t > 0 else 0
        else:
            t = -log((2 - x) * x)
            return -(0.147 * t ** 0.5 * log(t)) if t > 0 else 0
    
    def calculate_digitspan_metrics(
        self, 
        forward_results: List[Dict], 
        backward_results: List[Dict]
    ) -> Dict[str, Dict]:
        """
        Calculate Digit Span metrics.
        
        Args:
            forward_results: List of forward trial results
            backward_results: List of backward trial results
            
        Returns:
            Dictionary with metrics for both test types
        """
        def calculate_span(trials: List[Dict]) -> Dict:
            if not trials:
                return {'max_span': 0, 'total_errors': 0, 'total_time_ms': 0}
            
            max_span = max(t.get('sequence_length', 0) for t in trials if t.get('correct', False))
            total_errors = sum(1 for t in trials if not t.get('correct', False))
            total_time = sum(t.get('response_time_ms', 0) for t in trials)
            
            return {
                'max_span': max_span,
                'total_errors': total_errors,
                'total_time_ms': total_time,
                'trials_completed': len(trials)
            }
        
        return {
            'forward': calculate_span(forward_results),
            'backward': calculate_span(backward_results)
        }
    
    def generate_recommendations(self, scores: Dict) -> List[str]:
        """
        Generate general recommendations based on scores.
        Does NOT provide medical diagnosis.
        
        Args:
            scores: Dictionary containing dimension scores and stress level
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        stress_level = scores.get('stress_level', 'moderado')
        
        # General recommendations based on stress level
        if stress_level == 'alto':
            recommendations.append("Se recomienda tomar descansos regulares durante el uso de tecnología.")
            recommendations.append("Considere establecer límites de tiempo para el uso de dispositivos digitales.")
            recommendations.append("Practique técnicas de relajación antes y después de usar tecnología.")
        elif stress_level == 'moderado':
            recommendations.append("Mantenga un equilibrio entre el tiempo en línea y las actividades offline.")
            recommendations.append("Establezca pausas activas cada hora de uso tecnológico.")
        else:
            recommendations.append("Continúe manteniendo hábitos saludables en el uso de tecnología.")
        
        # Dimension-specific recommendations
        if scores.get('fatiga_tecnologica', 0) > 66:
            recommendations.append("Identifique fuentes de fatiga tecnológica y priorice tareas importantes.")
        
        if scores.get('ansiedad_tecnologica', 0) > 66:
            recommendations.append("Explore gradualmente nuevas tecnologías para reducir la ansiedad.")
        
        if scores.get('ineficacia', 0) > 66:
            recommendations.append("Considere capacitación adicional en herramientas tecnológicas específicas.")
        
        recommendations.append("Esta evaluación no constituye un diagnóstico médico. Consulte a un profesional si experimenta síntomas significativos.")
        
        return recommendations
    
    def generate_report_data(
        self, 
        user_id: int, 
        session_id: Optional[int] = None
    ) -> Dict:
        """
        Generate comprehensive report data for a user.
        
        Args:
            user_id: User ID
            session_id: Optional specific session ID
            
        Returns:
            Dictionary with all report data
        """
        report = {
            'user_id': user_id,
            'redtic_scores': None,
            'cognitive_results': {},
            'recommendations': []
        }
        
        # Get latest RED-TIC scores
        redtic_score = REDTICScore.query.filter_by(user_id=user_id)\
            .order_by(REDTICScore.created_at.desc()).first()
        
        if redtic_score:
            report['redtic_scores'] = {
                'fatiga_tecnologica': redtic_score.fatiga_tecnologica,
                'ansiedad_tecnologica': redtic_score.ansiedad_tecnologica,
                'escepticismo': redtic_score.escepticismo,
                'ineficacia': redtic_score.ineficacia,
                'total_score': redtic_score.total_score,
                'stress_level': redtic_score.stress_level
            }
            report['recommendations'] = self.generate_recommendations(report['redtic_scores'])
        
        # Get cognitive test results (latest for each type)
        for result_class, key in [
            (StroopResult, 'stroop'),
            (NBackResult, 'nback'),
            (DigitSpanResult, 'digitspan'),
            (TrailMakingResult, 'trailmaking'),
            (CRTResult, 'crt')
        ]:
            result = result_class.query.filter_by(user_id=user_id)\
                .order_by(result_class.created_at.desc()).first()
            
            if result:
                report['cognitive_results'][key] = self._result_to_dict(result)
        
        return report
    
    def _result_to_dict(self, result) -> Dict:
        """Convert SQLAlchemy result object to dictionary."""
        return {c.name: getattr(result, c.name) for c in result.__table__.columns}
