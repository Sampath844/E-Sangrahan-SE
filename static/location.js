// location.js (Integrated Code)
let map;
let userMarker;
let routingControl;
let userLocation;
let eWasteCenter = [12.9767, 77.5713]; // Fixed e-waste center coordinates

// Custom icons
const taxiIcon = L.icon({
    iconUrl: 'static/car.png',
    iconSize: [50, 50]
});

const eWasteIcon = L.icon({
    iconUrl: 'static/recycle.png', // Add your e-waste icon
    iconSize: [35, 35]
});

// Initialize map with user's location
navigator.geolocation.getCurrentPosition(
    (position) => {
        userLocation = [position.coords.latitude, position.coords.longitude];
        initMap(userLocation);
    },
    (error) => {
        alert('Enable location or enter manually.');
        console.error(error);
    }
);

function initMap(userCoords) {
    map = L.map('map').setView(userCoords, 13);
    
    L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
    }).addTo(map);

    // Add user marker
    userMarker = L.marker(userCoords, { icon: taxiIcon })
        .bindPopup('Your Location')
        .addTo(map);

    // Add fixed e-waste center marker
    L.marker(eWasteCenter, { icon: eWasteIcon })
        .bindPopup('E-Waste Center')
        .addTo(map);

    // Click handler for routing
    map.on('click', (e) => {
        if (routingControl) map.removeControl(routingControl);
        
        routingControl = L.Routing.control({
            waypoints: [
                L.latLng(userCoords[0], userCoords[1]), // User's location
                L.latLng(e.latlng.lat, e.latlng.lng) // Clicked point
            ],
            routeWhileDragging: true
        }).addTo(map);

        routingControl.on('routesfound', () => {
            document.getElementById('controls').style.display = 'block';
        });
    });
}


function confirmPickup() {
    const pickupTime = prompt('Enter pickup time (HH:MM):');
    const pickupDate = prompt('Enter pickup date (YYYY-MM-DD):');
    
    if (pickupTime && pickupDate) {
        generatePDF(pickupTime, pickupDate);
        setTimeout(() => {
            window.location.href = '/index2';
        }, 3000);
    } else {
        alert('Pickup time and date are required.');
    }
}

function generatePDF(time, date) {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    // Add colors
    const primaryColor = '#2c7be5';  // Blue
    const secondaryColor = '#27a779'; // Green
    const darkColor = '#2d373c';     // Dark gray

    // Add logo (replace with your actual path)
    const logoUrl = '/static/logo_waste.png'; // Update path as per your project
    doc.addImage(logoUrl, 'PNG', 10, 10, 30, 30);

    // Header
    doc.setFontSize(22);
    doc.setTextColor(primaryColor);
    doc.text('E-Waste Pickup Confirmation', 50, 20);
    
    // Reset text color
    doc.setTextColor(darkColor);
    doc.setFontSize(12);

    // User Details Section
    doc.setFont(undefined, 'bold');
    doc.text('Your Details:', 10, 45);
    doc.setFont(undefined, 'normal');
    doc.text(`Pickup Date: ${date}`, 10, 55);
    doc.text(`Pickup Time: ${time}`, 10, 65);
    doc.text(`Location Coordinates: ${userLocation[0].toFixed(6)}, ${userLocation[1].toFixed(6)}`, 10, 75);

    // Pickup Team Section
    doc.setFont(undefined, 'bold');
    doc.text('Pickup Team Information:', 10, 90);
    doc.setFont(undefined, 'normal');
    doc.text(`Driver Name: Meher Pranav`, 10, 100);
    doc.text(`Contact Number: +91 98765 43210`, 10, 110);
    doc.text(`Vehicle Number: KA-05-AB-1234`, 10, 120);

    // E-Waste Center Section
    // E-Waste Center details block
doc.setFont(undefined, 'bold');
doc.setTextColor(secondaryColor);
doc.text('E-Waste Center Details:', 10, 135);

doc.setFont(undefined, 'normal');
doc.setTextColor(darkColor);
doc.text(`Address: 15th Cross, Bengaluru, Karnataka`, 10, 145);
doc.text(`Coordinates: ${eWasteCenter[0]}, ${eWasteCenter[1]}`, 10, 155);
doc.text(`Contact: 080-2222 5555`, 10, 165);


    // Add decorative line
    doc.setDrawColor(primaryColor);
    doc.setLineWidth(0.5);
    doc.line(10, 170, 200, 170);

    // Footer note
    doc.setFontSize(10);
    doc.text('Thank you for responsible e-waste disposal!', 10, 180);

    doc.save('pickup-confirmation.pdf');
}

// Manual entry fallback
function manualLocationEntry() {
    const lat = prompt("Latitude (e.g., 12.9716):");
    const lng = prompt("Longitude (e.g., 77.5946):");
    if (lat && lng) {
        userLocation = [parseFloat(lat), parseFloat(lng)];
        initMap(userLocation);
    }
}

// Optional: Add button to navigate to e-waste center directly
function navigateToEWaste() {
    if (routingControl) map.removeControl(routingControl);
    
    routingControl = L.Routing.control({
        waypoints: [
            L.latLng(userLocation[0], userLocation[1]), // User's location
            L.latLng(eWasteCenter[0], eWasteCenter[1]) // E-waste center
        ]
    }).addTo(map);

    routingControl.on('routesfound', () => {
        document.getElementById('controls').style.display = 'block';
    });
}