"""
Evaluation routes for SIET.
Handles RED-TIC questionnaire and consent process.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_required, current_user
from datetime import datetime
import json
from app.models import db, Consent, Session, REDTICQuestion, REDTICAnswer, REDTICScore
from app.forms.auth_forms import ConsentForm
from app.psychometrics.questions import REDTICQuestions
from app.analytics.engine import AnalyticalEngine

evaluation_bp = Blueprint('evaluation', __name__, url_prefix='/evaluation')


@evaluation_bp.route('/consent', methods=['GET', 'POST'])
@login_required
def consent():
    """Informed consent page."""
    # Check if user already gave consent
    existing_consent = Consent.query.filter_by(user_id=current_user.id, accepted=True).first()
    if existing_consent:
        flash('Ya has aceptado el consentimiento informado.', 'info')
        return redirect(url_for('evaluation.redtic_questionnaire'))
    
    form = ConsentForm()
    if form.validate_on_submit():
        consent_record = Consent(
            user_id=current_user.id,
            accepted=True,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')[:500]
        )
        db.session.add(consent_record)
        
        # Create new evaluation session
        eval_session = Session(user_id=current_user.id, start_time=datetime.utcnow())
        db.session.add(eval_session)
        db.session.commit()
        
        # Store session ID in Flask session
        session['evaluation_session_id'] = eval_session.id
        
        flash('Consentimiento registrado. Puedes comenzar la evaluación.', 'success')
        return redirect(url_for('evaluation.redtic_questionnaire'))
    
    return render_template('consent/consent.html', form=form, title='Consentimiento Informado')


@evaluation_bp.route('/redtic')
@login_required
def redtic_questionnaire():
    """RED-TIC questionnaire page."""
    # Check consent
    consent = Consent.query.filter_by(user_id=current_user.id, accepted=True).first()
    if not consent:
        flash('Debes aceptar el consentimiento informado primero.', 'warning')
        return redirect(url_for('evaluation.consent'))
    
    questions = REDTICQuestions.get_questions()
    likert_scale = [
        {'value': 1, 'label': 'Nunca'},
        {'value': 2, 'label': 'Rara vez'},
        {'value': 3, 'label': 'Algunas veces'},
        {'value': 4, 'label': 'Frecuentemente'},
        {'value': 5, 'label': 'Siempre'}
    ]
    
    return render_template('evaluation/redtic.html', 
                         title='Cuestionario RED-TIC',
                         questions=questions,
                         likert_scale=likert_scale)


@evaluation_bp.route('/redtic/submit', methods=['POST'])
@login_required
def submit_redtic():
    """Submit RED-TIC questionnaire answers."""
    # Check consent
    consent = Consent.query.filter_by(user_id=current_user.id, accepted=True).first()
    if not consent:
        return jsonify({'error': 'Consentimiento requerido'}), 400
    
    data = request.get_json()
    if not data or 'answers' not in data:
        return jsonify({'error': 'Datos inválidos'}), 400
    
    answers_data = data['answers']
    timing_data = data.get('timing', {})
    
    # Get questions from database or use static ones
    questions = REDTICQuestions.get_questions()
    questions_dict = {q['id']: q for q in questions}
    
    # Save answers to database
    session_id = session.get('evaluation_session_id')
    
    for question_id, answer_value in answers_data.items():
        question_id = int(question_id)
        answer = REDTICAnswer(
            user_id=current_user.id,
            question_id=question_id,
            session_id=session_id,
            answer_value=int(answer_value),
            response_time_ms=timing_data.get(str(question_id), 0),
            changed_answer=False  # Could track this in frontend
        )
        db.session.add(answer)
    
    db.session.commit()
    
    # Calculate scores
    engine = AnalyticalEngine()
    scores = engine.calculate_redtic_scores(answers_data, questions)
    
    # Save scores
    redtic_score = REDTICScore(
        user_id=current_user.id,
        session_id=session_id,
        fatiga_tecnologica=scores.get('fatiga_tecnologica', 0),
        ansiedad_tecnologica=scores.get('ansiedad_tecnologica', 0),
        escepticismo=scores.get('escepticismo', 0),
        ineficacia=scores.get('ineficacia', 0),
        total_score=scores.get('total_score', 0),
        stress_level=scores.get('stress_level', 'moderado')
    )
    db.session.add(redtic_score)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'scores': scores,
        'redirect_url': url_for('cognitive.test_selection')
    })


@evaluation_bp.route('/results')
@login_required
def view_results():
    """View evaluation results."""
    # Check if user has completed RED-TIC
    score = REDTICScore.query.filter_by(user_id=current_user.id)\
        .order_by(REDTICScore.created_at.desc()).first()
    
    if not score:
        flash('No has completado la evaluación aún.', 'warning')
        return redirect(url_for('evaluation.redtic_questionnaire'))
    
    return render_template('evaluation/results.html', 
                         title='Resultados',
                         score=score)
