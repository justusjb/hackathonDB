<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import Select from 'svelte-select';
    import { darkMode } from '../stores/darkMode.js';


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
    .map(h => `${h.location.city}, ${h.location.country}`))]
    .sort()
    .map(cityCountry => {
        const [city, country] = cityCountry.split(', ');
        return { value: city, label: cityCountry };
    });
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



  $: isDarkMode = $darkMode;

  $: backgroundColor = isDarkMode ? 'rgb(31, 41, 55)' : 'rgb(255, 255, 255)';
  $: borderColor = isDarkMode ? 'rgb(75, 85, 99)' : 'rgb(209, 213, 219)';
  $: textColor = isDarkMode ? 'rgb(243, 244, 246)' : 'rgb(17, 24, 39)';
  $: placeholderColor = isDarkMode ? 'rgb(156, 163, 175)' : 'rgb(107, 114, 128)';
  //$: borderColor = isDarkMode ? 'rgb(75, 85, 99)' : 'rgb(229, 231, 235)';
  $: borderHoverColor = isDarkMode ? 'rgb(107, 114, 128)' : 'rgb(156, 163, 175)';
  $: borderFocusColor = 'rgb(96, 165, 250)';
  $: disbg = !checkedCountries.length ? backgroundColor : backgroundColor;
  $: cityBorder = `1px solid ${!checkedCountries.length ? borderColor : borderHoverColor}`;

  $: inputStyles = `
    border-color: ${borderColor};
    color: ${textColor};
    transition: border-color 0.1s;
  `;

</script>

<style>
    .item {
        pointer-events: none;
    }
      :global(.custom-select .item) {
    display: flex;
    align-items: center;
  }

  :global(.custom-select label) {
    display: flex;
    align-items: center;
    width: 100%;
    cursor: pointer;
  }
  :global(.custom-select input[type="checkbox"]) {
    appearance: none;
    -webkit-appearance: none;
    width: 16px;
    height: 16px;
    border: 1px solid var(--checkbox-border-color, #ccc);
    border-radius: 3px;
    outline: none;
    cursor: pointer;
    position: relative;
    margin-right: 8px;
    vertical-align: middle;
  }

  :global(.custom-select input[type="checkbox"]:checked) {
    background-color: var(--checkbox-bg-color, #3b82f6);
    border-color: var(--checkbox-bg-color, #3b82f6);
  }

  :global(.custom-select input[type="checkbox"]:checked::before) {
    content: '\2713';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: var(--checkbox-check-color, white);
    font-size: 12px;
  }

  :global(.dark .custom-select input[type="checkbox"]) {
    --checkbox-border-color: #4b5563;
    --checkbox-bg-color: #3b82f6;
    --checkbox-check-color: #1f2937;
  }
</style>


<!--

     :root{
    --border-color: #ccc;
    --list-background: #ff0000;
    --item-hover-bg: #f0f0f0;
    --multi-item-bg: #e2e8f0;
    --multi-item-text: #4a5568;
  }

 -->

<!--
How to add nice shadow to the bottom of dropdown:

--list-shadow="inset 0 -10px 10px -10px rgba(0, 0, 0, 0.5)"
--item-hover-bg="rgba(0, 123, 255, 0.1)"

-->

<div class="mb-4">
    <h3 class="font-bold mb-2 {isDarkMode ? 'text-gray-300' : 'text-black'}">Countries</h3>
    <div >
    <Select
            class="custom-select"
inputStyles={inputStyles}
--background={backgroundColor}

        --chevron-background = 'rgb(128, 128, 255)'

        --border= '1px solid {borderColor}'
        --border-hover= '1px solid {borderHoverColor}'
        --border-focused= '1px solid {borderFocusColor}'
        --input-color={textColor}
        --item-color={textColor}
        --item-hover-color={textColor}
        --placeholder-color={placeholderColor}
        --item-hover-bg={isDarkMode ? 'rgb(55, 65, 81)' : 'rgb(243, 244, 246)'}
        --list-background={backgroundColor}
        --list-border={borderColor}
        --multi-item-bg={borderColor}
        --multi-item-color={textColor}
        --multi-item-outline={borderColor}

items={countries}
    bind:value={valueCountry}
    multiple={true}
    filterSelectedItems={false}
    closeListOnChange={false}
    --list-max-height="10000px"
    on:select={e => handleChange(e, 'country')}
    on:clear={e => handleChange(e, 'country')}
    placeholder="Select countries">
    <div class="item" slot="item" let:item>
        <label for={item.value}>
            <input type="checkbox" id={item.value} bind:checked={isCheckedCountry[item.value]} />
            {item.label}
        </label>
    </div>
</Select>
        </div>
{#if !checkedCountries.length}
    <span class="text-sm text-gray-500 mt-1">All countries selected</span>
{:else}
    <span class="text-sm text-gray-500 mt-1 invisible">All countries selected</span>
{/if}
</div>

<div class="mb-4">
    <h3 class="font-bold mb-2 {isDarkMode ? 'text-gray-300' : 'text-black'}">Cities</h3>
<Select
        class="custom-select"
inputStyles={inputStyles}
--background={disbg}
        --chevron-background = 'rgb(128, 128, 255)'

        --border= '1px solid {borderColor}'
        --border-hover={cityBorder}
        --border-focused= '1px solid {borderFocusColor}'
        --input-color={textColor}
        --item-color={textColor}
        --item-hover-color={textColor}
        --placeholder-color={placeholderColor}
        --item-hover-bg={isDarkMode ? 'rgb(55, 65, 81)' : 'rgb(243, 244, 246)'}
        --list-background={backgroundColor}
        --list-border={borderColor}
        --multi-item-bg={borderColor}
        --multi-item-color={textColor}
        --multi-item-outline={borderColor}
        --disabled-color="rgb(255, 0, 0)"
        --disabled-background={isDarkMode ? "rgb(55, 65, 81)" : "rgb(229, 231, 235)"}
        --disabled-placeholder-color={placeholderColor}
        --disabled-border-color={borderColor}



    items={availableCities}
    bind:value={valueCity}
    multiple={true}
    filterSelectedItems={false}
    closeListOnChange={false}
    --list-max-height="10000px"
    on:select={e => handleChange(e, 'city')}
    on:clear={e => handleChange(e, 'city')}
    placeholder= {!checkedCountries.length ? "Select a country first to show cities" : "Select cities"}
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
{:else}
    <span class="text-sm text-gray-500 mt-1 invisible">All cities selected</span>
{/if}
</div>

<!-- --item-is-active-bg={isDarkMode ? 'rgb(30, 58, 138)' : 'rgb(219, 234, 254)'} -->
