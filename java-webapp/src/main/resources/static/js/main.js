// RhythmIQ Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('🫀 RhythmIQ ECG Analysis System Loaded');
    
    // Initialize features
    initializeImagePreview();
    initializeFileValidation();
    initializeFormSubmission();
    initializeTooltips();
});

/**
 * Initialize image preview functionality
 */
function initializeImagePreview() {
    const fileInput = document.getElementById('file');
    const imagePreview = document.getElementById('imagePreview');
    const previewImage = document.getElementById('previewImage');
    
    if (fileInput && imagePreview && previewImage) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            
            if (file) {
                // Validate file type
                if (!isValidImageFile(file)) {
                    showAlert('Please select a valid image file (PNG, JPG, JPEG)', 'warning');
                    this.value = '';
                    imagePreview.style.display = 'none';
                    return;
                }
                
                // Validate file size (10MB limit)
                if (file.size > 10 * 1024 * 1024) {
                    showAlert('File size must be less than 10MB', 'warning');
                    this.value = '';
                    imagePreview.style.display = 'none';
                    return;
                }
                
                // Show preview
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImage.src = e.target.result;
                    imagePreview.style.display = 'block';
                    
                    // Smooth scroll to preview
                    setTimeout(() => {
                        imagePreview.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                    }, 100);
                };
                reader.readAsDataURL(file);
            } else {
                imagePreview.style.display = 'none';
            }
        });
    }
}

/**
 * Initialize file validation
 */
function initializeFileValidation() {
    const fileInput = document.getElementById('file');
    
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            const submitBtn = document.getElementById('analyzeBtn');
            
            if (file) {
                if (isValidImageFile(file)) {
                    if (submitBtn) {
                        submitBtn.disabled = false;
                        submitBtn.classList.remove('disabled');
                    }
                } else {
                    if (submitBtn) {
                        submitBtn.disabled = true;
                        submitBtn.classList.add('disabled');
                    }
                }
            }
        });
    }
}

/**
 * Initialize form submission handling
 */
function initializeFormSubmission() {
    const uploadForm = document.getElementById('uploadForm');
    const analyzeBtn = document.getElementById('analyzeBtn');
    
    if (uploadForm && analyzeBtn) {
        uploadForm.addEventListener('submit', function(e) {
            const fileInput = document.getElementById('file');
            
            if (!fileInput || !fileInput.files[0]) {
                e.preventDefault();
                showAlert('Please select an ECG image file', 'warning');
                return false;
            }
            
            // Update button state
            analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing ECG...';
            analyzeBtn.disabled = true;
            analyzeBtn.classList.add('disabled');
            
            // Show loading message
            showAlert('Analyzing your ECG image. This may take a few moments...', 'info');
        });
    }
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Validate if file is a valid image
 */
function isValidImageFile(file) {
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg'];
    return validTypes.includes(file.type);
}

/**
 * Show alert messages
 */
function showAlert(message, type = 'info') {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert.fade-in');
    existingAlerts.forEach(alert => alert.remove());
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show fade-in`;
    alertDiv.style.position = 'fixed';
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.style.minWidth = '300px';
    
    const icon = getAlertIcon(type);
    
    alertDiv.innerHTML = `
        <i class="fas ${icon}"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

/**
 * Get appropriate icon for alert type
 */
function getAlertIcon(type) {
    switch(type) {
        case 'success': return 'fa-check-circle';
        case 'warning': return 'fa-exclamation-triangle';
        case 'danger': return 'fa-exclamation-circle';
        case 'info': return 'fa-info-circle';
        default: return 'fa-info-circle';
    }
}

/**
 * Format file size for display
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(function() {
            showAlert('Copied to clipboard!', 'success');
        }).catch(function(err) {
            console.error('Failed to copy: ', err);
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            showAlert('Copied to clipboard!', 'success');
        } catch (err) {
            console.error('Failed to copy: ', err);
        }
        document.body.removeChild(textArea);
    }
}

/**
 * Download results as JSON
 */
function downloadResults(results) {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(results, null, 2));
    const downloadAnchorNode = document.createElement('a');
    downloadAnchorNode.setAttribute("href", dataStr);
    downloadAnchorNode.setAttribute("download", "ecg_analysis_results.json");
    document.body.appendChild(downloadAnchorNode);
    downloadAnchorNode.click();
    downloadAnchorNode.remove();
}

/**
 * Smooth scroll to element
 */
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

/**
 * Handle API calls for demo purposes
 */
async function callRhythmIQAPI(endpoint, data) {
    try {
        const response = await fetch(`/api${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Export functions for global access
window.RhythmIQ = {
    showAlert,
    copyToClipboard,
    downloadResults,
    scrollToElement,
    callRhythmIQAPI
};