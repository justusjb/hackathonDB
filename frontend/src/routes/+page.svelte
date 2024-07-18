<script lang="ts">
    import { HackathonCard, InputWithSubmit } from '../lib';
    import { writable, derived } from 'svelte/store';
    import LocationFilter from './LocationFilter.svelte';
    import StatusFilter from './StatusFilter.svelte';
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

    function handleEmailSubmit() {
    // Handle email submit logic here
    console.log("Email submitted");
  }

  function handleHackathonSubmit() {
    // Handle hackathon submit logic here
    console.log("Hackathon submitted");
  }


    $: isDarkMode = $darkMode;

    $: backgroundColor = isDarkMode ? 'rgb(31, 41, 55)' : 'rgb(255, 255, 255)';
  $: borderColor = isDarkMode ? 'rgb(75, 85, 99)' : 'rgb(209, 213, 219)';
  $: textColor = isDarkMode ? 'rgb(243, 244, 246)' : 'rgb(17, 24, 39)';
  $: placeholderColor = isDarkMode ? 'rgb(156, 163, 175)' : 'rgb(107, 114, 128)';
  $: borderHoverColor = isDarkMode ? 'rgb(107, 114, 128)' : 'rgb(107, 114, 128)';
  $: borderFocusColor = 'rgb(96, 165, 250)';

  $: inputStyles = `
    background-color: ${backgroundColor};
    border-color: ${borderColor};
    color: ${textColor};
    transition: border-color 0.2s ease-in-out;
  `;

  function handleFocus(event:any) {
    if (event.target instanceof HTMLInputElement) {
      event.target.style.borderColor = borderFocusColor;
    }
  }

  function handleBlur(event:any) {
    if (event.target instanceof HTMLInputElement) {
      event.target.style.borderColor = borderColor;
    }
  }

  function handleMouseEnter(event:any) {
    if (event.target instanceof HTMLInputElement) {
      event.target.style.borderColor = borderHoverColor;
    }
  }

  function handleMouseLeave(event:any) {
    if (event.target instanceof HTMLInputElement) {
      event.target.style.borderColor = borderColor;
    }
  }

</script>

<style>
  input::placeholder {
    color: var(--placeholder-color);
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
<div class="flex flex-col items-center justify-center h-auto bg-gradient-to-r from-blue-100 via-blue-200 to-blue-300 dark:from-gray-700 dark:via-gray-800 dark:to-gray-900 text-center">
  <h2 class="text-6xl font-extrabold text-blue-900 dark:text-white mb-8 pt-32 px-4">
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

<!-- Hackathon finding Section -->
<div class="p-4 bg-white dark:bg-gray-900">

<input
  type="text"
  placeholder="Search hackathons..."
  class="w-full p-2 mb-4 border rounded focus:outline-none"
  on:input={handleInput}
  style={inputStyles}
  style:--placeholder-color={placeholderColor}
  on:focus={handleFocus}
  on:blur={handleBlur}
  on:mouseenter={handleMouseEnter}
  on:mouseleave={handleMouseLeave}
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
