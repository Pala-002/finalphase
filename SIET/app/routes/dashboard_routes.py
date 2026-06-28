"""
Dashboard routes for SIET.
Handles student and researcher dashboards with analytics visualization.
"""

from flask import Blueprint, render_template, jsonify, request, send_file
from flask_login import login_required, current_user
from app.models import db, User, REDTICScore, StroopResult, NBackResult, DigitSpanResult, TrailMakingResult, CRTResult, Session, AnalyticsLog
from app.analytics.engine import AnalyticalEngine
import io
import csv
from datetime import datetime

try:
    import openpyxl
    from openpyxl import Workbook
    EXCEL_SUPPORT = True
except ImportError:
    EXCEL_SUPPORT = False

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/student')
@login_required
def student_dashboard():
    """Student dashboard showing personal results."""
    # Get latest RED-TIC score
    redtic_score = REDTICScore.query.filter_by(user_id=current_user.id)\
        .order_by(REDTICScore.created_at.desc()).first()
    
    # Get cognitive test results
    stroop = StroopResult.query.filter_by(user_id=current_user.id)\
        .order_by(StroopResult.created_at.desc()).first()
    nback = NBackResult.query.filter_by(user_id=current_user.id)\
        .order_by(NBackResult.created_at.desc()).first()
    digitspan_forward = DigitSpanResult.query.filter_by(
        user_id=current_user.id, test_type='forward'
    ).order_by(DigitSpanResult.created_at.desc()).first()
    digitspan_backward = DigitSpanResult.query.filter_by(
        user_id=current_user.id, test_type='backward'
    ).order_by(DigitSpanResult.created_at.desc()).first()
    trailmaking_a = TrailMakingResult.query.filter_by(
        user_id=current_user.id, version='A'
    ).order_by(TrailMakingResult.created_at.desc()).first()
    crt = CRTResult.query.filter_by(user_id=current_user.id).all()
    
    # Calculate CRT summary
    crt_correct = sum(1 for r in crt if r.is_correct) if crt else 0
    crt_total = len(crt) if crt else 0
    
    # Generate recommendations
    engine = AnalyticalEngine()
    recommendations = []
    if redtic_score:
        scores_dict = {
            'fatiga_tecnologica': redtic_score.fatiga_tecnologica,
            'ansiedad_tecnologica': redtic_score.ansiedad_tecnologica,
            'escepticismo': redtic_score.escepticismo,
            'ineficacia': redtic_score.ineficacia,
            'total_score': redtic_score.total_score,
            'stress_level': redtic_score.stress_level
        }
        recommendations = engine.generate_recommendations(scores_dict)
    
    return render_template('dashboard/student.html',
                         title='Mi Dashboard',
                         redtic_score=redtic_score,
                         stroop=stroop,
                         nback=nback,
                         digitspan_forward=digitspan_forward,
                         digitspan_backward=digitspan_backward,
                         trailmaking_a=trailmaking_a,
                         crt_correct=crt_correct,
                         crt_total=crt_total,
                         recommendations=recommendations)


@dashboard_bp.route('/researcher')
@login_required
def researcher_dashboard():
    """Researcher dashboard with aggregated analytics."""
    # Check if user is researcher or admin
    if current_user.role.name not in ['investigador', 'administrador']:
        return render_template('errors/403.html', title='Acceso Denegado'), 403
    
    # Get aggregated statistics
    total_users = User.query.filter_by(is_active=True).count()
    total_sessions = Session.query.count()
    
    # RED-TIC statistics
    all_scores = REDTICScore.query.all()
    avg_stress = sum(s.total_score for s in all_scores) / len(all_scores) if all_scores else 0
    
    # Stress level distribution
    stress_distribution = {
        'bajo': REDTICScore.query.filter_by(stress_level='bajo').count(),
        'moderado': REDTICScore.query.filter_by(stress_level='moderado').count(),
        'alto': REDTICScore.query.filter_by(stress_level='alto').count()
    }
    
    # Cognitive test averages
    avg_stroop_accuracy = None
    avg_nback_accuracy = None
    
    stroop_results = StroopResult.query.all()
    if stroop_results:
        avg_stroop_accuracy = sum(r.completion_rate for r in stroop_results) / len(stroop_results)
    
    nback_results = NBackResult.query.all()
    if nback_results:
        avg_nback_accuracy = sum(r.accuracy for r in nback_results) / len(nback_results)
    
    return render_template('dashboard/researcher.html',
                         title='Dashboard Investigador',
                         total_users=total_users,
                         total_sessions=total_sessions,
                         avg_stress=round(avg_stress, 2),
                         stress_distribution=stress_distribution,
                         avg_stroop_accuracy=round(avg_stroop_accuracy, 2) if avg_stroop_accuracy else 0,
                         avg_nback_accuracy=round(avg_nback_accuracy, 2) if avg_nback_accuracy else 0)


