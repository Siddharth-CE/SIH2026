// GovPilot Outcome Wizard & AI Assistant Logic

class OutcomeWizard {
  constructor(wizardId) {
    this.container = document.getElementById(wizardId);
    if (!this.container) return;

    this.steps = this.container.querySelectorAll('.wizard-step-content');
    this.stepTabs = this.container.querySelectorAll('.wizard-step-item');
    this.currentStepIndex = 0;
    this.totalSteps = this.steps.length;

    this.initButtons();
    this.initAIAssistant();
  }

  initButtons() {
    const nextBtns = this.container.querySelectorAll('.btn-next-step');
    const prevBtns = this.container.querySelectorAll('.btn-prev-step');

    nextBtns.forEach(btn => {
      btn.addEventListener('click', () => this.goToStep(this.currentStepIndex + 1));
    });

    prevBtns.forEach(btn => {
      btn.addEventListener('click', () => this.goToStep(this.currentStepIndex - 1));
    });

    this.stepTabs.forEach((tab, index) => {
      tab.addEventListener('click', () => this.goToStep(index));
    });
  }

  goToStep(index) {
    if (index < 0 || index >= this.totalSteps) return;

    // Hide all
    this.steps.forEach(s => s.style.display = 'none');
    this.stepTabs.forEach(t => t.classList.remove('active'));

    // Show target
    this.steps[index].style.display = 'block';
    this.stepTabs[index].classList.add('active');

    // Mark previous as completed
    for (let i = 0; i < index; i++) {
      this.stepTabs[i].classList.add('completed');
    }

    this.currentStepIndex = index;

    // Update Step 8 Review Preview if active
    if (index === this.totalSteps - 1) {
      this.updateReviewSummary();
    }

    window.scrollTo({ top: this.container.offsetTop - 80, behavior: 'smooth' });
  }

  initAIAssistant() {
    const aiBtn = document.getElementById('btn-ai-generate');
    const promptInput = document.getElementById('ai-prompt-input');
    const statusMsg = document.getElementById('ai-status-msg');

    if (!aiBtn || !promptInput) return;

    aiBtn.addEventListener('click', async () => {
      const prompt = promptInput.value.trim();
      if (!prompt) {
        alert('Please enter an operational problem description for the AI Assistant.');
        return;
      }

      aiBtn.disabled = true;
      aiBtn.innerHTML = '<span>⚡ Synthesizing Outcome Blueprint...</span>';
      if (statusMsg) statusMsg.style.display = 'block';

      try {
        const response = await fetch('/challenges/ai-assist', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ prompt: prompt })
        });

        const data = await response.json();
        if (data.error) {
          alert(`Error: ${data.error}`);
          return;
        }

        // Auto-populate form fields across all steps
        this.populateFields(data);

        if (statusMsg) {
          statusMsg.innerHTML = '✓ Outcome-based challenge blueprint generated! Review steps below.';
          statusMsg.className = 'alert alert-success';
        }

        // Move to step 1 to inspect
        this.goToStep(0);
      } catch (err) {
        console.error(err);
        alert('Could not contact AI generator. Using heuristic fallback.');
      } finally {
        aiBtn.disabled = false;
        aiBtn.innerHTML = '<span>✨ Generate Challenge with AI</span>';
      }
    });
  }

  populateFields(d) {
    const setVal = (id, val) => {
      const el = document.getElementById(id);
      if (el && val !== undefined) el.value = val;
    };

    setVal('field-title', d.title);
    setVal('field-sector', d.sector);
    setVal('field-urgency', d.urgency);
    setVal('field-problem-summary', d.problem_summary);
    setVal('field-problem-details', d.problem_details);
    setVal('field-baseline-summary', d.baseline_summary);
    setVal('field-current-process', d.current_process);
    setVal('field-pain-points', d.pain_points);
    setVal('field-affected-users', d.affected_users);
    setVal('field-expected-outcome', d.expected_outcome);
    setVal('field-target-improvement', d.target_improvement);
    setVal('field-target-kpis', d.target_kpis_summary);
    setVal('field-geography', d.geography);
    setVal('field-users-count', d.target_users_count);
    setVal('field-facilities', d.test_facilities);
    setVal('field-duration', d.duration_days);
    setVal('field-budget', d.budget_indicative);
    setVal('field-datasets', d.available_datasets);
    setVal('field-sensitivity', d.data_sensitivity);
    setVal('field-api-availability', d.api_availability);
    setVal('field-technical-constraints', d.technical_constraints);
    setVal('field-security-reqs', d.security_requirements);
    setVal('field-integration-reqs', d.integration_requirements);
    setVal('field-eval-criteria', d.evaluation_criteria_notes);
    setVal('field-success-thresholds', d.success_thresholds);
  }

  updateReviewSummary() {
    const getVal = id => {
      const el = document.getElementById(id);
      return el ? el.value : '—';
    };

    const preview = document.getElementById('review-summary-container');
    if (!preview) return;

    preview.innerHTML = `
      <div class="gp-card" style="margin-bottom: 0;">
        <div class="gp-card-header">
          <span class="gp-card-title">Outcome-Based Challenge Blueprint Preview</span>
          <span class="badge badge-published">${getVal('field-sector')}</span>
        </div>
        <div class="gp-card-body">
          <h3 style="color: var(--primary); margin-bottom: 8px;">${getVal('field-title')}</h3>
          <p style="color: var(--text-muted); margin-bottom: 16px;">${getVal('field-problem-summary')}</p>
          
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; background: #f8fafc; padding: 14px; border-radius: 8px;">
            <div><strong>Baseline State:</strong><br/>${getVal('field-baseline-summary')}</div>
            <div><strong>Target Outcome:</strong><br/>${getVal('field-expected-outcome')}</div>
            <div><strong>Pilot Scope & Duration:</strong><br/>${getVal('field-geography')} (${getVal('field-duration')} Days)</div>
            <div><strong>Indicative Budget:</strong><br/>${getVal('field-budget')}</div>
          </div>
          <div><strong>Evaluation Criteria & KPIs:</strong><br/>${getVal('field-target-kpis')}</div>
        </div>
      </div>
    `;
  }
}

document.addEventListener('DOMContentLoaded', () => {
  new OutcomeWizard('challenge-wizard');
  new OutcomeWizard('application-wizard');
});
