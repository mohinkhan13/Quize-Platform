
// ----------------------------------------------------------------
//                  Theme Dark And light toggle 
// ----------------------------------------------------------------

// Apply the stored theme on page load
if (localStorage.getItem('color-theme') === 'dark') {
    document.documentElement.classList.add('dark');
} else {
    document.documentElement.classList.remove('dark');
}

var themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
var themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');
var themeToggleBtn = document.getElementById('theme-toggle');

// Change the icons inside the button based on previous settings
if (localStorage.getItem('color-theme') === 'dark') {
    themeToggleLightIcon.classList.remove('hidden');
} else {
    themeToggleDarkIcon.classList.remove('hidden');
}

themeToggleBtn.addEventListener('click', function() {
    // toggle icons inside button
    themeToggleDarkIcon.classList.toggle('hidden');
    themeToggleLightIcon.classList.toggle('hidden');

    // if set via local storage previously
    if (localStorage.getItem('color-theme')) {
        if (localStorage.getItem('color-theme') === 'light') {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        }
    } else {
        // if NOT set via local storage previously
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        } else {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        }
    }
});




// ----------------------------------------------------------------
//                  Password Strong And Suggestion 
// ----------------------------------------------------------------


document.addEventListener('DOMContentLoaded', function () {
    const passwordInput = document.getElementById('password');
    const popover = document.getElementById('popover-password');
    const requirements = document.querySelectorAll('.password-requirement');
    const strengthMeter = document.getElementById('strength-meter');
    const strengthBar = document.getElementById('strength-bar');
    const strengthLabel = document.getElementById('strength-label');

    // Show popover on focus
    passwordInput.addEventListener('focus', function () {
        popover.classList.remove('hidden');
        const rect = passwordInput.getBoundingClientRect();
        popover.style.top = rect.bottom + window.scrollY + 'px';
        popover.style.left = rect.left + 'px';
    });

    // Hide popover on blur
    passwordInput.addEventListener('blur', function () {
        setTimeout(() => {
            popover.classList.add('hidden');
        }, 100); // Delay hiding to allow click on popover
    });

    // Check password strength and update requirements
    passwordInput.addEventListener('input', function () {
        const password = passwordInput.value;
        const lengthRequirement = password.length >= 6;
        const uppercaseRequirement = /[A-Z]/.test(password);
        const lowercaseRequirement = /[a-z]/.test(password);
        const symbolRequirement = /[!@#$%^&*(),.?":{}|<>]/.test(password);

        const requirementsMet = [lengthRequirement, uppercaseRequirement, lowercaseRequirement, symbolRequirement];

        requirements.forEach((req, index) => {
            req.classList.toggle('text-gray-300', !requirementsMet[index]);
            req.classList.toggle('text-green-600', requirementsMet[index]);
        });

        // Calculate strength
        const strength = requirementsMet.filter(Boolean).length;
        const strengthPercent = (strength / requirements.length) * 100;

        strengthBar.style.width = strengthPercent + '%';
        if (strengthPercent === 100) {
            strengthLabel.innerText = 'Strong Password';
            strengthBar.classList.add('bg-green-500');
            strengthBar.classList.remove('bg-red-500');
        } else if (strengthPercent >= 50) {
            strengthLabel.innerText = 'Medium Password';
            strengthBar.classList.add('bg-yellow-500');
            strengthBar.classList.remove('bg-red-500', 'bg-green-500');
        } else {
            strengthLabel.innerText = 'Weak Password';
            strengthBar.classList.add('bg-red-500');
            strengthBar.classList.remove('bg-yellow-500', 'bg-green-500');
        }
    });
});


// -------------------------------------------------------


document.addEventListener('DOMContentLoaded', function() {
    const mcqCountInput = document.getElementById('mcq-count');
    const tfCountInput = document.getElementById('tf-count');
    const mcqContainer = document.getElementById('mcq-container');
    const tfContainer = document.getElementById('tf-container');
    const maxQuestions = {{ exam.number_of_questions }}; // Dynamic value from the server
    const warningMessage = document.getElementById('warning-message'); // Assume you have an element to show messages

    // Function to update the warning message visibility
    const updateWarningMessage = (isVisible) => {
        warningMessage.style.display = isVisible ? 'block' : 'none';
    };

    // Generate MCQ questions based on input
    mcqCountInput.addEventListener('input', function() {
        const mcqCount = parseInt(mcqCountInput.value, 10) || 0;
        const tfCount = parseInt(tfCountInput.value, 10) || 0;
        const totalCount = mcqCount + tfCount;

        mcqContainer.innerHTML = '';

        if (totalCount > maxQuestions) {
            updateWarningMessage(true);
            return; // Exit if the total exceeds the maximum
        } else {
            updateWarningMessage(false);
        }

        for (let i = 1; i <= mcqCount; i++) {
            const mcqHTML = `
            <div class="mb-6 border p-4 rounded-md shadow-md bg-white dark:bg-gray-800">
                <h3 class="text-lg font-semibold mb-2 dark:text-white">MCQ Question ${i}</h3>
                <div class="relative z-0 w-full mb-5">
                    <input type="text" id="mcq-question_${i}" name="question_${i}" class="peer bg-transparent border-b-2 border-gray-300 text-gray-900 dark:text-white focus:outline-none focus:border-blue-600 block w-full p-2.5 appearance-none transition duration-200" placeholder="Enter Your MCQ Question" required />
                </div>
                <div class="grid grid-cols-2 gap-6">
                    <div class="relative z-0 w-full mb-5">
                        <input type="text" id="mcq-option-a_${i}" name="option_a_${i}" class="peer bg-transparent border-b-2 border-gray-300 text-gray-900 dark:text-white focus:outline-none focus:border-blue-600 block w-full p-2.5 appearance-none transition duration-200" placeholder="Option A" required />
                    </div>
                    <div class="relative z-0 w-full mb-5">
                        <input type="text" id="mcq-option-b_${i}" name="option_b_${i}" class="peer bg-transparent border-b-2 border-gray-300 text-gray-900 dark:text-white focus:outline-none focus:border-blue-600 block w-full p-2.5 appearance-none transition duration-200" placeholder="Option B" required />
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-6">
                    <div class="relative z-0 w-full mb-5">
                        <input type="text" id="mcq-option-c_${i}" name="option_c_${i}" class="peer bg-transparent border-b-2 border-gray-300 text-gray-900 dark:text-white focus:outline-none focus:border-blue-600 block w-full p-2.5 appearance-none transition duration-200" placeholder="Option C" required />
                    </div>
                    <div class="relative z-0 w-full mb-5">
                        <input type="text" id="mcq-option-d_${i}" name="option_d_${i}" class="peer bg-transparent border-b-2 border-gray-300 text-gray-900 dark:text-white focus:outline-none focus:border-blue-600 block w-full p-2.5 appearance-none transition duration-200" placeholder="Option D" required />
                    </div>
                </div>
                <div class="relative z-0 w-full mb-5">
                    <select id="mcq-correct-answer_${i}" name="correct_answer_${i}" class="bg-transparent border-b-2 border-gray-300 text-gray-900 dark:text-white focus:outline-none focus:border-blue-600 block w-full p-2.5 appearance-none transition duration-200">
                        <option selected>Choose Correct Answer</option>
                        <option value="A">A</option>
                        <option value="B">B</option>
                        <option value="C">C</option>
                        <option value="D">D</option>
                    </select>
                </div>
            </div>`;

            mcqContainer.innerHTML += mcqHTML;
            console.log("Generated MCQ HTML:", mcqHTML);
        }
    });

    // Generate True/False questions based on input
    tfCountInput.addEventListener('input', function() {
        const tfCount = parseInt(tfCountInput.value, 10) || 0;
        const mcqCount = parseInt(mcqCountInput.value, 10) || 0;
        const totalCount = mcqCount + tfCount;

        tfContainer.innerHTML = '';

        if (totalCount > maxQuestions) {
            updateWarningMessage(true);
            return; // Exit if the total exceeds the maximum
        } else {
            updateWarningMessage(false);
        }

        for (let i = 1; i <= tfCount; i++) {
            const tfHTML = `
                <div class="mb-6 border p-4 rounded-md shadow-md bg-white dark:bg-gray-800">
                    <h3 class="text-lg font-semibold mb-2 dark:text-white">True/False Question ${i}</h3>
                    <div class="relative z-0 w-full mb-5">
                        <input type="text" id="tf-question_${i}" name="tf-question_${i}" class="peer bg-transparent border-b-2 border-gray-300 text-gray-900 dark:text-white focus:outline-none focus:border-blue-600 block w-full p-2.5 appearance-none transition duration-200" placeholder="Enter Your True/False Question" required />
                    </div>
                    <div class="relative z-0 w-full mb-5">
                        <select id="tf-correct-answer_${i}" name="tf-correct-answer_${i}" class="bg-transparent border-b-2 border-gray-300 text-gray-900 dark:text-white focus:outline-none focus:border-blue-600 block w-full p-2.5 appearance-none transition duration-200">
                            <option selected>Choose Correct Answer</option>
                            <option value="True">True</option>
                            <option value="False">False</option>
                        </select>
                    </div>
                </div>`;

            tfContainer.innerHTML += tfHTML;
            console.log("Generated TF HTML:", tfHTML);
        }
    });
});