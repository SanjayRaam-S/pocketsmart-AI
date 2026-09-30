/**
 * PocketSmart AI - Interactive Planners & Results Controller
 */

function showLoading(title = "PocketSmart AI is thinking...", subtitle = "Analyzing budget and generating personalized recommendations...") {
  let overlay = document.getElementById('loadingOverlay');
  if (!overlay) {
    overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.className = 'loading-overlay';
    overlay.innerHTML = `
      <div class="loading-spinner"></div>
      <h3 id="loadingTitle" style="font-size: 1.35rem; margin-bottom: 0.5rem; text-align: center;">${title}</h3>
      <p id="loadingSubtitle" style="color: #cbd5e1; font-size: 0.95rem; max-width: 400px; text-align: center;">${subtitle}</p>
    `;
    document.body.appendChild(overlay);
  } else {
    document.getElementById('loadingTitle').innerText = title;
    document.getElementById('loadingSubtitle').innerText = subtitle;
  }
  overlay.style.display = 'flex';
}

function hideLoading() {
  const overlay = document.getElementById('loadingOverlay');
  if (overlay) overlay.style.display = 'none';
}

// ----------------------------------------------------
// HOME INTERIOR PLANNER LOGIC
// ----------------------------------------------------
function initHomePlanner() {
  const form = document.getElementById('homePlannerForm');
  if (!form) return;

  // Room chip selection
  const chips = document.querySelectorAll('.room-chip');
  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      chip.classList.toggle('active');
    });
  });

  // Quantity adjusters
  document.querySelectorAll('.counter-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const action = btn.dataset.action;
      const targetId = btn.dataset.target;
      const input = document.getElementById(targetId);
      if (!input) return;

      let val = parseInt(input.value) || 0;
      if (action === 'plus') {
        val += 1;
      } else if (action === 'minus' && val > 0) {
        val -= 1;
      }
      input.value = val;
    });
  });

  // Form submission
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const budget = parseFloat(document.getElementById('total_budget').value);
    if (!budget || budget <= 0) {
      showToast('Please enter a valid budget greater than 0', 'danger');
      return;
    }

    const selectedRooms = [];
    document.querySelectorAll('.room-chip.active').forEach(chip => {
      selectedRooms.push(chip.dataset.room);
    });

    if (selectedRooms.length === 0) {
      showToast('Please select at least one room to plan', 'danger');
      return;
    }

    const quantities = {
      lights: parseInt(document.getElementById('qty_lights')?.value) || 0,
      ceiling_fans: parseInt(document.getElementById('qty_fans')?.value) || 0,
      sofa: parseInt(document.getElementById('qty_sofa')?.value) || 0,
      dining_table: parseInt(document.getElementById('qty_dining')?.value) || 0,
      chairs: parseInt(document.getElementById('qty_chairs')?.value) || 0,
      bed: parseInt(document.getElementById('qty_bed')?.value) || 0,
      wardrobe: parseInt(document.getElementById('qty_wardrobe')?.value) || 0,
      curtains: parseInt(document.getElementById('qty_curtains')?.value) || 0,
      rugs: parseInt(document.getElementById('qty_rugs')?.value) || 0,
      wall_art: parseInt(document.getElementById('qty_art')?.value) || 0,
      storage: parseInt(document.getElementById('qty_storage')?.value) || 0,
      decorative_items: parseInt(document.getElementById('qty_decor')?.value) || 0
    };

    const payload = {
      total_budget: budget,
      currency: document.getElementById('currency').value || '₹',
      home_type: document.getElementById('home_type').value,
      number_of_rooms: parseInt(document.getElementById('number_of_rooms').value) || 2,
      selected_rooms: selectedRooms,
      quantities: quantities,
      preferred_style: document.getElementById('preferred_style').value,
      preferred_colors: document.getElementById('preferred_colors').value || null,
      brand_preferences: document.getElementById('brand_preferences').value || null,
      additional_requirements: document.getElementById('additional_requirements').value || null
    };

    showLoading("Designing Your Smart Home Interior...", "Gemini AI is analyzing room layout, allocating funds, and curating product recommendations...");

    try {
      const response = await fetch('/api/generate-home', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'Failed to generate interior recommendations.');
      }

      window.location.href = `/home-planner/results/${data.plan_id}`;
    } catch (err) {
      hideLoading();
      showToast(err.message, 'danger');
    }
  });
}

// ----------------------------------------------------
// PARTY PLANNER LOGIC
// ----------------------------------------------------
function initPartyPlanner() {
  const form = document.getElementById('partyPlannerForm');
  if (!form) return;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const budget = parseFloat(document.getElementById('party_budget').value);
    const guests = parseInt(document.getElementById('party_guests').value);

    if (!budget || budget <= 0) {
      showToast('Please enter a valid event budget', 'danger');
      return;
    }
    if (!guests || guests <= 0) {
      showToast('Number of guests must be positive', 'danger');
      return;
    }

    const payload = {
      total_budget: budget,
      currency: document.getElementById('party_currency').value || '₹',
      event_type: document.getElementById('event_type').value,
      number_of_guests: guests,
      event_date: document.getElementById('event_date').value || null,
      location: document.getElementById('party_location').value || 'City Center',
      indoor_outdoor: document.getElementById('indoor_outdoor').value,
      event_duration: document.getElementById('event_duration').value,
      food_preference: document.getElementById('food_preference').value,
      decoration_style: document.getElementById('decoration_style').value,
      entertainment_preference: document.getElementById('entertainment_preference').value,
      accommodation_required: document.getElementById('accommodation_required').checked,
      additional_notes: document.getElementById('party_notes').value || null
    };

    showLoading("Planning Your Celebration...", "PocketSmart AI is balancing catering, venue, decor, and entertainment within your budget...");

    try {
      const response = await fetch('/api/generate-party', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'Failed to plan party.');
      }

      window.location.href = `/party-planner/results/${data.plan_id}`;
    } catch (err) {
      hideLoading();
      showToast(err.message, 'danger');
    }
  });
}

