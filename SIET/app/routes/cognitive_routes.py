"""
Cognitive tests routes for SIET.
Handles all cognitive test interfaces and result submission.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_required, current_user
from datetime import datetime
from app.models import db, Session, StroopResult, NBackResult, DigitSpanResult, TrailMakingResult, CRTResult
from app.analytics.engine import AnalyticalEngine

cognitive_bp = Blueprint('cognitive', __name__, url_prefix='/cognitive')


@cognitive_bp.route('/')
@login_required
def test_selection():
    """Cognitive tests selection page."""
    return render_template('cognitive/selection.html', title='Pruebas Cognitivas')


@cognitive_bp.route('/stroop')
@login_required
def stroop_test():
    """Stroop test interface."""
    return render_template('cognitive/stroop.html', title='Test Stroop')


@cognitive_bp.route('/stroop/submit', methods=['POST'])
@login_required
def submit_stroop():
    """Submit Stroop test results."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos inválidos'}), 400
    
    session_id = session.get('evaluation_session_id')
    
    # Calculate metrics using analytical engine
    engine = AnalyticalEngine()
    metrics = engine.calculate_stroop_metrics(data.get('trials', []))
    
    # Save results
    result = StroopResult(
        user_id=current_user.id,
        session_id=session_id,
        total_trials=metrics.get('total_trials', 0),
        correct_answers=metrics.get('correct_answers', 0),
        errors=metrics.get('errors', 0),
        avg_reaction_time_ms=metrics.get('avg_reaction_time_ms', 0),
        interference_score=metrics.get('interference_score', 0),
        completion_rate=metrics.get('completion_rate', 0)
    )
    db.session.add(result)
    db.session.commit()
    
    return jsonify({'success': True, 'metrics': metrics})


@cognitive_bp.route('/nback')
@login_required
def nback_test():
    """N-Back test interface."""
    return render_template('cognitive/nback.html', title='Test N-Back')


@cognitive_bp.route('/nback/submit', methods=['POST'])
@login_required
def submit_nback():
    """Submit N-Back test results."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos inválidos'}), 400
    
    session_id = session.get('evaluation_session_id')
    
    # Calculate metrics
    engine = AnalyticalEngine()
    metrics = engine.calculate_nback_metrics(data.get('trials', []))
    
    # Save results
    result = NBackResult(
        user_id=current_user.id,
        session_id=session_id,
        n_value=2,
        total_trials=metrics.get('total_trials', 0),
        hits=metrics.get('hits', 0),
        misses=metrics.get('misses', 0),
        false_alarms=metrics.get('false_alarms', 0),
        correct_rejections=metrics.get('correct_rejections', 0),
        accuracy=metrics.get('accuracy', 0),
        avg_reaction_time_ms=metrics.get('avg_reaction_time_ms', 0),
        d_prime=metrics.get('d_prime', 0)
    )
    db.session.add(result)
    db.session.commit()
    
    return jsonify({'success': True, 'metrics': metrics})


@cognitive_bp.route('/digitspan')
@login_required
def digitspan_test():
    """Digit Span test interface."""
    return render_template('cognitive/digitspan.html', title='Test Digit Span')


@cognitive_bp.route('/digitspan/submit', methods=['POST'])
@login_required
def submit_digitspan():
    """Submit Digit Span test results."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos inválidos'}), 400
    
    session_id = session.get('evaluation_session_id')
    
    forward_data = data.get('forward', [])
    backward_data = data.get('backward', [])
    
    # Calculate metrics
    engine = AnalyticalEngine()
    metrics = engine.calculate_digitspan_metrics(forward_data, backward_data)
    
    # Save forward results
    if forward_data:
        forward_result = DigitSpanResult(
            user_id=current_user.id,
            session_id=session_id,
            test_type='forward',
            max_span=metrics['forward']['max_span'],
            total_errors=metrics['forward']['total_errors'],
            total_time_ms=metrics['forward']['total_time_ms'],
            trials_completed=metrics['forward']['trials_completed']
        )
        db.session.add(forward_result)
    
    # Save backward results
    if backward_data:
        backward_result = DigitSpanResult(
            user_id=current_user.id,
            session_id=session_id,
            test_type='backward',
            max_span=metrics['backward']['max_span'],
            total_errors=metrics['backward']['total_errors'],
            total_time_ms=metrics['backward']['total_time_ms'],
            trials_completed=metrics['backward']['trials_completed']
        )
        db.session.add(backward_result)
    
    db.session.commit()
    
    return jsonify({'success': True, 'metrics': metrics})


