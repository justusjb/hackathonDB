<script lang="ts">
    export let data: { hackathons: { name: string; date: { start_date: string; end_date: string };  location: {city: string; country:string}; URL: string; status: string}[] };

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

<div>
<h1>Hackathon Events</h1>
<table>
    <thead>
        <tr>
            <th>Name</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Location</th>
            <th>Website</th>
            <th>Status</th>
        </tr>
    </thead>
    <tbody>
        {#each data.hackathons as hack}
            <tr>
                <td>{hack.name}</td>
                <td>{formatDate(hack.date.start_date)}</td>
                <td>{formatDate(hack.date.end_date)}</td>
                <td>{hack.location.city}, {hack.location.country}</td>
                <td><a href={hack.URL}>Website</a></td>
                <td>{hack.status}</td>
            </tr>
        {/each}
    </tbody>
</table>
</div>
