<script lang="ts">
  import { darkMode } from '../stores/darkMode.js';
  import { onMount } from 'svelte';
    import "../app.css";
  let isDarkMode: boolean = false;

  darkMode.subscribe((value:boolean) => {
    isDarkMode = value;
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
<div class="min-h-screen">
<div class="header-bar bg-white dark:bg-gray-800 py-4 shadow-md">
  <div class="container mx-auto px-4 flex items-center justify-between">
    <h1 class="text-2xl font-bold text-blue-900 dark:text-white">HackathonDB</h1>
    <button on:click={toggleDarkMode} class="p-1.5 border rounded text-black dark:text-white text-sm">
    {#if isDarkMode}
      Switch to Light Mode
    {:else}
      Switch to Dark Mode
    {/if}
  </button>

        </div>
    </div>


  <main class="flex-1 overflow-auto">
    <slot />
  </main>
</div>