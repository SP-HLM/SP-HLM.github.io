"use strict";
const tasks = ["Walk forward and pick up the cylinder.", "Pick up the bottle, step on the pedal to open the bin, and put it inside.", "Step on the pedal to open the trash bin.", "Pick up the bottle and place it in the box.", "Squat down and pull open the upper drawer of the cabinet.", "Pick up the object, squat down, and place it on the lower shelf.", "Kick the football into the goal.", "Push down the handle and push the door open."];
const titles = document.getElementById('task-title'), picture = document.getElementById('task-image');
document.querySelectorAll('[data-task]').forEach(button => button.addEventListener('click', () => {
 const i = Number(button.dataset.task);
 document.querySelectorAll('[data-task]').forEach(b => {const active=b===button; b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));});
 titles.textContent=tasks[i];document.getElementById('task-id').textContent=`TASK ${String(i+1).padStart(2,'0')}`;
 picture.src=`assets/images/task${i+1}_3frames_600dpi.webp`;picture.alt=`Three sequential execution frames. ${tasks[i]}`;
}));
