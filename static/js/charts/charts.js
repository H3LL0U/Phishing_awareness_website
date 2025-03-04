google.charts.load('current', {packages: ['corechart']});




    
var sent_email_data;
var visit_data;

var total_users; 
var typed;
var visited;
var typed_email;
var not_visited;

var trafic_data;
var email_trafic_data;
async function getDataFromAPI(link) {
    try {
        const response = await fetch(link, {
            method: "POST",
            headers: { "Content-Type": "application/json" }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        
        
        
        

        return data;  
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

(async function() {
    visit_data = await getDataFromAPI("/api/visit_data");
    sent_email_data =  await getDataFromAPI("/api/email_data")
    //raw data
    total_users = visit_data["total_users"]; 
    typed = visit_data["typed"]
    typed_email = visit_data["typed_email"]
    visited = visit_data["visited"]
    //processed into subcategories
    visited_without_action = visited - (typed_email)
    just_typed_email = typed_email - typed
    not_visited = total_users - visited;
    trafic_data = visit_data["visit_trafic"]
    email_trafic_data = sent_email_data["email_trafic"]
    alert(typed_email)
    google.charts.setOnLoadCallback(drawCharts);
})();


    

function drawTraficChart(){


    //chart for user trafic
    var pieDataArray = [['Gebruiker status', 'Aantal gebruikers']];

    // Only add non-zero values to the chart
    if (visited_without_action > 0) pieDataArray.push(['Bezocht zonder typen', visited_without_action]);
    if (not_visited > 0) pieDataArray.push(['Niet Bezocht', not_visited]);
    if (typed > 0) pieDataArray.push(['Bezocht en begon te typen in het wachtwoord veld', typed]);
    if (just_typed_email > 0) pieDataArray.push(['Bezocht en heeft alleen de email ingevoerd', just_typed_email]);
    var pieData = google.visualization.arrayToDataTable(pieDataArray);

    var pieOptions = {
        title: '',
        is3D: true,
        sliceVisibilityThreshold: 0
    };

    var pieChart = new google.visualization.PieChart(document.getElementById('pie_chart_visited_users'));
    pieChart.draw(pieData, pieOptions);

    
    window.pieChart = pieChart;
    window.pieData = pieData;
    window.pieOptions = pieOptions;
}
function drawTimeVisitChart(jsonData, idName, unit) {
    var data = new google.visualization.DataTable();
    data.addColumn('datetime', 'Datum');

    // Add a column for each redirect type + tooltip column
    var keys = Object.keys(jsonData);
    keys.forEach(key => {
        data.addColumn('number', key);
        data.addColumn({ type: 'string', role: 'tooltip' }); // Tooltip for each series
    });

    // Add a column for the total cumulative sum
    data.addColumn('number', 'Totaal');
    data.addColumn({ type: 'string', role: 'tooltip' });

    var allDates = new Set();

    // Collect all unique dates
    keys.forEach(key => {
        Object.keys(jsonData[key]).forEach(date => allDates.add(date));
    });

    // Convert the set to an array and sort it in ascending order
    var sortedDates = Array.from(allDates).sort((a, b) => new Date(a) - new Date(b));

    // Track cumulative values for each redirect type and the total
    var cumulativeData = {};
    keys.forEach(key => cumulativeData[key] = 0);
    var cumulativeTotal = 0;

    // Prepare data points
    var chartData = [];

    sortedDates.forEach(date => {
        var dateObj = new Date(date);
        var row = [dateObj];

        var totalAtThisTime = 0;
        var totalTooltip = `Tijd: ${dateObj.toLocaleString()}\n`;

        keys.forEach(key => {
            if (jsonData[key][date]) {
                cumulativeData[key] += jsonData[key][date];
            }
            row.push(cumulativeData[key]);

            // Create a tooltip for this specific redirect type
            let tooltipText = `Tijd: ${dateObj.toLocaleString()}\nRedirect type: ${key}\n${unit}: ${cumulativeData[key]}`;
            row.push(tooltipText);

            totalAtThisTime += cumulativeData[key];
        });

        // Update cumulative total
        cumulativeTotal = totalAtThisTime;
        row.push(cumulativeTotal);

        // Tooltip for the total
        totalTooltip += `Totaal ${unit}: ${cumulativeTotal}`;
        row.push(totalTooltip);

        chartData.push(row);
    });

    // Add rows to the data table
    data.addRows(chartData);

    // Chart options
    var options = {
        title: '',
        curveType: 'function',
        legend: { position: 'bottom' },
        hAxis: {
            title: 'Datum en tijd',
            format: 'MMM d, HH:mm:ss',
            gridlines: { count: -1 }
        },
        vAxis: { title: unit },
        tooltip: { isHtml: false, trigger: 'focus' }, // Standard tooltip behavior
    };

    // Create and draw the chart
    var chart = new google.visualization.LineChart(document.getElementById(idName));
    chart.draw(data, options);
}

function drawHourlyVisitHistogram(jsonData, idName, unit) {
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Uur'); // X-axis: Hours (0-23)
    data.addColumn('number', unit); // Y-axis: Total visits

    // Object to store visit counts per hour
    var hourlyVisits = Array(24).fill(0);

    // Loop through each redirect type
    Object.values(jsonData).forEach(entries => {
        Object.keys(entries).forEach(date => {
            var hour = new Date(date).getHours(); // Extract the hour (0-23)
            hourlyVisits[hour] += entries[date]; // Add visit count to the respective hour
        });
    });

    // Convert data into Google Charts format
    var chartData = [];
    for (var hour = 0; hour < 24; hour++) {
        chartData.push([hour.toString() + ":00", hourlyVisits[hour]]);
    }

    data.addRows(chartData);

    // Chart options
    var options = {
        title: '',
        legend: { position: 'none' }, // No legend needed for a single dataset
        hAxis: {
            title: 'Uur van de dag',
            format: 'H',
            gridlines: { count: 24 }
        },
        vAxis: {
            title: unit
        },
        histogram: { bucketSize: 1 }, // Each bucket represents an hour
    };

    // Create and draw the histogram
    var chart = new google.visualization.ColumnChart(document.getElementById(idName));
    chart.draw(data, options);
}





function drawCharts() {
    drawTraficChart()
    drawTimeVisitChart(jsonData=trafic_data,idName='time_visit_chart',unit = "Aantal redirects")
    drawTimeVisitChart(jsonData=email_trafic_data,'email_by_time', unit = "Aantal verstuurde e-mails")
    drawHourlyVisitHistogram(jsonData = trafic_data,"hourly_visit_chart", unit="Aantal bezochten op een bepaalde uur")
}



window.addEventListener('resize', function () {
    clearTimeout(window.resizedFinished);
    window.resizedFinished = setTimeout(function(){
        google.charts.setOnLoadCallback(drawCharts);
    }, 300); 
});