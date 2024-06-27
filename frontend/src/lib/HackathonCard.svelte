<script>
    export let hackathon;

    function formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString();
    }
</script>

<div class="bg-white shadow-md rounded-lg overflow-hidden m-4">
    <div class="p-4">
        <h2 class="text-2xl font-bold mb-2">{hackathon.name}</h2>
        <p class="text-gray-600">{hackathon.location.city}, {hackathon.location.country}</p>
        <p class="text-gray-600">Start Date: {formatDate(hackathon.date.start_date)}</p>
        <p class="text-gray-600">End Date: {formatDate(hackathon.date.end_date)}</p>
        <a href={hackathon.URL} class="text-blue-500 hover:underline mt-2 block">Website</a>
        <p class="text-gray-600">Status: {hackathon.status}</p>
    </div>
</div>