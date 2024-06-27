<script lang="ts">
    import { HackathonCard } from '../lib';
    import { writable, derived } from 'svelte/store';

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

    const filteredHackathons = derived(
        [filterText, writable(data.hackathons), selectedStatuses],
        ([$filterText, $hackathons, $selectedStatuses]) => {
            let filtered = $hackathons;

            if ($filterText) {
                filtered = filtered.filter(hackathon =>
                    hackathon.name.toLowerCase().includes($filterText.toLowerCase()) ||
                    hackathon.location.city.toLowerCase().includes($filterText.toLowerCase()) ||
                    hackathon.location.country.toLowerCase().includes($filterText.toLowerCase()) ||
                    hackathon.status.toLowerCase().includes($filterText.toLowerCase())
                );
            }

            if ($selectedStatuses.size > 0) {
                filtered = filtered.filter(hackathon =>
                    $selectedStatuses.has(hackathon.status)
                );
            }

            return filtered;
        }
    );

    function handleInput(event: Event) {
        const target = event.target as HTMLInputElement;
        if (target) {
            filterText.set(target.value);
        }
    }

        function toggleStatus(status: string) {
        selectedStatuses.update(set => {
            if (set.has(status)) {
                set.delete(status);
            } else {
                set.add(status);
            }
            return new Set(set);
        });
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

<div class="mb-4">
    <label class="inline-flex items-center mr-4">
        <input type="checkbox" class="form-checkbox text-yellow-500 h-5 w-5" on:change={() => toggleStatus('announced')}>
        <span class="ml-2 text-gray-700">Announced</span>
    </label>
    <label class="inline-flex items-center mr-4">
        <input type="checkbox" class="form-checkbox text-green-600 h-5 w-5" on:change={() => toggleStatus('applications_open')}>
        <span class="ml-2 text-gray-700">Applications Open</span>
    </label>
    <label class="inline-flex items-center mr-4">
        <input type="checkbox" class="form-checkbox text-red-600 h-5 w-5" on:change={() => toggleStatus('applications_closed')}>
        <span class="ml-2 text-gray-700">Applications Closed</span>
    </label>
    <label class="inline-flex items-center mr-4">
        <input type="checkbox" class="form-checkbox text-gray-400 h-5 w-5" on:change={() => toggleStatus('expected')}>
        <span class="ml-2 text-gray-700">Expected</span>
    </label>
</div>

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
