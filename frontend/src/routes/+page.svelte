<script lang="ts">
    export let data: { hackathons: { name: string; date: { start_date: string; end_date: string };  location: {city: string; country:string}; URL: string; status: string}[] };
    import { HackathonCard } from '../lib';
    import { writable, derived } from 'svelte/store';

    const filterText = writable('');

    const filteredHackathons = derived(
        [filterText, writable(data.hackathons)],
        ([$filterText, $hackathons]) => {
            if (!$filterText) return $hackathons;
            return $hackathons.filter(hackathon =>
                hackathon.name.toLowerCase().includes($filterText.toLowerCase()) ||
                hackathon.location.city.toLowerCase().includes($filterText.toLowerCase()) ||
                hackathon.location.country.toLowerCase().includes($filterText.toLowerCase()) ||
                hackathon.status.toLowerCase().includes($filterText.toLowerCase())
            );
        }
    );

    function handleInput(event: Event) {
        const target = event.target as HTMLInputElement;
        if (target) {
            filterText.set(target.value);
        }
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
