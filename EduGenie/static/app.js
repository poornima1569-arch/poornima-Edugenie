const task = document.getElementById('task');
const input = document.getElementById('input-text');
const label = document.getElementById('input-label');
const submit = document.getElementById('submit-btn');
const clear = document.getElementById('clear-btn');
const resultCard = document.getElementById('result-card');
const result = document.getElementById('result');
const status = document.getElementById('status');

const taskMeta = {
  qa: ['Your question', 'Example: What is the largest ocean?'],
  explain: ['Concept or topic', 'Example: Explain photosynthesis for a beginner.'],
  quiz: ['Topic or passage', 'Paste notes or a topic from which to create 3 MCQs.'],
  summarize: ['Text to summarize', 'Paste a paragraph, article section, or notes.'],
  learn: ['Topic to learn', 'Example: Create a beginner-to-advanced path for SQL.'],
};

task.addEventListener('change', () => {
  const [newLabel, placeholder] = taskMeta[task.value];
  label.textContent = newLabel;
  input.placeholder = placeholder;
  input.focus();
});

clear.addEventListener('click', () => {
  input.value = '';
  result.innerHTML = '';
  resultCard.classList.add('hidden');
  status.textContent = '';
});

submit.addEventListener('click', async () => {
  const text = input.value.trim();
  if (text.length < 2) {
    showError('Please enter at least a few words.');
    return;
  }

  submit.disabled = true;
  status.textContent = 'Generating…';
  resultCard.classList.remove('hidden');
  result.innerHTML = '<p class="result-text">Please wait…</p>';

  const endpoint = task.value === 'learn' ? '/learn/recommendations' : `/${task.value}`;
  const payload = task.value === 'qa' ? { question: text } : { text };

  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const body = await response.json();
    if (!response.ok || !body.success) throw new Error(body.error || 'Request failed.');
    render(body.data);
    status.textContent = 'Complete';
  } catch (error) {
    showError(error.message);
  } finally {
    submit.disabled = false;
  }
});

function render(data) {
  if (task.value === 'quiz') {
    renderQuiz(data.questions);
    return;
  }
  result.innerHTML = `<div class="result-text">${escapeHtml(String(data))}</div>`;
}

function renderQuiz(questions) {
  result.innerHTML = '';
  questions.forEach((item, index) => {
    const wrapper = document.createElement('div');
    wrapper.className = 'quiz-question';
    wrapper.innerHTML = `<h3>${index + 1}. ${escapeHtml(item.question)}</h3>`;
    item.options.forEach(option => {
      const button = document.createElement('button');
      button.className = 'option';
      button.type = 'button';
      button.textContent = option;
      button.addEventListener('click', () => {
        const buttons = wrapper.querySelectorAll('.option');
        buttons.forEach(b => b.disabled = true);
        const correct = option === item.correct_answer;
        button.classList.add(correct ? 'correct' : 'wrong');
        if (!correct) {
          buttons.forEach(b => {
            if (b.textContent === item.correct_answer) b.classList.add('correct');
          });
        }
        const feedback = document.createElement('p');
        feedback.className = 'quiz-feedback';
        feedback.textContent = correct ? `Correct! ${item.explanation}` : `Correct answer: ${item.correct_answer}. ${item.explanation}`;
        wrapper.appendChild(feedback);
      });
      wrapper.appendChild(button);
    });
    result.appendChild(wrapper);
  });
}

function showError(message) {
  resultCard.classList.remove('hidden');
  status.textContent = 'Error';
  result.innerHTML = `<div class="error">${escapeHtml(message)}</div>`;
}

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[char]));
}