@dashboard_bp.route('/api/student-data')
@login_required
def api_student_data():
    """API endpoint for student dashboard data."""
    redtic_score = REDTICScore.query.filter_by(user_id=current_user.id)\
        .order_by(REDTICScore.created_at.desc()).first()
    
    if not redtic_score:
        return jsonify({'error': 'No data available'}), 404
    
    data = {
        'redtic': {
            'fatiga_tecnologica': redtic_score.fatiga_tecnologica,
            'ansiedad_tecnologica': redtic_score.ansiedad_tecnologica,
            'escepticismo': redtic_score.escepticismo,
            'ineficacia': redtic_score.ineficacia,
            'total_score': redtic_score.total_score,
            'stress_level': redtic_score.stress_level
        }
    }
    
    return jsonify(data)


@dashboard_bp.route('/api/researcher-data')
@login_required
def api_researcher_data():
    """API endpoint for researcher dashboard data."""
    if current_user.role.name not in ['investigador', 'administrador']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get all scores for charts
    scores = REDTICScore.query.all()
    
    labels = [f'Usuario {s.user_id}' for s in scores[:20]]  # Limit to 20 for performance
    total_scores = [s.total_score for s in scores[:20]]
    
    data = {
        'labels': labels,
        'total_scores': total_scores,
        'stress_levels': {
            'bajo': REDTICScore.query.filter_by(stress_level='bajo').count(),
            'moderado': REDTICScore.query.filter_by(stress_level='moderado').count(),
            'alto': REDTICScore.query.filter_by(stress_level='alto').count()
        }
    }
    
    return jsonify(data)


@dashboard_bp.route('/export/csv')
@login_required
def export_csv():
    """Export data as CSV."""
    if current_user.role.name not in ['investigador', 'administrador']:
        return render_template('errors/403.html', title='Acceso Denegado'), 403
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        'Usuario', 'Email', 'Fatiga', 'Ansiedad', 'Escepticismo', 
        'Ineficacia', 'Total', 'Nivel Estrés', 'Fecha'
    ])
    
    # Data
    scores = REDTICScore.query.join(User).all()
    for score in scores:
        user = User.query.get(score.user_id)
        writer.writerow([
            user.username if user else 'N/A',
            user.email if user else 'N/A',
            round(score.fatiga_tecnologica, 2),
            round(score.ansiedad_tecnologica, 2),
            round(score.escepticismo, 2),
            round(score.ineficacia, 2),
            round(score.total_score, 2),
            score.stress_level,
            score.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'siet_export_{datetime.now().strftime("%Y%m%d")}.csv'
    )


@dashboard_bp.route('/export/excel')
@login_required
def export_excel():
    """Export data as Excel."""
    if not EXCEL_SUPPORT:
        return jsonify({'error': 'Excel support not available'}), 500
    
    if current_user.role.name not in ['investigador', 'administrador']:
        return render_template('errors/403.html', title='Acceso Denegado'), 403
    
    # Create Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = 'RED-TIC Scores'
    
    # Header
    headers = [
        'Usuario', 'Email', 'Fatiga', 'Ansiedad', 'Escepticismo',
        'Ineficacia', 'Total', 'Nivel Estrés', 'Fecha'
    ]
    ws.append(headers)
    
    # Data
    scores = REDTICScore.query.join(User).all()
    for score in scores:
        user = User.query.get(score.user_id)
        ws.append([
            user.username if user else 'N/A',
            user.email if user else 'N/A',
            round(score.fatiga_tecnologica, 2),
            round(score.ansiedad_tecnologica, 2),
            round(score.escepticismo, 2),
            round(score.ineficacia, 2),
            round(score.total_score, 2),
            score.stress_level,
            score.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    
    # Save to bytes
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=f'siet_export_{datetime.now().strftime("%Y%m%d")}.xlsx'
    )
