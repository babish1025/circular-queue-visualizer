/**
 * Circular Queue Visualizer — Frontend Application Logic
 * Mobile-First Interactive System (ES6+)
 * Authors: Babish P K, Bersha S K, Alisha, Jharna (2026)
 */

(function () {
  'use strict';

  // --- State Variables ---
  let currentState = null;
  let toastTimer = null;
  let wrapToastTimer = null;
  let demoSteps = [];
  let currentDemoStepIndex = 0;
  let isDemoPlaying = false;
  let demoTimer = null;
  let defaultInputValue = 10;

  // --- DOM Elements ---
  const el = {
    // Header & Status
    backendStatusPill: document.getElementById('backendStatusPill'),
    backendStatusText: document.getElementById('backendStatusText'),
    dbStatusPill: document.getElementById('dbStatusPill'),
    dbStatusText: document.getElementById('dbStatusText'),
    learnToggleBtn: document.getElementById('learnToggleBtn'),
    demoToggleBtn: document.getElementById('demoToggleBtn'),

    // Nav
    navTabs: document.querySelectorAll('.nav-tab'),
    tabPages: document.querySelectorAll('.tab-page'),

    // Toasts
    toastBanner: document.getElementById('toastBanner'),
    toastContent: document.getElementById('toastContent'),
    wrapToast: document.getElementById('wrapToast'),
    wrapToastTitle: document.getElementById('wrapToastTitle'),
    wrapToastBody: document.getElementById('wrapToastBody'),

    // Queue Viewport
    headerCapBadge: document.getElementById('headerCapBadge'),
    openCapModalBtn: document.getElementById('openCapModalBtn'),
    queueSlotsWrapper: document.getElementById('queueSlotsWrapper'),

    // Info Strip
    valFront: document.getElementById('valFront'),
    valRear: document.getElementById('valRear'),
    valSize: document.getElementById('valSize'),
    valCap: document.getElementById('valCap'),
    valStatus: document.getElementById('valStatus'),

    // Dual Representation
    physicalArrayBubbles: document.getElementById('physicalArrayBubbles'),
    logicalQueueBubbles: document.getElementById('logicalQueueBubbles'),

    // Controls
    enqueueForm: document.getElementById('enqueueForm'),
    enqueueValueInput: document.getElementById('enqueueValueInput'),
    quickValBtn: document.getElementById('quickValBtn'),
    btnEnqueue: document.getElementById('btnEnqueue'),
    btnDequeue: document.getElementById('btnDequeue'),
    btnPeek: document.getElementById('btnPeek'),
    btnDisplay: document.getElementById('btnDisplay'),
    btnClear: document.getElementById('btnClear'),
    btnReset: document.getElementById('btnReset'),
    btnChangeCap: document.getElementById('btnChangeCap'),

    // Bottom Quick Bar
    quickAddBtn: document.getElementById('quickAddBtn'),
    quickRemoveBtn: document.getElementById('quickRemoveBtn'),
    quickPeekBtn: document.getElementById('quickPeekBtn'),
    quickDisplayBtn: document.getElementById('quickDisplayBtn'),

    // Learning Sheet
    learningSheet: document.getElementById('learningSheet'),
    sheetHandle: document.getElementById('sheetHandle'),
    sheetCloseBtn: document.getElementById('sheetCloseBtn'),
    stepOpName: document.getElementById('stepOpName'),
    stepOpSummary: document.getElementById('stepOpSummary'),
    stepList: document.getElementById('stepList'),

    // Demo Controller
    demoControllerCard: document.getElementById('demoControllerCard'),
    demoStepBadge: document.getElementById('demoStepBadge'),
    demoCloseBtn: document.getElementById('demoCloseBtn'),
    demoStepText: document.getElementById('demoStepText'),
    demoPlayBtn: document.getElementById('demoPlayBtn'),
    demoPauseBtn: document.getElementById('demoPauseBtn'),
    demoStepBtn: document.getElementById('demoStepBtn'),
    demoResetBtn: document.getElementById('demoResetBtn'),
    demoSpeedSelect: document.getElementById('demoSpeedSelect'),

    // Modal
    capModal: document.getElementById('capModal'),
    closeCapModalBtn: document.getElementById('closeCapModalBtn'),
    capSelectBtns: document.querySelectorAll('.btn-cap-select'),

    // History Tab
    historyTableBody: document.getElementById('historyTableBody'),
    btnClearHistory: document.getElementById('btnClearHistory')
  };

  // ==========================================
  // INITIALIZATION
  // ==========================================
  document.addEventListener('DOMContentLoaded', () => {
    initServiceWorker();
    bindEvents();
    checkHealth();
    fetchState();
    loadDemoSteps();
  });

  // Register PWA Service Worker
  function initServiceWorker() {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker
        .register('/service-worker.js')
        .then((reg) => console.log('ServiceWorker registered:', reg.scope))
        .catch((err) => console.warn('ServiceWorker registration failed:', err));
    }
  }

  // Bind All Event Handlers
  function bindEvents() {
    // Navigation Tabs
    el.navTabs.forEach((tab) => {
      tab.addEventListener('click', () => switchTab(tab.dataset.tab));
    });

    // Learning Sheet Toggle
    el.learnToggleBtn.addEventListener('click', toggleLearningSheet);
    el.sheetCloseBtn.addEventListener('click', closeLearningSheet);
    el.sheetHandle.addEventListener('click', toggleLearningSheet);

    // Demo Toggle
    el.demoToggleBtn.addEventListener('click', toggleDemoMode);
    el.demoCloseBtn.addEventListener('click', closeDemoMode);
    el.demoPlayBtn.addEventListener('click', playDemo);
    el.demoPauseBtn.addEventListener('click', pauseDemo);
    el.demoStepBtn.addEventListener('click', stepDemo);
    el.demoResetBtn.addEventListener('click', resetDemo);

    // Form & Controls
    el.enqueueForm.addEventListener('submit', (e) => {
      e.preventDefault();
      handleEnqueue();
    });
    el.btnEnqueue.addEventListener('click', handleEnqueue);
    el.btnDequeue.addEventListener('click', handleDequeue);
    el.btnPeek.addEventListener('click', handlePeek);
    el.btnDisplay.addEventListener('click', handleDisplay);
    el.btnClear.addEventListener('click', handleClear);
    el.btnReset.addEventListener('click', handleReset);
    el.quickValBtn.addEventListener('click', generateRandomValue);

    // Capacity Modal
    el.openCapModalBtn.addEventListener('click', () => openModal(true));
    el.btnChangeCap.addEventListener('click', () => openModal(true));
    el.closeCapModalBtn.addEventListener('click', () => openModal(false));
    el.capSelectBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        const newCap = parseInt(btn.dataset.cap, 10);
        handleSetCapacity(newCap);
        openModal(false);
      });
    });

    // Quick Bottom Action Bar
    el.quickAddBtn.addEventListener('click', () => {
      if (!el.enqueueValueInput.value.trim()) {
        generateRandomValue();
      }
      handleEnqueue();
    });
    el.quickRemoveBtn.addEventListener('click', handleDequeue);
    el.quickPeekBtn.addEventListener('click', handlePeek);
    el.quickDisplayBtn.addEventListener('click', handleDisplay);

    // History Actions
    if (el.btnClearHistory) {
      el.btnClearHistory.addEventListener('click', handleClearHistory);
    }
  }

  // ==========================================
  // NAVIGATION & UI TOGGLES
  // ==========================================
  function switchTab(tabId) {
    el.navTabs.forEach((t) => t.classList.toggle('active', t.dataset.tab === tabId));
    el.tabPages.forEach((page) => {
      const isTarget = page.id === `page${tabId.charAt(0).toUpperCase() + tabId.slice(1)}`;
      page.classList.toggle('active-tab', isTarget);
    });

    if (tabId === 'history') {
      fetchHistory();
    }
  }

  function toggleLearningSheet() {
    el.learningSheet.classList.toggle('open');
  }

  function closeLearningSheet() {
    el.learningSheet.classList.remove('open');
  }

  function openModal(show) {
    el.capModal.style.display = show ? 'flex' : 'none';
  }

  // ==========================================
  // TOAST & NOTIFICATION SYSTEM
  // ==========================================
  function showToast(message, type = 'info', duration = 3000) {
    clearTimeout(toastTimer);
    el.toastBanner.className = `toast-banner ${type}`;
    el.toastContent.innerHTML = message;

    toastTimer = setTimeout(() => {
      el.toastBanner.className = 'toast-banner';
    }, duration);
  }

  function showWrapNotification(wrapInfo) {
    clearTimeout(wrapToastTimer);
    el.wrapToastTitle.textContent = wrapInfo.message || 'CIRCULAR WRAP-AROUND';
    el.wrapToastBody.textContent = `Path: ${wrapInfo.from_index} → ${wrapInfo.to_index} | Formula: ${wrapInfo.formula}`;
    el.wrapToast.style.display = 'block';

    wrapToastTimer = setTimeout(() => {
      el.wrapToast.style.display = 'none';
    }, 4500);
  }

  // ==========================================
  // API CLIENT & HEALTH CHECK
  // ==========================================
  async function checkHealth() {
    try {
      const res = await fetch('/api/health');
      if (res.ok) {
        const data = await res.json();
        el.backendStatusPill.className = 'status-pill status-running';
        el.backendStatusText.textContent = 'Running';
        el.dbStatusText.textContent = `● ${data.database?.badge_text || 'SQLite Mode'}`;
      } else {
        markOffline();
      }
    } catch (e) {
      markOffline();
    }
  }

  function markOffline() {
    el.backendStatusPill.className = 'status-pill status-running';
    el.backendStatusPill.style.background = 'rgba(239, 68, 68, 0.15)';
    el.backendStatusPill.style.color = '#f87171';
    el.backendStatusPill.style.borderColor = 'rgba(239, 68, 68, 0.3)';
    el.backendStatusText.textContent = '⚠ Backend Offline';
  }

  async function fetchState() {
    try {
      const res = await fetch('/api/queue/state');
      if (res.ok) {
        const state = await res.json();
        updateUI(state);
      }
    } catch (e) {
      console.error('Failed to fetch state:', e);
    }
  }

  // ==========================================
  // UI RENDERING
  // ==========================================
  function updateUI(state) {
    currentState = state;

    // 1. Update Info Strip
    el.valFront.textContent = state.front;
    el.valRear.textContent = state.rear;
    el.valSize.textContent = state.size;
    el.valCap.textContent = state.capacity;
    el.headerCapBadge.textContent = `CAPACITY: ${state.capacity}`;

    let statusText = 'ACTIVE';
    if (state.is_full) {
      statusText = 'FULL';
      el.valStatus.className = 'cell-val text-amber';
    } else if (state.is_empty) {
      statusText = 'EMPTY';
      el.valStatus.className = 'cell-val text-muted';
    } else {
      el.valStatus.className = 'cell-val text-emerald';
    }
    el.valStatus.textContent = statusText;

    // Update active modal button
    el.capSelectBtns.forEach((btn) => {
      btn.classList.toggle('active', parseInt(btn.dataset.cap, 10) === state.capacity);
    });

    // 2. Render Queue Slots
    renderSlots(state);

    // 3. Render Dual Representation (Physical Array vs Logical FIFO Queue)
    renderDualRepresentation(state);

    // 4. Update Learning Sheet
    if (state.last_operation) {
      renderLearningDetails(state.last_operation);
    }

    // 5. Check if Circular Wrap Occurred
    if (state.last_operation && state.last_operation.wrapped && state.last_operation.wrap_detail) {
      showWrapNotification(state.last_operation.wrap_detail);
    }
  }

  function renderSlots(state) {
    el.queueSlotsWrapper.innerHTML = '';
    const lastOp = state.last_operation || {};
    const isLargeCap = state.capacity > 5;

    state.slots.forEach((slot) => {
      const slotEl = document.createElement('div');
      const classes = ['queue-slot', slot.is_occupied ? 'occupied' : 'empty'];
      if (isLargeCap) classes.push('cap-lg');
      slotEl.className = classes.join(' ');


      // Highlight animation if slot was just targeted
      if (lastOp.operation === 'ENQUEUE' && lastOp.inserted_at === slot.index) {
        slotEl.classList.add('just-enqueued');
      } else if (lastOp.operation === 'DEQUEUE' && lastOp.removed_from === slot.index) {
        slotEl.classList.add('just-dequeued');
      }

      // Top Pointer Badge (FRONT or FRONT & REAR)
      const topBadgeContainer = document.createElement('div');
      topBadgeContainer.className = 'slot-pointer-top';
      if (slot.is_front && slot.is_rear) {
        topBadgeContainer.innerHTML = `<span class="badge-front-rear">F &amp; R ↓</span>`;
      } else if (slot.is_front) {
        topBadgeContainer.innerHTML = `<span class="badge-front">FRONT ↓</span>`;
      }
      slotEl.appendChild(topBadgeContainer);

      // Value Box
      const valueBox = document.createElement('div');
      valueBox.className = 'slot-value-box';
      valueBox.textContent = slot.is_occupied ? slot.value : '—';
      slotEl.appendChild(valueBox);

      // Index Label
      const indexLabel = document.createElement('div');
      indexLabel.className = 'slot-index-label';
      indexLabel.textContent = `[ ${slot.index} ]`;
      slotEl.appendChild(indexLabel);

      // Bottom Pointer Badge (REAR - only if not already merged with front)
      const bottomBadgeContainer = document.createElement('div');
      bottomBadgeContainer.className = 'slot-pointer-bottom';
      if (slot.is_rear && !slot.is_front) {
        bottomBadgeContainer.innerHTML = `<span class="badge-rear">↑ REAR</span>`;
      }
      slotEl.appendChild(bottomBadgeContainer);

      el.queueSlotsWrapper.appendChild(slotEl);
    });
  }

  function renderDualRepresentation(state) {
    // Physical Array
    el.physicalArrayBubbles.innerHTML = '';
    state.physical_array.forEach((val, idx) => {
      const bubble = document.createElement('div');
      bubble.className = `bubble-slot ${val !== null ? 'occupied' : 'empty'}`;
      bubble.innerHTML = `
        <span>${val !== null ? val : '—'}</span>
        <span class="bubble-idx">${idx}</span>
      `;
      el.physicalArrayBubbles.appendChild(bubble);
    });

    // Logical FIFO Queue
    el.logicalQueueBubbles.innerHTML = '';
    const logical = state.logical_queue || [];
    if (logical.length === 0) {
      el.logicalQueueBubbles.innerHTML = `<span class="rep-sub">Queue is currently empty</span>`;
    } else {
      logical.forEach((val, i) => {
        const item = document.createElement('div');
        item.className = 'logical-flow-item';
        item.innerHTML = `
          <div class="logical-bubble">${val}</div>
          ${i < logical.length - 1 ? '<span class="logical-arrow">→</span>' : ''}
        `;
        el.logicalQueueBubbles.appendChild(item);
      });
    }
  }

  function renderLearningDetails(opInfo) {
    el.stepOpName.textContent = opInfo.operation || opInfo.type || 'OPERATION';
    el.stepOpSummary.innerHTML = `<strong>${opInfo.operation || 'STATUS'}</strong>: ${opInfo.message || ''}`;

    el.stepList.innerHTML = '';
    const steps = opInfo.steps || [];
    if (steps.length > 0) {
      steps.forEach((step) => {
        const li = document.createElement('li');
        li.textContent = step;
        el.stepList.appendChild(li);
      });
    } else {
      const li = document.createElement('li');
      li.textContent = opInfo.message || 'No steps recorded.';
      el.stepList.appendChild(li);
    }
  }

  // ==========================================
  // QUEUE OPERATIONS (HANDLERS)
  // ==========================================
  async function handleEnqueue() {
    const rawVal = el.enqueueValueInput.value.trim();
    if (!rawVal) {
      showToast('⚠️ Please enter a value to enqueue.', 'warning');
      el.enqueueValueInput.focus();
      return;
    }

    try {
      const res = await fetch('/api/queue/enqueue', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ value: rawVal })
      });
      const data = await res.json();

      if (data.success) {
        showToast(`✓ Enqueued <strong>${rawVal}</strong> at index ${data.rear}`, 'success');
        defaultInputValue = (parseInt(rawVal, 10) || 10) + 10;
        el.enqueueValueInput.value = '';
        el.enqueueValueInput.placeholder = `Next: ${defaultInputValue}`;
      } else {
        if (data.error === 'OVERFLOW') {
          showToast(`⚠️ <strong>OVERFLOW!</strong> Queue is Full (${data.size}/${data.capacity})`, 'warning', 4000);
        } else {
          showToast(`✕ ${data.message || 'Enqueue error'}`, 'error');
        }
      }
      updateUI(data);
    } catch (e) {
      showToast('✕ Network connection error.', 'error');
    }
  }

  async function handleDequeue() {
    try {
      const res = await fetch('/api/queue/dequeue', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await res.json();

      if (data.success) {
        const removed = data.operation_result?.removed_value;
        const fromIdx = data.operation_result?.removed_from;
        showToast(`✓ Dequeued <strong>${removed}</strong> from index ${fromIdx}`, 'info');
      } else {
        if (data.error === 'UNDERFLOW') {
          showToast('✕ <strong>UNDERFLOW!</strong> Queue is empty.', 'error');
        } else {
          showToast(`✕ ${data.message || 'Dequeue error'}`, 'error');
        }
      }
      updateUI(data);
    } catch (e) {
      showToast('✕ Network connection error.', 'error');
    }
  }

  async function handlePeek() {
    try {
      const res = await fetch('/api/queue/peek');
      const data = await res.json();

      if (data.success) {
        const val = data.operation_result?.front_element;
        const idx = data.operation_result?.front_index;
        showToast(`👁 <strong>PEEK</strong>: Front element is <strong>${val}</strong> (Index ${idx})`, 'info', 3500);
      } else {
        showToast('✕ Queue is empty! No element to peek.', 'error');
      }
      updateUI(data);
    } catch (e) {
      showToast('✕ Network connection error.', 'error');
    }
  }

  async function handleDisplay() {
    try {
      const res = await fetch('/api/queue/display');
      const data = await res.json();
      const logical = data.logical_queue || [];

      if (logical.length > 0) {
        showToast(`≡ <strong>FIFO ORDER:</strong> ${logical.join(' → ')}`, 'info', 4000);
      } else {
        showToast('≡ Queue is empty.', 'info');
      }
      updateUI(data);
    } catch (e) {
      showToast('✕ Network connection error.', 'error');
    }
  }

  async function handleClear() {
    try {
      const res = await fetch('/api/queue/clear', { method: 'POST' });
      const data = await res.json();
      showToast('⌫ All queue slots cleared.', 'info');
      updateUI(data);
    } catch (e) {
      showToast('✕ Network connection error.', 'error');
    }
  }

  async function handleReset() {
    try {
      const res = await fetch('/api/queue/reset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ capacity: 5 })
      });
      const data = await res.json();
      defaultInputValue = 10;
      el.enqueueValueInput.value = '';
      el.enqueueValueInput.placeholder = 'Enter value (e.g. 10)';
      showToast('↺ Queue reset to default capacity 5.', 'info');
      updateUI(data);
    } catch (e) {
      showToast('✕ Network connection error.', 'error');
    }
  }

  async function handleSetCapacity(cap) {
    try {
      const res = await fetch('/api/queue/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ capacity: cap })
      });
      const data = await res.json();
      if (data.success) {
        showToast(`⚙ Capacity set to ${cap}.`, 'info');
        updateUI(data);
      }
    } catch (e) {
      showToast('✕ Error updating capacity.', 'error');
    }
  }

  function generateRandomValue() {
    el.enqueueValueInput.value = defaultInputValue;
    defaultInputValue += 10;
    el.enqueueValueInput.focus();
  }

  // ==========================================
  // PROFESSOR DEMO MODE CONTROLLER
  // ==========================================
  async function loadDemoSteps() {
    try {
      const res = await fetch('/api/queue/demo-steps');
      const data = await res.json();
      if (data.success) {
        demoSteps = data.steps;
      }
    } catch (e) {
      console.warn('Could not load demo steps:', e);
    }
  }

  function toggleDemoMode() {
    const isVisible = el.demoControllerCard.style.display !== 'none';
    if (isVisible) {
      closeDemoMode();
    } else {
      openDemoMode();
    }
  }

  function openDemoMode() {
    switchTab('queue');
    el.demoControllerCard.style.display = 'flex';
    currentDemoStepIndex = 0;
    updateDemoControllerUI();
  }

  function closeDemoMode() {
    pauseDemo();
    el.demoControllerCard.style.display = 'none';
  }

  function updateDemoControllerUI() {
    el.demoStepBadge.textContent = `Step ${currentDemoStepIndex + 1} of ${demoSteps.length}`;
    if (demoSteps[currentDemoStepIndex]) {
      el.demoStepText.textContent = demoSteps[currentDemoStepIndex].description;
    }
  }

  async function executeDemoStep(stepObj) {
    if (!stepObj) return;

    if (stepObj.action === 'create') {
      await fetch('/api/queue/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ capacity: stepObj.capacity })
      });
    } else if (stepObj.action === 'enqueue') {
      await fetch('/api/queue/enqueue', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ value: stepObj.value })
      });
    } else if (stepObj.action === 'dequeue') {
      await fetch('/api/queue/dequeue', { method: 'POST' });
    } else if (stepObj.action === 'display') {
      await fetch('/api/queue/display');
    }

    await fetchState();
  }

  async function stepDemo() {
    if (currentDemoStepIndex >= demoSteps.length) {
      currentDemoStepIndex = 0;
    }

    const currentStep = demoSteps[currentDemoStepIndex];
    updateDemoControllerUI();
    await executeDemoStep(currentStep);

    currentDemoStepIndex++;
    if (currentDemoStepIndex >= demoSteps.length) {
      pauseDemo();
      showToast('🎓 Professor Demo Sequence Completed!', 'success', 4000);
    }
  }

  function playDemo() {
    isDemoPlaying = true;
    el.demoPlayBtn.disabled = true;
    el.demoPauseBtn.disabled = false;
    runDemoLoop();
  }

  function pauseDemo() {
    isDemoPlaying = false;
    clearTimeout(demoTimer);
    el.demoPlayBtn.disabled = false;
    el.demoPauseBtn.disabled = true;
  }

  function resetDemo() {
    pauseDemo();
    currentDemoStepIndex = 0;
    updateDemoControllerUI();
    handleReset();
  }

  async function runDemoLoop() {
    if (!isDemoPlaying) return;

    await stepDemo();

    if (isDemoPlaying && currentDemoStepIndex < demoSteps.length) {
      const speed = parseInt(el.demoSpeedSelect.value, 10) || 1800;
      demoTimer = setTimeout(runDemoLoop, speed);
    }
  }

  // ==========================================
  // OPERATION HISTORY TAB
  // ==========================================
  async function fetchHistory() {
    try {
      const res = await fetch('/api/history?limit=30');
      const data = await res.json();
      if (data.success && el.historyTableBody) {
        renderHistoryTable(data.history);
      }
    } catch (e) {
      console.error('Failed to load history:', e);
    }
  }

  function renderHistoryTable(records) {
    if (!records || records.length === 0) {
      el.historyTableBody.innerHTML = `<tr><td colspan="7" class="text-center">No operation history yet.</td></tr>`;
      return;
    }

    el.historyTableBody.innerHTML = '';
    records.forEach((row) => {
      const tr = document.createElement('tr');
      const timeStr = row.created_at ? row.created_at.split(' ')[1] || row.created_at : '—';
      tr.innerHTML = `
        <td>${timeStr}</td>
        <td><strong>${row.operation}</strong></td>
        <td>${row.value !== null ? row.value : '—'}</td>
        <td>${row.front_index}</td>
        <td>${row.rear_index}</td>
        <td>${row.size}/${row.capacity}</td>
        <td>${row.wrapped ? '<span class="text-amber">↻ Yes</span>' : 'No'}</td>
      `;
      el.historyTableBody.appendChild(tr);
    });
  }

  async function handleClearHistory() {
    try {
      const res = await fetch('/api/history/clear', { method: 'POST' });
      const data = await res.json();
      if (data.success) {
        showToast('History log cleared.', 'info');
        fetchHistory();
      }
    } catch (e) {
      showToast('Error clearing history.', 'error');
    }
  }

})();
