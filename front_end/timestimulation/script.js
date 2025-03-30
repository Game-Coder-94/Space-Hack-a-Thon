document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Elements ---
    const itemNameInput = document.getElementById('itemName');
    const expiryDaysInput = document.getElementById('expiryDays');
    const usesInput = document.getElementById('uses');
    const addItemBtn = document.getElementById('addItemBtn');

    const currentDaySpan = document.getElementById('currentDay');
    const nextDayBtn = document.getElementById('nextDayBtn');
    const fastForwardDaysInput = document.getElementById('fastForwardDays');
    const fastForwardBtn = document.getElementById('fastForwardBtn');

    const inventoryBody = document.getElementById('inventoryBody');
    const inventoryStatus = document.getElementById('inventoryStatus');
    const wasteList = document.getElementById('wasteList');
    const wasteStatus = document.getElementById('wasteStatus');

    // --- State Variables ---
    let items = []; // Array to hold item objects: { id, name, expiryDays, uses }
    let waste = []; // Array to hold wasted item objects: { name, reason, day }
    let currentDay = 0;
    let nextId = 1; // Simple way to generate unique IDs

    // --- Functions ---

    /** Renders the current inventory table */
    function renderInventory() {
        inventoryBody.innerHTML = ''; // Clear existing rows
        if (items.length === 0) {
            inventoryStatus.style.display = 'block'; // Show status message
            inventoryBody.innerHTML = ''; // Ensure table body is empty if message shown
        } else {
            inventoryStatus.style.display = 'none'; // Hide status message
            items.forEach(item => {
                const row = inventoryBody.insertRow();
                row.innerHTML = `
                    <td>${item.name}</td>
                    <td>${item.expiryDays}</td>
                    <td>${item.uses}</td>
                `;
            });
        }
    }

    /** Renders the waste list */
    function renderWaste() {
         if (waste.length === 0) {
            wasteStatus.style.display = 'block'; // Show status message
            wasteList.innerHTML = ''; // Ensure list is empty
        } else {
            wasteStatus.style.display = 'none'; // Hide status message
             wasteList.innerHTML = ''; // Clear existing list
             // Show most recent waste first
            [...waste].reverse().forEach(wastedItem => {
                const listItem = document.createElement('li');
                listItem.textContent = `Day ${wastedItem.day}: ${wastedItem.name} (${wastedItem.reason})`;
                wasteList.appendChild(listItem);
            });
        }
    }

    /** Updates the current day display */
    function updateDayDisplay() {
        currentDaySpan.textContent = currentDay;
    }

    /** Adds a new item to the inventory */
    function addItem() {
        const name = itemNameInput.value.trim();
        const expiryDays = parseInt(expiryDaysInput.value, 10);
        const uses = parseInt(usesInput.value, 10);

        if (!name) {
            alert('Please enter an item name.');
            return;
        }
        if (isNaN(expiryDays) || expiryDays <= 0) {
            alert('Please enter a valid number of expiry days (must be 1 or more).');
            return;
        }
        if (isNaN(uses) || uses <= 0) {
            alert('Please enter a valid number of uses (must be 1 or more).');
            return;
        }

        const newItem = {
            id: nextId++,
            name: name,
            expiryDays: expiryDays,
            uses: uses
        };

        items.push(newItem);

        // Clear inputs
        itemNameInput.value = '';
        expiryDaysInput.value = 10; // Reset to default
        usesInput.value = 5;    // Reset to default

        renderInventory(); // Update the display
    }

    /** Simulates the passing of one day */
    function simulateOneDay() {
        currentDay++;
        updateDayDisplay();

        const itemsToRemoveIds = new Set(); // Keep track of items to remove by ID

        // Process items for the day
        items.forEach(item => {
            item.expiryDays--; // Decrease expiry days
            item.uses--;       // Decrease uses (assuming one use per day simulation)

            let wastedReason = null;
            if (item.expiryDays <= 0 && item.uses <= 0) {
                 wastedReason = "Expired & Used Up";
            } else if (item.expiryDays <= 0) {
                wastedReason = "Expired";
            } else if (item.uses <= 0) {
                wastedReason = "Used Up";
            }

            if (wastedReason) {
                waste.push({
                    name: item.name,
                    reason: wastedReason,
                    day: currentDay
                });
                itemsToRemoveIds.add(item.id); // Mark item for removal
            }
        });

        // Remove wasted items from the main inventory array
        if (itemsToRemoveIds.size > 0) {
            items = items.filter(item => !itemsToRemoveIds.has(item.id));
        }

        // Update displays
        renderInventory();
        renderWaste();
    }

    /** Simulates multiple days */
    function fastForward() {
        const days = parseInt(fastForwardDaysInput.value, 10);
        if (isNaN(days) || days <= 0) {
            alert('Please enter a valid number of days to fast forward.');
            return;
        }

        for (let i = 0; i < days; i++) {
            // Stop if no items left to simulate
            if(items.length === 0) {
                 console.log(`Simulation stopped after ${i} days as cargo hold is empty.`);
                 break;
            }
            simulateOneDay();
        }
         fastForwardDaysInput.value = 5; // Reset to default
    }

    // --- Event Listeners ---
    addItemBtn.addEventListener('click', addItem);
    nextDayBtn.addEventListener('click', simulateOneDay);
    fastForwardBtn.addEventListener('click', fastForward);

    // Allow pressing Enter in input fields to add item
    itemNameInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') addItem(); });
    expiryDaysInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') addItem(); });
    usesInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') addItem(); });

    // --- Initial Render ---
    updateDayDisplay();
    renderInventory();
    renderWaste();
});