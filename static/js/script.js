document.addEventListener('DOMContentLoaded', function() {
    // Form validation for the test creation form
    const testForm = document.getElementById('test-form');
    if (testForm) {
        testForm.addEventListener('submit', function(event) {
            const numQuestions = document.getElementById('num_questions').value;
            const topics = document.querySelectorAll('input[name="topics"]:checked');
            
            let isValid = true;
            let errorMessage = '';
            
            // Validate number of questions
            if (numQuestions < 1 || numQuestions > 50) {
                isValid = false;
                errorMessage += 'Number of questions must be between 1 and 50.\n';
            }
            
            // Validate that at least one topic is selected
            if (topics.length === 0) {
                isValid = false;
                errorMessage += 'Please select at least one math topic.\n';
            }
            
            // Display error or submit form
            if (!isValid) {
                event.preventDefault();
                alert(errorMessage);
            }
        });
    }
    
    // Preview PDF functionality (if PDF.js is available)
    const pdfPreview = document.getElementById('pdf-preview');
    const pdfUrl = pdfPreview ? pdfPreview.getAttribute('data-pdf-url') : null;
    
    if (pdfPreview && pdfUrl && window.pdfjsLib) {
        // Using PDF.js to render a preview
        pdfjsLib.getDocument(pdfUrl).promise.then(function(pdf) {
            pdf.getPage(1).then(function(page) {
                const scale = 1.5;
                const viewport = page.getViewport({ scale: scale });
                
                // Prepare canvas for PDF rendering
                const canvas = document.createElement('canvas');
                const context = canvas.getContext('2d');
                canvas.height = viewport.height;
                canvas.width = viewport.width;
                pdfPreview.appendChild(canvas);
                
                // Render PDF page
                page.render({
                    canvasContext: context,
                    viewport: viewport
                });
            });
        }).catch(function(error) {
            console.error('Error loading PDF:', error);
            pdfPreview.innerHTML = '<p class="text-danger">Error loading PDF preview</p>';
        });
    }
    
    // Topic selection toggle all functionality
    const toggleAllBtn = document.getElementById('toggle-all-topics');
    if (toggleAllBtn) {
        toggleAllBtn.addEventListener('click', function() {
            const topicCheckboxes = document.querySelectorAll('input[name="topics"]');
            const allChecked = Array.from(topicCheckboxes).every(cb => cb.checked);
            
            topicCheckboxes.forEach(checkbox => {
                checkbox.checked = !allChecked;
            });
            
            this.textContent = allChecked ? 'Select All' : 'Deselect All';
        });
    }
    
    // Dynamic form validation for number of questions
    const numQuestionsInput = document.getElementById('num_questions');
    if (numQuestionsInput) {
        numQuestionsInput.addEventListener('input', function() {
            const value = parseInt(this.value);
            const feedbackElement = document.getElementById('num-questions-feedback');
            
            if (value < 1 || value > 50 || isNaN(value)) {
                this.classList.add('is-invalid');
                this.classList.remove('is-valid');
                if (feedbackElement) {
                    feedbackElement.textContent = 'Please enter a number between 1 and 50';
                    feedbackElement.classList.add('invalid-feedback');
                    feedbackElement.classList.remove('valid-feedback');
                }
            } else {
                this.classList.add('is-valid');
                this.classList.remove('is-invalid');
                if (feedbackElement) {
                    feedbackElement.textContent = 'Looks good!';
                    feedbackElement.classList.add('valid-feedback');
                    feedbackElement.classList.remove('invalid-feedback');
                }
            }
        });
    }
});
