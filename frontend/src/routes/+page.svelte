<script lang="ts">
    import { HackathonCard } from '../lib';
    import { writable, derived } from 'svelte/store';
    import LocationFilter from './LocationFilter.svelte';
    import StatusFilter from './StatusFilter.svelte';

    type Hackathon = {
        name: string;
        date: { start_date: string; end_date: string };
        location: { city: string; country: string };
        URL: string;
        status: string;
    };

    export let data: { hackathons: Hackathon[] };

    const filterText = writable('');
    const selectedStatuses = writable<Set<string>>(new Set());
    const selectedLocations = writable<{ countries: string[], cities: string[] }>({ countries: [], cities: [] });

    const filteredHackathons = derived(
        [filterText, writable(data.hackathons), selectedStatuses, selectedLocations],
        ([$filterText, $hackathons, $selectedStatuses, $selectedLocations]) => {
            return $hackathons.filter(hackathon => {
                const textMatch = !$filterText ||
                    hackathon.name.toLowerCase().includes($filterText.toLowerCase()) ||
                    hackathon.location.city.toLowerCase().includes($filterText.toLowerCase()) ||
                    hackathon.location.country.toLowerCase().includes($filterText.toLowerCase())

                const statusMatch = $selectedStatuses.size === 0 || $selectedStatuses.has(hackathon.status);

                const countryMatch = $selectedLocations.countries.length === 0 ||
                    $selectedLocations.countries.includes(hackathon.location.country);

                const cityMatch = $selectedLocations.cities.length === 0 ||
                    $selectedLocations.cities.includes(hackathon.location.city);

                return textMatch && statusMatch && countryMatch && cityMatch;
            }).sort((a, b) => new Date(a.date.start_date).getTime() - new Date(b.date.start_date).getTime());
        }
    );

    function handleInput(event: Event) {
        const target = event.target as HTMLInputElement;
        if (target) {
            filterText.set(target.value);
        }
    }

    function handleLocationFilterUpdate(event: CustomEvent<{ countries: string[], cities: string[] }>) {
        selectedLocations.set(event.detail);
    }
    function handleStatusFilterUpdate(event: CustomEvent<{ statuses: Set<string> }>) {
        selectedStatuses.set(event.detail.statuses);
    }

</script>


<svelte:head>
    <title>Hackathon Events</title>
    <meta name="description" content="Find upcoming hackathons!" />
</svelte:head>



<div class="p-4">

    <input
        type="text"
        placeholder="Search hackathons..."
        class="border p-2 mb-4 w-full"
        on:input={handleInput}
    />

    <StatusFilter on:statusUpdate={handleStatusFilterUpdate} />


    <LocationFilter
        hackathons={data.hackathons}
        on:filterUpdate={handleLocationFilterUpdate}
    />

<div class="grid grid-cols-1 gap-4 justify-items-center">
    {#if data.hackathons.length === 0}
        <div class="flex justify-center items-center h-full">
            <p>No hackathons available.</p>
        </div>
    {/if}
    {#each $filteredHackathons as hackathon}
        <div class="max-w-lg w-full">
            <HackathonCard {hackathon} />
        </div>
    {/each}
</div>
</div>
