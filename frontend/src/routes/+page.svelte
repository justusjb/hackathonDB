<script lang="ts">
    export let data: { hackathons: { name: string; date: { start_date: string; end_date: string };  location: {city: string; country:string}; URL: string; status: string}[] };
    import { HackathonCard } from '../lib';

    // Function to format the date
    function formatDate(dateString: string): string {
        const date = new Date(dateString);
        return date.toLocaleDateString();
    }
</script>



<style>
    table {
        /* width: 100%; */
        border-collapse: collapse;
        margin: 20px 0;
        font-size: 18px;
        text-align: left;
    }

    th, td {
        padding: 12px;
        border-bottom: 1px solid #ddd;
    }

    th {
        background-color: #f2f2f2;
    }

    tr:hover {
        background-color: #f5f5f5;
    }
</style>


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
