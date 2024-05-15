<script lang="ts">
    export let data: { hackathons: { name: string; date: string }[] };
</script>

<svelte:head>
    <title>Hackathon Events</title>
    <meta name="description" content="Find upcoming hackathons!" />
</svelte:head>

<div>
    <h1>Hackathon Events</h1>
    {#each data.hackathons as hack}
        <div>{hack.name} - {hack.date}</div>
    {/each}
</div>
