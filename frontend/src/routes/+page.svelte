<script lang="ts">
    export let data: { hackathons: { name: string; date: string }[] };

    // Function to format the date
    function formatDate(dateString: string): string {
        const date = new Date(dateString);
        return date.toLocaleDateString(); // You can customize the format as needed
    }
</script>

<svelte:head>
    <title>Hackathon Events</title>
    <meta name="description" content="Find upcoming hackathons!" />
</svelte:head>

<div>
    <h1>Hackathon Events</h1>
    {#each data.hackathons as hack}
        <div>{hack.name} - {formatDate(hack.date)}</div>
    {/each}
</div>
