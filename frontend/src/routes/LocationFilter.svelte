<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import Select from 'svelte-select';

    export let hackathons: Array<{ location: { country: string; city: string } }>;

    const dispatch = createEventDispatcher();

    type SelectOption = { value: string; label: string };

    let availableCities: SelectOption[] = [];
    let checkedCountries: string[] = [];
    let checkedCities: string[] = [];

    let isCheckedCountry: { [key: string]: boolean } = {};
    let isCheckedCity: { [key: string]: boolean } = {};
    let valueCountry: SelectOption[] = [];
    let valueCity: SelectOption[] = [];

    function getHackathonCounts() {
    const counts: { [key: string]: number } = {};
    hackathons.forEach(h => {
        counts[h.location.country] = (counts[h.location.country] || 0) + 1;
    });
    return counts;
}

const hackathonCounts = getHackathonCounts();

$: countries = [...new Set(hackathons.map(h => h.location.country))]
    .sort()
    .map(country => ({
        value: country,
        label: `${country} (${hackathonCounts[country]})`
    }));

function computeCheckedStates() {
    availableCities = [...new Set(hackathons
        .filter(h => !checkedCountries.length || checkedCountries.includes(h.location.country))
        .map(h => h.location.city))]
        .sort()
        .map(city => ({ value: city, label: city }));
    checkedCities = checkedCities.filter(city => availableCities.some(ac => ac.value === city));
    updateFilters();
}

function computeIsChecked(type: 'country' | 'city') {
    if (type === 'country') {
        isCheckedCountry = {};
        checkedCountries.forEach((c) => (isCheckedCountry[c] = true));
    } else if (type === 'city') {
        isCheckedCity = {};
        checkedCities.forEach((c) => (isCheckedCity[c] = true));
    }
}

function computeValue(type: 'country' | 'city') {
    if (type === 'country') {
        valueCountry = checkedCountries.map((c) => countries.find((i) => i.value === c)).filter((i): i is SelectOption => i !== undefined);
    } else if (type === 'city') {
        valueCity = checkedCities.map((c) => availableCities.find((i) => i.value === c)).filter((i): i is SelectOption => i !== undefined);
    }
}

function handleChange(event: CustomEvent, type: 'country' | 'city') {
    if (type === 'country') {
        if (event.type === 'select') {
            if (checkedCountries.includes(event.detail.value)) {
                checkedCountries = checkedCountries.filter(c => c !== event.detail.value);
            } else {
                checkedCountries = [...checkedCountries, event.detail.value];
            }
        } else if (event.type === 'clear') {
            if (Array.isArray(event.detail)) {
                checkedCountries = [];
            } else if (event.detail.value) {
                checkedCountries = checkedCountries.filter(c => c !== event.detail.value);
            }
        }
    } else if (type === 'city') {
        if (event.type === 'select') {
            if (checkedCities.includes(event.detail.value)) {
                checkedCities = checkedCities.filter(c => c !== event.detail.value);
            } else {
                checkedCities = [...checkedCities, event.detail.value];
            }
        } else if (event.type === 'clear') {
            if (Array.isArray(event.detail)) {
                checkedCities = [];
            } else if (event.detail.value) {
                checkedCities = checkedCities.filter(c => c !== event.detail.value);
            }
        }
    }
    computeCheckedStates();
    computeIsChecked('country');
    computeIsChecked('city');
    computeValue('country');
    computeValue('city');
    updateFilters();
}


function updateFilters() {
    dispatch('filterUpdate', {
        countries: checkedCountries,
        cities: checkedCities
    });
}
</script>

<style>
    .item {
        pointer-events: none;
    }
</style>

<!--
How to add nice shadow to the bottom of dropdown:

--list-shadow="inset 0 -10px 10px -10px rgba(0, 0, 0, 0.5)"
--item-hover-bg="rgba(0, 123, 255, 0.1)"

-->

<div class="mb-4">
    <h3 class="font-bold mb-2">Countries</h3>
    <Select
    items={countries}
    bind:value={valueCountry}
    multiple={true}
    filterSelectedItems={false}
    closeListOnChange={false}
    --list-max-height="10000px"
    on:select={e => handleChange(e, 'country')}
    on:clear={e => handleChange(e, 'country')}>
    <div class="item" slot="item" let:item>
        <label for={item.value}>
            <input type="checkbox" id={item.value} bind:checked={isCheckedCountry[item.value]} />
            {item.label}
        </label>
    </div>
</Select>
{#if !checkedCountries.length}
    <span class="text-sm text-gray-500 mt-1">All countries selected</span>
{/if}
</div>

<div class="mb-4">
    <h3 class="font-bold mb-2">Cities</h3>
<Select
    items={availableCities}
    bind:value={valueCity}
    multiple={true}
    filterSelectedItems={false}
    closeListOnChange={false}
    --list-max-height="10000px"
    on:select={e => handleChange(e, 'city')}
    on:clear={e => handleChange(e, 'city')}
    disabled={!checkedCountries.length}>
    <div class="item" slot="item" let:item>
        <label for={item.value}>
            <input type="checkbox" id={item.value} bind:checked={isCheckedCity[item.value]} />
            {item.label}
        </label>
    </div>
</Select>
{#if !checkedCities.length}
    <span class="text-sm text-gray-500 mt-1">All cities selected</span>
{/if}
</div>