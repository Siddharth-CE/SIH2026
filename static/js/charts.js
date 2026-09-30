// GovPilot Canvas Chart Engine
// Clean vanilla implementation with zero external framework dependencies

class GovChart {
  static drawLineTrend(canvasId, labels, dataPoints, targetValue, unit = '', color = '#1e3a8a') {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width = canvas.parentElement.clientWidth || 500;
    const height = canvas.height = 220;

    ctx.clearRect(0, 0, width, height);

    const padding = { top: 20, right: 30, bottom: 40, left: 50 };
    const chartW = width - padding.left - padding.right;
    const chartH = height - padding.top - padding.bottom;

    if (!dataPoints || dataPoints.length === 0) {
      ctx.fillStyle = '#64748b';
      ctx.font = '12px sans-serif';
      ctx.fillText('No historical observations recorded yet.', width / 2 - 100, height / 2);
      return;
    }

    const minVal = Math.min(...dataPoints, targetValue || 0) * 0.9;
    const maxVal = Math.max(...dataPoints, targetValue || 0) * 1.1;
    const range = maxVal - minVal || 1;

    // Draw Gridlines & Y-Axis
    ctx.strokeStyle = '#e2e8f0';
    ctx.lineWidth = 1;
    ctx.fillStyle = '#64748b';
    ctx.font = '10px sans-serif';

    for (let i = 0; i <= 4; i++) {
      const yVal = minVal + (range * (i / 4));
      const y = padding.top + chartH - ((yVal - minVal) / range * chartH);
      ctx.beginPath();
      ctx.moveTo(padding.left, y);
      ctx.lineTo(width - padding.right, y);
      ctx.stroke();
      ctx.fillText(yVal.toFixed(1), 10, y + 3);
    }

    // Draw Target Line if provided
    if (targetValue !== undefined) {
      const targetY = padding.top + chartH - ((targetValue - minVal) / range * chartH);
      ctx.strokeStyle = '#d97706';
      ctx.lineWidth = 1.5;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(padding.left, targetY);
      ctx.lineTo(width - padding.right, targetY);
      ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = '#d97706';
      ctx.fillText(`Target (${targetValue} ${unit})`, width - padding.right - 90, targetY - 4);
    }

    // Draw Data Line
    const xStep = chartW / (dataPoints.length - 1 || 1);
    ctx.strokeStyle = color;
    ctx.lineWidth = 2.5;
    ctx.beginPath();

    dataPoints.forEach((val, idx) => {
      const x = padding.left + (idx * xStep);
      const y = padding.top + chartH - ((val - minVal) / range * chartH);
      if (idx === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();

    // Draw Data Points & Labels
    dataPoints.forEach((val, idx) => {
      const x = padding.left + (idx * xStep);
      const y = padding.top + chartH - ((val - minVal) / range * chartH);

      // Circle Point
      ctx.fillStyle = '#ffffff';
      ctx.strokeStyle = color;
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(x, y, 4, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();

      // X Label
      if (labels && labels[idx] && (idx % Math.ceil(labels.length / 6) === 0 || idx === labels.length - 1)) {
        ctx.fillStyle = '#64748b';
        ctx.font = '10px sans-serif';
        ctx.fillText(labels[idx], x - 15, height - 12);
      }
    });
  }

  static drawBarComparison(canvasId, items) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const width = canvas.width = canvas.parentElement.clientWidth || 500;
    const height = canvas.height = items.length * 45 + 40;

    ctx.clearRect(0, 0, width, height);

    items.forEach((item, idx) => {
      const y = 20 + (idx * 45);
      
      // Label
      ctx.fillStyle = '#1e293b';
      ctx.font = 'bold 12px sans-serif';
      ctx.fillText(item.name, 20, y);

      // Baseline bar
      const maxW = width - 240;
      const bRatio = Math.min(1, item.baseline / (Math.max(item.baseline, item.target, item.actual) * 1.15));
      const tRatio = Math.min(1, item.target / (Math.max(item.baseline, item.target, item.actual) * 1.15));
      const aRatio = Math.min(1, item.actual / (Math.max(item.baseline, item.target, item.actual) * 1.15));

      // Bar track
      const barY = y + 8;
      const barH = 16;
      const startX = 20;

      // Draw Baseline (Gray)
      ctx.fillStyle = '#cbd5e1';
      ctx.fillRect(startX, barY, maxW * bRatio, barH);
      ctx.fillStyle = '#475569';
      ctx.font = '10px sans-serif';
      ctx.fillText(`Base: ${item.baseline}${item.unit}`, startX + maxW * bRatio + 8, barY + 12);

      // Target indicator
      const targetX = startX + (maxW * tRatio);
      ctx.fillStyle = '#d97706';
      ctx.fillRect(targetX, barY - 4, 3, barH + 8);

      // Actual (Green/Blue)
      ctx.fillStyle = item.actualAchieved ? '#15803d' : '#2563eb';
      ctx.fillRect(startX, barY + 3, maxW * aRatio, barH - 6);
      ctx.fillStyle = item.actualAchieved ? '#15803d' : '#2563eb';
      ctx.font = 'bold 11px sans-serif';
      ctx.fillText(`Actual: ${item.actual}${item.unit}`, startX + maxW * aRatio + 70, barY + 12);
    });
  }
}
window.GovChart = GovChart;
