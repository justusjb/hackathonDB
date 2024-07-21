<script lang="ts">
    import { HackathonCard, InputWithSubmit } from '../lib';
    import { writable, derived } from 'svelte/store';
    import LocationFilter from './LocationFilter.svelte';
    import StatusFilter from './StatusFilter.svelte';
    import TextFilter from "./TextFilter.svelte";
    import { darkMode } from '../stores/darkMode.js';


    type Hackathon = {
        name: string;
        date: { start_date: string; end_date: string };
        location: { city: string; country: string };
        URL: string;
        status: string;
    };


    //export let data: { hackathons: Hackathon[] };
    //export let error: string | null;

    export let data: { hackathons: Hackathon[]; error: string | null };

    const { hackathons, error } = data;

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

    function handleEmailSubmit(value: string) {
    // Handle email submit logic here
    console.log("Email submitted:", value);
  }

  function handleHackathonSubmit(value: string) {
    // Handle hackathon submit logic here
    console.log("Hackathon submitted:", value);
  }

</script>

<style>
  :global(.custom-select.svelte-select-wrapper:hover) {
    border: var(--border-hover) !important;
  }
</style>


<svelte:head>
    <title>Hackathon Database</title>
    <meta name="description" content="Find upcoming hackathons!" />
</svelte:head>

{#if error}
    <div class="h-full bg-gray-100 dark:bg-gray-900">

<div class="flex-grow p-4">
    <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <strong class="font-bold">Error:</strong>
        <span class="block sm:inline">{error}</span>
    </div>
</div>
        </div>

{:else}

<!-- Landing page Section -->
<div class="flex flex-col items-center justify-center bg-gradient-to-r from-blue-100 via-blue-200 to-blue-300 dark:from-gray-700 dark:via-gray-800 dark:to-gray-900 text-center pb-6 pt-12 sm:pb-10 sm:pt-16 md:pb-12 md:pt-24 lg:pb-20 lg:pt-36">
  <h2 class="text-4xl sm:text-5xl md:text-6xl lg:text-6xl font-extrabold text-blue-900 dark:text-white mb-4 sm:mb-6 md:mb-8 px-4">
    The best place to find hackathons
  </h2>

  <div class="w-full max-w-md px-4 py-4 sm:py-6 md:py-8">
    <InputWithSubmit
      placeholder="Enter your email"
      buttonText="Submit"
      description="Get updates on the future of HackathonDB 🚀 no spam, pinky promise 🥺"
      onSubmit={handleEmailSubmit}
    />

    <div class="mt-4 sm:mt-6 md:mt-8">
      <InputWithSubmit
        placeholder="Input a new hackathon..."
        buttonText="Submit"
        description="Know a hackathon that's missing? Please share it! 🤩"
        onSubmit={handleHackathonSubmit}
      />
    </div>
  </div>
</div>

<!-- Hackathon finding Section -->
<div class="p-4 bg-white dark:bg-gray-900">

<TextFilter
  placeholder="Search hackathons"
  on:input={handleInput}
/>

    <StatusFilter on:statusUpdate={handleStatusFilterUpdate} />


    <LocationFilter
        hackathons={data.hackathons}
        on:filterUpdate={handleLocationFilterUpdate}
    />

    <div class="min-h-screen">
<div class="grid grid-cols-1 gap-4 justify-items-center">
    {#if data.hackathons.length === 0}
        <div class="flex justify-center items-center h-full">
            <p>No hackathons available.</p>
        </div>
    {:else if $filteredHackathons.length === 0}
        <div class="flex justify-center items-center h-full">
            <p>No hackathons match the selected filters.</p>
        </div>
    {/if}
    {#each $filteredHackathons as hackathon}
        <div class="max-w-lg w-full">
            <HackathonCard {hackathon} />
        </div>
    {/each}
</div>
</div>
</div>

{/if}
