"use strict";

$(function () {
    $('.nav-btn').on('click', function () {
        $(this).toggleClass('open');
    });

    $(document).on('click', '.tab', function () {
        let tabs = $(this).closest('.tabs');
        let tabContent = tabs.siblings('.tab-content');

        tabs.find('.tab').removeClass('active');
        $(this).addClass("active");

        let selectedTab = $(this).data("tab");
        tabContent.find(".content").removeClass("active");
        tabContent.find("#" + selectedTab).addClass("active");
    });

    $('.marquee-container').each(function () {
        const cont = $(this);
        const content = cont.find('.marquee-content');
        const clone = content.clone();
        const clone2 = clone.clone();
        cont.append(clone);
        cont.append(clone2);

        cont.find('.marquee-content').addClass('marquee');
    });

    $(document).on('click', '.icon-box', function () {
        $('.icon-box').removeClass('active');
        $(this).addClass('active');
    });
});

function formatNumber(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function animateNumber(element, targetNumber, duration) {
    const startTime = performance.now();
    const startNumber = 0;

    function updateNumber(currentTime) {
        const elapsedTime = currentTime - startTime;
        const progress = Math.min(elapsedTime / duration, 1);
        const currentNumber = Math.floor(startNumber + progress * (targetNumber - startNumber));
        element.innerText = formatNumber(currentNumber);

        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        }
    }

    requestAnimationFrame(updateNumber);
}

function checkScroll() {
    const numberElements = document.querySelectorAll('.number');
    numberElements.forEach(element => {
        if (!element.classList.contains('animated')) {
            const targetValue = parseInt(element.getAttribute("data-target"), 10);
            const durationValue = parseInt(element.getAttribute("data-duration"), 10);

            const rect = element.getBoundingClientRect();
            if (rect.top >= 0 && rect.bottom <= window.innerHeight) {
                animateNumber(element, targetValue, durationValue);
                element.classList.add('animated');
            }
        }
    });
}

window.addEventListener('scroll', checkScroll);


"use strict";

$(function () {
    $('.nav-btn').on('click', function () {
        $(this).toggleClass('open');
    });

    $(document).on('click', '.tab', function () {
        let tabs = $(this).closest('.tabs');
        let tabContent = tabs.siblings('.tab-content');

        tabs.find('.tab').removeClass('active');
        $(this).addClass("active");

        let selectedTab = $(this).data("tab");
        tabContent.find(".content").removeClass("active");
        tabContent.find("#" + selectedTab).addClass("active");
    });

    $('.marquee-container').each(function () {
        const cont = $(this);
        const content = cont.find('.marquee-content');
        const clone = content.clone();
        const clone2 = clone.clone();
        cont.append(clone);
        cont.append(clone2);

        cont.find('.marquee-content').addClass('marquee');
    });

    $(document).on('click', '.icon-box', function () {
        $('.icon-box').removeClass('active');
        $(this).addClass('active');
    });
});

function formatNumber(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function animateNumber(element, targetNumber, duration) {
    const startTime = performance.now();
    const startNumber = 0;

    function updateNumber(currentTime) {
        const elapsedTime = currentTime - startTime;
        const progress = Math.min(elapsedTime / duration, 1);
        const currentNumber = Math.floor(startNumber + progress * (targetNumber - startNumber));
        element.innerText = formatNumber(currentNumber);

        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        }
    }

    requestAnimationFrame(updateNumber);
}

function checkScroll() {
    const numberElements = document.querySelectorAll('.number');
    numberElements.forEach(element => {
        if (!element.classList.contains('animated')) {
            const targetValue = parseInt(element.getAttribute("data-target"), 10);
            const durationValue = parseInt(element.getAttribute("data-duration"), 10);

            const rect = element.getBoundingClientRect();
            if (rect.top >= 0 && rect.bottom <= window.innerHeight) {
                animateNumber(element, targetValue, durationValue);
                element.classList.add('animated');
            }
        }
    });
}

window.addEventListener('scroll', checkScroll);


/* ===============================
   EMI CALCULATOR SCRIPT (ADDED)
   =============================== */

