document.getElementById('algorithm-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Preluăm valorile din formular
    let processTimeInput = document.getElementById('process_time').value;
    let algorithm = document.querySelector('input[name="algorithm"]:checked').value;
    let quantum = document.getElementById('quantum').value;
    
    if ((algorithm === 'srtf' || algorithm === 'rr')  && (quantum === '' || quantum <= 0)) {
        return; // Oprim trimiterea formularului
    }

    // Dacă algoritmul nu este SRTF, setăm cuantumul la 0
    if ((algorithm !== 'srtf' || algorithm !== 'rr') && quantum === '') {
        quantum = 0;
    }

    // Trimitem datele către server
    fetch('/', {
        method: 'POST',
        body: new URLSearchParams({
            process_time: processTimeInput,
            algorithm: algorithm,
            quantum: quantum
        }),
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    })
    .then(response => response.json())
    .then(data => {
        // Afișăm rezultatele
        document.getElementById('results').style.display = 'block';

        // Generăm tabelul
        let resultsBody = document.getElementById('results-body');
        resultsBody.innerHTML = ''; // Curățăm rezultatele anterioare

        data.execution_order.forEach((process, index) => {
            let row = document.createElement('tr');
            row.innerHTML = `<td>${process}</td>
                             <td>${data.step_durations[index]}</td>
                             <td>${data.completion_time[index]}</td>
                             <td>${data.waiting_time[index]}</td>`;
            resultsBody.appendChild(row);
        });

        // Afișăm timpii medii
        document.getElementById('avg-turn-around-time').textContent = 'Timp Mediu de Realizare: ' + data.avg_completion_time;
        document.getElementById('avg-waiting-time').textContent = 'Timp Mediu de Așteptare: ' + data.avg_waiting_time;
        document.getElementById('execution_order').textContent = 'Ordinea de Executare: ' + data.execution_order.join(', ');

    })
    .catch(error => console.error('Error:', error));
});


document.addEventListener('DOMContentLoaded', function() {
    // Ascultăm modificările pe butoanele radio
    document.querySelectorAll('input[name="algorithm"]').forEach(function(radioButton) {
        radioButton.addEventListener('change', function() {
            // Verificăm ce algoritm a fost selectat
            if (document.getElementById('srtf').checked || document.getElementById('rr').checked) {
                // Dacă algoritmul selectat este SRTF sau Round Robin, afisăm inputul pentru cuantum
                document.getElementById('quantum-container').style.display = 'block';
            } else {
                // Dacă alt algoritm este selectat, ascundem inputul pentru cuantum
                document.getElementById('quantum-container').style.display = 'none';
            }
        });
    });

    // Verificăm și la încărcarea paginii dacă SRTF sau Round Robin sunt selectate pentru a arăta sau ascunde inputul
    if (document.getElementById('srtf').checked || document.getElementById('rr').checked) {
        document.getElementById('quantum-container').style.display = 'block';
    } else {
        document.getElementById('quantum-container').style.display = 'none';
    }
});