<script lang="ts">
    import { createEventDispatcher } from 'svelte';

    export let hackathons: any[];

    const dispatch = createEventDispatcher();

    let selectedCountries = new Set();
    let selectedCities = new Set();

    $: countries = [...new Set(hackathons.map(h => h.location.country))].sort();
    $: cities = [...new Set(hackathons.map(h => h.location.city))].sort();

    function toggleCountry(country: string) {
        if (selectedCountries.has(country)) {
            selectedCountries.delete(country);
            selectedCities = new Set([...selectedCities].filter(city =>
                hackathons.some(h => h.location.city === city && h.location.country !== country)
            ));
        } else {
            selectedCountries.add(country);
        }
        updateFilters();
    }

    function toggleCity(city: string) {
        if (selectedCities.has(city)) {
            selectedCities.delete(city);
        } else {
            selectedCities.add(city);
            const country = hackathons.find(h => h.location.city === city)?.location.country;
            if (country) selectedCountries.add(country);
        }
        updateFilters();
    }

    function updateFilters() {
        dispatch('filterUpdate', {
            countries: [...selectedCountries],
            cities: [...selectedCities]
        });
    }
</script>

<div class="mb-4">
    <h3 class="font-bold mb-2">Countries</h3>
    {#each countries as country}
        <label class="inline-flex items-center mr-4 mb-2">
            <input type="checkbox" class="form-checkbox h-5 w-5"
                   checked={selectedCountries.has(country)}
                   on:change={() => toggleCountry(country)}>
            <span class="ml-2 text-gray-700">{country}</span>
        </label>
    {/each}
</div>

<div class="mb-4">
    <h3 class="font-bold mb-2">Cities</h3>
    {#each cities as city}
        <label class="inline-flex items-center mr-4 mb-2">
            <input type="checkbox" class="form-checkbox h-5 w-5"
                   checked={selectedCities.has(city)}
                   on:change={() => toggleCity(city)}>
            <span class="ml-2 text-gray-700">{city}</span>
        </label>
    {/each}
</div>