@cognitive_bp.route('/trailmaking')
@login_required
def trailmaking_test():
    """Trail Making Test interface."""
    return render_template('cognitive/trailmaking.html', title='Trail Making Test')


@cognitive_bp.route('/trailmaking/submit', methods=['POST'])
@login_required
def submit_trailmaking():
    """Submit Trail Making Test results."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos inválidos'}), 400
    
    session_id = session.get('evaluation_session_id')
    
    # Save version A results
    version_a = data.get('version_a', {})
    if version_a:
        result_a = TrailMakingResult(
            user_id=current_user.id,
            session_id=session_id,
            version='A',
            completion_time_ms=version_a.get('time_ms', 0),
            errors=version_a.get('errors', 0),
            completed=version_a.get('completed', False),
            path_efficiency=version_a.get('path_efficiency', 1.0)
        )
        db.session.add(result_a)
    
    # Save version B results
    version_b = data.get('version_b', {})
    if version_b:
        result_b = TrailMakingResult(
            user_id=current_user.id,
            session_id=session_id,
            version='B',
            completion_time_ms=version_b.get('time_ms', 0),
            errors=version_b.get('errors', 0),
            completed=version_b.get('completed', False),
            path_efficiency=version_b.get('path_efficiency', 1.0)
        )
        db.session.add(result_b)
    
    db.session.commit()
    
    return jsonify({'success': True})


@cognitive_bp.route('/crt')
@login_required
def crt_test():
    """Cognitive Reflection Test interface."""
    return render_template('cognitive/crt.html', title='Test de Reflexión Cognitiva')


@cognitive_bp.route('/crt/submit', methods=['POST'])
@login_required
def submit_crt():
    """Submit CRT results."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos inválidos'}), 400
    
    session_id = session.get('evaluation_session_id')
    answers = data.get('answers', [])
    
    # Correct answers
    correct_answers = ['$0.05', '5 minutos', '47 días']
    
    # Save each answer
    for i, answer in enumerate(answers):
        question_num = i + 1
        is_correct = answer.get('answer') == correct_answers[i]
        
        result = CRTResult(
            user_id=current_user.id,
            session_id=session_id,
            question_number=question_num,
            answer_given=answer.get('answer', ''),
            is_correct=is_correct,
            response_time_ms=answer.get('response_time_ms', 0)
        )
        db.session.add(result)
    
    db.session.commit()
    
    # Calculate summary
    total_correct = sum(1 for a in answers if a.get('answer') == correct_answers[answers.index(a)])
    
    return jsonify({
        'success': True,
        'score': total_correct,
        'total': len(answers)
    })


@cognitive_bp.route('/complete')
@login_required
def complete_evaluation():
    """Complete evaluation and update session."""
    session_id = session.get('evaluation_session_id')
    
    if session_id:
        eval_session = Session.query.get(session_id)
        if eval_session:
            eval_session.end_time = datetime.utcnow()
            eval_session.status = 'completed'
            duration = (eval_session.end_time - eval_session.start_time).total_seconds()
            eval_session.total_duration_seconds = int(duration)
            db.session.commit()
    
    flash('Evaluación completada exitosamente.', 'success')
    return redirect(url_for('dashboard.student_dashboard'))
