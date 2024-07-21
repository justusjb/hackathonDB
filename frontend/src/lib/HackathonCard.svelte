<script lang="ts">
    export let hackathon: {
        name: string;
        date: { start_date: string; end_date: string };
        location: { city: string; country: string };
        URL: string;
        status: string;
    };

    function formatDate(dateString: string) {
        const date = new Date(dateString);
        return date.toLocaleDateString();
    }

    function getStatusClass(status: string) {
        switch (status) {
            case 'announced':
                return 'bg-yellow-500';
            case 'applications_open':
                return 'bg-green-600';
            case 'applications_closed':
                return 'bg-red-600';
            case 'expected':
                return 'bg-gray-300';
            default:
                return 'bg-gray-600';
        }
    }
</script>

<div class="bg-white dark:bg-gray-800 shadow-md rounded-lg overflow-hidden m-4">
    <div class="p-4">
        <h2 class="text-2xl font-bold mb-2 text-gray-800 dark:text-gray-300">{hackathon.name}</h2>
        <p class="text-gray-600 dark:text-gray-300">{hackathon.location.city}, {hackathon.location.country}</p>
        <p class="text-gray-600 dark:text-gray-300">Start Date: {formatDate(hackathon.date.start_date)}</p>
        <p class="text-gray-600 dark:text-gray-300">End Date: {formatDate(hackathon.date.end_date)}</p>
        <a href={hackathon.URL} class="text-blue-500 hover:underline mt-2 inline-block dark:text-blue-400" target="_blank" rel="noopener noreferrer">Website</a>
        <div class="flex items-center mt-2">
            <div class={`w-3 h-3 rounded-full ${getStatusClass(hackathon.status)} mr-2`}></div>
            <p class="text-gray-600 dark:text-gray-300">Status: {hackathon.status.replace('_', ' ')}</p>
        </div>
    </div>
</div>