function calculateEMI() {
    const loanAmount = document.getElementById("loanAmount");
    const interestRate = document.getElementById("interestRate");
    const loanTenure = document.getElementById("loanTenure");

    if (!loanAmount || !interestRate || !loanTenure) {
        console.error("EMI fields not found");
        return;
    }

    const P = parseFloat(loanAmount.value);
    const annualRate = parseFloat(interestRate.value);
    const N = parseInt(loanTenure.value);

    if (isNaN(P) || isNaN(annualRate) || isNaN(N) || P <= 0 || annualRate <= 0 || N <= 0) {
        alert("Please enter valid EMI values");
        return;
    }

    const R = annualRate / 12 / 100;

    const EMI =
        (P * R * Math.pow(1 + R, N)) /
        (Math.pow(1 + R, N) - 1);

    const totalPayment = EMI * N;
    const totalInterest = totalPayment - P;

   animateEmiValue("monthlyEmi", EMI.toFixed(2));
animateEmiValue("totalInterest", totalInterest.toFixed(2));
animateEmiValue("totalPayment", totalPayment.toFixed(2));

}




function animateEmiValue(id, finalValue) {
    const el = document.getElementById(id);
    if (!el) return;

    const target = parseFloat(finalValue);
    let start = 0;
    const duration = 800;
    const startTime = performance.now();

    function animate(time) {
        const progress = Math.min((time - startTime) / duration, 1);
        const current = start + progress * (target - start);

        el.innerText =
            "₹" + current.toLocaleString("en-IN", {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });

        if (progress < 1) requestAnimationFrame(animate);
    }

    requestAnimationFrame(animate);
}




/* =========================
   GLOBAL SCROLL ANIMATION
   ========================= */

document.addEventListener("DOMContentLoaded", function () {
    const animatedElements = document.querySelectorAll(".scroll-animate");

    function onScrollAnimate() {
        const triggerPoint = window.innerHeight * 0.85;

        animatedElements.forEach(el => {
            const elementTop = el.getBoundingClientRect().top;

            if (elementTop < triggerPoint) {
                el.classList.add("show");
            }
        });
    }

    window.addEventListener("scroll", onScrollAnimate);
    onScrollAnimate();

});


/* ===============================
   EMI MODAL AUTO FETCH SCRIPT
   =============================== */

document.addEventListener("DOMContentLoaded", function () {

    const emiModal = document.getElementById("emiModal");

    if (!emiModal) return;

    emiModal.addEventListener("show.bs.modal", function (event) {

        const button = event.relatedTarget;

        if (!button) return;

        const interestValue = button.getAttribute("data-interest");

        const interestInput = document.getElementById("interestRate");
        const loanAmountInput = document.getElementById("loanAmount");
        const tenureInput = document.getElementById("tenure");
        const emiResult = document.getElementById("emiResult");

        if (interestInput) {
            interestInput.value = interestValue;
        }

        if (loanAmountInput) loanAmountInput.value = "";
        if (tenureInput) tenureInput.value = "";
        if (emiResult) emiResult.innerText = "0";

    });

});


function toggleProfileMenu(){

let menu = document.getElementById("profileMenu");

if(menu.style.display === "block"){
menu.style.display="none";
}else{
menu.style.display="block";
}

}

document.addEventListener("click", function(e){

const profile = document.querySelector(".nav-profile");

if(profile && !profile.contains(e.target)){
let menu = document.getElementById("profileMenu");
if(menu){menu.style.display="none";}
}

});









document.addEventListener("DOMContentLoaded", function(){

const formApp = document.querySelector(".loan-form-app");

let currentStep = 0;

const steps = formApp.querySelectorAll(".form-step");
const nextBtns = formApp.querySelectorAll(".next-btn");
const prevBtns = formApp.querySelectorAll(".prev-btn");
const indicators = formApp.querySelectorAll(".step");

function updateStep(){

steps.forEach((step,index)=>{
step.classList.toggle("active", index === currentStep);
});

indicators.forEach((step,index)=>{
step.classList.toggle("active", index === currentStep);
});

}

nextBtns.forEach(btn=>{
btn.addEventListener("click",function(){

if(currentStep < steps.length-1){
currentStep++;
updateStep();
}

});
});

prevBtns.forEach(btn=>{
btn.addEventListener("click",function(){

if(currentStep > 0){
currentStep--;
updateStep();
}

});
});

});




document.addEventListener("DOMContentLoaded", function () {

    const loanType = document.getElementById("loanType");
    const interestField = document.getElementById("interestRate");

    if (!loanType || !interestField) return;

    loanType.addEventListener("change", function () {

        let rates = {
            "personal": 5,
            "home": 7,
            "business": 10,
            "education": 6
        };

        interestField.value = rates[this.value] || 5;
    });

});








