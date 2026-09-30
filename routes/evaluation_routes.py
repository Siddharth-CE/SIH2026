from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Evaluation, Application, EvaluationScore
from services.audit_service import log_audit_event
from datetime import datetime

evaluation_bp = Blueprint('evaluation', __name__)

@evaluation_bp.route('/evaluations')
@login_required
def index():
    if current_user.is_evaluator:
        evaluations = Evaluation.query.filter_by(evaluator_id=current_user.id).all()
        # Find applications ready for evaluation
        assigned_applications = Application.query.filter_by(status='in_evaluation').all()
    else:
        evaluations = Evaluation.query.all()
        assigned_applications = Application.query.filter(Application.status.in_(['in_evaluation', 'shortlisted', 'pilot_selected'])).all()

    return render_template('evaluations/index.html', evaluations=evaluations, assigned_applications=assigned_applications)


@evaluation_bp.route('/applications/<int:app_id>/evaluate', methods=['GET', 'POST'])
@login_required
def evaluate(app_id):
    application = Application.query.get_or_404(app_id)
    
    # Look for existing evaluation by this user
    evaluation = Evaluation.query.filter_by(application_id=application.id, evaluator_id=current_user.id).first()
    if not evaluation:
        evaluation = Evaluation(
            application_id=application.id,
            evaluator_id=current_user.id,
            status='draft'
        )
        db.session.add(evaluation)
        db.session.commit()

    if request.method == 'POST':
        coi = bool(request.form.get('conflict_of_interest'))
        if not coi:
            flash("You must confirm the Conflict of Interest declaration before submitting.", "danger")
            return redirect(url_for('evaluation.evaluate', app_id=app_id))

        evaluation.conflict_of_interest_cleared = coi
        evaluation.technical_feasibility_score = float(request.form.get('technical_feasibility_score', 0))
        evaluation.technical_feasibility_comment = request.form.get('technical_feasibility_comment', '')

        evaluation.expected_outcome_score = float(request.form.get('expected_outcome_score', 0))
        evaluation.expected_outcome_comment = request.form.get('expected_outcome_comment', '')

        evaluation.scalability_score = float(request.form.get('scalability_score', 0))
        evaluation.scalability_comment = request.form.get('scalability_comment', '')

        evaluation.security_risk_score = float(request.form.get('security_risk_score', 0))
        evaluation.security_risk_comment = request.form.get('security_risk_comment', '')

        evaluation.implementation_readiness_score = float(request.form.get('implementation_readiness_score', 0))
        evaluation.implementation_readiness_comment = request.form.get('implementation_readiness_comment', '')

        evaluation.cost_value_score = float(request.form.get('cost_value_score', 0))
        evaluation.cost_value_comment = request.form.get('cost_value_comment', '')

        evaluation.overall_recommendation = request.form.get('overall_recommendation', 'Recommend with Standard Oversight')
        evaluation.general_remarks = request.form.get('general_remarks', '')

        score = evaluation.calculate_weighted_score()
        evaluation.status = 'submitted'
        evaluation.submitted_at = datetime.utcnow()

        # Update application average score
        application.average_score = score
        db.session.commit()

        log_audit_event(
            f"Submitted Expert Evaluation for {application.code}",
            "Evaluation",
            str(evaluation.id),
            f"Weighted Score: {score}/100. Recommendation: {evaluation.overall_recommendation}",
            current_user
        )
        flash(f"Evaluation submitted successfully with weighted score of {score}/100!", "success")
        return redirect(url_for('evaluation.index'))

    return render_template('evaluations/evaluate.html', application=application, evaluation=evaluation)
