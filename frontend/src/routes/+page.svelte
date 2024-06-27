<script lang="ts">
    export let data: { hackathons: { name: string; date: { start_date: string; end_date: string };  location: {city: string; country:string}; URL: string; status: string}[] };
    import { HackathonCard } from '../lib';
</script>


<svelte:head>
    <title>Hackathon Events</title>
    <meta name="description" content="Find upcoming hackathons!" />
</svelte:head>


<div class="grid grid-cols-1 gap-4 justify-items-center">
    {#if data.hackathons.length === 0}
        <div class="flex justify-center items-center h-full">
            <p>No hackathons available.</p>
        </div>
    {/if}
    {#each data.hackathons as hackathon}
        <div class="max-w-lg w-full">
            <HackathonCard {hackathon} />
        </div>
    {/each}
</div>