// ----------------------------------------------------
// JEWELRY PLANNER LOGIC & IMAGE UPLOAD
// ----------------------------------------------------
function initJewelryPlanner() {
  const form = document.getElementById('jewelryPlannerForm');
  if (!form) return;

  const fileInput = document.getElementById('outfit_image');
  const uploadBox = document.getElementById('uploadBox');
  const previewImg = document.getElementById('imagePreview');

  if (uploadBox && fileInput) {
    uploadBox.addEventListener('click', () => fileInput.click());

    fileInput.addEventListener('change', () => {
      const file = fileInput.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          previewImg.src = e.target.result;
          previewImg.style.display = 'block';
          uploadBox.querySelector('.upload-prompt').style.display = 'none';
        };
        reader.readAsDataURL(file);
      }
    });

    // Drag and drop
    uploadBox.addEventListener('dragover', (e) => {
      e.preventDefault();
      uploadBox.classList.add('dragover');
    });

    uploadBox.addEventListener('dragleave', () => {
      uploadBox.classList.remove('dragover');
    });

    uploadBox.addEventListener('drop', (e) => {
      e.preventDefault();
      uploadBox.classList.remove('dragover');
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        fileInput.files = e.dataTransfer.files;
        const event = new Event('change');
        fileInput.dispatchEvent(event);
      }
    });
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const budget = parseFloat(document.getElementById('jewelry_budget').value);
    if (!budget || budget <= 0) {
      showToast('Please enter a valid jewelry budget', 'danger');
      return;
    }

    const formData = new FormData();
    formData.append('total_budget', budget);
    formData.append('currency', document.getElementById('jewelry_currency').value || '₹');
    formData.append('occasion', document.getElementById('jewelry_occasion').value);
    formData.append('jewelry_type', document.getElementById('jewelry_type').value);
    formData.append('preferred_style', document.getElementById('jewelry_style').value);
    formData.append('metal_preference', document.getElementById('metal_preference').value);
    formData.append('color_preference', document.getElementById('color_preference').value || '');
    formData.append('outfit_description', document.getElementById('outfit_description').value || '');

    if (fileInput && fileInput.files[0]) {
      formData.append('outfit_image', fileInput.files[0]);
    }

    showLoading("Analyzing Outfit & Styling Jewelry...", "Gemini AI is examining palette and neckline compatibility, allocating your budget, and selecting matching jewelry...");

    try {
      const response = await fetch('/api/generate-jewelry', {
        method: 'POST',
        body: formData
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'Failed to generate jewelry recommendations.');
      }

      window.location.href = `/jewelry-planner/results/${data.plan_id}`;
    } catch (err) {
      hideLoading();
      showToast(err.message, 'danger');
    }
  });
}

// ----------------------------------------------------
// RESULT ACTIONS (Save, Delete, Reuse)
// ----------------------------------------------------
async function toggleSavePlan(planId, btnElement) {
  try {
    const res = await fetch(`/api/recommendations/${planId}/save`, { method: 'POST' });
    const data = await res.json();
    if (res.ok) {
      if (data.is_saved) {
        btnElement.classList.add('btn-primary');
        btnElement.classList.remove('btn-outline');
        btnElement.innerHTML = '★ Saved in Collection';
        showToast('Plan saved to your collection!', 'success');
      } else {
        btnElement.classList.remove('btn-primary');
        btnElement.classList.add('btn-outline');
        btnElement.innerHTML = '☆ Save Recommendation';
        showToast('Plan removed from saved collection.', 'info');
      }
    }
  } catch (err) {
    showToast('Failed to update saved status', 'danger');
  }
}

async function deletePlan(planId, rowId) {
  if (!confirm("Are you sure you want to delete this plan? This action cannot be undone.")) {
    return;
  }
  try {
    const res = await fetch(`/api/history/${planId}`, { method: 'DELETE' });
    if (res.ok) {
      showToast('Plan deleted successfully', 'success');
      const elem = document.getElementById(rowId);
      if (elem) {
        elem.remove();
      }
      // If table empty, reload
      const remaining = document.querySelectorAll('.history-item');
      if (remaining.length === 0) {
        setTimeout(() => window.location.reload(), 500);
      }
    } else {
      const data = await res.json();
      showToast(data.detail || 'Could not delete plan', 'danger');
    }
  } catch (err) {
    showToast('Error deleting plan', 'danger');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  initHomePlanner();
  initPartyPlanner();
  initJewelryPlanner();
});
