<script lang="ts">
    import { createEventDispatcher } from 'svelte';
    import Select from 'svelte-select';

    export let hackathons: Array<{ location: { country: string; city: string } }>;

    const dispatch = createEventDispatcher();

    type SelectOption = { value: string; label: string };

    let selectedCountries: SelectOption[] = [];
    let selectedCities: SelectOption[] = [];

    $: countries = [...new Set(hackathons.map(h => h.location.country))]
        .sort()
        .map(country => ({ value: country, label: country }));

    $: availableCities = [...new Set(hackathons
        .filter(h => !selectedCountries || selectedCountries.length === 0 || selectedCountries.find(sc => sc.value === h.location.country))
        .map(h => h.location.city))]
        .sort()
        .map(city => ({ value: city, label: city }));

    function handleCountryChange(event: CustomEvent) {
        selectedCountries = event.detail || [];
        selectedCities = selectedCities.filter(city =>
            availableCities.find(ac => ac.value === city.value)
        );
        updateFilters();
    }


    function handleCityChange(event: CustomEvent) {
        selectedCities = event.detail || [];
        updateFilters();
    }


function updateFilters() {
    dispatch('filterUpdate', {
        countries: selectedCountries.map(c => c.value),
        cities: selectedCities.map(c => c.value)
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
        bind:value={selectedCountries}
        on:change={handleCountryChange}
        placeholder="Select countries..."
    />
    {#if !selectedCountries || selectedCountries.length === 0}
        <span class="text-sm text-gray-500 mt-1">All countries selected</span>
    {/if}
</div>

<div class="mb-4">
    <h3 class="font-bold mb-2">Cities</h3>
    <Select
        items={availableCities}
        multiple={true}
        bind:value={selectedCities}
        on:change={handleCityChange}
        placeholder="Select cities..."
        disabled={!selectedCountries || selectedCountries.length === 0}
    />
    {#if !selectedCities || selectedCities.length === 0}
        <span class="text-sm text-gray-500 mt-1">All cities selected</span>
    {/if}
</div>