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

    $: countries = [...new Set(hackathons.map(h => h.location.country))]
    .sort()
    .map(country => ({ value: country, label: country }));

    $: computeCheckedStates();
    $: computeIsChecked();

    function computeCheckedStates() {
        availableCities = [...new Set(hackathons
            .filter(h => !checkedCountries.length || checkedCountries.includes(h.location.country))
            .map(h => h.location.city))]
            .sort()
            .map(city => ({ value: city, label: city }));
        checkedCities = checkedCities.filter(city => availableCities.some(ac => ac.value === city));
        updateFilters();
    }

    function computeIsChecked() {
        isCheckedCountry = {};
        checkedCountries.forEach((c) => (isCheckedCountry[c] = true));
        isCheckedCity = {};
        checkedCities.forEach((c) => (isCheckedCity[c] = true));
    }

    function handleChange(event: CustomEvent, type: 'country' | 'city') {
        if (type === 'country') {
            if (checkedCountries.includes(event.detail.value)) {
                checkedCountries = checkedCountries.filter(c => c !== event.detail.value);
            } else {
                checkedCountries = [...checkedCountries, event.detail.value];
            }
        } else if (type === 'city') {
            if (checkedCities.includes(event.detail.value)) {
                checkedCities = checkedCities.filter(c => c !== event.detail.value);
            } else {
                checkedCities = [...checkedCities, event.detail.value];
            }
        }
        computeCheckedStates();
    }


function updateFilters() {
    dispatch('filterUpdate', {
        countries: checkedCountries,
        cities: checkedCities
    });
}

$: {
    updateFilters();
}
</script>

<div class="mb-4">
    <h3 class="font-bold mb-2">Countries</h3>
    <Select
    items={countries}
    multiple={true}
    filterSelectedItems={false}
    closeListOnChange={false}
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
        multiple={true}
        filterSelectedItems={false}
        closeListOnChange={false}
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