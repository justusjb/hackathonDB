<script lang="ts">
    import { HackathonCard, InputWithSubmit } from '../lib';
    import { writable, derived } from 'svelte/store';
    import LocationFilter from './LocationFilter.svelte';
    import StatusFilter from './StatusFilter.svelte';

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

    function handleEmailSubmit() {
    // Handle email submit logic here
    console.log("Email submitted");
  }

  function handleHackathonSubmit() {
    // Handle hackathon submit logic here
    console.log("Hackathon submitted");
  }

</script>


<style>
    .custom-button {
        background-color: #1E3A8A; /* Darker blue color */
        border: 2px solid #1E3A8A; /* Matching border color */
        color: white;
        border-radius: 0 0.5rem 0.5rem 0; /* Adjusted border-radius to match input */
        padding: 0.5rem 1rem;
        transition: background-color 0.3s, border-color 0.3s; /* Smooth transition */
    }

    .custom-button:hover {
        background-color: #1D4ED8; /* Slightly lighter blue on hover */
        border-color: #1D4ED8; /* Matching border color on hover */
    }

    .custom-button:focus {
        outline: none;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.5); /* Focus ring */
    }
</style>



<svelte:head>
    <title>Hackathon Database</title>
    <meta name="description" content="Find upcoming hackathons!" />
</svelte:head>



<!-- Header Bar -->
    <div class="header-bar bg-white py-4 shadow-md">
        <div class="container mx-auto px-4">
            <h1 class="text-2xl font-bold text-blue-900">HackathonDB</h1>
        </div>
    </div>




    <!-- Hero Section -->
    <div class="flex flex-col items-center justify-center h-auto bg-gradient-to-r from-blue-100 via-blue-200 to-blue-300 text-center">
        <h2 class="text-6xl font-extrabold text-blue-900 mb-8 pt-32 px-4">
            The best place to find hackathons
        </h2>

<div class="w-full max-w-md pb-28 px-4 pt-6">

    <InputWithSubmit
      placeholder="Enter your email"
      buttonText="Submit"
      description="Get updates on the future of HackathonDB 🚀 no spam, pinky promise 🥺"
      onSubmit={handleEmailSubmit}
    />

    <InputWithSubmit
      placeholder="Input a new hackathon..."
      buttonText="Submit"
      description="Know a hackathon that’s missing? Please share it! 🤩"
      onSubmit={handleHackathonSubmit}
    />

</div>
    </div>


<div class="p-4 min-h-screen">

    <input
        type="text"
        placeholder="Search hackathons..."
        class="border p-2 mb-4 w-full"
        on:input={handleInput}
    />

    <StatusFilter on:statusUpdate={handleStatusFilterUpdate} />


    <LocationFilter
        hackathons={data.hackathons}
        on:filterUpdate={handleLocationFilterUpdate}
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
