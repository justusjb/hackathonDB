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
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    darkMode.set(prefersDark);
  });
</script>

<style>
  :root {
    --color-gray-700: 55, 65, 81;
  }
</style>

<!-- Header Bar -->
<div class="min-h-screen">
<div class="header-bar bg-white dark:bg-gray-800 py-4 shadow-md">
  <div class="container mx-auto px-4 flex items-center justify-between">
    <h1 class="text-2xl font-bold text-blue-900 dark:text-white">HackathonDB</h1>


      <label class="flex cursor-pointer gap-2 items-center">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="text-gray-600 dark:text-gray-400">
          <circle cx="12" cy="12" r="5" />
          <path
            d="M12 1v2M12 21v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M1 12h2M21 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4" />
        </svg>
        <input
          type="checkbox"
          class="toggle theme-controller hover:bg-blue-900 dark:hover:bg-gray-400 bg-blue-900 dark:bg-gray-400 border-gray-500 dark:border-gray-400 [--tglbg:white] dark:[--tglbg:theme(colors.gray.800)]"
          checked={isDarkMode}
          on:change={toggleDarkMode}
        />
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="text-gray-600 dark:text-gray-400">
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        </svg>
      </label>

        </div>
    </div>


  <main class="flex-1 overflow-auto">
    <slot />
  </main>
</div>