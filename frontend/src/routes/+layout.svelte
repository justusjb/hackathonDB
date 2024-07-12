<script lang="ts">
  import { darkMode } from '../stores/darkMode.js';
  import { onMount } from 'svelte';
    import "../app.css";
  let isDarkMode: boolean = false;

  darkMode.subscribe((value:boolean) => {
    isDarkMode = value;
      console.log(isDarkMode)
  });

  function toggleDarkMode() {
    darkMode.update((n:boolean) => !n);
  }

    onMount(() => {
    if (isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  });
</script>

<!-- Header Bar -->
    <div class="header-bar bg-white py-4 shadow-md dark:bg-black">
        <div class="container mx-auto px-4">
            <h1 class="text-2xl font-bold text-blue-900">HackathonDB</h1>

            <button on:click={toggleDarkMode} class="m-4 p-2 border rounded">
    {#if isDarkMode}
      Switch to Light Mode
    {:else}
      Switch to Dark Mode
    {/if}
  </button>

        </div>
    </div>


<slot/>
